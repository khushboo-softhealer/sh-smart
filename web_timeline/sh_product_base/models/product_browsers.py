# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields

class ProductBrowsers(models.Model):
    _name = 'product.browsers'
    _description = "Product Browsers"
    
    name = fields.Char('Name')
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.company)