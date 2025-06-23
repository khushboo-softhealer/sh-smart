# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models


class ShConfirmSaleAccount(models.Model):
    _inherit = 'account.move'

    """
        INHERITED BY SOFTHEALER TECHNOLOGIES.

        # _compute_payment_state override because when payment state is changed,
        then the respected sale order bool(is_sh_confirm_sale) is updated
    """

    # @api.depends('amount_residual', 'move_type', 'state', 'company_id')
    def _compute_payment_state(self):
        super()._compute_payment_state()
        for rec in self:
            if rec.payment_state == 'paid' or rec.state == 'posted':
                orders = rec.line_ids.sale_line_ids.order_id
                if orders:
                    orders._is_sale_order_confirmed()

    def button_draft(self):
        super(ShConfirmSaleAccount, self).button_draft()
        for move in self:
            orders = move.line_ids.sale_line_ids.order_id
            if orders:
                orders._is_sale_order_confirmed()

    def unlink(self):
        orders_list = []
        for move in self:
            orders_list.append(move.line_ids.sale_line_ids.order_id)
        super(ShConfirmSaleAccount, self).unlink()
        for order_obj in orders_list:
            order_obj._is_sale_order_confirmed()

    def _send_download_module_mail(self):
        if not self:
            return
        out_invoice_list = []
        for move in self:
            # If not customer invoice
            if move.move_type != 'out_invoice':
                continue
            # If the invoice is partialy paid
            if move.amount_residual:
                continue
            out_invoice_list.append(move)
        if not out_invoice_list:
            return
        for invoice in out_invoice_list:
            for order in invoice.line_ids.sale_line_ids.order_id:
                order._send_mail_to_download_module()
