# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models,api,_
import math   
from datetime import date,datetime, timedelta
import calendar

class AccountMove(models.Model):
    _inherit = 'account.move'

    sh_invoice_task_count = fields.Integer('Tasks',compute='_compute_sh_invoice_task_count')
    sh_invoice_task_ids = fields.Many2many('project.task','invoice_task_rel', 'invoice_id', 'task_id',string='Invoiced Tasks')

    def _compute_sh_invoice_task_count(self):
        for rec in self:

            rec.sh_invoice_task_count = 0
            sale_orders = self.env['sale.order'].search([('invoice_ids.id','in',rec.ids)])

            if sale_orders:
                tasks = self.env['project.task'].sudo().search(['|','|',('id','=',sale_orders[0].sh_task_id.id),('sh_ticket_ids','in',sale_orders[0].sh_sale_ticket_ids.ids),('account_move_id.line_ids.sale_line_ids.order_id','=',sale_orders[0].name)])
                if tasks:
                    rec.sh_invoice_task_count = len(tasks.ids)
                    rec.sh_invoice_task_ids = [(6,0,tasks.ids)]
 
# as this flow now works on sale confirm in project_mgmt
class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.model_create_multi
    def create(self,vals_list):
        res = super(AccountPayment,self).create(vals_list)
        domain = [('name', '=', res['ref'])]
        find_invoice = self.env['account.move'].search(domain,limit=1)
        if not find_invoice:
            # for online payment
            if res.payment_transaction_id and res.payment_transaction_id.invoice_ids:
                find_invoice = res.payment_transaction_id.invoice_ids[0]
                
        users = self.env['res.users'].search([])
        account_manager_listt = []

        if res.payment_transaction_id:
            for user in users:
                if user.has_group('account.group_account_manager'):
                    account_manager_listt.append(user)
        else:
            for user in users:
                if user.has_group('account.group_account_manager') and user.id!=self.env.user.id:
                    account_manager_listt.append(user)

        if find_invoice:

            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            self.env['user.push.notification'].push_notification(account_manager_listt,'New Payment Created for','Invoice Reference: '+find_invoice.name,base_url+"/mail/view?model=account.move&res_id="+str(find_invoice.id),
                                                        'account.move',find_invoice.id,'sale')
        else:
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            self.env['user.push.notification'].push_notification(account_manager_listt,'New Payment Created','',base_url+"/mail/view?model=account.payment&res_id="+str(res.id),
                                                        'account.payment',res.id,'sale')

        return res
        # if find_invoice:
        #     sale_orders = self.env['sale.order'].search([('invoice_ids.id','=',find_invoice.id)],limit=1)
        #     if sale_orders and sale_orders[0].responsible_user_id:

        #         if self.env.user.company_id.project_id_created_from_so:

        #             description = ''

        #             for i in find_invoice.invoice_line_ids:
        #                 if i.product_id.sh_technical_name and  i.product_id.name  and i.name:

        #                     description = description +  "<b>" + i.product_id.name + "</b>" + "  " + "(" + i.product_id.sh_technical_name + ")" + "<br/>" + i.name + "<br/>" + "<br/>"

        #                 elif i.product_id.name and i.name:

        #                     description = description + "<b>" + i.product_id.name + "</b>" + "<br/>" +i.name + "<br/>" + "<br/>"

        #             ticket_names = ''
        #             for ticket in find_invoice.sh_ticket_ids:
        #                 ticket_names = ticket_names + ticket.name + ' '
                    
        #             total_days_to_finish = math.ceil(sale_orders[0].estimated_hrs/8.5)
        #             deliver_date = date.today() + timedelta(total_days_to_finish)
        #             sdate = date.today()

        #             count = 0

        #             date_list = [sdate+timedelta(days=x) for x in range((deliver_date-sdate).days + 1)]
        #             for each_date in date_list:
        #                 if each_date.isoweekday() == 6 or each_date.isoweekday() == 7:
        #                     count = count + 1
                    
        #             if sdate.isoweekday() == 6 or sdate.isoweekday() == 7:
        #                 count = count - 1

        #             deliver_date = deliver_date + timedelta(count)

        #             task = self.env['project.task'].sudo().search(['|','|',('id','=',sale_orders[0].sh_task_id.id),('sh_ticket_ids','in',sale_orders[0].sh_sale_ticket_ids.ids),('account_move_id.line_ids.sale_line_ids.order_id','=',sale_orders[0].id)], limit=1)

        #             if task:
        #                 resp_user_ids = sale_orders[0].sh_responsible_user_ids.ids
                        
        #                 if task.user_ids:
        #                     resp_user_ids += task.user_ids.ids
        #                 # if task.responsible_ids:
                            
        #                 #     resp_user_ids.extend(task.responsible_ids.ids)

        #                 # task = task[0]

        #                 task_vals = { 
                            
        #                 'name' : sale_orders[0].partner_id.name + ' ' + sale_orders[0].name + ' ' + ticket_names,
        #                     'date_deadline' : deliver_date,
        #                     'user_ids' : [(6, 0, resp_user_ids)],
        #                     "description" : description or '' + task.description or '',
        #                     'odoo_edition':sale_orders[0].odoo_edition,
        #                     'estimated_hrs' : sale_orders[0].estimated_hrs,
        #                     'account_move_id':find_invoice.id,
        #                     'stage_id':self.env.user.company_id.developement_project_stage_id.id
                            
        #                 }
        #                 if sale_orders[0].odoo_version:
        #                     task_vals.update({'version_ids':[(6,0,[sale_orders[0].odoo_version.id])]})

        #                 task.write(task_vals)

        #                 base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        #                 task_notification_ids = [sale_orders[0].responsible_user_id]
        #                 # task_notification_ids.append(sale_orders[0].responsible_user_id)

        #                 if sale_orders[0].responsible_user_id:
        #                     self.env['user.push.notification'].push_notification(task_notification_ids,
        #                                                     'Task Confirmed','Task Confirmed By client !',
        #                                                                     base_url+"/mail/view?model=project.task&res_id="+str(task.id),
        #                                                                     'project.task',task.id,'project')

        #                 # if sale_orders[0].responsible_user_id and sale_orders[0].responsible_user_id.id not in task_notification_ids.ids:
        #                 #     self.env['user.push.notification'].push_notification(task_notification_ids,
        #                 #                                 'Task Confirmed','Task Confirmed By client !',
        #                 #                                                 base_url+"/mail/view?model=project.task&res_id="+str(task.id),
        #                 #                                                 'project.task',task.id,'project')

        #                 message_vals = {
        #                     'message_type' : 'comment',
        #                     'model' : 'project.task',
        #                     'res_id' : task.id,
        #                     'author_id' : self.env.user.partner_id.id,
        #                     'body' : description
        #                 }
        #                 self.env['mail.message'].sudo().create(message_vals)
                        
        #             else:
        #                 resp_user_ids = sale_orders[0].sh_responsible_user_ids.ids
                        
                        
        #                 resp_user_ids += sale_orders[0].responsible_user_id.ids

        #                 task_vals = { 
                            
        #                     'name' : sale_orders[0].partner_id.name + '  ' + sale_orders[0].name + ' ' + ticket_names,
        #                     'project_id' : self.env.user.company_id.project_id_created_from_so.id,                        
        #                     "user_ids": [(6, 0, resp_user_ids)],
        #                     "description" : description,
        #                     'date_deadline' : deliver_date,
        #                     'account_move_id':find_invoice.id,
        #                     'estimated_hrs' : sale_orders[0].estimated_hrs,
        #                     'odoo_edition':sale_orders[0].odoo_edition
                            
        #                 }

        #                 if sale_orders[0].odoo_version:
        #                     task_vals.update({'version_ids':[(6,0,[sale_orders[0].odoo_version.id])]})

        #                 # if sale_orders[0].odoo_version:
        #                 #     task_vals.update({'version_ids':[(6,0,[sale_orders[0].odoo_version.id])]})

        #                 task = self.env['project.task'].create(task_vals)
        #                 base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        #                 task_notification_ids = [sale_orders[0].responsible_user_id]

        #                 self.env['user.push.notification'].push_notification(task_notification_ids,'New Task Created','New Task Confirmed !',
        #                                                             base_url+"/mail/view?model=project.task&res_id="+str(task.id),
        #                                                             'project.task',task.id,'project')


                        
        #             find_invoice.write({'project_task_id': [(4, task.id)]})

                    
            
        #         else:

        #             users = self.env['res.users'].search([])
        #             sale_manager_list = []
        #             for user in users:
        #                 if user.has_group('sales_team.group_sale_manager'):
        #                     sale_manager_list.append(user)

        #             base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        #             self.env['user.push.notification'].push_notification(sale_manager_list,'Task not Created on Payment Done','Related project not found ! You must have to set project in sale configuration !',
        #                                                             base_url+"/mail/view?model=sale.order&res_id="+str(sale_orders[0].id),
        #                                                             'sale.order',sale_orders[0].id,'sale')
        
        return res
