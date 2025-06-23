# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models
from datetime import datetime, timedelta

class ProjectProject(models.Model):
    _inherit = 'project.project'

    sh_move_task_to_preapp_store = fields.Boolean('Create Task To PreApp Store',tracking=True)

    def action_open_move_timesheet_wizard(self):
        view = self.env.ref('sh_internal_project_custom.sh_move_timesheet_wizard_form_view')
        return {
            'name': 'Move Timesheet To App Store',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.move.timesheet.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': { 
                'default_project_id' : self.id,
                'default_appstore_project_id' : self.company_id.appstore_project_id.id or False 
            }
        }
    
    def _cron_create_task_in_preapp_store(self):
        
        today = datetime.now()
        before_date = today - timedelta(days=1)
        
        project_ids = self.env['project.project'].sudo().search([('sh_move_task_to_preapp_store','=',True),('write_date','>',before_date),('project_type_selection','=','external')])
        task_ids = self.env['project.task'].sudo().search([('sh_move_task_to_preapp_store','=',True),('write_date','>',before_date),('project_id.project_type_selection','=','external')])
        sale_order_ids = self.env['sale.order'].sudo().search([('sh_move_task_to_preapp_store','=',True),('write_date','>',before_date),])
        ticket_ids = self.env['sh.helpdesk.ticket'].sudo().search([('sh_move_task_to_preapp_store','=',True),('write_date','>',before_date),])
        
        company_ids = self.env['res.company'].sudo().search([])
        if company_ids:
            for comapny in company_ids:
                if comapny.preappstore_project_id and comapny.sh_under_review_task_stage_id:
                    print(f"\n\n\n>>> PREAppStore Project ID ={comapny.preappstore_project_id} \n UNDER REVIEW TASK STAGE ID = {comapny.sh_under_review_task_stage_id}")
                    
                    if project_ids:
                        for project_id in project_ids:
                            existing_task_with_project_id =  self.env['project.task'].sudo().search([('sh_created_from_project_id','=',project_id.id)])
                            if not existing_task_with_project_id:
                                vals = {
                                    'company_id' : comapny.id,
                                    'name' : project_id.name,
                                    'project_id' : comapny.preappstore_project_id.id,
                                    'sh_created_from_project_id' : project_id.id,
                                    'sh_created_from_project_stage_id' : project_id.stage_id.id,
                                    'stage_id' : comapny.sh_under_review_task_stage_id.id,
                                }
                                self.env['project.task'].sudo().create(vals)
                    
                    if task_ids:
                        for task_id in task_ids:
                            existing_task_with_task_id =  self.env['project.task'].sudo().search([('sh_created_from_task_id','=',task_id.id)])
                            if not existing_task_with_task_id:
                                vals = {
                                    'company_id' : comapny.id,
                                    'name' : task_id.name,
                                    'project_id' : comapny.preappstore_project_id.id,
                                    'sh_created_from_task_id' : task_id.id,
                                    'sh_created_from_task_stage_id' : task_id.stage_id.id,
                                    'stage_id' : comapny.sh_under_review_task_stage_id.id,
                                }
                                self.env['project.task'].sudo().create(vals)
                    
                    if sale_order_ids:
                        for sale_order_id in sale_order_ids:
                            existing_task_with_sale_order_id =  self.env['project.task'].sudo().search([('sh_created_from_sale_order_id','=',sale_order_id.id)])
                            if not existing_task_with_sale_order_id:
                                vals = {
                                    'company_id' : comapny.id,
                                    'name' : sale_order_id.name,
                                    'project_id' : comapny.preappstore_project_id.id,
                                    'sh_created_from_sale_order_id' : sale_order_id.id,
                                    'sh_created_from_sale_order_state' : sale_order_id.state,
                                    'stage_id' : comapny.sh_under_review_task_stage_id.id,
                                }
                                self.env['project.task'].sudo().create(vals)
                    
                    if ticket_ids:
                        for ticket_id in ticket_ids:
                            existing_task_with_ticket_id =  self.env['project.task'].sudo().search([('sh_created_from_ticket_id','=',ticket_id.id)])
                            if not existing_task_with_ticket_id:
                                vals = {
                                    'company_id' : comapny.id,
                                    'name' : ticket_id.name,
                                    'project_id' : comapny.preappstore_project_id.id,
                                    'sh_created_from_ticket_id' : ticket_id.id,
                                    'sh_created_from_ticket_stage_id' : ticket_id.stage_id.id,
                                    'stage_id' : comapny.sh_under_review_task_stage_id.id,
                                }
                                self.env['project.task'].sudo().create(vals)