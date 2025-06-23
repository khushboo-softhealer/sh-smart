
# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo.exceptions import UserError
from odoo import api, fields, models, tools, _
import babel
from dateutil.relativedelta import relativedelta
from datetime import datetime, time
from pytz import timezone


class Payslip(models.Model):
    _inherit = 'hr.payslip'

    # @api.constrains('employee_id', 'date_from', 'date_to')
    # def check_date_and_employee(self):
    #     if self.env['hr.payslip'].search([('id', '!=', self.id), ('employee_id', '=', self.employee_id.id), ('date_from', '=', self.date_from), ('date_to', '=', self.date_to), ('state', '!=', 'cancel')]):
    #         raise UserError("For this date period payslip is already created for employee %s " % (
    #             self.employee_id.name))

    def action_payslip_done(self):
        res = super(Payslip, self).action_payslip_done()
        base_url = self.env['ir.config_parameter'].sudo(
        ).get_param('web.base.url')
        datem = datetime.strptime(str(self.date_from), "%Y-%m-%d")
        self.env['user.push.notification'].push_notification(self.employee_id.user_id, 'Your Payslip Generated', 'Payslip for %s generated & sent by email.' % (
            datem.strftime("%B")), base_url+"/mail/view?model=sh.hr.dashboard&res_id="+str(1), 'sh.hr.dashboard', 1, 'hr')
        return res

    # TODO move this function into hr_contract module, on hr.employee object
    @api.model
    def get_contract(self, employee, date_from, date_to):
        """
        @param employee: recordset of employee
        @param date_from: date field
        @param date_to: date field
        @return: returns the ids of all the contracts for the given employee that need to be considered for the given dates
        """
        # a contract is valid if it ends between the given dates
        clause_1 = ['&', ('date_end', '<=', date_to),
                    ('date_end', '>=', date_from)]
        # OR if it starts between the given dates
        clause_2 = ['&', ('date_start', '<=', date_to),
                    ('date_start', '>=', date_from)]
        # OR if it starts before the date_from and finish after the date_end (or never finish)
        clause_3 = ['&', ('date_start', '<=', date_from), '|',
                    ('date_end', '=', False), ('date_end', '>=', date_to)]
        clause_final = [('employee_id', '=', employee.id), ('state', 'in',
                                                            ('open', 'pending', 'close')), '|', '|'] + clause_1 + clause_2 + clause_3
        return self.env['hr.contract'].search(clause_final).ids

    def print_payslip(self):
        return self.env.ref('sh_hr_payroll.action_report_payslip').sudo().report_action(self)

    # YTI TODO To rename. This method is not really an onchange, as it is not in any view
    # employee_id and contract_id could be browse records
    def onchange_employee_id(self, date_from, date_to, employee_id=False, contract_id=False):
        # defaults
        res = {
            'value': {
                'line_ids': [],
                # delete old input lines
                'input_line_ids': [(2, x,) for x in self.input_line_ids.ids],
                # delete old worked days lines
                'worked_days_line_ids': [(2, x,) for x in self.worked_days_line_ids.ids],
                # 'details_by_salary_head':[], TODO put me back
                'name': '',
                'contract_id': False,
                'struct_id': False,
            }
        }
        slip_data2 = {
            'value': {
                'line_ids': [],
                # delete old input lines
                'input_line_ids': [(2, x,) for x in self.input_line_ids.ids],
                # delete old worked days lines
                'worked_days_line_ids': [(2, x,) for x in self.worked_days_line_ids.ids],
                # 'details_by_salary_head':[], TODO put me back
                'name': '',
                'contract_id': False,
                'struct_id': False,
            }
        }
        if (not employee_id) or (not date_from) or (not date_to):
            return res, {}
        ttyme = datetime.combine(fields.Date.from_string(date_from), time.min)
        employee = self.env['hr.employee'].browse(employee_id)
        locale = self.env.context.get('lang') or 'en_US'
        res['value'].update({
            'name': _('Salary Slip of %s for %s') % (employee.name, tools.ustr(babel.dates.format_date(date=ttyme, format='MMMM-y', locale=locale))),
            'company_id': employee.company_id.id,
        })
        slip_data2['value'].update({
            'name': _('Salary Slip of %s for %s') % (employee.name, tools.ustr(babel.dates.format_date(date=ttyme, format='MMMM-y', locale=locale))),
            'company_id': employee.company_id.id,
        })
        if not self.env.context.get('contract'):
            # fill with the first contract of the employee
            contract_ids = self.get_contract(employee, date_from, date_to)
        else:
            if contract_id:
                # set the list of contract for which the input have to be filled
                contract_ids = [contract_id]
            else:
                # if we don't give the contract, then the input to fill should be for all current contracts of the employee
                contract_ids = self.get_contract(employee, date_from, date_to)

        if not contract_ids:
            return res, {}

        contract = self.env['hr.contract'].browse(contract_ids[0])

        if contract.date_end != True or contract.date_end != False:
            if len(contract_ids) > 1 or contract.date_end < date_to:

                contract = self.env['hr.contract'].browse(contract_ids[0])
                res['value'].update({
                    'contract_id': contract.id
                })
                struct = contract.struct_id
                if not struct:
                    return res, {}
                res['value'].update({
                    'struct_id': struct.id,
                    'date_to': contract.date_end,
                    'date_from': date_from
                })
                # computation of the salary input
                contracts = self.env['hr.contract'].browse(contract_ids)
                worked_days_line_ids = self.get_worked_day_lines(
                    contract, date_from, contract.date_end)
                input_line_ids = self.get_inputs(
                    contract, date_from, contract.date_end)
                res['value'].update({
                    'worked_days_line_ids': worked_days_line_ids,
                    'input_line_ids': input_line_ids,
                })
                # create new payslip
                if len(contract_ids) == 1:
                    raise UserError("Please Generate New Contract for %s" % (
                        contract.employee_id.name))
                else:
                    contract1 = self.env['hr.contract'].browse(contract_ids[1])
                    slip_data2['value'].update({
                        'contract_id': contract1.id
                    })
                    struct = contract1.struct_id
                    if not struct:
                        return slip_data2, {}
                    slip_data2['value'].update({
                        'struct_id': struct.id,
                        'date_from': contract1.date_start,
                        'date_to': date_to
                    })
                    # computation of the salary input
                    contracts = self.env['hr.contract'].browse(contract_ids)
                    worked_days_line_ids = self.get_worked_day_lines(
                        contract1, contract1.date_start, date_to)
                    input_line_ids = self.get_inputs(
                        contract1, contract1.date_start, date_to)
                    slip_data2['value'].update({
                        'worked_days_line_ids': worked_days_line_ids,
                        'input_line_ids': input_line_ids,
                    })

                return res, slip_data2

            else:
                contract = self.env['hr.contract'].browse(contract_ids[0])
                res['value'].update({
                    'contract_id': contract.id
                })
                struct = contract.struct_id
                if not struct:
                    return res, {}

                if contract.date_start > date_from:
                    res['value'].update({
                        'struct_id': struct.id,
                        'date_to': date_to,
                        'date_from': contract.date_start
                    })
                    # computation of the salary input
                    contracts = self.env['hr.contract'].browse(contract_ids)
                    worked_days_line_ids = self.get_worked_day_lines(
                        contracts, contract.date_start, date_to)
                    input_line_ids = self.get_inputs(
                        contracts, contract.date_start, date_to)
                    res['value'].update({
                        'worked_days_line_ids': worked_days_line_ids,
                        'input_line_ids': input_line_ids,
                    })
                else:
                    res['value'].update({
                        'struct_id': struct.id,
                        'date_to': date_to,
                        'date_from': date_from
                    })
                    # computation of the salary input
                    contracts = self.env['hr.contract'].browse(contract_ids)
                    worked_days_line_ids = self.get_worked_day_lines(
                        contracts, date_from, date_to)
                    input_line_ids = self.get_inputs(
                        contracts, date_from, date_to)
                    res['value'].update({
                        'worked_days_line_ids': worked_days_line_ids,
                        'input_line_ids': input_line_ids,
                    })
                return res, {}

    # @api.model
    # def get_worked_day_lines(self, contracts, date_from, date_to):
    #     """
    #     @param contract: Browse record of contracts
    #     @return: returns a list of dict containing the input that should be applied for the given contract between date_from and date_to
    #     """
    #     res = []
    #     # fill only if the contract as a working schedule linked

    #     for contract in contracts.filtered(lambda contract: contract.resource_calendar_id and contract.date_start >= date_from or contract.date_end >= date_to):

    #         month_start_date = fields.Date.to_string(date_from.replace(day=1))
    #         month_end_date = fields.Date.to_string(
    #             date_to + relativedelta(months=+1, day=1, days=-1, hours=23, minutes=59, seconds=59))
    #         day_from = datetime.combine(
    #             fields.Date.from_string(date_from), time.min)
    #         day_to = datetime.combine(
    #             fields.Date.from_string(date_to), time.max)

    #         # compute leave days
    #         leaves = {}
    #         calendar = contract.resource_calendar_id
    #         tz = timezone(calendar.tz)

    #         month_end_day = datetime.combine(
    #             fields.Date.from_string(month_end_date), time.max)
    #         month_start_day = datetime.combine(
    #             fields.Date.from_string(month_start_date), time.min)

    #         day_leave_intervals = contract.employee_id.list_leaves(
    #             month_start_day, month_end_day, calendar=contract.resource_calendar_id)

    #         global_leave_days = 0.0
    #         global_leave_hours = 0.0
    #         for day, hours, leave in day_leave_intervals:
    #             holiday = leave[:1].holiday_id

    #             if not leave.is_saturday_leave:
    #                 current_leave_struct = leaves.setdefault(holiday.holiday_status_id, {
    #                     'name': holiday.holiday_status_id.name or _('Public Holiday'),
    #                     'sequence': 5,
    #                     'code': holiday.holiday_status_id.name or 'GLOBAL',
    #                     'number_of_days': 0.0,
    #                     'number_of_hours': 0.0,
    #                     'contract_id': contract.id,
    #                 })
    #                 current_leave_struct['number_of_hours'] += hours
    #             if not holiday.holiday_status_id.name:
    #                 global_leave_hours += hours
    #             work_hours = calendar.get_work_hours_count(
    #                 tz.localize(datetime.combine(day, time.min)),
    #                 tz.localize(datetime.combine(day, time.max)),
    #                 compute_leaves=False,
    #             )
    #             if work_hours:
    #                 if not leave.is_saturday_leave:
    #                     current_leave_struct['number_of_days'] += hours / work_hours
    #                 if not holiday.holiday_status_id.name:
    #                     global_leave_days += hours / work_hours

    #         # compute total days
    #         work_data = contract.employee_id.get_full_work_days_data(
    #             month_start_day, month_end_day, calendar=contract.resource_calendar_id)
    #         attendances = {
    #             'name': _("Total Working Days"),
    #             'sequence': 1,
    #             'code': 'TOTAL',
    #             'number_of_days': work_data['days'] - global_leave_days,
    #             'number_of_hours': work_data['hours'] - global_leave_hours,
    #             'contract_id': contract.id,
    #         }

    #         res.append(attendances)

    #         # leave payment
    #         last_contract = self.env['hr.contract'].search([('employee_id', '=', contract.employee_id.id),
    #                                                         ('date_end', '<=',
    #                                                          contract.date_start),
    #                                                         ('id', '!=', contract.id)], order='date_start desc', limit=1)

    #         if last_contract and last_contract.allocation_id and last_contract.allocation_id != contract.allocation_id and not last_contract.leave_payment_done:
    #             paid_leave_type = self.env['hr.leave.type'].sudo().search(
    #                 [('unpaid', '=', False)], limit=1)
    #             if paid_leave_type:
    #                 leave_days = paid_leave_type.get_days(contract.employee_id.id)[
    #                     paid_leave_type.id]
    #                 leave_payment = leave_days['remaining_leaves']
    #                 if leave_payment > 0:
    #                     attendances = {
    #                         'name': _("Extra Leave Payment"),
    #                         'sequence': 1,
    #                         'code': 'LEAVE',
    #                         'number_of_days': leave_payment,
    #                         'number_of_hours': 0.0,
    #                         'contract_id': contract.id,
    #                     }

    #                     res.append(attendances)
    #                 last_contract.write({'leave_payment_done': True})

    #          # compute worked days
    #         work_data = contract.employee_id._get_work_days_data_batch(
    #             day_from, day_to, calendar=contract.resource_calendar_id)
    #         attendances = {
    #             'name': _("Normal Working Days paid at 100%"),
    #             'sequence': 1,
    #             'code': 'WORK100',
    #             'number_of_days': round(work_data[contract.employee_id.id]['days'], 2),
    #             'number_of_hours': work_data[contract.employee_id.id]['hours'],
    #             'contract_id': contract.id,
    #         }

    #         res.append(attendances)

    #         res.extend(leaves.values())
    #     return res
