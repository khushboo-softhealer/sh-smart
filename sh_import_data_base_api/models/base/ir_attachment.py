# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    remote_ir_attachment_id = fields.Char("Remote Attachment ID",copy=False)