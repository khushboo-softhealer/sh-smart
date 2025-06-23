# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields

class Timesheet(models.Model):
    _inherit = 'account.analytic.line'

    ticket_id = fields.Many2one('sh.helpdesk.ticket', string='Helpdesk Ticket')
    start_date = fields.Datetime("Start Date", readonly=True)
    end_date = fields.Datetime("End Date", readonly=True)

