# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class ShGithubIrAttachment(models.Model):
    _inherit = 'ir.attachment'

    sh_path = fields.Char('Index Path')
