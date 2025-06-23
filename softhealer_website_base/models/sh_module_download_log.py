# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models

class ShModuleDownloadLog(models.Model):
    _name = "sh.module.download.log"
 
    name = fields.Char()
    partner_id = fields.Many2one(
        string='User',
        comodel_name='res.partner',
        ondelete='set null'
    )
    sale_order_id = fields.Many2one(
        string='Order',
        comodel_name='sale.order',
        ondelete='set null'
    )
    product_id = fields.Many2one(
        string='Product',
        comodel_name='product.product',
        ondelete='set null'
    )
    download_count = fields.Integer(
        string='Download Count',
    )
    type = fields.Selection(
        string='Type',
        selection=[
            ('info', 'Info'),
            ('error', 'Error')
        ]
    )
    download_comment = fields.Text(
        string='Comment',
    )
    
    

    
    
    
