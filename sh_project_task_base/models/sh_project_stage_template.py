# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class UpdatemassProject(models.Model):
    _name = "sh.project.stage.template"
    _description = "Project Task Template"

    name = fields.Char(required=True) 
    stage_ids = fields.Many2many('project.task.type', string="Stages", required=True)
    sh_pricing_mode = fields.Selection([
        ('fp', 'FP - Fixed Price'),
        ('tm', 'T&M - Time and Material'),
    ], string="Pricing Model")
    sh_fp_based_on = fields.Selection([
        ('no_milestone', 'No Milestone - One shot'),
        ('milestone', 'Implementation Project'),
    ], string='FP Based On', help='')
    sh_tm_based_on = fields.Selection([
        ('success_pack', 'Success Packs Based'),
        ('billable', 'Billable Hours Based'),
    ], string='T&M Based On',
    help='Success Packs Based (Renewable required based on usage) - SO\nBillable Hours Based (Monthly billable invoice created) - MANUALLY')
