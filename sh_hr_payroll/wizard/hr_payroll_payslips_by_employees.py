# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _
from odoo.exceptions import UserError


class HrPayslipEmployees(models.TransientModel):
    _name = 'hr.payslip.employees'
    _description = 'Generate payslips for all selected employees'

    employee_ids = fields.Many2many('hr.employee', 'hr_employee_group_rel', 'payslip_id', 'employee_id', 'Employees')
    leave_employee_ids = fields.Many2many('hr.employee', 'hr_employee_leave_group_rel', 'payslip_id', 'employee_id', 'Employees')
    attendance_employee_ids = fields.Many2many('hr.employee', 'hr_employee_attendance_group_rel', 'payslip_id', 'employee_id', 'Employees')

    
    def auto_add_employee_batch(self):

        exclude_employee_ids = self.env.user.company_id.sh_employee_ids.ids
        # employees = self.env['hr.employee'].sudo().search(
        #     [('id', 'not in', exclude_employee_ids)])

        if 'active_model' in self.env.context and 'active_id' in self.env.context and self.env.context.get('active_model')=='hr.payslip.run':
            batch_id = self.env['hr.payslip.run'].sudo().browse(self.env.context.get('active_id'))
            if batch_id:
                #check running contract related employee list
                employees = False
                running_contract = self.env['hr.contract'].sudo().search([
                    ('date_start','<=',batch_id.date_end),
                    ('date_end','>=',batch_id.date_end),
                    ('state','in',['open','pending']),
                ])
                
                if running_contract:
                    employees =  running_contract.mapped('employee_id')

                # Check payslip already gerenerated    
                already_payslip_generated = self.env['hr.payslip'].sudo().search(
                    [('employee_id','in',employees.ids),
                     ('date_from','>=',batch_id.date_start),
                     ('date_to','<=',batch_id.date_end)])
                if already_payslip_generated:
                    already_payslip_generated_employee = already_payslip_generated.mapped('employee_id')
                    employees = employees - already_payslip_generated_employee

                # Check mofification request in draft or waiting stage
                date_start_with_time = str(batch_id.date_start) + " 00:00:00"
                date_end_with_time = str(batch_id.date_end) + " 23:59:59"
                pending_approval_modification_req = self.env['sh.attendance.modification.request'].sudo().search(
                    [('employee_id','in',employees.ids),
                     ('attendance_id.check_in','>=',date_start_with_time),
                     ('attendance_id.check_in','<=',date_end_with_time),
                     ('state','in',['waiting_for_approve'])
                     ])

                
                # Check leave request in to submit or to approve stage
               
                pending_leave_req = self.env['hr.leave'].sudo().search(
                    [('employee_ids','in',employees.ids),
                     ('request_date_from','>=',batch_id.date_start),
                     ('request_date_to','<=',batch_id.date_end),
                     ('state','in',['draft','confirm','validate1'])
                     ])
                
                if pending_approval_modification_req:
                    pending_approval_modification_req_employee = pending_approval_modification_req.mapped('employee_id')
                    employees = employees - pending_approval_modification_req_employee
                    self.attendance_employee_ids = [(6,0,pending_approval_modification_req_employee.ids)]



                if pending_leave_req:
                    pending_leave_req_employee = pending_leave_req.mapped('employee_id')
                    employees = employees - pending_leave_req_employee
                    self.leave_employee_ids = [(6,0,pending_leave_req_employee.ids)]




            if employees:
                self.employee_ids = [(6,0,employees.ids)]

        return {
            'name': _('Generate payslips for all selected employees'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.payslip.employees',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context':self.env.context
        }


    def compute_sheet(self):
        payslips = self.env['hr.payslip']
        [data] = self.read()
        active_id = self.env.context.get('active_id')
        if active_id:
            [run_data] = self.env['hr.payslip.run'].browse(active_id).read(['date_start', 'date_end', 'credit_note'])
        from_date = run_data.get('date_start')
        to_date = run_data.get('date_end')
        if not data['employee_ids']:
            raise UserError(_("You must select employee(s) to generate payslip(s)."))
        for employee in self.env['hr.employee'].browse(data['employee_ids']):
            slip_data = self.env['hr.payslip'].onchange_employee_id(from_date, to_date, employee.id, contract_id=False)
            res = {
                'employee_id': employee.id,
                'name': slip_data['value'].get('name'),
                'struct_id': slip_data['value'].get('struct_id'),
                'contract_id': slip_data['value'].get('contract_id'),
                'payslip_run_id': active_id,
                'input_line_ids': [(0, 0, x) for x in slip_data['value'].get('input_line_ids')],
                'worked_days_line_ids': [(0, 0, x) for x in slip_data['value'].get('worked_days_line_ids')],
                'date_from': from_date,
                'date_to': to_date,
                'credit_note': run_data.get('credit_note'),
                'company_id': employee.company_id.id,
            }
            payslips += self.env['hr.payslip'].create(res)
        payslips.compute_sheet()
        return {'type': 'ir.actions.act_window_close'}
