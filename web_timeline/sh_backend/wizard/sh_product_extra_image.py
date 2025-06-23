from odoo import models, fields,api
from odoo.tools.translate import html_translate
from odoo.exceptions import ValidationError
from datetime import timedelta, datetime

class ProductExtraImage(models.Model):
    _name = 'sh.product.extra.image'
    _description = "Product Extra Image"

    product_image_line = fields.One2many('product.image','product_extra_image_id',string = "Image")
    product_ids = fields.Many2many('product.product')

    def add_images(self):
        image_vals = []
        for rec in self.product_image_line:
            image_vals.append((0,0,{
                'name' : rec.name,
                'image' : rec.image
            }))

        self.product_ids.write({
            'product_image_ids' : image_vals,
            'product_variant_image_ids' : image_vals
        })
class ShProductImage(models.Model):
    _inherit = 'product.image'

    product_extra_image_id = fields.Many2one('sh.product.extra.image',string="product")