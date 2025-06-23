# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
from datetime import datetime
import requests
import json
class InheritImportBase(models.Model):
    _inherit = "sh.import.base"
    
    import_lead=fields.Boolean("Import Crm Lead")
    records_per_page_lead = fields.Integer("No of Lead per page")
    current_import_page_lead = fields.Integer("Current Lead Page",default=0) 
    sh_import_filter_crm=fields.Boolean("Import Filtered CRM")  
    sh_from_date_crm=fields.Datetime("From Date ")
    sh_to_date_crm=fields.Datetime("To Date ") 
    sh_import_crm_ids=fields.Char("CRM Team ids")

    def import_crm_filtered_to_queue(self):        
        ''' ========== Import Filtered CRM 
        between from date and end date ==================  ''' 
        confid = self.env['sh.import.base'].search([],limit=1)  
        if confid.sh_import_filter_crm:
            response = requests.get('''%s/api/public/crm.lead?query={id,write_date}&filter=["|",["active","=",true],["active","=",false],["write_date",">=","%s"],["write_date","<=","%s"],["company_id","=",1]]''' 
                %(confid.base_url,str(confid.sh_from_date_crm),str(confid.sh_to_date_crm)))
            response_json = response.json()
            if response_json.get('result'):
                confid.sh_import_crm_ids=[r['id'] for r in response_json.get('result')]

    def import_crm_from_queue(self):        
        confid = self.env['sh.import.base'].search([],limit=1)
        if confid.sh_import_filter_crm and confid.sh_import_crm_ids:   
            crms = confid.sh_import_crm_ids.strip('][').split(', ')
            count=0
            failed=0  
            for crm in crms[0:100]:
                response = requests.get('''%s/api/public/crm.lead/%s?query={*,message_follower_ids{*},tag_ids{*},lost_reason{*},medium_id{*},source_id{*},stage_id{*},state_id{name,code},
            message_ids{id,subtype_id{*},author_id,body,channel_ids{*},date,display_name,email_from,has_error,layout,mail_activity_type_id{*},
            message_id,message_type,model,moderation_status,moderator_id,need_moderation,needaction,no_auto_thread,notification_ids,rating_value,record_name,reply_to,res_id,starred,subject}
            }''' %(confid.base_url,crm))
                response_json = response.json()
                if response.status_code==200:               
                    for data in response_json['result']:
                        
                        # ======== PREPARE DATA FOR CRM LEAD CREATION OR UPDATE =========== 
                        
                        lead_vals = confid.process_lead_data(data)
                        domain = [('remote_crm_lead_id', '=', data['id'])]
                        find_lead = self.env['crm.lead'].search(domain)
                        # ========== IF EXIST CRM LEAD THEN UPDATE IT'S DATA ==========
                        if find_lead:
                            find_lead.write(lead_vals)     
                            print("\n\n=====find_lead",find_lead)
                            count += 1


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
                                                if partner not in find_lead.sudo().message_partner_ids.ids]
                                            find_lead.sudo().message_subscribe(partner_ids=part_list)
                                            find_follower=self.env['mail.followers'].search([('partner_id','=',find_customer.id),('res_id','=',find_lead.id)])
                                            if find_follower:
                                                find_follower.update({
                                                    'subtype_ids':  [(6,0,subtype_list)],
                                                })
                            
                        # ========== ELSE CREATE CRM LEAD  ==========                           
                        else:
                            create_lead=self.env['crm.lead'].create(lead_vals)
                            print("\n\n========create_lead",create_lead)
                            count += 1

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
                                                if partner not in create_lead.sudo().message_partner_ids.ids]
                                            create_lead.sudo().message_subscribe(partner_ids=part_list)
                                            find_follower=self.env['mail.followers'].search([('partner_id','=',find_customer.id),('res_id','=',create_lead.id)])
                                            if find_follower:
                                                find_follower.update({
                                                    'subtype_ids':  [(6,0,subtype_list)],
                                                })
                        
                        # ======= CREATE LOG FOR EXCEPTION WHICH IS GENERATE DURING IMPORT CRM LEAD ======= 
                                        
                    # ======= CREATE LOG FOR IMPORT SUCCESSFULLY CRM LEAD =======  
                    confid.sh_import_crm_ids='['+', '.join([str(elem) for elem in crms[100:]])+']'       
                    if count > 0:              
                        vals = {
                            "name": confid.name,
                            "state": "success",
                            "field_type": "lead",
                            "error": "%s Lead Imported Successfully" %(count - failed),
                            "datetime": datetime.now(),
                            "base_config_id": confid.id,
                            "operation": "import"
                        }
                        self.env['sh.import.base.log'].create(vals)
                        
                    # ======= CREATE LOG FOR IMPORT FAILED CRM LEAD =======  
                    if failed > 0:
                        vals = {
                            "name": confid.name,
                            "state": "error",
                            "field_type": "lead",
                            "error": "%s Failed To Import" %(failed),
                            "datetime": datetime.now(),
                            "base_config_id": confid.id,
                            "operation": "import"
                        }
                        self.env['sh.import.base.log'].create(vals)
                        
                # ======= CREATE LOG FOR ERROR WHICH IS GENERATE DURING IMPORT CRM LEAD ======= 
                else:
                    vals = {
                        "name": confid.name,
                        "state": "error",
                        "field_type": "lead",
                        "error": response.text,
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals) 
    
    
    def import_basic_crm_lead_cron(self):   
        self.import_crm_from_queue()
        ''' ========== Connect db for import Crm Lead basic  ==================  '''
        # confid = self.env['sh.import.base'].search([],limit=1)
        # if confid.import_lead:
        #     confid.current_import_page_lead += 1
        #     response = requests.get('''%s/api/public/crm.lead?query={*,message_follower_ids{*},tag_ids{*},lost_reason{*},medium_id{*},source_id{*},stage_id{*},state_id{name,code},
        #     message_ids{id,subtype_id{*},author_id,body,channel_ids{*},date,display_name,email_from,has_error,layout,mail_activity_type_id{*},
        #     message_id,message_type,model,moderation_status,moderator_id,need_moderation,needaction,no_auto_thread,notification_ids,rating_value,record_name,reply_to,res_id,starred,subject}
        #     }&page_size=%s&page=%s&filter=["|",["active","=",true],["active","=",false],["company_id","=",1]] ''' %(confid.base_url,confid.records_per_page_lead,confid.current_import_page_lead))
        #     response_json = response.json()
        #     if response.status_code==200:
        #         # pass
        #         if response_json.get('count') and confid.records_per_page_lead != response_json['count']:
        #             confid.import_lead = False
        #             confid.current_import_page_lead = 0
        #         count = 0
        #         failed = 0
                
        #         for data in response_json['result']:
                    
        #             # ======== PREPARE DATA FOR CRM LEAD CREATION OR UPDATE =========== 
                    
        #             lead_vals = confid.process_lead_data(data)
        #             domain = [('remote_crm_lead_id', '=', data['id'])]
        #             find_lead = self.env['crm.lead'].search(domain)
        #             print("\nn\============lead_vals",lead_vals)
        #             # try:
        #             # ========== IF EXIST CRM LEAD THEN UPDATE IT'S DATA ==========
        #             if find_lead:
        #                 count += 1
        #                 find_lead.write(lead_vals)     
        #                 # if lead_vals.get('sh_ticket_ids'):
        #                 #     for ticket in lead_vals.get('sh_ticket_ids'):
        #                 #         find_ticket=self.env['sh.helpdesk.ticket'].search([('remote_sh_helpdesk_ticket_id','=',ticket)])
        #                 #         if find_ticket:
        #                 #             find_ticket.sh_lead_ids=[(4,find_lead.id)]

        #                 if data.get('message_follower_ids'):
        #                     # follower_ids=[]
        #                     for follower in data.get('message_follower_ids'):
        #                         if follower.get('partner_id'):
        #                             domain = [('remote_res_partner_id', '=', follower.get('partner_id'))]
        #                             find_customer = self.env['res.partner'].search(domain)
        #                             subtype_list=[]
        #                             if follower.get('subtype_ids'):
                                    
        #                                 for subtype in follower.get('subtype_ids'):
        #                                     domain = [('remote_mail_message_subtype_id', '=', subtype)]
        #                                     find_subtype = self.env['mail.message.subtype'].search(domain)
        #                                     subtype_list.append(find_subtype.id)
        #                             if find_customer:
        #                                 part_list=[partner
        #                                     for partner in find_customer.ids
        #                                     if partner not in find_lead.sudo().message_partner_ids.ids]
        #                                 print("\n\n=======find_customer",find_customer)
        #                                 print("\nn\======part_list",part_list)
        #                                 find_lead.sudo().message_subscribe(partner_ids=part_list)
        #                                 find_follower=self.env['mail.followers'].search([('partner_id','=',find_customer.id),('res_model','=','crm.lead'),('res_id','=',find_lead.id)])
        #                                 print("\n\n========find_follower",find_follower)
        #                                 if find_follower:
        #                                     find_follower.update({
        #                                         'subtype_ids':  [(6,0,subtype_list)],
        #                                     })




        #             # ========== ELSE CREATE CRM LEAD  ==========                           
        #             else:
        #                 count += 1
        #                 create_lead=self.env['crm.lead'].create(lead_vals)
        #                 # if lead_vals.get('sh_ticket_ids'):
        #                 #     for ticket in lead_vals.get('sh_ticket_ids'):
        #                 #         find_ticket=self.env['sh.helpdesk.ticket'].search([('remote_sh_helpdesk_ticket_id','=',ticket)])
        #                 #         if find_ticket:
        #                 #             find_ticket.sh_lead_ids=[(4,find_lead.id)]

        #                 if data.get('message_follower_ids'):
        #                     # follower_ids=[]
        #                     for follower in data.get('message_follower_ids'):
        #                         if follower.get('partner_id'):
        #                             domain = [('remote_res_partner_id', '=', follower.get('partner_id'))]
        #                             find_customer = self.env['res.partner'].search(domain)
        #                             subtype_list=[]
        #                             if follower.get('subtype_ids'):
                                    
        #                                 for subtype in follower.get('subtype_ids'):
        #                                     domain = [('remote_mail_message_subtype_id', '=', subtype)]
        #                                     find_subtype = self.env['mail.message.subtype'].search(domain)
        #                                     subtype_list.append(find_subtype.id)
        #                             if find_customer:
        #                                 part_list=[partner
        #                                     for partner in find_customer.ids
        #                                     if partner not in create_lead.sudo().message_partner_ids.ids]
        #                                 create_lead.sudo().message_subscribe(partner_ids=part_list)
        #                                 find_follower=self.env['mail.followers'].search([('partner_id','=',find_customer.id),('res_model','=','crm.lead'),('res_id','=',create_lead.id)])
        #                                 if find_follower:
        #                                     find_follower.update({
        #                                         'subtype_ids':  [(6,0,subtype_list)],
        #                                     })
                    
        #             # ======= CREATE LOG FOR EXCEPTION WHICH IS GENERATE DURING IMPORT CRM LEAD ======= 
                    
        #             # except Exception as e:
        #             #     vals = {
        #             #         "name": data['id'],
        #             #         "error": e,
        #             #         "import_json" : data,
        #             #         "field_type": "crm_basic",                           
        #             #         "datetime": datetime.now(),
        #             #         "base_config_id": self.id,
        #             #     }
        #             #     self.env['sh.import.failed'].create(vals)    
                        
        #         # ======= CREATE LOG FOR IMPORT SUCCESSFULLY CRM LEAD =======  
                           
        #         if count > 0:              
        #             vals = {
        #                 "name": confid.name,
        #                 "state": "success",
        #                 "field_type": "lead",
        #                 "error": "%s Lead Imported Successfully" %(count - failed),
        #                 "datetime": datetime.now(),
        #                 "base_config_id": confid.id,
        #                 "operation": "import"
        #             }
        #             self.env['sh.import.base.log'].create(vals)
                    
        #         # ======= CREATE LOG FOR IMPORT FAILED CRM LEAD =======  
        #         if failed > 0:
        #             vals = {
        #                 "name": confid.name,
        #                 "state": "error",
        #                 "field_type": "lead",
        #                 "error": "%s Failed To Import" %(failed),
        #                 "datetime": datetime.now(),
        #                 "base_config_id": confid.id,
        #                 "operation": "import"
        #             }
        #             self.env['sh.import.base.log'].create(vals)
                    
        #     # ======= CREATE LOG FOR ERROR WHICH IS GENERATE DURING IMPORT CRM LEAD ======= 
        #     else:
        #         vals = {
        #             "name": confid.name,
        #             "state": "error",
        #             "field_type": "lead",
        #             "error": response.text,
        #             "datetime": datetime.now(),
        #             "base_config_id": confid.id,
        #             "operation": "import"
        #         }
        #         self.env['sh.import.base.log'].create(vals) 
    
    
    
    
    def process_lead_data(self,data):
        ''' =========== PREPARE VALUES FOR CRM LEAD IMPORT ==============='''
        
        lead_vals={
           'remote_crm_lead_id':data.get('id'),
           'active':data.get('active'),
           'day_open':data.get('day_open'),
           'day_close':data.get('day_close'),
           'prorated_revenue':data.get('planned_revenue'),
           'city':data.get('city'),
           'color':data.get('acticolorve'),
           'contact_name':data.get('contact_name'),
           'description':data.get('description'),
           'display_name':data.get('display_name'),
           'email_cc':data.get('email_cc'),
           'email_from':data.get('email_from'),
           'expected_revenue':data.get('expected_revenue'),
           'function':data.get('function'),
           'is_blacklisted':data.get('is_blacklisted'), 
           'kanban_state':data.get('kanban_state').get('sh_api_current_state'),
           'message_is_follower':data.get('message_is_follower'),
           'message_has_error':data.get('message_has_error'),
           'message_needaction':data.get('message_needaction'),
           'mobile':data.get('mobile'),
           'name':data.get('name'),
           'partner_is_blacklisted':data.get('partner_is_blacklisted'),
           'partner_name':data.get('partner_name'),
           'phone':data.get('phone'),
           'priority':data.get('priority').get('sh_api_current_state'),
           'probability':data.get('probability'),
           'referred':data.get('referred'),
           'street':data.get('street'),
           'street2':data.get('street2'),
           'title':data.get('title'),
           'type':data.get('type').get('sh_api_current_state'),
           'sh_replied_status':data.get('sh_replied_status').get('sh_api_current_state'),
           'website':data.get('website'),
           'zip':data.get('zip'), 
           'company_id':1,
        }
        
        # ============ Get stage if already created or create ==============
        if data.get('stage_id'):
            domain_by_id=[('remote_crm_stage_id','=',data.get('stage_id').get('id'))]
            already_crm_stage_id = self.env['crm.stage'].search(domain_by_id,limit=1)
            domain_by_name=[('name','=',data.get('stage_id').get('name'))]
            already_crm_stage_name = self.env['crm.stage'].search(domain_by_name,limit=1)
            
            # ======== CHECK IF CRM STAGE IS CREATED OR NOT IF CREATE THEN RETURN ELSE CREATE =======
            
            if already_crm_stage_id:
                lead_vals['stage_id']=already_crm_stage_id.id
            elif already_crm_stage_name:
                lead_vals['stage_id']=already_crm_stage_name.id
            else:
                crm_stage_data = self.process_lead_stage_data(data.get('stage_id'))
                crm_stage_id=self.env['crm.stage'].create(crm_stage_data)
                if crm_stage_id:
                    lead_vals['stage_id']=crm_stage_id.id

        if data.get('sh_ticket_ids'):
            ticket_list=[]
            for ticket in data.get('sh_ticket_ids'):
                find_ticket=self.env['sh.helpdesk.ticket'].search([('remote_sh_helpdesk_ticket_id','=',ticket)])
                if find_ticket:
                    ticket_list.append(find_ticket.id)
            if ticket_list:
                lead_vals['sh_ticket_ids']=ticket_list
                    
        # ============ Get Team if already created or create ==============
        if data.get('team_id'):
            domain=[('remote_crm_team_id','=',data.get('team_id'))]
            already_crm_team = self.env['crm.team'].search(domain,limit=1)
            
            # ======== CHECK IF CRM TEAM IS CREATED OR NOT IF CREATE THEN RETURN ELSE CREATE =======
            if already_crm_team:
                lead_vals['team_id']=already_crm_team.id
                    
        # =========== Preapre tags related to crm leads==========
        if data.get('tag_ids'):
            tag_list=[]
            for tag in data.get('tag_ids'):
                domain_by_id=[('remote_crm_tag_id','=',tag.get('id'))]
                already_crm_tag_id = self.env['crm.tag'].search(domain_by_id,limit=1)
                domain_by_name=[('name','=',tag.get('name'))]
                already_crm_tag_name = self.env['crm.tag'].search(domain_by_name,limit=1) 
                
                # ======== CHECK IF CRM TAG IS CREATED OR NOT IF CREATE THEN RETURN ELSE CREATE =======           
                if already_crm_tag_id:
                    tag_list.append((4,already_crm_tag_id.id))
                elif already_crm_tag_name:
                    tag_list.append((4,already_crm_tag_name.id))
                else:
                    crm_tag_data={
                    'remote_crm_tag_id':tag.get('id'),
                    'color' : tag.get('color'),  
                    'display_name':tag.get('display_name'),
                    'name':tag.get('name'),
                    }
                    crm_tag_id=self.env['crm.tag'].create(crm_tag_data)
                    tag_list.append((4,crm_tag_id.id))
                    
            if tag_list:
                lead_vals['tag_ids']=tag_list
                
        # ======== Get Partner if already created or create =========
        
        if data.get('partner_id'):
            domain = [('remote_res_partner_id', '=', data['partner_id'])]
            find_customer = self.env['res.partner'].search(domain,limit=1)
            
            # ======== CHECK IF PARTNER IS CREATED OR NOT IF CREATE THEN RETURN ELSE CREATE =======
            if find_customer:
                lead_vals['partner_id'] = find_customer.id
        
        if data.get('medium_id'):
            domain = ['|', ('remote_medium_id', '=', data.get('medium_id').get('id')),
                        ('name', '=', data.get('medium_id').get('name'))]
            find_medium = self.env['utm.medium'].search(domain)
            if find_medium:
                lead_vals['medium_id'] = find_medium.id    

        # ======== Get Message Partner if already created or create =========
        
        # if data.get('message_partner_ids'):
        #     partner_list=[]
        #     for m_partner in data.get('message_partner_ids'):
        #         domain = [('remote_res_partner_id', '=',m_partner)]
        #         find_customer = self.env['res.partner'].search(domain,limit=1)
                
        #         # ======== CHECK IF PARTNER IS CREATED OR NOT IF CREATE THEN RETURN ELSE CREATE =======
        #         if find_customer:
        #             partner_list.append((4,find_customer.id))
                        
        #     lead_vals['message_partner_ids']=partner_list
        
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
                            
        #     lead_vals['message_ids']=message_list+message_list_create
                
        # ======== Get User if already created or create =========
            
        if data.get('user_id') and data.get('user_id')!=0:
            domain_by_id = [('remote_res_user_id','=',data['user_id'])]
            find_user_id=self.env['res.users'].search(domain_by_id)
            
            # ======== CHECK IF USER IS CREATED OR NOT IF CREATE THEN RETURN ELSE CREATE =======
            
            if find_user_id:
                lead_vals['user_id']=find_user_id.id 
        
        return lead_vals