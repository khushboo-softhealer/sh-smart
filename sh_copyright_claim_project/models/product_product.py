# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models


class ShProductProduct(models.Model):
    _inherit = 'product.product'

    def redirect_store(self):
        return {
            'type': 'ir.actions.act_url',
            'url': self.odoo_url,
            'target': 'new',
        }

    def redirect_shop(self):
        return {
            'type': 'ir.actions.act_url',
            'url': self.soft_url,
            'target': 'new',
        }
