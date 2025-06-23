# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    sh_leave_type_id = fields.Many2one('hr.leave.type', 'Leave Type')
    sh_unpaid_leave_type_id = fields.Many2one(
        'hr.leave.type', 'Unpaid Leave Type')
    sh_employee_ids = fields.Many2many('hr.employee', string="Exclude Employees")


class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_leave_type_id = fields.Many2one(
        'hr.leave.type', 'Leave Type', readonly=False, related='company_id.sh_leave_type_id')
    sh_unpaid_leave_type_id = fields.Many2one(
        'hr.leave.type', 'Unpaid Leave Type', readonly=False, related='company_id.sh_unpaid_leave_type_id')
    sh_employee_ids = fields.Many2many(
        'hr.employee', string="Exclude Employees", readonly=False, related='company_id.sh_employee_ids')
