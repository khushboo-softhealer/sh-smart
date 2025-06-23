# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class HrPayrollStructure(models.Model):
    _inherit = 'hr.payroll.structure'

    remote_hr_payroll_structure_id = fields.Char("Remote Hr Payroll Structure Id",copy=False)
