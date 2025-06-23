# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class MailMessageSubtype(models.Model):
    _inherit = 'mail.message.subtype'

    remote_mail_message_subtype_id = fields.Char("Remote Mail Message Subtype ID",copy=False)