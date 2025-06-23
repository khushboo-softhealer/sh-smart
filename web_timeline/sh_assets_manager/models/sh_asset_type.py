# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models


class AssetType(models.Model):
    _inherit = ['mail.thread',
                'mail.activity.mixin']
    _name = "sh.asset.type"
    _description = "Asset Type Details"

    name = fields.Char("Name", required=True, tracking=True)
