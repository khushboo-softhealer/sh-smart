# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields

class HelpdeskTicket(models.Model):
    _name = 'sh.helpdesk.ticket'
    _description = "Helpdesk Ticket"
    
    name = fields.Char('Name')
