# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    property_account_position_id = fields.Many2one('account.fiscal.position',
        string="Fiscal Position",
        company_dependent=False,
        domain="[]",
        help="The fiscal position determines the taxes/accounts used for this contact.")
