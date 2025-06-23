# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError


class TicketTimeAccountLine(models.Model):
    _name = 'ticket.time.account.line'
    _description = 'Ticket Time Account Line'

    def _get_default_start_time(self):
        active_model = self.env.context.get('active_model')
        if active_model == 'sh.helpdesk.ticket':
            active_id = self.env.context.get('active_id')
            if active_id:
                ticket_search = self.env['sh.helpdesk.ticket'].search(
                    [('id', '=', active_id)], limit=1)
                return ticket_search.start_time

    def _get_default_end_time(self):
        return datetime.now()

    def _get_default_duration(self):
        active_model = self.env.context.get('active_model')
        if active_model == 'sh.helpdesk.ticket':
            active_id = self.env.context.get('active_id')
            if active_id:
                ticket_search = self.env['sh.helpdesk.ticket'].search(
                    [('id', '=', active_id)], limit=1)
                diff = fields.Datetime.from_string(fields.Datetime.now(
                )) - fields.Datetime.from_string(ticket_search.start_time)
                if diff:
                    duration = float(diff.days) * 24 + \
                        (float(diff.seconds) / 3600)
                    return round(duration, 2)

    name = fields.Char("Description", required=True)
    start_date = fields.Datetime(
        "Start Date", default=_get_default_start_time, readonly=True)
    end_date = fields.Datetime(
        "End Date", default=_get_default_end_time, readonly=True)
    duration = fields.Float(
        "Duration (HH:MM)", default=_get_default_duration, readonly=True)
    company_id = fields.Many2one(
        'res.company', string='Company', default=lambda self: self.env.user.company_id)
    project_id = fields.Many2one('project.project', string='Project')

    @api.model
    def default_get(self, fields_list):
        res = super(TicketTimeAccountLine, self).default_get(fields_list)
        active_id = self.env.context.get('active_id')
        ticket_id = self.env['sh.helpdesk.ticket'].sudo().browse(active_id)
        if ticket_id:
            timesheet_line = ticket_id.timehseet_ids.filtered(
                lambda x: x.ticket_id.id == ticket_id.id and x.end_date == False and x.start_date != False)
            if timesheet_line:
                res.update({
                    'project_id': timesheet_line.project_id.id,
                })
        else:
            if self.env.user.company_id.project_id:
                res.update({
                    'project_id': self.env.user.company_id.project_id.id,
                })
        return res

    def end_ticket(self):

        if self.sh_ticket_task_id:
            res = self.sh_ticket_task_id.action_task_end()
            return res
