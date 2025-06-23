# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.http import request
import datetime

from odoo import http
from odoo.http import request
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class TicketDashboard(models.Model):
    _name = 'sh.ticket.dashboard'
    _description = 'Ticket Dashboard'

    name = fields.Char('Name')

    def get_ticket_data(self, ids):
        return {
            'name': _('Tickets'),
            'type': 'ir.actions.act_window',
            'res_model': 'sh.helpdesk.ticket',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', ids)],
            'target': 'current'
        }
