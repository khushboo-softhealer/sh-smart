# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class SaleOrderOption(models.Model):
    _inherit = 'sale.order.option'
    
    remote_sale_order_option_id = fields.Char("Remote sale Order option ID",copy=False)
    