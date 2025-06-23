# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class TaskTransfer(models.Model):
    _name = 'sh.transfer.timesheet'
    _description = 'Used To Transfer the Timesheet From Temporary'

    def _get_default_transfer_duration(self):
        context = dict(self.env.context or {})
        analytic_id = self.env['account.analytic.line'].browse(
            int(context.get('analytic_id')))
        return analytic_id.unit_amount

    def _get_default_transfer_project(self):
        context = dict(self.env.context or {})
        analytic_id = self.env['account.analytic.line'].browse(
            int(context.get('analytic_id')))
        return analytic_id.project_id

    def _get_default_transfer_task(self):
        context = dict(self.env.context or {})
        analytic_id = self.env['account.analytic.line'].browse(
            int(context.get('analytic_id')))
        return analytic_id.task_id

    def _get_default_description(self):
        context = dict(self.env.context or {})
        analytic_id = self.env['account.analytic.line'].browse(
            int(context.get('analytic_id')))
        return analytic_id.name
    
    def _get_default_ticket_id(self):
        ticket_id = self.env.context.get('ticket_id')
        return ticket_id


    name = fields.Text("Description", default=_get_default_description)
    duration = fields.Float("Duration (HH:MM)",
                            default=_get_default_transfer_duration,
                            readonly=True)

    project_id = fields.Many2one(
        'project.project', 'Project', default=_get_default_transfer_project)
    ticket_id = fields.Many2one('sh.helpdesk.ticket', string="Ticket No", default=_get_default_ticket_id)
    task_id = fields.Many2one('project.task', 'Task', default=_get_default_transfer_task, domain=[
                              ('project_id', '=', 'project_id.id')])

    def transfer_timesheet(self):
        allow_timesheet_in_done_task = False
        if self.ticket_id and (self.env.user.id in self.ticket_id.sh_user_ids.ids) and self.ticket_id.stage_id.id in [self.env.company.sh_customer_replied_stage_id.id, self.env.company.sh_in_progress_stage_id.id]:
            allow_timesheet_in_done_task = True

        if not allow_timesheet_in_done_task and self.project_id and self.env.user.company_id.done_project_stage_id and not self.project_id.is_task_editable_in_done_stage and self.env.user.company_id.done_project_stage_id.id == self.task_id.stage_id.id :
            raise ValidationError("You can not Transfer Timesheet in Done Task.")
        context = dict(self.env.context or {})
        analytic_id = self.env['account.analytic.line'].browse(
            int(context.get('analytic_id')))
        if analytic_id.task_id.id == self.task_id.id:
            analytic_id.write({
                'name': self.name,
                'ticket_id':self.ticket_id.id if self.ticket_id else False 
            })
        else:
            vals = {
                'name': self.name,
                'unit_amount': self.duration,
                'unit_amount_invoice': self.duration,
                'amount': self.duration,
                'project_id': self.project_id.id,
                'date': analytic_id.date,
                # 'account_id': analytic_id.account_id.id,
                'start_date': analytic_id.start_date,
                'end_date': analytic_id.end_date,
                'task_id': self.task_id.id,
                'employee_id': analytic_id.employee_id.id,
                'ticket_id':self.ticket_id.id if self.ticket_id else False ,
                'account_id':self.project_id.analytic_account_id.id,
            }
            self.env['account.analytic.line'].sudo().create(vals)
            analytic_id.task_id.sudo().write({
                'timesheet_ids': [(2, analytic_id.id)]
            })
        self.sudo()._cr.commit()
        return {'type': 'ir.actions.client', 'tag': 'reload'}
