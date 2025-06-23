# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import api, fields, models
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class Contract(models.Model):
    _inherit = 'hr.contract'

    contract_type = fields.Selection([("month", "Month"), ("year", "Year")],
                                     default="year", string='Contract Type ', tracking=True)

    contract_period = fields.Integer(
        string="Period ", default=1, tracking=True)
    allocation_id = fields.Many2one("hr.leave.allocation",
                                    string="Allocation Request", copy=False)

    leaves_count = fields.Integer(compute='_compute_leave_count',
                                  string='Leaves Count')

    date_start = fields.Date('Start Date', required=True, default=fields.Date.today,
                             help="Start date of the contract.", tracking=True)
    date_end = fields.Date('End Date',
                           help="End date of the contract (if it's a fixed-term contract).", tracking=True)
    days_extend = fields.Integer(
        string="Days Extend", tracking=True)

    def _get_sunday_count(self, from_date, to_date, sunday_list):
        # --------------- Sunday Count ----------------
        sunday = 0
        while from_date <= to_date:
            # If sunday
            if from_date.weekday() == 6:
                if sunday_list and from_date in sunday_list:
                    from_date += timedelta(days=1)
                    continue
                sunday_list.append(from_date)
                sunday += 1
            from_date += timedelta(days=1)
        return sunday

    def _add_holidays(self, start_date):
        end_date = self.date_end
        holiday = 0
        # ----------- Public holiday Count -----------
        if self.employee_id:
            if self.employee_id.resource_calendar_id:
                public_holidays = self.env['resource.calendar.leaves'].sudo().search([
                    ('date_from', '<=', end_date),
                    ('date_from', '>=', start_date),
                ])
                if public_holidays:
                    # holiday = len(public_holidays)
                    for public_holiday in public_holidays:
                        public_holiday_start_date = public_holiday.date_from
                        while public_holiday_start_date <= public_holiday.date_to:
                            # public_holiday_start_date += timedelta(days=1)
                            if public_holiday_start_date.weekday() == 6:
                                public_holiday_start_date += timedelta(days=1)
                                continue
                            holiday += 1
                            public_holiday_start_date += timedelta(days=1)
                if holiday:
                    self.date_end += timedelta(days=holiday)
        # --------------- Sunday Count ----------------
        sunday_list = []
        end_date = self.date_end
        while True:
            sunday = self._get_sunday_count(start_date, end_date, sunday_list)
            if not sunday:
                break
            start_date = self.date_end
            self.date_end += timedelta(days=sunday)
            end_date = self.date_end

    @api.onchange('days_extend')
    def _onchange_days_extend(self):
        # self._onchange_for_date_end()
        if self.date_end:
            old_end_date = self.date_end + timedelta(1)
            self.date_end += timedelta(days=self.days_extend)
            self._add_holidays(old_end_date)

    @api.onchange('contract_type', 'contract_period', 'date_start',)
    def _onchange_for_date_end(self):
        if self.date_start or self.contract_period:
            date = ' '
            if self.contract_type == 'month':
                date = self.date_start + \
                    relativedelta(months=self.contract_period, days=-1)
                self.date_end = date
            if self.contract_type == 'year':
                date = self.date_start + \
                    relativedelta(years=self.contract_period, days=-1)
                self.date_end = date

    def _compute_leave_count(self):
        for rec in self:
            in_contract_list = []
            domain = [("employee_id.id", "=", rec.employee_id.id),('state','=','validate')]
            hr_leaves = self.env['hr.leave'].sudo().search(domain)

            for leave in hr_leaves:
                if rec.date_end and rec.date_start and leave.request_date_from and leave.request_date_to:
                    if rec.date_start <= leave.request_date_from and rec.date_end >= leave.request_date_to:
                        in_contract_list.append(leave.id)
            rec.leaves_count = len(in_contract_list)

    def action_view_allocation_leaves(self):
        in_contract_list = []
        domain = [("employee_id.id", "=", self.employee_id.id),('state','=','validate')]
        hr_leaves = self.env['hr.leave'].sudo().search(domain)
        for leave in hr_leaves:
            if self.date_end and self.date_start and leave.request_date_from and leave.request_date_to:
                if self.date_start <= leave.request_date_from and self.date_end >= leave.request_date_to:
                    in_contract_list.append(leave.id)
        return {
            "type": "ir.actions.act_window",
            "name": "Leaves",
            "view_mode": "tree,form",
            "res_model": "hr.leave",
            "domain": [("id", "in", in_contract_list)]
        }

    def action_view_allocation(self):
        if self.allocation_id:
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                "res_model": "hr.leave.allocation",
                'target': 'self',
                'res_id': self.allocation_id.id
            }

    def allocate_leave(self):
        if self.employee_id:
            last_contract = self.search(
                [('employee_id', '=', self.employee_id.id),
                 ('date_end', '<=', self.date_start), ('id', '!=', self.id)],
                order='date_start desc',
                limit=1)
            return_view = {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                "res_model": "sh.employee.leave.allocation.wizard",
                'target': 'new',
            }
            if last_contract and last_contract.allocation_id:
                context = {
                    "default_allocation_id": last_contract.allocation_id.id,
                    "default_type": 'last',
                    "default_employee_id": self.employee_id.id,
                    "default_contract_id": self.id
                }
                return_view.update({'context': context})
                return return_view
            else:
                context = {
                    "default_employee_id": self.employee_id.id,
                    "default_contract_id": self.id
                }
                return_view.update({'context': context})
                return return_view
        else:
            raise UserError(
                "Please provide an Employee to allocate leave...!")
