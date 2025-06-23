# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ShHelpdeskTicketType(models.Model):
    _inherit = 'sh.helpdesk.ticket.type'

    remote_sh_helpdesk_ticket_type_id = fields.Char("Remote Helpdesk Ticket Type ID",copy=False)

class ShHelpdeskTicketSubType(models.Model):
    _inherit = 'sh.helpdesk.sub.type'

    remote_helpdesk_sub_type_id = fields.Char("Remote Helpdesk Sub Type ID",copy=False)