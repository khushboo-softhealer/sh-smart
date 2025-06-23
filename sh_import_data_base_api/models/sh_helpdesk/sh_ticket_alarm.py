# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ShTicketAlarm(models.Model):
    _inherit = 'sh.ticket.alarm'

    remote_sh_ticket_alarm_id = fields.Char("Remote Helpdesk Ticket ID",copy=False)