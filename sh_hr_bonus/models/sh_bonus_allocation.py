# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import api, fields, models


class BonusAllocation(models.Model):
    _name = 'sh.bonus.allocation'
    _description = "Bonus Allocation"

    name = fields.Char(readonly=True)
    application_date = fields.Date()
    payslip_date = fields.Date()
    bonus_template_id = fields.Many2one('sh.bonus.template', required=True)
    bonus_employee_allocation_line = fields.One2many(
        'sh.bonus.employee.allocation', 'bonus_allocation_id')
    status = fields.Selection(
        [('new', 'New'), ('close', 'Close')], string="State", default='new')
    bank_format = fields.Text("Icici Bank Format")
    trancation_date = fields.Char("Transaction Date")
    bank_ref = fields.Char("Bank Refrence")
    default_payment = fields.Many2many(
        "sh.default.payment", string="Default Format")

    def generate_format(self):
        lines = []
        total_salary = 0.00
        data = ''
        for emp in self.bonus_employee_allocation_line:
            if emp.bonus_amount:

                total_salary += round(emp.bonus_amount, 2)
                data = "PRB|NFT|" + str(round(emp.bonus_amount, 2)) + "|INR|" + str(
                    emp.employee_id.sh_bank_account) + "|015305010946|0011|" + str(self.bank_ref) + "|N|PRBNBB^\n"
            lines.append(data)
        for values in self.default_payment:
            total_salary += round(values.total_amount, 2)
            lines.append(values.default_formate + "\n")
        # total_salary = total_salary
        first_line = "FHR|0011|015305010946|INR|" + str(total_salary) + "|" + str(len(self.bonus_employee_allocation_line)+len(
            self.default_payment)) + "|" + str(self.trancation_date) + "|" + str(self.bank_ref) + "^\n"
        str1 = ''.join(lines)
        final_format = first_line + str1
        self.bank_format = final_format

    def add_employees(self):
        self.bonus_employee_allocation_line = False
        all_employees = self.env['hr.employee'].search([])

        for employee in all_employees:
            average_wage = 0
            payslips = self.env['hr.payslip'].sudo().search(
                [('employee_id', '=', employee.id), ('state', '=', 'done')], order='id desc', limit=12)
            if payslips:
                if len(payslips) == 12:
                    for payslip in payslips:
                        basic_salary = payslip.line_ids.filtered(
                            lambda x: x.code == 'GROSS')
                        average_wage += basic_salary.total
                    average_wage = average_wage/12
                else:
                    for payslip in payslips:
                        basic_salary = payslip.line_ids.filtered(
                            lambda x: x.code == 'GROSS')
                        average_wage += basic_salary.total

                    average_wage = average_wage/len(payslips)

            self.env['sh.bonus.employee.allocation'].create({
                'employee_id': employee.id,
                'average_wage': average_wage,
                'bonus_allocation_id': self.id
            })

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals.update(
                {'name': self.env['ir.sequence'].next_by_code('bonus.allocation')})
        res = super(BonusAllocation, self).create(vals_list)
        return res
