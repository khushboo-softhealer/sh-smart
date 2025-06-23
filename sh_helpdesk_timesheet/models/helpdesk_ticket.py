# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError


class ShHelpdesk(models.Model):
    _inherit = 'sh.helpdesk.ticket'

    start_time = fields.Datetime("Start Time", copy=False)
    end_time = fields.Datetime("End Time", copy=False)
    total_time = fields.Char("Total Time", copy=False)
    timehseet_ids = fields.One2many(
        'account.analytic.line', 'ticket_id', string='Timesheets')
    duration = fields.Float('Real Duration', compute='_compute_duration')
    ticket_running = fields.Boolean("Ticket Running")
    start_task_bool = fields.Boolean("Start Task",
                                     compute='_compute_start_task_bool')
    sh_ticket_task_id = fields.Many2one('project.task', string='Task ')

    def _compute_start_task_bool(self):
        for rec in self:
            rec.start_task_bool = True
            if not rec.sh_ticket_task_id:
                rec.start_task_bool = True
            else:
                if self.env.user.task_id.id == rec.sh_ticket_task_id.id:
                    rec.start_task_bool = False

    @api.model
    def get_duration(self, ticket):
        if ticket:
            ticket = self.sudo().browse(int(ticket))
            if ticket and ticket.start_time:
                diff = fields.Datetime.from_string(
                    fields.Datetime.now()) - fields.Datetime.from_string(ticket.start_time)
                if diff:
                    duration = float(diff.days) * 24 + \
                        (float(diff.seconds) / 3600)
                    return diff.total_seconds() * 1000

    @api.depends('timehseet_ids.unit_amount')
    def _compute_duration(self):
        for rec in self:
            rec.duration = 0.0
            if rec and rec.timehseet_ids:
                timesheet_line = rec.timehseet_ids.filtered(
                    lambda x: x.ticket_id.id == rec.id and x.end_date == False and x.start_date != False)
                if timesheet_line:
                    rec.duration = timesheet_line[0].unit_amount

    def action_ticket_start(self):
        return {
            'name': "Start Ticket",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.start.ticket',
            'target': 'new',
            'context': {'ticket_id':self.id}
        }

    def action_ticket_end(self):
        if self.sh_ticket_task_id:
            res = self.sh_ticket_task_id.action_task_end()
            return res

