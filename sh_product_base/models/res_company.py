# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, api, _


class ResCompany(models.Model):
    _inherit = 'res.company'
    
    current_euro_rate = fields.Float(string="Current Euro Rate")
    current_usd_rate = fields.Float(string="Current USD Rate")

    # @api.multi
    def on_update_press(self):
        search_product = self.env['product.product'].search([('euro_price','>',0.00)])
        for product in search_product:
            product.list_price = product.euro_price * self.current_euro_rate
            
    # @api.multi
    def on_update_press_usd(self):
        search_product = self.env['product.product'].search([('euro_price','>',0.00)])
        for product in search_product:
            product.list_price = product.list_price * self.current_usd_rate
