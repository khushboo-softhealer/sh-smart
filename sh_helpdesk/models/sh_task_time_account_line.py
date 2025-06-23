# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields,api


class TaskTimeAccountLine(models.Model):
    _inherit = 'task.time.account.line'

    @api.model
    def _get_default_ticket(self):

        # when end from pause task entry
        active_model = self.env.context.get('active_model')
        if active_model == 'sh.pause.task.entry':
            active_id = self.env.context.get('active_id')
            entry_search = self.env['sh.pause.task.entry'].search(
                [('id', '=', active_id)], limit=1)
            if entry_search:

                if entry_search.account_analytic_id and entry_search.account_analytic_id.ticket_id.id:
                    return entry_search.account_analytic_id.ticket_id.id

        if self.env.user.ticket_id:
            return self.env.user.ticket_id.id

        
    ticket_id = fields.Many2one('sh.helpdesk.ticket', string="Ticket No", default=_get_default_ticket)
    split_ticket_id = fields.Many2one('sh.helpdesk.ticket', string="Ticket No")

