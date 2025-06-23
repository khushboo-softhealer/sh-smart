# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models,fields,api,_

class ShProject(models.Model):
    _inherit='project.project'
    
    sh_product_id = fields.Many2one('product.product','Invoice Product',tracking=True)