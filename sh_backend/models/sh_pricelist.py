# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, api, _


class sh_product_pricelist(models.Model):
    _inherit = 'product.pricelist'
    
    sh_show_in_offer_page = fields.Boolean(string="Show in offer page?")
    sh_description = fields.Html(string="Description")
