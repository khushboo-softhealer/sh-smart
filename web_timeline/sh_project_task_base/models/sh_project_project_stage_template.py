# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ProjectStageTemplate(models.Model):
    _name = "sh.project.project.stage.template"
    _description = "Project Stage Template"

    name = fields.Char('Name') 
    sh_stage_ids = fields.Many2many('project.project.stage', string="Stages")
    sh_pricing_mode = fields.Selection([
        ('fp', 'FP - Fixed Price'),
        ('tm', 'T&M - Time and Material'),
    ], string='Pricing Mode')
    sh_fp_based_on = fields.Selection([
        ('no_milestone', 'No Milestone - One shot'),
        ('milestone', 'Implementation Project'),
    ], string='FP Based On', help='')
    sh_tm_based_on = fields.Selection([
        ('success_pack', 'Success Packs Based'),
        ('billable', 'Billable Hours Based'),
    ], string='T&M Based On',
    help='Success Packs Based (Renewable required based on usage) - SO\nBillable Hours Based (Monthly billable invoice created) - MANUALLY')
    sh_default_stage_id = fields.Many2one('project.project.stage', string='Default Stage When Create')