# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    annexure_b_notes = fields.Html(related='company_id.annexure_b_notes', string='Annexure - B ',readonly=False)
