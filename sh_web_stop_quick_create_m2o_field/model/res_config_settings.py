# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    sh_model_ids = fields.Many2many("ir.model", string="Restrict Models")

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    sh_model_ids = fields.Many2many(
        "ir.model", string="Restrict Models",
        related="company_id.sh_model_ids", readonly=False)
