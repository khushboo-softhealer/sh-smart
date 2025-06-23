# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sh_training_project_id = fields.Many2one(
        comodel_name='project.project', string=' Project ')
