# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, api, fields, _
from odoo.exceptions import ValidationError
from collections import namedtuple
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.addons.resource.models.resource import float_to_time
from odoo.exceptions import UserError, ValidationError
from pytz import timezone, UTC
from odoo.tools import float_compare


DummyAttendance = namedtuple(
    'DummyAttendance', 'hour_from, hour_to, dayofweek, day_period')


class Leave(models.Model):
    _inherit = 'hr.leave'

    def action_refuse_leaves(self):
        for rec in self:
            if self.env.user.has_group('hr.group_hr_manager'):
                rec.sudo().action_refuse()
            else:
                raise ValidationError(
                    'You are not authorized to perform this action !')


# class Leave(models.AbstractModel):
#     _inherit = "hr.leave"

    sh_timesheet_count = fields.Float(compute="compute_timesheet_count")
    sh_attendance_count = fields.Float(
        compute="compute_attendance_count_for_modif")
    leaves_count = fields.Float(
        related="employee_id.leaves_count", string="Remaining Leave Count")
    leave_taken_3_month = fields.Float(
        "Leaves taken last 3 months", compute='_compute_leave_taken_last_3_month')
    custom_hour_from = fields.Float("Hour From")
    custom_hour_to = fields.Float("Hour To")
    available_leaves = fields.Float(
        compute="_compute_available_leaves", string="Total Available Leaves")
    total_taken_leave_in_current_contract = fields.Float(
        compute="_compute_available_leaves", string="Total Leaves taken in Current Contract")
    employee_ids = fields.Many2many(
        'hr.employee', compute='_compute_from_holiday_type', store=True, string='Employees', readonly=False, groups="base.group_user",
        states={'cancel': [('readonly', True)], 'refuse': [('readonly', True)], 'validate1': [('readonly', True)], 'validate': [('readonly', True)]})


    # ==============================
    # Onchange Methods
    # ==============================

    @api.onchange('request_date_from_period', 'custom_hour_from', 'custom_hour_to', 'request_date_from', 'request_date_to', 'employee_id')
    def _onchange_request_parameters(self):
        if not self.request_date_from:
            self.date_from = False
            return

        if self.request_unit_half or self.request_unit_hours:
            self.request_date_to = self.request_date_from

        if not self.request_date_to:
            self.date_to = False
            return

        domain = [('calendar_id', '=',
                   self.employee_id.resource_calendar_id.id or self.env.user.company_id.resource_calendar_id.id)]
        attendances = self.env['resource.calendar.attendance'].read_group(
            domain, ['ids:array_agg(id)', 'hour_from:min(hour_from)', 'hour_to:max(hour_to)', 'dayofweek', 'day_period'], ['dayofweek', 'day_period'], lazy=False)

        # Must be sorted by dayofweek ASC and day_period DESC
        attendances = sorted([DummyAttendance(group['hour_from'], group['hour_to'], group['dayofweek'], group['day_period'])
                             for group in attendances], key=lambda att: (att.dayofweek, att.day_period != 'morning'))

        default_value = DummyAttendance(0, 0, 0, 'morning')

        # find first attendance coming after first_day
        attendance_from = next((att for att in attendances if int(
            att.dayofweek) >= self.request_date_from.weekday()), attendances[0] if attendances else default_value)
        # find last attendance coming before last_day
        attendance_to = next((att for att in reversed(attendances) if int(
            att.dayofweek) <= self.request_date_to.weekday()), attendances[-1] if attendances else default_value)

        if self.request_unit_half:
            if self.request_date_from_period == 'am':
                hour_from = float_to_time(attendance_from.hour_from)
                hour_to = float_to_time(attendance_from.hour_to)
            else:
                hour_from = float_to_time(attendance_to.hour_from)
                hour_to = float_to_time(attendance_to.hour_to)
        elif self.request_unit_hours:
            # This hack is related to the definition of the field, basically we convert
            # the negative integer into .5 floats
            hour_from = float_to_time(self.custom_hour_from)
            hour_to = float_to_time(self.custom_hour_to)
        else:
            hour_from = float_to_time(attendance_from.hour_from)
            hour_to = float_to_time(attendance_to.hour_to)
        self.date_from = timezone(self.tz).localize(datetime.combine(
            self.request_date_from, hour_from)).astimezone(UTC).replace(tzinfo=None)
        self.date_to = timezone(self.tz).localize(datetime.combine(
            self.request_date_to, hour_to)).astimezone(UTC).replace(tzinfo=None)
        # _onchange_leave_dates(v12) -> _compute_number_of_days(v16)
        self._compute_number_of_days()

    # ==============================
    # Compute Methods
    # ==============================

    def _compute_available_leaves(self):
        for leave in self:
            leave.available_leaves = 0.0
            leave.total_taken_leave_in_current_contract = 0.0
            if leave.employee_id:
                leave.available_leaves = leave.employee_id.leaves_count
                employee_id = leave.employee_id
                current_contract_id = self.env['hr.contract'].sudo().search([
                    ('employee_id', '=', employee_id.id),
                    ('state', 'in', ('open', 'pending')),
                    ('date_start', '<=', fields.Date.today()),
                    ('date_end', '>=', fields.Date.today())
                ], limit=1)
                if current_contract_id:
                    requests = self.env['hr.leave'].sudo().search([
                        ('employee_id', '=', employee_id.id),
                        ('state', 'in', ['confirm', 'validate1', 'validate']),
                        ('request_date_from', '>=',
                         current_contract_id.date_start),
                        ('request_date_to', '<=',
                         current_contract_id.date_end)
                    ])
                    if requests:
                        for request in requests:
                            leave.total_taken_leave_in_current_contract += request.number_of_days_display

    def _compute_leave_taken_last_3_month(self):
        for rec in self:
            rec.leave_taken_3_month = 0.0
            three_months = fields.Date.today() - relativedelta(months=3)
            rec.leave_taken_3_month = self.sudo().search_count([
                ('employee_id', 'in', rec.employee_ids.ids),
                ('state', 'in', ['validate', 'validate1']),
                ('date_from', '>=', three_months)
            ])

    def compute_attendance_count_for_modif(self):
        for rec in self:
            rec.sh_attendance_count = 0.0
            curr_start_date = datetime.strftime(
                self.date_from, "%Y/%m/%d 00:00:00")
            curr_end_date = datetime.strftime(
                self.date_to, "%Y/%m/%d 23:59:59")
            attendances = self.env['hr.attendance'].search([('employee_id', 'in', self.employee_ids.ids), (
                'check_in', '>=', curr_start_date), ('check_in', '<=', curr_end_date)])
            rec.sh_attendance_count = sum(attendances.mapped('total_time'))

    # ==============================
    # Other Methods
    # ==============================

    def action_view_attendance(self):
        curr_start_date = datetime.strftime(
            self.date_from, "%Y/%m/%d 00:00:00")
        curr_end_date = datetime.strftime(self.date_to, "%Y/%m/%d 23:59:59")
        attendances = self.env['hr.attendance'].search([('employee_id', 'in', self.employee_ids.ids), (
            'check_in', '>=', curr_start_date), ('check_in', '<=', curr_end_date)])
        return {
            'type': 'ir.actions.act_window',
            'name': 'Attendances',
            'view_mode': 'tree,form',
            'res_model': 'hr.attendance',
            'domain': [('id', 'in', attendances.ids)],
        }

    def compute_timesheet_count(self):
        for rec in self:
            rec.sh_timesheet_count = 0
            check_in_date = self.date_from.date()
            check_out_date = self.date_to.date()
            timesheets = self.env['account.analytic.line'].sudo().search([('employee_id', 'in', self.employee_ids.ids)]).filtered(
                lambda x: x.date >= check_in_date and x.date <= check_out_date)
            rec.sh_timesheet_count = sum(timesheets.mapped('unit_amount'))

    def action_view_timesheet(self):
        check_in_date = self.date_from.date()
        check_out_date = self.date_to.date()
        timesheets = self.env['account.analytic.line'].sudo().search(
            [('employee_id', '=', self.employee_id.id)])
        # timesheets = self.env['account.analytic.line'].sudo().search(
        #     [('employee_id', '=', 1)])
        if timesheets:
            timesheets = timesheets.filtered(
                lambda x: x.date >= check_in_date and x.date <= check_out_date)
            # res = {
            #     'type': 'ir.actions.act_window',
            #     'name': 'Timesheets',
            #     'view_mode': 'tree,form',
            #     'view_type': 'tree,form',
            #     'res_model': 'account.analytic.line',
            #     'domain': [('id', 'in', timesheets.ids)],
            # }
            # return res

    # =======START========Odoo not allowed to edit old leave so forecfully skip this part
    def write(self, values):
        if any(hol.date_from.date() < fields.Date.today() for hol in self) and 'force_write' not in self.env.context:
            result = super(Leave, self).with_context(force_write=True).sudo().write(values)
        else:
            result = super(Leave, self).write(values)
        return result
    # ========END===========Odoo not allowed to edit old leave so forecfully skip this part
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'number_of_days_display' in vals and vals['number_of_days_display'] == 0:
                raise UserError("Duration must be greater than zero")

        records = super(Leave, self).create(vals_list)
        for res in records:
            # users = res.env['res.users'].search([])
            listt = []
            # for user in users:
            #     if user.has_group('hr.group_hr_manager'):
            #         listt.append(user)

            if res.employee_id.coach_id.sudo().user_id.id:
                listt.append(res.employee_id.coach_id.sudo().user_id)

            base_url = self.env['ir.config_parameter'].sudo(
            ).get_param('web.base.url')
            self.env['user.push.notification'].push_notification(listt, 'New Leave Request', 'Leave Request Created By %s:' % (
                res.employee_id.name), base_url+"/mail/view?model=hr.leave&res_id="+str(res.id), 'hr.leave', res.id, 'hr')
        return records

    def action_refuse(self):
        for rec in self:    
            find_tl_employee=self.env['hr.employee'].search([('user_id','=',self.env.user.id )],limit=1)
            if find_tl_employee and not self.env.user.has_group('hr.group_hr_manager'):
                if any(employee.id == find_tl_employee.id  for employee in rec.employee_ids):
                    raise UserError(_("You can't Refuse own leave."))

            users = self.env['res.users'].search([])
            listt = []

            for user in users:
                if user.has_group('hr.group_hr_manager') and user != self.env.user:
                    listt.append(user)

            if rec.state == 'validate1':
                if rec.employee_id.coach_id.user_id not in listt and rec.employee_id.coach_id.user_id.id!=self.env.user.id:
                    listt.append(rec.employee_id.coach_id.user_id)   

    
            base_url = self.env['ir.config_parameter'].sudo(
            ).get_param('web.base.url')
            self.env['user.push.notification'].push_notification(listt, 'Leave Request Refused', "%s's Leave Request is Refused by %s:" % (
                rec.employee_id.name, self.env.user.name), base_url+"/mail/view?model=hr.leave&res_id="+str(rec.id), 'hr.leave', rec.id, 'hr')

            if rec.employee_id.user_id.id:
                base_url = self.env['ir.config_parameter'].sudo(
                ).get_param('web.base.url')
                self.env['user.push.notification'].push_notification([rec.employee_id.user_id], 'Leave Request Refused', 'Your Leave Request is Refused By %s:' % (
                    self.env.user.name), base_url+"/mail/view?model=hr.leave&res_id="+str(rec.id), 'hr.leave', rec.id, 'hr')

        return super(Leave, self).action_refuse()

    def action_approve(self):
        find_tl_employee=self.env['hr.employee'].search([('user_id','=',self.env.user.id )],limit=1)
        if find_tl_employee and not self.env.user.has_group('hr.group_hr_manager'):
            if any(employee.id == find_tl_employee.id  for employee in self.employee_ids):
                raise UserError(_("You can't Approve own leave."))
        if 'sudo_approve' not in self.env.context or self.env.context.get('sudo_approve') == False:
            res = super(Leave, self).action_approve()
        else:
            res = super(Leave, self).action_approve()
        if self.state == 'validate1' and self.env.uid != 1:
            users = self.env['res.users'].search([])
            listt = []

            for user in users:
                if user.has_group('hr.group_hr_manager') and user != self.env.user:
                    listt.append(user)

            base_url = self.env['ir.config_parameter'].sudo(
            ).get_param('web.base.url')
            self.env['user.push.notification'].push_notification(listt, 'Leave Request Approved', "%s's Leave Request is Approved by %s:" % (
                self.employee_id.name, self.env.user.name), base_url+"/mail/view?model=hr.leave&res_id="+str(self.id), 'hr.leave', self.id, 'hr')
            if self.employee_id.user_id.id:
                base_url = self.env['ir.config_parameter'].sudo(
                ).get_param('web.base.url')
                self.env['user.push.notification'].push_notification([self.employee_id.user_id], 'Leave Request Approved', 'Your Leave Request is Approved By %s:' % (
                    self.env.user.name), base_url+"/mail/view?model=hr.leave&res_id="+str(self.id), 'hr.leave', self.id, 'hr')
        return res

    def action_validate(self):
        if 'sudo_approve' not in self.env.context or self.env.context.get('sudo_approve') == False:
            res = super(Leave, self).action_validate()
        else:
            res = super(Leave, self).action_validate()
        if self.state == 'validate' and self.env.uid != 1:
            listt = []
            if self.employee_id.coach_id.user_id.id and self.employee_id.coach_id.user_id.id != self.env.user.id:
                listt.append(self.employee_id.coach_id.user_id)
            base_url = self.env['ir.config_parameter'].sudo(
            ).get_param('web.base.url')
            self.env['user.push.notification'].push_notification(listt, 'Leave Request Approved', "%s's Leave Request is Approved by %s:" % (
                self.employee_id.name, self.env.user.name), base_url+"/mail/view?model=hr.leave&res_id="+str(self.id), 'hr.leave', self.id, 'hr')
            if self.employee_id.user_id.id:
                base_url = self.env['ir.config_parameter'].sudo(
                ).get_param('web.base.url')
                self.env['user.push.notification'].push_notification([self.employee_id.user_id], 'Leave Request Approved', 'Your Leave Request is Approved By %s:' % (
                    self.env.user.name), base_url+"/mail/view?model=hr.leave&res_id="+str(self.id), 'hr.leave', self.id, 'hr')
        return res

    def _check_approval_update(self, state):
        """ Check if target state is achievable.
            (Standard method is overwrite) """
        if self.env.is_superuser():
            return

        current_employee = self.env.user.employee_id
        is_officer = self.env.user.has_group(
            'hr_holidays.group_hr_holidays_user')
        is_manager = self.env.user.has_group(
            'hr_holidays.group_hr_holidays_manager')

        for holiday in self:
            val_type = holiday.validation_type

            if not is_manager and state != 'confirm':
                if state == 'draft':
                    if holiday.state == 'refuse':
                        raise UserError(
                            _('Only a Time Off Manager can reset a refused leave.'))
                    if holiday.date_from and holiday.date_from.date() <= fields.Date.today():
                        raise UserError(
                            _('Only a Time Off Manager can reset a started leave.'))
                    if holiday.employee_id != current_employee:
                        raise UserError(
                            _('Only a Time Off Manager can reset other people leaves.'))
                else:
                    if val_type == 'no_validation' and current_employee == holiday.employee_id:
                        continue
                    holiday.check_access_rule('write')

                    if holiday.employee_id == current_employee:
                        raise UserError(
                            _('Only a Time Off Manager can approve/refuse its own requests.'))

                    # Change is here below
                    coach = holiday.employee_id.coach_id
                    if (state == 'validate1' and val_type == 'both') and holiday.holiday_type == 'employee':
                        if not is_officer and coach and coach != holiday.employee_id and self.env.user != holiday.employee_id.leave_manager_id:
                            raise UserError(_('You must be either %s\'s manager or Time off Manager to approve this leave') % (
                                holiday.employee_id.name))

                    if (state == 'validate' and val_type == 'both') and self.env.user != holiday.employee_id.leave_manager_id:
                        if coach and coach != holiday.employee_id:
                            raise UserError(
                                _('You must be %s\'s Manager to approve this leave', holiday.employee_id.name))

                    if not is_officer and (state == 'validate' and val_type == 'hr') and holiday.holiday_type == 'employee':
                        raise UserError(
                            _('You must either be a Time off Officer or Time off Manager to approve this leave'))

    # @api.constrains('state', 'number_of_days', 'holiday_status_id')
    # def _check_holidays(self):
    #     for holiday in self:

    #         if holiday.holiday_type != 'employee' or not holiday.employee_id or holiday.holiday_status_id.allocation_type == 'no':
    #             continue
    #         leave_days = holiday.holiday_status_id.get_days(
    #             holiday.employee_id.id)[holiday.holiday_status_id.id]
    #         if float_compare(leave_days['remaining_leaves'], 0, precision_digits=2) == -1 or \
    #                 float_compare(leave_days['virtual_remaining_leaves'], 0, precision_digits=2) == -1 or leave_days['virtual_remaining_leaves'] == 0 or leave_days['remaining_leaves'] == 0:
    #             raise ValidationError(
    #                 _('The number of remaining leaves is not sufficient for this leave type.\n'
    #                   'Please also check the leaves waiting for validation.'))

    #         current_contract_id = self.env['hr.contract'].search(
    #             [('employee_id', '=', holiday.employee_id.id),
    #              ('state', 'in', ('open', 'pending')),
    #              ('date_start', '<=', holiday.request_date_from),
    #              ('date_end', '>=', holiday.request_date_from)],
    #             limit=1)
    #         print("\n\n======current_contract_id",current_contract_id,current_contract_id.allocation_id)
    #         if current_contract_id and current_contract_id.allocation_id:
    #             current_month = fields.Date.today().month
    #             total_allowed_leave = (
    #                 current_month - current_contract_id.date_start.month + 1) * 1.25
    #             print("\n\n=====total_allowed_leave",total_allowed_leave)
    #             print("\n\n=====leave_days['virtual_remaining_leaves']",leave_days['virtual_remaining_leaves'])
    #             print("\n\n=====leave_days['max_leaves']",leave_days['max_leaves'])
    #             if (total_allowed_leave < (leave_days['max_leaves'] - leave_days['virtual_remaining_leaves'])):
    #                 raise ValidationError('You have no sufficient paid Leaves !')
