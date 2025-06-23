# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models


class placement(models.Model):
    _inherit = ['mail.thread',
                'mail.activity.mixin']
    _name = 'sh.placement'
    _description = 'Placement Data'

    name = fields.Char(required=True, tracking=True)
    date = fields.Date(tracking=True)
    note = fields.Text(tracking=True)
    placement_line = fields.One2many(
        comodel_name='sh.placement.line', inverse_name='placement_id', string='Placement Lines',)


class PlecementLine(models.Model):
    _name = 'sh.placement.line'
    _description = 'Placement Line'

    placement_id = fields.Many2one('sh.placement', string='placement Reference',
                                   required=True)
    college_id = fields.Many2one(comodel_name='sh.college', string='College')
    total_candidate_applied = fields.Integer()
    selected_candidate = fields.Integer()
    present_candidate = fields.Integer()
    absent_candidate = fields.Integer()
