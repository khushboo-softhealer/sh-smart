# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    claim_project_id = fields.Many2one(comodel_name='project.project')
    claim_users = fields.Many2many('res.users',string="Claim Responsible Users")

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    claim_project_id = fields.Many2one(
        comodel_name='project.project', related="company_id.claim_project_id", readonly=False)
    claim_users = fields.Many2many('res.users', related="company_id.claim_users", readonly=False, string="Claim Responsible User")