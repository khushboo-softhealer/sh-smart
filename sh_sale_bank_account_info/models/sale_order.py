# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models, api


class ShSaleBankAccountInfoSaleOrder(models.Model):
    _inherit = 'sale.order'

    sh_bank_account_id = fields.Many2one("res.partner.bank", "Bank Account")
    odoo_version = fields.Many2one('sh.version', string="Version")
    timeline = fields.Char(string="Timeline")
    estimated_hrs = fields.Float(string="Estimated Hours", copy=False)
    odoo_edition = fields.Selection(
        [('community', 'Community'), ('enterprise', 'Enterprise')], string=" Edition")

    # @api.onchange('order_line')
    # def onchange_of_estimated_hrs(self):
    #     if not self.website_id:
    #         self.estimated_hrs = sum(self.order_line.mapped('product_uom_qty'))

    # @api.depends("order_line.product_uom_qty")
    # def _compute_estimated_hrs(self):
    #     for rec in self:
    #         rec.estimated_hrs = sum(rec.order_line.mapped('product_uom_qty'))
            