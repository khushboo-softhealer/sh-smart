# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    remote_sale_order_id = fields.Char("Remote Order ID",copy=False)
    

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    remote_sale_order_line_id = fields.Char("Remote Order line ID",copy=False)