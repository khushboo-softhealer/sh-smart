# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields


class EmployeeSheetCategoryLine(models.Model):
    _name = 'sh.goal.sheet.category.line'
    _description = "List of all Category Line"

    name = fields.Char("Category Line Name", required=True)
    description = fields.Text("Description")
    need_rating = fields.Boolean("Need Rating", default=True)
    category_id = fields.Many2one("sh.goal.sheet.category")
    sequence = fields.Integer(index=True, default=1)
