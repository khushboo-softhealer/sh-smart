# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import _, api, fields, models

class ShSaleOrderCancel(models.TransientModel):
    _inherit = 'sale.order.cancel'
    _description = "Sale Order Cancel"

    def open_sale_quotation_cancel_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cancel Quotation Reason',
            'res_model': 'sh.sale.quotation.cancel',
            'view_mode': 'form',
            'target': 'new',
            'context':{'default_order_id':self.env.context.get('active_id')}
        }