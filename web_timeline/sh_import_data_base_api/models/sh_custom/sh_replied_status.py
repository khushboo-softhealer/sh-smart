# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ShRepliedStatus(models.Model):
    _inherit = 'sh.replied.status'

    remote_sh_replied_status_id = fields.Char("Remote Replied Status ID",copy=False)

