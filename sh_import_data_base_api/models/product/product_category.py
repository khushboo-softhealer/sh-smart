# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ProductCategory(models.Model):
    _inherit = 'product.category'

    remote_product_category_id = fields.Char("Remote Product Category ID",copy=False)


class ProductPublicCategory(models.Model):
    _inherit="product.public.category"

    remote_product_public_categ_id = fields.Char("Remote Ecommerce Category ID",copy=False)

class ProductAttributeValue(models.Model):
    _inherit="product.attribute.value"

    remote_product_attribute_value_id =fields.Char("Remote Product Attribute Value",copy=False)