# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    remote_hr_payslip_id = fields.Char("Remote Payslip Id",copy=False)

class HrPayslipLine(models.Model):
    _inherit = 'hr.payslip.line'

    remote_hr_payslip_line_id = fields.Char("Remote Payslip Line Id",copy=False)

class HrPayslipInput(models.Model):
    _inherit = 'hr.payslip.input'

    remote_hr_payslip_input_id = fields.Char("Remote Payslip Input Id",copy=False)

class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    remote_hr_payslip_run_id = fields.Char("Remote Payslip Run Id",copy=False)

class HrPayslipWorked_days(models.Model):
    _inherit = 'hr.payslip.worked_days'

    remote_hr_payslip_worked_days_id = fields.Char("Remote Payslip Work Day Id",copy=False)

class ShDefaultPayment(models.Model):
    _inherit = 'sh.default.payment'

    remote_sh_default_payment_id = fields.Char("Remote Default Payment Id",copy=False)

