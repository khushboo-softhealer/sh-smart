# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    send_payslip = fields.Boolean(
        "Send Payslip in Email ?", related='company_id.send_payslip', readonly=False)


class HrEmployee(models.Model):
    _inherit = 'hr.employee.public'

    send_payslip = fields.Boolean(
        "Send Payslip in Email ?", related='company_id.send_payslip', readonly=False)
