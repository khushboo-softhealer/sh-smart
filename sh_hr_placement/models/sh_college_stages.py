# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models


class CollegeStages(models.Model):
    _name = 'sh.college.stages'
    _order = 'sequence, id'
    _description = "College Stages"

    name = fields.Char(string='Stage Name', required=True, translate=True)
    fold = fields.Boolean(string='Folded in Kanban',
                          help='This stage is folded in the kanban view when there are no records in that stage to display.')
    sequence = fields.Integer(
        default=1, help="Gives the sequence order when displaying a list of Stages.")
