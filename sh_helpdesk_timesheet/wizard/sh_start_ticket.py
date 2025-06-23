# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api
from odoo.exceptions import UserError

class StartTicket(models.TransientModel):
    _name = 'sh.start.ticket'
    _description = 'STart Ticket'

    project_id = fields.Many2one(
        'project.project', string='Project', required=True)
    task_id = fields.Many2one('project.task', string='Task', required=True)
    ticket_id = fields.Many2one('sh.helpdesk.ticket',string="Ticket No.")

    @api.model
    def default_get(self, fields_list):
        res = super(StartTicket, self).default_get(fields_list)
        if self.env.user.company_id.project_id:
            res.update({
                'project_id': self.env.user.company_id.project_id.id,
            })
        if self.env.context.get('active_model') == 'sh.helpdesk.ticket' and self.env.context.get('active_id'):
            ticket_id = self.env['sh.helpdesk.ticket'].sudo().browse(
                self.env.context.get('active_id'))
            if ticket_id:
                product_id = False
                version_id = False
                if ticket_id.product_ids:
                    product_id = ticket_id.product_ids[0]
                if ticket_id.sh_version_id:
                    version_id = ticket_id.sh_version_id
                if product_id and version_id:
                    sub_task_id = self.env['project.task'].search([
                        ('version_ids', 'in', [version_id.id]),
                        ('sh_product_id', '=', product_id.id),
                        ('parent_id', '!=', False)
                    ], limit=1)
                    if sub_task_id:
                        res.update({
                            'task_id': sub_task_id.id
                        })
                    else:
                        main_task_id = self.env['project.task'].search([
                            ('version_ids', 'in', [version_id.id]),
                            ('product_template_id', '=',
                             product_id.product_tmpl_id.id),
                            ('parent_id', '=', False)
                        ], limit=1)
                        if main_task_id:
                            res.update({
                                'task_id': main_task_id.id
                            })
                else:
                    last_timesheet_id = self.env['account.analytic.line'].sudo().search([('ticket_id','=',ticket_id.id)],limit=1)
                    if last_timesheet_id:
                        res.update({
                            'task_id':last_timesheet_id.task_id.id
                        })
        
        #my code
        ticket_id = self.env['sh.helpdesk.ticket'].sudo().browse(self.env.context.get('active_id'))
        if ticket_id.task_count > 0:

            res.update({
                'project_id': ticket_id.task_ids[0].project_id.id,
                'task_id': ticket_id.task_ids[0].id,
            })

        res.update({
                'ticket_id': self.env.context.get('ticket_id') or False,
            })
        return res

    def action_start_ticket(self):
        self.ensure_one()
        if self.env.context.get('active_id'):
            ticket_id = self.env['sh.helpdesk.ticket'].sudo().browse(
                self.env.context.get('active_id'))

            if ticket_id.stage_id.id in [self.env.company.sh_in_progress_stage_id.id,self.env.company.sh_customer_replied_stage_id.id]:
                ticket_id.sh_ticket_task_id = self.task_id.id
                res = self.task_id.with_context(by_pass_done_validation=True).action_task_start()
                return res
            
            res = self.task_id.action_task_start()
            
        # return res
