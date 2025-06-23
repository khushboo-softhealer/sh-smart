# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ShHelpdeskTicket(models.Model):
    _inherit = 'sh.helpdesk.ticket'

    remote_sh_helpdesk_ticket_id = fields.Char("Remote Helpdesk Ticket ID",copy=False)