# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields


class EmployeeGoalMarks(models.Model):
    _name = 'sh.goal.marks'
    _description = "Marks Given by Coach or Employee"
    _order = 'sequence,id'

    name = fields.Char("Marks")
    sequence = fields.Integer(index=True, default=1)
    is_required_for_emp = fields.Boolean("Is Required(Employee)")
    is_required_for_coach = fields.Boolean ("Is Required(coach)")