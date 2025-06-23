# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    project_id = fields.Many2one('project.project', string="Project")
