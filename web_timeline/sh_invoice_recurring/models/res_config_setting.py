# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_invoice_online_signature = fields.Boolean('Invoice Recurring Online Signature', related='company_id.sh_invoice_online_signature', readonly=False)
