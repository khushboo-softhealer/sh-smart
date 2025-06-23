# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models


class website(models.Model):
    _inherit = "website"
    
    sh_website_prod_price_label_label = fields.Char(string = "Product Prices Label")    
    
    category_style = fields.Selection( [('style1','Style 1'),('style2','Style 2'),('style3','Style 3'),('style4','Style 4')], string="Category Style")
    category_header_style = fields.Selection( [('style1','Style 1'),('style2','Style 2'),('style3','Style 3')], string="Category Header Style")
    sub_category_style = fields.Selection( [('style1','Style 1'),('style2','Style 2'),('style3','Style 3'),('style4','Style 4')], string="Subcategory Style")   
