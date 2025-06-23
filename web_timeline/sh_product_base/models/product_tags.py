# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields

class product_tags(models.Model):
    _name = 'product.tags'
    _description = "Product Tags"
    
    name = fields.Char(string="Tag Name", required="1")
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.company)