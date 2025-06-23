# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, api


class HRDashboard(models.Model):
    _name = 'sh.hr.dashboard'
    _description = 'HR Dashboard'

    name = fields.Char("Name")

    def create_expense(self):
        employee = self.env['hr.employee'].sudo().search(
            [('user_id', '=', self.env.user.id)], limit=1)
        if employee:

            return {
                'name': "Expense",
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'hr.expense',
                'target': 'current',
                'context': {'default_employee_id': employee.id}
            }

    def create_modification_request(self):
        return {
            'name': "Attendance Modification Request",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sh.attendance.modification.request',
            'target': 'current',
        }

    def create_leave(self):
        employee = self.env['hr.employee'].sudo().search(
            [('user_id', '=', self.env.user.id)], limit=1)
        if employee:

            return {
                'name': "Leave Request",
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'hr.leave',
                'target': 'current',
                'context': {'default_employee_id': employee.id}
            }

    def create_complain(self):
        return {
            'name': "Complain",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.complain',
            'target': 'current',
        }

    def create_idea(self):
        return {
            'name': "Idea",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.idea',
            'target': 'current',
        }

    def open_employee_payslip(self):
        view_id = self.env.ref('hr_payroll.view_hr_payslip_tree')

        return {
            'name': "Payslips",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,kanban,form',
            'res_model': 'hr.payslip',
            'domain': [('employee_id.user_id', '=', self.env.user.id), ('state', '=', 'done')],
            'target': 'current',
        }

    def get_payslip_count(self):
        for rec in self:
            rec.payslip_count = self.env['hr.payslip'].sudo().search_count(
                [('employee_id.user_id', '=', self.env.user.id), ('state', '=', 'done')])

    def open_employee_leave(self):

        return {
            'name': "Leaves",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form,activity',
            'res_model': 'hr.leave',
            'domain': [('employee_id.user_id', '=', self.env.user.id)],
            'target': 'current',
        }

    def get_leave_count(self):
        for rec in self:
            rec.leave_count = 0
            rec.allocated_leave_count = 0

            data_days = {}

            paid_leave_type = self.env['hr.leave.type'].sudo().search(
                [('allocation_type', '=', 'fixed_allocation')], limit=1)
            employee = self.env['hr.employee'].sudo().search(
                [('user_id', '=', self.env.uid)], limit=1)
            if paid_leave_type and employee:
                employee_id = employee.id

                if employee_id:
                    data_days = paid_leave_type.get_days(employee_id)

                result = data_days.get(paid_leave_type.id, {})
                rec.leave_count = result.get('leaves_taken', 0)
                rec.allocated_leave_count = result.get('max_leaves', 0)

    def open_employee_attendnace(self):

        return {
            'name': "Attendance",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,kanban,form',
            'res_model': 'hr.attendance',
            'domain': [('employee_id.user_id', '=', self.env.user.id)],
            'target': 'current',
        }

    def get_attendance_count(self):
        for rec in self:
            rec.attendance_count = self.env['hr.attendance'].sudo().search_count(
                [('employee_id.user_id', '=', self.env.user.id)])

    def open_employee_expense(self):

        return {
            'name': "Expense",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,kanban,form,graph,pivot,activity',
            'res_model': 'hr.expense',
            'domain': [('employee_id.user_id', '=', self.env.user.id)],
            'target': 'current',
        }

    def get_expense_count(self):
        for rec in self:
            rec.expense_count = 0
            expenses = self.env['hr.expense'].sudo().search(
                [('employee_id.user_id', '=', self.env.user.id)])
            if expenses:
                for expense in expenses:
                    rec.expense_count += expense.total_amount

    def open_employee_contract(self):

        return {
            'name': "Contract",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form,activity',
            'res_model': 'hr.contract',
            'domain': [('employee_id.user_id', '=', self.env.user.id)],
            'target': 'current',
        }

    def get_contract_count(self):
        for rec in self:
            rec.contract_count = self.env['hr.contract'].sudo().search_count(
                [('employee_id.user_id', '=', self.env.user.id)])

    # def get_wallet_amount(self):
    #     for rec in self:
    #         related_employee = self.env['sh.wallet'].sudo().search(
    #             [('user_id', '=', self.env.user.id)], limit=1)
    #         rec.wallet_amount = related_employee.wallet_amount
    #         if not related_employee and self.env.user.has_group('sh_expense_wallet.group_expense_wallet'):
    #             total_amount = 0.0
    #             wallets = self.env['sh.wallet'].sudo().search([])
    #             for wallet in wallets:
    #                 total_amount = total_amount + wallet.wallet_amount

    #             rec.wallet_amount = total_amount

    def get_login_user(self):
        for rec in self:
            rec.user_id = self.env.uid

    name = fields.Char("Name")
    user_id = fields.Many2one(
        'res.users', string="User", compute='get_login_user')
    payslip_count = fields.Integer(
        "Payslip Count", compute='get_payslip_count')
    leave_count = fields.Float("Leave Count", compute='get_leave_count')
    allocated_leave_count = fields.Integer(
        "Leave Count ", compute='get_leave_count')
    attendance_count = fields.Integer(
        "Attendance Count", compute='get_attendance_count')
    expense_count = fields.Integer(
        "Expense Count", compute='get_expense_count')
    contract_count = fields.Integer(
        "Contract Count", compute='get_contract_count')
    wallet_amount = fields.Float("Wallet Amount", compute="get_wallet_amount")
