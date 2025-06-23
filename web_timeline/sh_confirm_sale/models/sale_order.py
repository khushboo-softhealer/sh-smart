# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models


class ShConfirmSale(models.Model):
    _inherit = 'sale.order'

    """
        INHERITED BY SOFTHEALER TECHNOLOGIES.

        field bool : is_sh_confirm_sale for Check That Sale Is Confirmed
    """

    is_sh_confirm_sale = fields.Boolean(string="Is Confirm Sale", default=False, copy=False)
    sh_is_download_module_mail_sent = fields.Boolean(string="Is Download Module Mail Sent", default=False, copy=False)

    def _is_sale_order_confirmed(self):
        for order in self:
            order.is_sh_confirm_sale = False
            if not order.order_line:
                continue
            # Check if Not have any products tech name
            if not any(line.product_id.sh_technical_name for line in order.order_line):
                continue
            if not order.invoice_ids:
                continue
            credit_notes = filter(lambda inv: inv.move_type == 'out_refund', order.invoice_ids)
            if credit_notes:
                if any(credit_note.state == 'posted' for credit_note in credit_notes):
                    continue
            for invoice in filter(lambda inv: inv.move_type == 'out_invoice', order.invoice_ids):
                # Customer Invoice
                if invoice.state == 'posted' and not invoice.amount_residual:
                    order.is_sh_confirm_sale = True
                    order._send_mail_to_download_module()
                    break

    def _send_mail_to_download_module(self):
        """
        Send mail if the order have any downloadable module in order line
        :return: None
        """
        if not self.is_sh_confirm_sale:
            return False
        if self.partner_id.sh_confirm_sale_is_odoo_customer:
            return False
        if self.sh_is_download_module_mail_sent:
            return True
        # Get the email template
        email_template_id = self.env.ref('sh_confirm_sale.sh_confirm_sale_download_module_mail', raise_if_not_found=False)
        if not email_template_id:
            # Failed to get mail template view !
            return False
        email_template = self.env['mail.template'].browse(email_template_id.id)
        if not email_template:
            # Failed to get mail template record !
            return False
        
        # self._notify_get_recipients_groups()
        email_template.sudo().send_mail(self.id, force_send=True)
        self.sh_is_download_module_mail_sent = True
        return True

    def multi_action_is_sale_confirm(self):
        self = self or self.browse(self.env.context.get('active_ids'))
        self._is_sale_order_confirmed()
    
    def _get_sale_order_link(self):
        groups = self._notify_get_recipients_groups()
        for list_item in groups:
            if isinstance(list_item, tuple):
                for tuple_item in list_item:
                    if isinstance(tuple_item, dict):
                        for key,val in tuple_item.items():
                            if key == 'button_access':
                                if isinstance(val, dict):
                                    if val.get('url'):
                                        return val['url']
        return False
