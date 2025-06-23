# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields


class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    user_id = fields.Many2one('res.users', string='Responsible Person',
                              related='company_id.user_id', readonly=False)
