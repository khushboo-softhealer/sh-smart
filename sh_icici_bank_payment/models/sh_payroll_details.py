from odoo import models, fields, api


class Payroll(models.Model):
    _inherit = "hr.payslip.run"

    bank_format = fields.Text("Icici Bank Format",copy=False)
    trancation_date = fields.Char("Trancation Date")
    bank_ref = fields.Char("Bank Refrence")
    default_payment = fields.Many2many(
        "sh.default.payment", string="Default Format",copy=False)

    def generate_format(self):
        lines = []
        total_salary = 0.00
        data = ''
        for emp in self.slip_ids:
            if emp.line_ids:
                for x in emp.line_ids:
                    if x.code == 'NET':
                        if x.amount > 0.00:
                            total_salary += round(x.amount, 2)
                            data = "PRB|NFT|" + str(round(x.amount, 2)) + "|INR|" + str(
                                emp.employee_id.sh_bank_account) + "|015305010946|0011|" + str(self.bank_ref) + "|N|PRBNBB^\n"
            lines.append(data)
        for values in self.default_payment:
            total_salary += round(values.total_amount, 2)
            lines.append(values.default_formate + "\n")
        # total_salary = total_salary
        first_line = "FHR|0011|015305010946|INR|" + str(total_salary) + "|" + str(len(self.slip_ids)+len(
            self.default_payment)) + "|" + str(self.trancation_date) + "|" + str(self.bank_ref) + "^\n"
        str1 = ''.join(lines)
        final_format = first_line + str1
        self.bank_format = final_format


class EmployeeAdditional(models.Model):
    _inherit = "hr.employee"

    sh_bank_account = fields.Char("Bank Refrence")


class EmployeeAdditional(models.Model):
    _inherit = "hr.employee.public"

    sh_bank_account = fields.Char("Bank Refrence")
