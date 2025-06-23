# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import _, models, fields


class ResCompanyPartnerCateg(models.Model):
    _inherit = 'res.company'

    sh_partner_categ = fields.Many2one(
        'partner.category', string='Responsible Person ')


class ResConfigSettingsPartnerCategory(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_partner_categ = fields.Many2one(
        'partner.category', string='Partner Category', related='company_id.sh_partner_categ', readonly=False)
