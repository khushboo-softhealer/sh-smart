# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models


class ShConfirmSalePaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    def _send_mail_to_download_module(self):
        active_model = self._context.get('active_model')
        active_ids = self._context.get('active_ids')
        if not (active_model and active_ids):
            return
        if active_model != 'account.move':
            return
        account_move_ids = self.env[active_model].browse(active_ids)
        account_move_ids._send_download_module_mail()

    def action_create_payments(self):
        status = super(ShConfirmSalePaymentRegister, self).action_create_payments()
        self._send_mail_to_download_module()
        return status
