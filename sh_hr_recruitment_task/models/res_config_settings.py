# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models


class ResConfigSetting(models.TransientModel):
    _inherit = "res.config.settings"

    project_id = fields.Many2one('project.project',
                                 string="Project",
                                 related='company_id.project_id',
                                 readonly=False)
