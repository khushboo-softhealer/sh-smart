# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_sale_online_signature = fields.Boolean(
        'Sale Recurring Online Signature', related='company_id.sh_sale_online_signature', readonly=False)
