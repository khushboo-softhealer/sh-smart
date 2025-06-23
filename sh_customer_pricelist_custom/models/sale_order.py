# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _action_confirm(self):
        result = super()._action_confirm()
        if self.pricelist_id != self.partner_id.property_product_pricelist:
            self.partner_id.property_product_pricelist = self.pricelist_id
        return result
