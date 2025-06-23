# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class HelpdeskPriority(models.Model):
    _inherit = 'helpdesk.priority'

    remote_helpdesk_priority_id = fields.Char("Remote Helpdesk Priority ID",copy=False)