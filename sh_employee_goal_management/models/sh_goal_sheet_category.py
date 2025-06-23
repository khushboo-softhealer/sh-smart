# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields


class EmployeeSheetCategory(models.Model):
    _name = 'sh.goal.sheet.category'
    _description = "List of all Category"
    _order = 'sequence, id'

    name = fields.Char(string="Category", required=True)
    sequence = fields.Integer("Sequence")
    category_line_ids = fields.One2many(
        "sh.goal.sheet.category.line", "category_id")
    active = fields.Boolean('Active', default=True)
    goal_marks_ids = fields.Many2many("sh.goal.marks",string="Goal Marks")
