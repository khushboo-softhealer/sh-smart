# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_training_project_id = fields.Many2one(
        comodel_name='project.project', string=' Project ', related='company_id.sh_training_project_id', readonly=False)
