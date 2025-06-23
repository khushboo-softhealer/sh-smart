# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ProductTags(models.Model):
    _inherit = 'product.tags'

    remote_product_tags_id = fields.Char("Remote Product Tags ID",copy=False)