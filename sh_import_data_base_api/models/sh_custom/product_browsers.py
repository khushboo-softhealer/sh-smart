# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ProductBrowsers(models.Model):
    _inherit = 'product.browsers'

    remote_product_browsers_id = fields.Char("Remote Product Browser ID",copy=False)





