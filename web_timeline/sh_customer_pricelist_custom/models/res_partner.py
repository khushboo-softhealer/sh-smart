# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    property_product_pricelist = fields.Many2one(
        'product.pricelist', 'Pricelist', compute='_compute_product_pricelist',
        inverse="_inverse_product_pricelist", company_dependent=False,
        help="This pricelist will be used, instead of the default one, for sales to the current partner", store=True)
