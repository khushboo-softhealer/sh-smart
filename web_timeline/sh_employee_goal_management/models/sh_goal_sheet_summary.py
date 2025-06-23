# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields


class GoalSheetSummary(models.Model):
    _name = 'sh.goal.sheet.summary'
    _description = "List of all Goal Sheet Summary"

    category_id = fields.Many2one('sh.goal.sheet.category', string="Category")
    employee_sum = fields.Integer("Employee Total")
    coach_sum = fields.Integer("Coach Sum")
    goal_id = fields.Many2one('sh.goal.sheet')
    total_sum = fields.Integer("Total")
