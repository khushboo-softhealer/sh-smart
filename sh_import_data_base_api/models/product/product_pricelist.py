# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    remote_product_pricelist_id = fields.Char("Remote Product Pricelist ID",copy=False)