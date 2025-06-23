# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    @api.onchange('product_id')
    def _onchange_product_id_warning(self):

        res = super(SaleOrderLine,self)._onchange_product_id_warning()

        self.update({
            'name' : self.product_id.name
        })

        return res
