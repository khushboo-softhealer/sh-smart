# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models


class ShSalesPersonCurrencyAlertSaleOrder(models.Model):
    _inherit = "sale.order"

    pricelist_alert = fields.Boolean(
        string="", default=False, compute="_currency_alert_compute")

    @api.depends('partner_id', 'pricelist_id')
    def _currency_alert_compute(self):
        for rec in self:
            rec.pricelist_alert = False
            if rec.pricelist_id and rec.pricelist_id.currency_id == self.company_id.currency_id:
                rec.pricelist_alert = True
            else:
                rec.pricelist_alert = False

    def update_prices(self):
        for line in self.order_line:
            line.update({'price_unit':  line._get_display_price()})
