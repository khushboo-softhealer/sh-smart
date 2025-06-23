# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.


from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import UserError

class Sale(models.Model):
    _inherit = 'sale.order'

    sh_replied_status = fields.Selection([('staff_replied','Staff Replied'),('customer_replied','Customer Replied'),('running','Running'),('closed','Closed')],string="Replied Status")
    sh_replied_status_id = fields.Many2one('sh.replied.status',string='Replied Status ', index=True, group_expand='_read_group_replied_stage_ids',tracking=True)
    responsible_user_names = fields.Char(compute='onchange_sale_responsible_ids')

    # def write(self,vals):
    #     for rec in self:
    #         notif_users = []
    #         base_url = self.env['ir.config_parameter'].sudo(
    #         ).get_param('web.base.url')
    #         if rec.user_id:
    #             if rec.user_id.id not in notif_users and self.env.user.sh_sale_customer_reply_notif:
    #                 notif_users.append(rec.user_id.id)
    #         if rec.responsible_user_id:
    #             if rec.responsible_user_id.id not in notif_users and self.env.user.sh_sale_customer_reply_notif:
    #                 notif_users.append(rec.responsible_user_id.id)
    #         if vals.get('sh_replied_status_id') and vals.get('sh_replied_status_id') == self.env.ref('sh_sale_lead_replied_status.sh_customer_replied_stage').id:
    #             self.env['sh.push.notification'].push_notification(list(set(notif_users)), 'Customer Replied', 'Order Ref %s:' % (
    #                     rec.name), base_url+"/mail/view?model=sale.order&res_id="+str(rec.id), 'sale.order', rec.id,'sale')
    #     return super(Sale, self).write(vals)

    @api.depends('sh_responsible_user_ids')
    def onchange_sale_responsible_ids(self):
        for rec in self:
            rec.responsible_user_names = False
            names = ''
            count = 0
            for user in rec.sh_responsible_user_ids:
                if count == 0:
                    names = user.name
                    count = 1
                else:
                    names += ',' + user.name

            rec.responsible_user_names = names

    @api.model
    def _read_group_replied_stage_ids(self, stages, domain, order):
        all_stages = self.env['sh.replied.status'].sudo().search([])
        search_domain = [('id', 'in', all_stages.ids)]

        # perform search
        stage_ids = stages._search(
            search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model_create_multi
    def create(self, vals_list):
        
        results = super(MailMessage,self).create(vals_list)

        for result in results:
            # MOVE Order TO CUSTOMER REPLIES
            if result.message_type and result.subtype_id and result.message_type == 'email' and result.subtype_id.id == self.env.ref('mail.mt_comment').id and result.res_id:
                if result.model == 'sale.order':
                    order = self.env['sale.order'].sudo().browse(result.res_id)
                    if order:
                        body_message = "Order signed by " + order.partner_id.name
                        if body_message not in result.body:
                            order.sudo().sh_replied_status_id = self.env.ref('sh_sale_lead_replied_status.sh_customer_replied_stage').id
                            order.sudo().sh_replied_status = 'customer_replied'
                            notif_users = []
                            if order.responsible_user_id and order.responsible_user_id not in notif_users: 
                                notif_users.append(order.responsible_user_id)
                            if order.user_id and order.user_id not in notif_users:
                                notif_users.append(order.user_id)
                            sale_manager_group_id = self.env.ref('sales_team.group_sale_manager')
                            if sale_manager_group_id:
                                sale_manager_ids = self.env['res.users'].search([('groups_id','in',[sale_manager_group_id.id])])
                                if sale_manager_ids:
                                    for sale_manager in sale_manager_ids:
                                        if sale_manager not in notif_users:
                                            notif_users.append(sale_manager)
                            if notif_users:
                                base_url = self.env['ir.config_parameter'].get_param('web.base.url')
                                self.env['user.push.notification'].push_notification(list(set(notif_users)), 'Customer Replied', 'Order Ref %s:' % (
                                order.name), base_url+"/mail/view?model=sale.order&res_id="+str(order.id), 'sale.order', order.id,'sale')
                if result.model == 'crm.lead':
                    lead = self.env['crm.lead'].sudo().browse(result.res_id)
                    if lead:
                        lead.sudo().sh_replied_status_id = self.env.ref('sh_sale_lead_replied_status.sh_customer_replied_stage').id
                        lead.sudo().sh_replied_status = 'customer_replied'
                        if lead.company_id and lead.company_id.sh_crm_customer_replied:
                            lead.sudo().stage_id = lead.company_id.sh_crm_customer_replied_stage_id.id
                        notif_users = []
                        sale_manager_group_id = self.env.ref('sales_team.group_sale_manager')
                        if sale_manager_group_id:
                            sale_manager_ids = self.env['res.users'].search([('groups_id','in',[sale_manager_group_id.id])])
                            if sale_manager_ids:
                                for sale_manager in sale_manager_ids:
                                    if sale_manager not in notif_users:
                                        notif_users.append(sale_manager)
                        if notif_users:
                            base_url = self.env['ir.config_parameter'].get_param('web.base.url')
                            self.env['user.push.notification'].push_notification(list(set(notif_users)), 'Customer Replied', 'Lead/Opportunity Ref %s:' % (
                            lead.name), base_url+"/mail/view?model=crm.lead&res_id="+str(lead.id), 'crm.lead', lead.id,'sale') 
                if result.model == 'account.move':
                    move = self.env['account.move'].sudo().browse(result.res_id)
                    if move:
                        move.sudo().sh_replied_status_id = self.env.ref('sh_sale_lead_replied_status.sh_customer_replied_stage').id
                        move.sudo().sh_replied_status = 'customer_replied'
                        notif_users = []
                        sale_manager_group_id = self.env.ref('sales_team.group_sale_manager')
                        if sale_manager_group_id:
                            sale_manager_ids = self.env['res.users'].search([('groups_id','in',[sale_manager_group_id.id])])
                            if sale_manager_ids:
                                for sale_manager in sale_manager_ids:
                                    if sale_manager not in notif_users:
                                        notif_users.append(sale_manager)
                        if move.invoice_user_id:
                            notif_users.append(move.invoice_user_id)
                        if move.responsible_user_id:
                            notif_users.append(move.responsible_user_id)
                        if move.responsible_user_ids:
                            for r_user in move.responsible_user_ids:
                                notif_users.append(r_user)
                        if notif_users:
                            base_url = self.env['ir.config_parameter'].get_param('web.base.url')
                            self.env['user.push.notification'].push_notification(list(set(notif_users)), 'Customer Replied', 'Invoice/Move Ref %s:' % (
                            move.name), base_url+"/mail/view?model=account.move&res_id="+str(move.id), 'account.move', move.id,'sale')       
            if result.message_type and result.subtype_id and result.message_type == 'comment' and result.subtype_id.id == self.env.ref('mail.mt_comment').id and result.res_id:
                if result.model == 'sale.order':
                    order = self.env['sale.order'].sudo().browse(result.res_id)
                    if order:
                        if result.author_id.id == order.partner_id.id:
                            body_message = "Order signed by " + order.partner_id.name
                            if body_message not in result.body:
                                order.sudo().sh_replied_status_id = self.env.ref('sh_sale_lead_replied_status.sh_customer_replied_stage').id
                                order.sudo().sh_replied_status = 'customer_replied'
                                notif_users = []
                                if order.responsible_user_id and order.responsible_user_id not in notif_users: 
                                    notif_users.append(order.responsible_user_id)
                                if order.user_id and order.user_id not in notif_users:
                                    notif_users.append(order.user_id)
                                sale_manager_group_id = self.env.ref('sales_team.group_sale_manager')
                                if sale_manager_group_id:
                                    sale_manager_ids = self.env['res.users'].search([('groups_id','in',[sale_manager_group_id.id])])
                                    if sale_manager_ids:
                                        for sale_manager in sale_manager_ids:
                                            if sale_manager not in notif_users:
                                                notif_users.append(sale_manager)
                                if notif_users:
                                    base_url = self.env['ir.config_parameter'].get_param('web.base.url')
                                    self.env['user.push.notification'].push_notification(list(set(notif_users)), 'Customer Replied', 'Order Ref %s:' % (
                                    order.name), base_url+"/mail/view?model=sale.order&res_id="+str(order.id), 'sale.order', order.id,'sale')
                        else:
                            order.sudo().sh_replied_status_id = self.env.ref('sh_sale_lead_replied_status.sh_staff_replied_stage').id
                            order.sudo().sh_replied_status = 'staff_replied'
                if result.model == 'crm.lead':
                    lead = self.env['crm.lead'].sudo().browse(result.res_id)
                    if lead:
                        lead.sudo().sh_replied_status_id = self.env.ref('sh_sale_lead_replied_status.sh_staff_replied_stage').id
                        lead.sudo().sh_replied_status = 'staff_replied'
                        if lead.company_id and lead.company_id.sh_crm_staff_replied:
                            lead.stage_id = lead.company_id.sh_crm_staff_replied_stage_id.id
                if result.model == 'account.move':
                    move = self.env['account.move'].sudo().browse(result.res_id)
                    if move:
                        move.sudo().sh_replied_status_id = self.env.ref('sh_sale_lead_replied_status.sh_staff_replied_stage').id
                        move.sudo().sh_replied_status = 'staff_replied'
        
        return results


    # def _compute_replied_status(self):
    #     for rec in self:
    #         status = 'staff_replied'
    #         message_id = self.env['mail.message'].sudo().search([('subtype_id','!=',self.env.ref('mail.mt_note').id),('res_id','=',rec.id),('model','=','sale.order')],limit=1)
    #         if message_id:
    #             if message_id.author_id:
    #                 user_id = self.env['res.users'].sudo().search([('partner_id','=',message_id.author_id.id)],limit=1)
    #                 if user_id and user_id.has_group('base.group_portal'):
    #                     status = 'customer_replied'
    #                 elif user_id and not user_id.has_group('base.group_portal'):
    #                     status = 'staff_replied'
    #                 elif not user_id:
    #                     status = 'customer_replied'
    #         rec.sh_replied_status = status

    # @api.model
    # def _search_replied_status(self, operator, operand):
    #     staff_replied_orders = []
    #     customer_replied_orders = []
    #     for rec in self.search([]):
    #         if rec.sh_replied_status == 'staff_replied':
    #             staff_replied_orders.append(rec.id)
    #         elif rec.sh_replied_status == 'customer_replied':
    #             customer_replied_orders.append(rec.id)
        
    #     if operator == '=' and operand == 'staff_replied':
    #         return [('id', 'in', staff_replied_orders)]
    #     elif operator == '=' and operand == 'customer_replied':
    #         return [('id', 'in', customer_replied_orders)]
    #     else:
    #         return []

