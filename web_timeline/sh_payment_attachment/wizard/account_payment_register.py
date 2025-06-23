# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields


class ShPaymentAttachmentAccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    """
        INHERITED BY SOFTHEALER TECHNOLOGIES
    """
    sh_attachments = fields.Many2many('ir.attachment', string="Attachments")

    def _init_payments(self, to_process, edit_mode=False):
        """
            Write attachments values in account payment.
        """
        # OVERRIDE
        payments = super()._init_payments(to_process, edit_mode=edit_mode)

        if self.sh_attachments:
            payments.sudo().write({
                'sh_attachments': self.sh_attachments.ids,
            })
            payments.sh_attachments.sudo().write({
                'res_id': payments.id,
                'res_model': 'account.payment',
            })
            if self.display_name:
                payments.sh_attachments.sudo().write({
                    'res_name': payments.display_name,
                })

        return payments
