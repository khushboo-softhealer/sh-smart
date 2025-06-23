# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
import requests
import json
from datetime import datetime

class InheritImportHelpdeskTicket(models.Model):
    _inherit = "sh.import.base"
    
    import_ticket=fields.Boolean("Import Ticket")
    records_per_page_ticket = fields.Integer("No of Ticket per page")
    current_import_page_ticket = fields.Integer("Current Page(Ticket)",default=0) 
    sh_import_filter_ticket=fields.Boolean("Import Filtered Tickets")  
    sh_from_date_ticket=fields.Datetime("From Date(Ticket)")
    sh_to_date_ticket=fields.Datetime("To Date(Ticket)") 
    sh_import_ticket_ids=fields.Char("Helpdesk Ticket ids")
    def import_ticket_filtered_to_queue(self):
        ''' ========== Import Filtered Ticket 
        between from date and end date ==================  ''' 
        confid = self.env['sh.import.base'].search([],limit=1)  
        if confid.sh_import_filter_ticket:
            response = requests.get('''%s/api/public/helpdesk.ticket?query={id,write_date}&filter=[["write_date",">=","%s"],["write_date","<=","%s"]]'''
            # response = requests.get('''%s/api/public/helpdesk.ticket?query={id,write_date}&filter=[["active","=",false]]''' %(confid.base_url))
                %(confid.base_url,str(confid.sh_from_date_ticket),str(confid.sh_to_date_ticket)))

            # print("\n\n\=========response",response)
            # print("\n\n\=========response",response)
            
            response_json = response.json()
            if response_json.get('result'):
                confid.sh_import_ticket_ids=[r['id'] for r in response_json.get('result')]
            else:
                confid.sh_import_ticket_ids=False

    def import_ticket_from_queue(self):       
        ''' ========== Import Helpdesk Ticket ==================  '''
        confid = self.env['sh.import.base'].search([],limit=1)
        if confid.sh_import_filter_ticket and confid.sh_import_ticket_ids:   
            tickets = confid.sh_import_ticket_ids.strip('][').split(', ')
            count=0
            failed=0  
            for ticket in tickets[0:50]:
                response = requests.get('''%s/api/public/helpdesk.ticket/%s?query={*,message_follower_ids{*},-sh_ticket_report_url,sh_edition_id{id,name},sh_db_log_ids{*},partner_category_id{id,name},message_ids{id,subtype_id{*},author_id,body,channel_ids{*},date,display_name,email_from,has_error,layout,mail_activity_type_id{*},
                message_id,message_type,model,moderation_status,moderator_id,need_moderation,needaction,no_auto_thread,notification_ids,rating_value,record_name,reply_to,res_id,starred,subject},sh_odoo_end_ticket_id{*},sh_odoo_hosted_id{*,sh_edtion_id{*}},sh_version_id{*},source_id{*},sh_sla_status_ids{*},timehseet_ids{*}
                }''' %(confid.base_url,int(ticket)))
                response_json = response.json()
                if response.status_code==200:
                    for data in response_json['result']:
                    
                        # ======= PREAPRE VALUE FOR CREATE OR UPDATE HELPDESK TICKET =========
                        ticket_vals = confid.process_helpdesk_ticket_data(data)
                        domain = [('remote_sh_helpdesk_ticket_id', '=', data['id'])]
                        find_ticket = self.env['sh.helpdesk.ticket'].search(domain)
                        # try:
                        # followers_list=[]
                        # if 'message_follower_ids' in ticket_vals:
                        #     followers_list = ticket_vals['message_follower_ids']
                        #     del ticket_vals['message_follower_ids']
                        # ======== CHECK IF HELPDESK TICKET IS CREATED OR NOT IF CREATE THEN UPDATE ELSE CREATE =======
                        
                        if find_ticket:
                            count += 1
                            find_ticket.write(ticket_vals) 


                            if data.get('message_follower_ids'):
                                # follower_ids=[]
                                for follower in data.get('message_follower_ids'):
                                    if follower.get('partner_id'):
                                        domain = [('remote_res_partner_id', '=', follower.get('partner_id'))]
                                        find_customer = self.env['res.partner'].search(domain)
                                        subtype_list=[]
                                        if follower.get('subtype_ids'):
                                        
                                            for subtype in follower.get('subtype_ids'):
                                                domain = [('remote_mail_message_subtype_id', '=', subtype)]
                                                find_subtype = self.env['mail.message.subtype'].search(domain)
                                                subtype_list.append(find_subtype.id)
                                        if find_customer:
                                            part_list=[partner
                                                for partner in find_customer.ids
                                                if partner not in find_ticket.sudo().message_partner_ids.ids]
                                            find_ticket.sudo().message_subscribe(partner_ids=part_list)
                                            find_follower=self.env['mail.followers'].search([('partner_id','=',find_customer.id),('res_id','=',find_ticket.id)])
                                            if find_follower:
                                                find_follower.update({
                                                    'subtype_ids':  [(6,0,subtype_list)],
                                                })


                            # if followers_list:
                            #     find_ticket.message_subscribe(partner_ids=[partner
                            #         for partner in followers_list
                            #         if partner not in find_ticket.sudo().message_partner_ids.ids])  
                            if data.get('sh_lead_ids'):
                                for lead in data.get('sh_lead_ids'):
                                    find_lead=self.env['crm.lead'].search([('remote_crm_lead_id','=',lead)])
                                    if find_lead:
                                        find_lead.sh_ticket_ids=[(4,find_ticket.id)]                         
                        else:
                            if 'partner_id' in ticket_vals and ticket_vals['partner_id']:
                                create_ticket=self.env['sh.helpdesk.ticket'].create(ticket_vals)  

                                if data.get('message_follower_ids'):
                                    # follower_ids=[]
                                    for follower in data.get('message_follower_ids'):
                                        if follower.get('partner_id'):
                                            domain = [('remote_res_partner_id', '=', follower.get('partner_id'))]
                                            find_customer = self.env['res.partner'].search(domain)
                                            subtype_list=[]
                                            if follower.get('subtype_ids'):
                                            
                                                for subtype in follower.get('subtype_ids'):
                                                    domain = [('remote_mail_message_subtype_id', '=', subtype)]
                                                    find_subtype = self.env['mail.message.subtype'].search(domain)
                                                    subtype_list.append(find_subtype.id)

                                            if find_customer:
                                                create_ticket.message_subscribe(partner_ids=[partner
                                                    for partner in find_customer.ids
                                                    if partner not in create_ticket.sudo().message_partner_ids.ids])
                                                find_follower=self.env['mail.followers'].search([('partner_id','=',find_customer.id),('res_id','=',find_ticket.id)])
                                                if find_follower:
                                                    find_follower.update({
                                                        'subtype_ids':  [(6,0,subtype_list)],
                                                    })
                                                # follower_ids.append(find_customer.id)
                                    # ticket_vals['message_follower_ids']= follower_ids


                                # if followers_list:
                                #     create_ticket.message_subscribe(partner_ids=[partner
                                #     for partner in followers_list
                                #     if partner not in create_ticket.sudo().message_partner_ids.ids])
                                count += 1
                                if create_ticket and data.get('stage_id'):
                                    domain = [('remote_sh_helpdesk_stages_id', '=', data.get('stage_id'))]
                                    find_stage = self.env['sh.helpdesk.stages'].search(domain)
                                    if find_stage:
                                        create_ticket.write({
                                            'stage_id':find_stage.id,   
                                        })
                                if data.get('sh_lead_ids'):
                                    for lead in data.get('sh_lead_ids'):
                                        find_lead=self.env['crm.lead'].search([('remote_crm_lead_id','=',lead)])
                                        if find_lead:
                                            find_lead.sh_ticket_ids=[(4,create_ticket.id)]  

                            else:
                                vals = {
                                    "name": data['id'],
                                    # "error": e,
                                    "import_json" : data,
                                    "field_type": "helpdesk_ticket",                           
                                    "datetime": datetime.now(),
                                    "base_config_id": confid.id,
                                }
                                self.env['sh.import.failed'].create(vals) 

            confid.sh_import_ticket_ids='['+', '.join([str(elem) for elem in tickets[50:]])+']'                          
            if count > 0:              
                vals = {
                    "name": confid.name,
                    "state": "success",
                    "field_type": "helpdesk_ticket",
                    "error": "%s Helpdesk Ticket Imported Successfully" %(count - failed),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)
            if failed > 0:
                vals = {
                    "name": confid.name,
                    "state": "error",
                    "field_type": "helpdesk_ticket",
                    "error": "%s Failed To Import" %(failed),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)

                # else:
                #     vals = {
                #         "name": confid.name,
                #         "state": "error",
                #         "field_type": "helpdesk_ticket",
                #         "error": response.text,
                #         "datetime": datetime.now(),
                #         "base_config_id": confid.id,
                #         "operation": "import"
                #     }
                #     self.env['sh.import.base.log'].create(vals)
                    
    def import_helpdesk_ticket_cron(self):
        ''' ========== Import Helpdesk Ticket ============ '''
        
        confid = self.env['sh.import.base'].search([],limit=1)
        if confid.import_ticket:
            confid.current_import_page_ticket += 1            
            response = requests.get('''%s/api/public/helpdesk.ticket?query={*,-portal_ticket_url_wp,-sh_ticket_report_url,message_follower_ids{*},sh_edition_id{id,name},sh_db_log_ids{*},partner_category_id{id,name},message_ids{id,subtype_id{*},author_id,body,channel_ids{*},date,display_name,email_from,has_error,layout,mail_activity_type_id{*},
            message_id,message_type,model,moderation_status,moderator_id,need_moderation,needaction,no_auto_thread,notification_ids,rating_value,record_name,reply_to,res_id,starred,subject},sh_odoo_end_ticket_id{*},sh_odoo_hosted_id{*,sh_edtion_id{*}},sh_version_id{*},source_id{*},sh_sla_status_ids{*},timehseet_ids{*}
            }&page_size=%s&page=%s''' %(confid.base_url,confid.records_per_page_ticket,confid.current_import_page_ticket))
            response_json = response.json()
            # response = requests.get('''%s/api/public/helpdesk.ticket?query={id,message_follower_ids{*}}&page_size=%s&page=%s''' %(confid.base_url,confid.records_per_page_ticket,confid.current_import_page_ticket))
            # response_json = response.json()
            if response.status_code==200:
                if response_json.get('count') and confid.records_per_page_ticket != response_json['count']:
                    confid.import_ticket = False
                    confid.current_import_page_ticket = 0
                count = 0
                failed = 0
                
                for data in response_json['result']:
                    # ======= PREAPRE VALUE FOR CREATE OR UPDATE HELPDESK TICKET =========
                    ticket_vals = confid.process_helpdesk_ticket_data(data)
                    domain = [('remote_sh_helpdesk_ticket_id', '=', data['id'])]
                    find_ticket = self.env['sh.helpdesk.ticket'].search(domain)
                    # try:
                    # followers_list=[]
                    # if 'message_follower_ids' in ticket_vals:
                    #     followers_list = ticket_vals['message_follower_ids']
                    #     del ticket_vals['message_follower_ids']
                    # ======== CHECK IF HELPDESK TICKET IS CREATED OR NOT IF CREATE THEN UPDATE ELSE CREATE =======
                    
                    if find_ticket:
                        count += 1
                        find_ticket.write(ticket_vals) 


                        if data.get('message_follower_ids'):
                            # follower_ids=[]
                            for follower in data.get('message_follower_ids'):
                                if follower.get('partner_id'):
                                    domain = [('remote_res_partner_id', '=', follower.get('partner_id'))]
                                    find_customer = self.env['res.partner'].search(domain)
                                    subtype_list=[]
                                    if follower.get('subtype_ids'):
                                    
                                        for subtype in follower.get('subtype_ids'):
                                            domain = [('remote_mail_message_subtype_id', '=', subtype)]
                                            find_subtype = self.env['mail.message.subtype'].search(domain)
                                            subtype_list.append(find_subtype.id)
                                    if find_customer:
                                        find_ticket.message_subscribe(partner_ids=[partner
                                            for partner in find_customer.ids
                                            if partner not in find_ticket.sudo().message_partner_ids.ids], subtype_ids=subtype_list)

                                        find_follower=self.env['mail.followers'].search([('partner_id','=',find_customer.id),('res_id','=',find_ticket.id)])
                                        if find_follower:
                                            find_follower.update({
                                                'subtype_ids':  [(6,0,subtype_list)],
                                            })


                        # if followers_list:
                        #     find_ticket.message_subscribe(partner_ids=[partner
                        #         for partner in followers_list
                        #         if partner not in find_ticket.sudo().message_partner_ids.ids])  
                        if data.get('sh_lead_ids'):
                            for lead in data.get('sh_lead_ids'):
                                find_lead=self.env['crm.lead'].search([('remote_crm_lead_id','=',lead)])
                                if find_lead:
                                    find_lead.sh_ticket_ids=[(4,find_ticket.id)]                         
                    else:
                        if 'partner_id' in ticket_vals and ticket_vals['partner_id']:
                            create_ticket=self.env['sh.helpdesk.ticket'].create(ticket_vals)  

                            if data.get('message_follower_ids'):
                                # follower_ids=[]
                                for follower in data.get('message_follower_ids'):
                                    if follower.get('partner_id'):
                                        domain = [('remote_res_partner_id', '=', follower.get('partner_id'))]
                                        find_customer = self.env['res.partner'].search(domain)
                                        subtype_list=[]
                                        if follower.get('subtype_ids'):
                                        
                                            for subtype in follower.get('subtype_ids'):
                                                domain = [('remote_mail_message_subtype_id', '=', subtype)]
                                                find_subtype = self.env['mail.message.subtype'].search(domain)
                                                subtype_list.append(find_subtype.id)
                                        if find_customer:
                                            create_ticket.message_subscribe(partner_ids=[partner
                                                for partner in find_customer.ids
                                                if partner not in create_ticket.sudo().message_partner_ids.ids], subtype_ids=subtype_list)
                                            
                                            find_follower=self.env['mail.followers'].search([('partner_id','=',find_customer.id),('res_id','=',find_ticket.id)])
                                            if find_follower:
                                                find_follower.update({
                                                    'subtype_ids':  [(6,0,subtype_list)],
                                                })
                                            # follower_ids.append(find_customer.id)
                                # ticket_vals['message_follower_ids']= follower_ids


                            # if followers_list:
                            #     create_ticket.message_subscribe(partner_ids=[partner
                            #     for partner in followers_list
                            #     if partner not in create_ticket.sudo().message_partner_ids.ids])
                            count += 1
                            if create_ticket and data.get('stage_id'):
                                domain = [('remote_sh_helpdesk_stages_id', '=', data.get('stage_id'))]
                                find_stage = self.env['sh.helpdesk.stages'].search(domain)
                                if find_stage:
                                    create_ticket.write({
                                        'stage_id':find_stage.id,   
                                    })
                            if data.get('sh_lead_ids'):
                                for lead in data.get('sh_lead_ids'):
                                    find_lead=self.env['crm.lead'].search([('remote_crm_lead_id','=',lead)])
                                    if find_lead:
                                        find_lead.sh_ticket_ids=[(4,create_ticket.id)]  

                        else:
                            vals = {
                                "name": data['id'],
                                # "error": e,
                                "import_json" : data,
                                "field_type": "helpdesk_ticket",                           
                                "datetime": datetime.now(),
                                "base_config_id": confid.id,
                            }
                            self.env['sh.import.failed'].create(vals) 
                    # except Exception as e:
                    #     failed += 1
                    #     vals = {
                    #         "name": data['id'],
                    #         "error": e,
                    #         "import_json" : data,
                    #         "field_type": "helpdesk_ticket",                           
                    #         "datetime": datetime.now(),
                    #         "base_config_id": confid.id,
                    #     }
                    #     self.env['sh.import.failed'].create(vals) 
                    
                if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "helpdesk_ticket",
                        "error": "%s Helpdesk Ticket Imported Successfully" %(count - failed),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
                if failed > 0:
                    vals = {
                        "name": confid.name,
                        "state": "error",
                        "field_type": "helpdesk_ticket",
                        "error": "%s Failed To Import" %(failed),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)

            else:
                vals = {
                    "name": confid.name,
                    "state": "error",
                    "field_type": "helpdesk_ticket",
                    "error": response.text,
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)
                
                
    def process_helpdesk_ticket_data(self,data):
        ticket_vals={
            'remote_sh_helpdesk_ticket_id':data.get('id'),
            'access_token':data.get('access_token'),
            'access_url':data.get('access_url'),
            'access_warning':data.get('access_warning'),
            'active':True,
            'sh_active':data.get('active'),
            'cancel_button_boolean':data.get('cancel_button_boolean'),
            'cancel_reason':data.get('cancel_reason'),
            'cancel_stage_boolean':data.get('cancel_stage_boolean'),
            'category_bool':data.get('category_bool'),
            'closed_stage_boolean':data.get('closed_stage_boolean'),
            'color':data.get('color'),
            'comment':data.get('comment'),
            'customer_comment':data.get('customer_comment'),
            'description':data.get('description'),
            'display_name':data.get('display_name'),
            'done_button_boolean':data.get('done_button_boolean'),
            'done_stage_boolean':data.get('done_stage_boolean'),
            'email':data.get('email'),
            'email_subject':data.get('email_subject'),
            'form_url':data.get('form_url'),
            'message_has_error':data.get('message_has_error'),
            'message_has_error_counter':data.get('message_has_error_counter'),
            'message_is_follower':data.get('message_is_follower'),
            'message_needaction':data.get('message_needaction'),
            'mobile_no':data.get('mobile_no'),
            'name':data.get('name'),
            'open_boolean':data.get('open_boolean'),
            'person_name':data.get('person_name'),
            # 'portal_ticket_url_wp':data.get('portal_ticket_url_wp'),
            'priority_new':data.get('priority_new').get('sh_api_current_state') ,
            'rating_bool':data.get('rating_bool'),
            'reopen_stage_boolean':data.get('reopen_stage_boolean'),
            'report_token':data.get('report_token'),
            'sh_days_to_late':data.get('sh_days_to_late'),
            'sh_days_to_reach':data.get('sh_days_to_reach'),
            'sh_display_multi_user':data.get('sh_display_multi_user'),
            'sh_display_product':data.get('sh_display_product'),
            'sh_status':data.get('sh_status').get('sh_api_current_state'),
            'sh_status_boolean':data.get('sh_status_boolean'),
            'sh_ticket_report_url':data.get('sh_ticket_report_url'),
            'state':data.get('state').get('sh_api_current_state'),
            'sub_category_bool':data.get('sub_category_bool'),
            'ticket_allocated':data.get('ticket_allocated'),
            'ticket_from_website':data.get('ticket_from_website'),
            'sh_ticket_replied_status':data.get('sh_ticket_replied_status').get('sh_api_current_state'),
            'sh_days_left':data.get('sh_days_left'),
            'new_stage_boolean':data.get('new_stage_boolean'),
            'odoo_store_ticket':data.get('odoo_store_ticket'),
            'store_reference':data.get('store_reference'),
            'sh_total_order_price_unit':data.get('sh_total_order_price_unit'),
            'sh_total_order_qty' : data.get('sh_total_order_qty'),
            'sh_special':data.get('sh_special'),
            'sh_check_downgrade':data.get('sh_check_downgrade'),
            'sh_original_module_send':data.get('sh_original_module_send'),
            'estimation_description':data.get('estimation_description') ,
            'estimation_hours':data.get('estimation_hours') ,
            'sh_invoice_verified':data.get('sh_invoice_verified').get('sh_api_current_state'),
            'sh_latest_update':data.get('sh_latest_update').get('sh_api_current_state') ,
            'sh_custom_module_conflict':data.get('sh_custom_module_conflict').get('sh_api_current_state') ,
            'sh_need_to_setup_environment':data.get('sh_need_to_setup_environment').get('sh_api_current_state') ,
            'sh_deployment_required':data.get('sh_deployment_required').get('sh_api_current_state') ,
            'sh_demo_ticket':data.get('sh_demo_ticket'),
            'sh_demo_content':data.get('sh_demo_content'),
            'followers_added':data.get('followers_added'),
            'company_id':1,
        }
        
        if data.get('sh_sla_deadline'):
            date_time=datetime.strptime(data.get('sh_sla_deadline'),'%Y-%m-%d-%H-%M-%S')
            date_time=date_time.strftime('%Y-%m-%d %H:%M:%S')
            ticket_vals['sh_sla_deadline']=date_time

        if data.get('sh_order_date'):
            date_time=datetime.strptime(data.get('sh_order_date'),'%Y-%m-%d-%H-%M-%S')
            date_time=date_time.strftime('%Y-%m-%d %H:%M:%S')
            ticket_vals['sh_order_date']=date_time

        if data.get('close_date'):
            date_time=datetime.strptime(data.get('close_date'),'%Y-%m-%d-%H-%M-%S')
            ticket_vals['close_date']=date_time

        if data.get('cancel_date'):
            date_time=datetime.strptime(data.get('cancel_date'),'%Y-%m-%d-%H-%M-%S')
            ticket_vals['cancel_date']=date_time
        
        if data.get('replied_date'):
            date_time=datetime.strptime(data.get('replied_date'),'%Y-%m-%d-%H-%M-%S')
            ticket_vals['replied_date']=date_time
        
        if data.get('sh_demo_db_create_date'):
            date_time=datetime.strptime(data.get('sh_demo_db_create_date'),'%Y-%m-%d-%H-%M-%S')
            ticket_vals['sh_demo_db_create_date']=date_time

        if data.get('sh_demo_db_expired_date'):
            date_time=datetime.strptime(data.get('sh_demo_db_expired_date'),'%Y-%m-%d-%H-%M-%S')
            ticket_vals['sh_demo_db_expired_date']=date_time


        if data.get('partner_category_id'):

            domain=['|',('remote_partner_category_id','=',data.get('partner_category_id').get('id')),('name','=',data.get('partner_category_id').get('name'))]    
            find_partner_category=self.env['partner.category'].search(domain,limit=1)
            if find_partner_category:
                ticket_vals['partner_category_id']= find_partner_category.id
        
        if data.get('sh_edition_id') and data.get('sh_edition_id').get('id') and data.get('sh_edition_id').get('id')!=0:
            find_edition=self.env['sh.edition'].search(['|',('remote_sh_edition_id','=',data.get('sh_edition_id').get('id')),('name','=',data.get('sh_edition_id').get('name'))])
            if find_edition:
                ticket_vals['sh_edition_id']= find_edition.id
            else:
                edition_vals={
                    'remote_sh_edition_id': data.get('sh_edtion_id').get('id'),
                    'name':data.get('sh_edtion_id').get('name'),
                }
                find_edition=self.env['sh.edition'].create(edition_vals)
                ticket_vals['sh_edition_id']= find_edition.id

        if data.get('sh_odoo_hosted_id'):
            find_odoo_hosted=self.env['sh.odoo.hosted.on'].search([('remote_sh_odoo_hosted_id','=',data.get('sh_edition_id').get('id')),'|',('active','=',True),('active','=',False)],limit=1)
            if find_odoo_hosted:
                ticket_vals['sh_odoo_hosted_id']= find_odoo_hosted.id   
            else:
                odoo_hosted_vals={
                    'remote_sh_odoo_hosted_id':data.get('sh_odoo_hosted_id').get('id'),
                    'name':data.get('sh_odoo_hosted_id').get('name'),
                    'active':data.get('sh_odoo_hosted_id').get('active'),
                    'sh_display_in_frontend':data.get('sh_odoo_hosted_id').get('sh_display_in_frontend'),
                    'company_id':1,
                }
                if data.get('sh_odoo_hosted_id').get('sh_edtion_id'):
                    find_edition=self.env['sh.edition'].search(['|',('remote_sh_edition_id','=',data.get('sh_odoo_hosted_id').get('sh_edtion_id').get('id')),('name','=',data.get('sh_odoo_hosted_id').get('sh_edtion_id').get('name'))])
                    if find_edition:
                        odoo_hosted_vals['sh_edtion_id']= find_edition.id
                    else:
                        edition_vals={
                            'remote_sh_edition_id': data.get('sh_odoo_hosted_id').get('sh_edtion_id').get('id'),
                            'name':data.get('sh_odoo_hosted_id').get('sh_edtion_id').get('name'),
                        }
                        find_edition=self.env['sh.edition'].create(edition_vals)
                        odoo_hosted_vals['sh_edtion_id']= find_edition.id
                if odoo_hosted_vals:
                    find_odoo_hosted=self.env['sh.odoo.hosted.on'].create(odoo_hosted_vals)
                    if find_odoo_hosted:
                        ticket_vals['sh_odoo_hosted_id']= find_odoo_hosted.id 

        if data.get('sh_version_id'):
            domain=[('remote_sh_version_id','=',data.get('sh_version_id').get('id'))]
            find_version=self.env['sh.version'].search(domain)
            if find_version:
                ticket_vals['sh_version_id']=find_version.id
            else:
                version_vals={
                    'remote_sh_version_id': data.get('sh_version_id').get('id'),
                    'name':data.get('sh_version_id').get('name'),
                }
                find_version=self.env['sh.version'].create(version_vals)
                ticket_vals['sh_version_id']= find_version.id

        

        if data.get('sh_estimation_product_id'):
            domain=[('remote_product_product_id','=',data.get('sh_estimation_product_id'))]
            find_product=self.env['product.product'].sudo().search(domain)
            if find_product:
                ticket_vals['sh_estimation_product_id']= find_product.id

        if data.get('sh_lead_ids'):
            lead_list=[]
            # print("\n\n=========data.get('sh_lead_ids')",data.get('sh_lead_ids'))
            for lead in data.get('sh_lead_ids'):
                domain_lead = [('remote_crm_lead_id', '=',lead)]
                find_lead = self.env['crm.lead'].search(domain_lead)
                if find_lead:
                    lead_list.append(find_lead.id)
            if lead_list:
                ticket_vals['sh_lead_ids']= [(6,0,lead_list)] 

        if data.get('sh_odoo_end_ticket_id') and data.get('sh_odoo_end_ticket_id').get('id') and data.get('sh_odoo_end_ticket_id').get('id')!=0:
            find_odoo_end_ticket = self.env['sh.odoo.end.ticket'].search([('remote_sh_odoo_end_ticket_id','=',data.get('sh_odoo_end_ticket_id').get('id'))])
            if find_odoo_end_ticket:
                ticket_vals['sh_odoo_end_ticket_id']= find_odoo_end_ticket.id

            else:
                odoo_end_ticket_vals={
                    'description':data.get('sh_odoo_end_ticket_id').get('description'),
                    'display_name':data.get('sh_odoo_end_ticket_id').get('display_name'),
                    'email':data.get('sh_odoo_end_ticket_id').get('email'),
                    'email_subject':data.get('sh_odoo_end_ticket_id').get('email_subject'),
                    'has_message':data.get('sh_odoo_end_ticket_id').get('has_message'),
                    'remote_sh_odoo_end_ticket_id':data.get('sh_odoo_end_ticket_id').get('id'),
                    'sh_store_link':data.get('sh_odoo_end_ticket_id').get('sh_store_link'),
                    'sh_tech_name':data.get('sh_odoo_end_ticket_id').get('sh_tech_name'),
                    'sh_ticket_created':data.get('sh_odoo_end_ticket_id').get('sh_ticket_created'),
                    'state':data.get('sh_odoo_end_ticket_id').get('state').get('sh_api_current_state'),
                }
                if data.get('sh_odoo_end_ticket_id').get('sh_user_ids'):
                    user_list=[]
                    for user in data.get('sh_odoo_end_ticket_id').get('sh_user_ids'):
                        domain_by_id = [('remote_res_user_id','=',user)]
                        find_user_id=self.env['res.users'].search(domain_by_id)

                        # ========== SEARCH USER BY ID OR BY NAME IF EXIST THEN RETURN ELSE CREATE USE AND RETURN IT =====
                        if find_user_id:
                            user_list.append((4,find_user_id.id))

                    if user_list:
                        odoo_end_ticket_vals['sh_user_ids']=user_list 

                if data.get('sh_odoo_end_ticket_id').get('sh_responsible_user_id'):
                    domain_by_id = [('remote_res_user_id','=',data.get('sh_odoo_end_ticket_id').get('sh_responsible_user_id'))]
                    find_user_id=self.env['res.users'].search(domain_by_id)

                    # ========== SEARCH USER BY ID OR BY NAME IF EXIST THEN RETURN ELSE CREATE USE AND RETURN IT =====
                    if find_user_id:
                        odoo_end_ticket_vals['sh_responsible_user_id']= find_user_id.id

                if data.get('sh_odoo_end_ticket_id').get('sh_ticket_id'):
                    find_ticket=self.env['sh.helpdesk.ticket'].search([('remote_sh_helpdesk_ticket_id','=',data.get('sh_odoo_end_ticket_id').get('sh_ticket_id'))])   
                    if find_ticket:
                        odoo_end_ticket_vals['sh_ticket_id']= find_ticket.id
                
                if data.get('sh_odoo_end_ticket_id').get('partner_id'):
                    domain = [('remote_res_partner_id', '=', data.get('sh_odoo_end_ticket_id')['partner_id'])]
                    find_customer = self.env['res.partner'].search(domain,limit=1)
                    if find_customer:
                        odoo_end_ticket_vals['partner_id'] = find_customer.id


                if odoo_end_ticket_vals:
                    find_odoo_end_ticket = self.env['sh.odoo.end.ticket'].create(odoo_end_ticket_vals)
                    if find_odoo_end_ticket:
                        ticket_vals['sh_odoo_end_ticket_id']= find_odoo_end_ticket.id


        if data.get('priority'):
            domain = [('remote_helpdesk_priority_id', '=', data.get('priority'))]
            find_priority = self.env['helpdesk.priority'].search(domain)
            if find_priority:
                ticket_vals['priority']=find_priority.id
            # else:
                # helpdesk_priority_vals={
                #     'remote_helpdesk_priority_id' : data.get('priority')['id'],
                #     'display_name':data.get('priority')['display_name'],
                #     'name':data.get('priority')['name'],
                #     'sequence' : data.get('priority')['sequence'],
                #     'color':data.get('priority')['color'],
                # }
                # find_priority=self.env['helpdesk.priority'].create(helpdesk_priority_vals)
                # if find_priority:
                #     ticket_vals['priority']=find_priority.id
                
        if data.get('sh_db_log_ids'):
            db_log_list=[]
            for db_log in data.get('sh_db_log_ids'):
                find_log=self.env['sh.demo.db.log'].search([('remote_sh_demo_db_log_id','=',db_log.get('id'))])   
                if not find_log:
                    log_vals={
                        'remote_sh_demo_db_log_id' : db_log.get('id'),
                        'log_message':db_log.get('log_message'),
                        'sh_database_name' : db_log.get('sh_database_name'),
                        'sh_password':db_log.get('sh_password'),
                        'sh_url' : db_log.get('sh_url'),
                        'sh_username':db_log.get('sh_username'),
                    }    
                    if db_log.get('sh_db_ids'):
                        db_list=[]
                        for db in db_log.get('sh_db_ids'):
                            find_product=self.env['product.template'].search([('remote_product_template_id','=',db)],limit=1)
                            if find_product:
                                db_list.append((4,find_product.id))
                        if db_list:
                            log_vals['sh_db_ids'] = db_list
                    if db_log.get('partner_id'):
                        find_partner=self.env['res.partner'].search([('remote_res_partner_id','=',db_log.get('id'))],limit=1)
                        if find_partner:
                            log_vals['partner_id']=find_partner.id
                    
                    if log_vals:
                        db_log_list.append((0,0,log_vals))

        # ======== Get User if already created or create =========
        if data.get('cancel_by') and data.get('cancel_by')!=0:
            
            domain_by_id = [('remote_res_user_id','=',data['cancel_by'])]
            find_user_id=self.env['res.users'].search(domain_by_id)

            # ========== SEARCH USER BY ID OR BY NAME IF EXIST THEN RETURN ELSE CREATE USE AND RETURN IT =====
            if find_user_id:
                ticket_vals['cancel_by']=find_user_id.id 
    
        # ======== Get User if already created or create =========
        if data.get('close_by') and data.get('close_by')!=0:
            
            domain_by_id = [('remote_res_user_id','=',data['close_by'])]
            find_user_id=self.env['res.users'].search(domain_by_id)

            # ========== SEARCH USER BY ID OR BY NAME IF EXIST THEN RETURN ELSE CREATE USE AND RETURN IT =====
            if find_user_id:
                ticket_vals['close_by']=find_user_id.id 

        
        # ======== GET CATEGORY IF EXIST =============
        
        if data.get('category_id'):
            domain_category=[('remote_sh_helpdesk_category_id','=',data.get('category_id'))] 
            find_category=self.env['sh.helpdesk.category'].search(domain_category)
            if find_category:
                ticket_vals['category_id']=find_category.id
            # else:
            #     helpdesk_category_vals={
            #         'remote_sh_helpdesk_category_id' : data['category_id']['id'],
            #         'display_name':data['category_id']['display_name'],
            #         'name':data['category_id']['name'],
            #         'sequence' : data['category_id']['sequence'],
            #     }
            #     helpdesk_category=self.env['sh.helpdesk.category'].create(helpdesk_category_vals)
            #     ticket_vals['category_id']=helpdesk_category.id
                
        # ============== Prepare Mail_Message Data =================
        
        # if data.get('message_ids'):
        #     message_list = []
        #     message_list_create=[]
        #     remain_mail=[]           
        #     for message in data.get('message_ids'):   
        #         if message['id']:             
        #             domain = [('remote_mail_message_id','=',message['id'])]
        #             find_message = self.env['mail.message'].search(domain,limit=1)                    
        #             if find_message:
        #                 message_list.append((4,find_message.id))
        #             else:
        #                 remain_mail.append(message)
        #     if remain_mail:
        #         message_list_create = self.process_message_data(remain_mail)                                                
                            
        #     ticket_vals['message_ids']=message_list+message_list_create
        
        # ======== Get Message Partner if already created or create =========
        
        # if data.get('message_partner_ids'):
        #     partner_list=[]
        #     for m_partner in data.get('message_partner_ids'):
        #         domain = [('remote_res_partner_id', '=',m_partner)]
        #         find_customer = self.env['res.partner'].search(domain,limit=1)
                
        #         # ======== CHECK IF PARTNER IS CREATED OR NOT IF CREATE THEN RETURN ELSE CREATE =======
        #         if find_customer:
        #             partner_list.append((4,find_customer.id))
        #     ticket_vals['message_partner_ids']=partner_list
            
            
        # ======== Get partner if already created or create =====
            
        if data.get('partner_id'):
            domain = [('remote_res_partner_id', '=', data['partner_id'])]
            find_customer = self.env['res.partner'].search(domain,limit=1)
            if find_customer:
                ticket_vals['partner_id'] = find_customer.id
        
        # ======== prepare products list which are related to helpdesk ticket  =====
        
        if data.get('product_ids'):
            product_ids=[]
            for product in data.get('product_ids'):
                domain=[('remote_product_product_id','=',product)]
                find_product=self.env['product.product'].sudo().search(domain)
                if find_product:
                    product_ids.append(find_product.id)
                    
        
            if product_ids:
                ticket_vals['product_ids']=[(6,0,product_ids)]

        if data.get('partner_ids'):
            partner_ids=[]
            for partner in data.get('partner_ids'):
                domain=[('remote_res_partner_id','=',partner)]
                find_partner=self.env['res.partner'].sudo().search(domain)
                if find_partner:
                    partner_ids.append(find_partner.id)
                    
        
            if partner_ids:
                ticket_vals['partner_ids']=[(6,0,partner_ids)]
                
        # ======== prepare sla product list which are related to helpdesk ticket  =====
        
        if data.get('sh_sla_policy_ids'):        
            sla_policy_ids=[]
            for sla_policy in data.get('sh_sla_policy_ids'): 
                
                domain = [('remote_sh_helpdesk_sla_id', '=', sla_policy['id'])]
                find_sla = self.env['sh.helpdesk.sla'].search(domain)
                if find_sla:
                    sla_policy_ids.append((4,find_sla.id))
                else:
                    helpdesk_sla_vals=self.process_helpdesk_sla_data(sla_policy)      
                    find_sla=self.env['sh.helpdesk.sla'].create(helpdesk_sla_vals)
                    sla_policy_ids.append((4,find_sla.id))
            if sla_policy_ids:
                ticket_vals['sh_sla_policy_ids']=sla_policy_ids        
        
        # ==========  Prepare helpdesk ticket related alarm ========
        
        if data.get('sh_ticket_alarm_ids'):
            alarm_list=[]
            for alarm in data.get('sh_ticket_alarm_ids'):
                if alarm:
                    domain = [('remote_sh_ticket_alarm_id', '=', alarm['id'])]
                    find_alarm = self.env['sh.ticket.alarm'].search(domain)
                    if find_alarm:
                        alarm_list.append((4,find_alarm.id))
                    else:
                        helpdesk_ticket_alarm_vals={
                            'remote_sh_ticket_alarm_id' : alarm['id'],
                            'display_name':alarm['display_name'],
                            'name':alarm['name'],
                            'sh_remind_before':alarm['sh_remind_before'],
                            'sh_reminder_unit':alarm['sh_reminder_unit']['sh_api_current_state'],
                            'type':alarm['type']['sh_api_current_state'],
                        }
                        find_alarm=self.env['sh.ticket.alarm'].create(helpdesk_ticket_alarm_vals)
                        if find_alarm:
                            alarm_list.append((4,find_alarm.id))
                        
            if alarm_list:
               ticket_vals['sh_ticket_alarm_ids']=alarm_list             
                        
        # ======== Get User if already created or create =========
            
        if data.get('sh_user_ids') :
            sh_users=[]
            for f_user in data.get('sh_user_ids'):
                if f_user and f_user!=0:
                    domain_by_id = [('remote_res_user_id','=',f_user)]
                    find_user_id=self.env['res.users'].search(domain_by_id)
                    
                    # ========== SEARCH USER BY ID OR BY NAME IF EXIST THEN RETURN ELSE CREATE USE AND RETURN IT =====
                    
                    if find_user_id:
                        sh_users.append((4,find_user_id.id ))

            if sh_users:
                ticket_vals['sh_user_ids']=sh_users   

        if data.get('sh_estimation_respon_user_ids'):
            estimation_users=[]
            for user in data.get('sh_estimation_respon_user_ids'):
                if user and user!=0:
                    domain_by_id = [('remote_res_user_id','=',user)]
                    find_user_id=self.env['res.users'].search(domain_by_id)
                    
                    # ========== SEARCH USER BY ID OR BY NAME IF EXIST THEN RETURN ELSE CREATE USE AND RETURN IT =====
                    
                    if find_user_id:
                        estimation_users.append((4,find_user_id.id ))

            if estimation_users:
                ticket_vals['sh_user_ids']=estimation_users                
                        
        # ======= get stage if created or create =========
        if data.get('stage_id'):
            domain = [('remote_sh_helpdesk_stages_id', '=', data.get('stage_id'))]
            find_stage = self.env['sh.helpdesk.stages'].search(domain)
            if find_stage:
                ticket_vals['stage_id']=find_stage.id
      
        # ========= get sub-category which is connected to helpdesk ticket ======
        if data.get('sub_category_id'):
            domain = [('remote_helpdesk_subcategory_id', '=', data.get('sub_category_id'))]
            find_subcategory = self.env['helpdesk.subcategory'].search(domain)
            
            # ============== check Sub-category created or not if created then return  ==========
            if find_subcategory:
                ticket_vals['sub_category_id']=find_subcategory.id
            
            # ============= else prepare vals for created sub category ============
            # else:        
                    
            #     helpdesk_subcategory_vals={
            #         'remote_helpdesk_subcategory_id' : data.get('sub_category_id')['id'],
            #         'display_name':data.get('sub_category_id')['display_name'],
            #         'name':data.get('sub_category_id')['name'],
            #         'sequence' : data.get('sub_category_id')['sequence'],
            #     } 
                
            #     # =========== SEARCH PARENT CATEGORY IF EXIST THEN CONNECT DIRECTLY ELSE CREATE AND THEN CONNECT ==========
            #     domain_category=[('remote_sh_helpdesk_category_id','=',data.get('sub_category_id').get('parent_category_id').get('id'))] 
            #     find_category=self.env['sh.helpdesk.category'].search(domain_category)
            #     if find_category:
            #         helpdesk_subcategory_vals['parent_category_id']=find_category.id
            #     else:
            #         helpdesk_category_vals={
            #             'remote_sh_helpdesk_category_id' : data.get('sub_category_id')['parent_category_id']['id'],
            #             'display_name':data.get('sub_category_id')['parent_category_id']['display_name'],
            #             'name':data.get('sub_category_id')['parent_category_id']['name'],
            #             'sequence' : data.get('sub_category_id')['parent_category_id']['sequence'],
            #         }
            #         helpdesk_category=self.env['sh.helpdesk.category'].create(helpdesk_category_vals)
            #         helpdesk_subcategory_vals['parent_category_id']=helpdesk_category.id                 
                        
            #     created_subcategory=self.env['helpdesk.subcategory'].create(helpdesk_subcategory_vals)
                
            #     if created_subcategory:
            #         ticket_vals['sub_category_id']=created_subcategory.id
                
        # ============= CHECK HELPDESK TICKET SUBJECT IS EXIST OR NOT =============
        
        if data.get('subject_id'):
            domain = [('remote_sh_helpdesk_sub_type_id', '=', data.get('subject_id'))]
            find_sub_type = self.env['sh.helpdesk.sub.type'].search(domain)
            if find_sub_type:
               ticket_vals['subject_id'] = find_sub_type.id
               
            # else:   
            #     helpdesk_sub_type_vals={
            #         'remote_sh_helpdesk_sub_type_id' : data.get('subject_id')['id'],
            #         'display_name':data.get('subject_id')['display_name'],
            #         'name':data.get('subject_id')['name'],
            #     }
            #     create_subject=self.env['sh.helpdesk.sub.type'].create(helpdesk_sub_type_vals)
            #     if create_subject:
            #         ticket_vals['subject_id']=create_subject.id
                    
        # ============== CHECK TAGS ARE EXIST OR NOT WHICH ARE CONNECTED TO HELPDESK TICKET ========== 
        
        if data.get('tag_ids'):
            tag_list=[]
            for tag in data.get('tag_ids'):
                domain = [('remote_sh_helpdesk_tags_id', '=', tag)]
                find_tag = self.env['sh.helpdesk.tags'].search(domain)
                if find_tag:
                    tag_list.append((4,find_tag.id))
            if tag_list:
                ticket_vals['tag_ids']=tag_list 
                    
        # ============== GET TEAM HEAD DATA WHICH IS ASSIGNED IN HELPDESK TICKET ========
        
        if data.get('team_head') and data.get('team_head')!=0:
           
            domain_by_id = [('remote_res_user_id','=',data.get('team_head'))]
            find_user_id=self.env['res.users'].search(domain_by_id)
            # domain_by_login = [('login','=',data.get('team_head')['login'])]
            # find_user_login=self.env['res.users'].search(domain_by_login)
            if find_user_id:
                ticket_vals['team_head']=find_user_id.id 
            # elif find_user_login:
            #     ticket_vals['team_head']=find_user_login.id 
            # else:
            #     user_vals=self.process_user_data(data.get('team_head'))       
            #     user_id=self.env['res.users'].create(user_vals)
            #     if user_id:
            #         ticket_vals['team_head']=user_id.id
                    
        # ========== GET TEAM DATA WHICH IS CONNECTED TO HELPDESK TICKET ==========
        
        if data.get('team_id') and data.get('team_id')!=0:
            domain = [('remote_sh_helpdesk_team_id','=',data.get('team_id'))]
            find_team = self.env['sh.helpdesk.team'].search(domain)
            if find_team:
                ticket_vals['team_id']=find_team.id
            # else:
            #     helpdesk_team_vals = self.process_helpdesk_team_data(data.get('team_id'))
            #     team_id=self.env['sh.helpdesk.team'].create(helpdesk_team_vals)
            #     ticket_vals['team_id']=team_id.id
                    
        # =========== GET TICKET TYPE IF ALREADY EXIST OTHERWISE CREATE ====
        
        if data.get('ticket_type'):
            domain = [('remote_sh_helpdesk_ticket_type_id', '=', data.get('ticket_type'))]
            find_ticket_type = self.env['sh.helpdesk.ticket.type'].search(domain)
            if find_ticket_type:
                ticket_vals['ticket_type']=find_ticket_type.id
                    
        # ========= GET USER WHICH IS ASSIGN IN HELPDESK TICKET ==========
        
        if data.get('user_id') and data.get('user_id')!=0:
            
            domain_by_id = [('remote_res_user_id','=',data['user_id'])]
            find_user_id=self.env['res.users'].search(domain_by_id)
            # domain_by_login = [('login','=',data['cancel_by']['login'])]
            # find_user_login=self.env['res.users'].search(domain_by_login)
            
            # ========== SEARCH USER BY ID OR BY NAME IF EXIST THEN RETURN ELSE CREATE USE AND RETURN IT =====
            if find_user_id:
                ticket_vals['user_id']=find_user_id.id 
            # elif find_user_login:
            #     ticket_vals['user_id']=find_user_login.id 
            # else:
            #     user_vals=self.process_user_data(data['user_id'])       
            #     user_id=self.env['res.users'].create(user_vals)
            #     if user_id:
            #         ticket_vals['user_id']=user_id.id              
                                  
        return ticket_vals
    
    
        