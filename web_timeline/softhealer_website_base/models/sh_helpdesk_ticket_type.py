# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields

class HelpdeskTicketType(models.Model):
    _inherit = 'sh.helpdesk.ticket.type'

    sh_display_at_so_portal = fields.Boolean('Display at so portal view')