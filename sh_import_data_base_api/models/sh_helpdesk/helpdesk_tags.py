# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class HelpdeskTags(models.Model):
    _inherit = 'sh.helpdesk.tags'

    remote_sh_helpdesk_tags_id = fields.Char("Remote Helpdesk Tags ID",copy=False)