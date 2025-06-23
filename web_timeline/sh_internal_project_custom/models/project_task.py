# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models

class ProjectTask(models.Model):
    _inherit = 'project.task'

    sh_move_task_to_preapp_store = fields.Boolean('Create Task To PreApp Store')
    note = fields.Html('Note')
    
    sh_created_from_project_id = fields.Many2one('project.project', string='Created From Project')
    sh_created_from_project_stage_id = fields.Many2one('project.project.stage', string='Created From Project Stage',
                                                       related="sh_created_from_project_id.stage_id")
    
    sh_created_from_task_id = fields.Many2one('project.task', string='Created From Task')
    sh_created_from_task_stage_id = fields.Many2one('project.task.type', string='Created From Task Stage',
                                                    related="sh_created_from_task_id.stage_id")
    
    sh_created_from_sale_order_id = fields.Many2one('sale.order', string='Created From Sale Order')
    sh_created_from_sale_order_state = fields.Selection([
                                ('draft','Quotation'),('sent','Quotation Sent'),
                                ('sale','Sale Order'),('done','Locked'),('cancel','Cancelled'),
                                ], string='Created From Sale Order State',related="sh_created_from_sale_order_id.state")

    sh_created_from_ticket_id = fields.Many2one('sh.helpdesk.ticket', string='Created From Ticket')
    sh_created_from_ticket_stage_id = fields.Many2one('sh.helpdesk.stages', string='Created From Ticket Stage',
                                                      related="sh_created_from_ticket_id.stage_id")
