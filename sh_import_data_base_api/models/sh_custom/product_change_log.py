# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ProductChangeLog(models.Model):
    _inherit = 'product.change.log'

    remote_product_change_log_id = fields.Char("Remote Product Change Log ID",copy=False)




