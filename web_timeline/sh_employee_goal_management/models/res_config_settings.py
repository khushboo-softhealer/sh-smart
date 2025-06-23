# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    # sh_goal_sheet_employee_ids = fields.Many2many('hr.employee','rel_goal_employee', string="Goal Sheet Employee")
    sh_goal_sheet_template_ids = fields.Many2many('sh.goal.sheet.template',string="Template For auto generate Goal Sheet")
    coach_deadline = fields.Integer("Coach Due Days")
    employee_deadline = fields.Integer("Employee Due Days")

class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    # sh_goal_sheet_employee_ids = fields.Many2many(
    #     'hr.employee', string="Goal Sheet Employees", readonly=False, related='company_id.sh_goal_sheet_employee_ids')
    sh_goal_sheet_template_ids = fields.Many2many('sh.goal.sheet.template',string="Template For auto generate Goal Sheet",readonly=False, related='company_id.sh_goal_sheet_template_ids')
    coach_deadline = fields.Integer(string="Coach Due Days", readonly=False, related='company_id.coach_deadline')
    employee_deadline = fields.Integer(string="Employee Due Days", readonly=False, related='company_id.employee_deadline')