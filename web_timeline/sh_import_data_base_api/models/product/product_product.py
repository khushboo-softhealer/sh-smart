# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    remote_product_product_id = fields.Char("Remote Product Varient ID",copy=False)