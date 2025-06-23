# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields


class ShPaymentAttachmentAccountPayment(models.Model):
    _inherit = 'account.payment'

    """
        INHERITED BY SOFTHEALER TECHNOLOGIES
    """

    sh_attachments = fields.Many2many('ir.attachment', string="Payment Attachments")
