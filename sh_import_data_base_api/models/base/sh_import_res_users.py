
# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
import requests
import json
from datetime import datetime

class InheritImportBase(models.Model):
    _inherit = "sh.import.base"
    
    import_user=fields.Boolean("Import User")
    records_per_page_user = fields.Integer("No of User per page")
    current_import_page_user = fields.Integer(" Current Page ",default=0) 

    update_user_partner = fields.Boolean("Update User Partner")
    update_user = fields.Integer("Update No of User partner")
    update_current_page = fields.Integer("Update Current Page ",default=0) 
    users=fields.Char("Users")

    def sh_update_partner_id(self):
        confid = self.env['sh.import.base'].search([],limit=1)
        if confid.update_user_partner:
            confid.update_current_page += 1
            response = requests.get('''%s/api/public/res.users?query={id,partner_id,team_id}&page_size=%s&page=%s&filter=[["company_id","=",1]]''' %(confid.base_url,confid.update_user,confid.update_current_page))
            response_json = response.json()
            print("\n\n=====response_json",response_json)  
            if response.status_code == 200:
                if 'count' in response_json and confid.update_user != response_json['count'] : 
                    confid.update_user_partner = False
                    confid.update_current_page = 0
                count=0
                failed=0
                for data in response_json['result']:
                    # try:
                    print("\n\n========vvvvvvvvvvvvvvvv")
                    if data.get('id') and data.get('id')!=0:
                        find_user=self.env['res.users'].search([('remote_res_user_id','=',data.get('id'))],limit=1)
                        if find_user and data.get('partner_id') and find_user.partner_id:
                            find_duplicate_partner=self.env['res.partner'].search([('id','!=',find_user.partner_id.id),('remote_res_partner_id','=',data.get('partner_id'))])
                            print("\n\n========data.get('partner_id')",data.get('partner_id'),find_duplicate_partner)
                            if find_duplicate_partner:
                                find_duplicate_partner.unlink()
                            find_user.partner_id.write({
                                'remote_res_partner_id':data.get('partner_id'),
                            })
                        # if find_user and data.get('team_id'):
                        #     find_team = self.env['crm.team'].search(['remote_crm_team_id', '=', data.get('team_id')],limit=1)
                        #     print("\n\n\n\n",find_team)
                        #     if find_team:
                        #         find_user.write({
                        #             'team_id' : find_team.id
                        #         })
                            count += 1
                    
                    # except Exception as e:
                    #     failed += 1
                    #     vals = {
                    #         "name": data['id'],
                    #         "error": e,
                    #         "import_json" : data,
                    #         "field_type": "res_users",                           
                    #         "datetime": datetime.now(),
                    #         "base_config_id": confid.id,
                    #     }
                    #     self.env['sh.import.failed'].create(vals) 
                # ========= CREATE LOG FOR SUCCESSFULLY IMPORT UOM =================
                    
                if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "res_users",
                        "error": "%s Users Update Successfully" %(count - failed),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
                if failed > 0:
                    vals = {
                        "name": confid.name,
                        "state": "error",
                        "field_type": "res_users",
                        "error": "%s Failed To Import" %(failed),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)


    
    def import_res_users(self):
        ''' ============ IMPORT Users ===========   '''
        confid = self.env['sh.import.base'].search([],limit=1)
        if confid.import_user:
            confid.current_import_page_user += 1 
            response = requests.get('''%s/api/public/res.users?query={id,active,active_partner,groups_id{id,name,full_name,display_name},customer,employee,barcode,is_blacklisted,is_moderator,is_published,is_seo_optimized,city,color,comment,contact_address,login,mobile,name,new_password,
            credit_limit,debit,debit_limit,display_name,email,email_formatted,password,phone,state,street,street2,vat,tz,tz_offset,message_is_follower,message_needaction,
            partner_share,sh_customer_reply_notification_on_off,sh_enable_night_mode,sh_job_applicant_notification_on_off,sh_new_notification_on_off,
            sh_portal_user,sh_sale_customer_reply_notif,sh_ticket_assigned_notification_on_off,share,show_in_website,signup_valid,website_published,additional_info,commercial_company_name,
            company_name,function,im_status,parent_name,partner_ledger_label,ref,signup_token,signup_url,website,
            website_url,support_hours,color,credit,total_invoiced,invoice_warn,notification_type,odoobot_state,sale_warn,sh_portal_user_access,trust,
            sale_warn_msg,sign,website_meta_description,website_short_description}&page_size=%s&page=%s&filter=[["company_id","=",1]]''' %(confid.base_url,confid.records_per_page_user,confid.current_import_page_user))
            if response.status_code == 200:
                response_json = response.json()     
                if 'count' in response_json and confid.records_per_page_user != response_json['count'] : 
                    confid.import_user = False
                    confid.current_import_page_user = 0
                count=0
                failed=0
                for data in response_json['result']:
                    try:
                        #  ============= PREAPRE users VALS FOR IMPORT THAT ==============
                        # if data.get('login') and data.get('login')=='admin':
                        #     count += 1
                        #     continue
                        # else:
                        user_vals = confid.process_user_data(data)
                        domain = ['|',('remote_res_user_id', '=', data['id']),('login','=',data['login']),'|',('active','=',True),('active','=',False)]
                        find_user = self.env['res.users'].search(domain)
                            
                        # ============ CHECK IF user EXIST OR NOT ===============
                        if find_user:
                            find_user.write(user_vals)
                        else:
                            self.env['res.users'].create(user_vals)  
                        count += 1
                    
                    except Exception as e:
                        failed += 1
                        vals = {
                            "name": data['id'],
                            "error": e,
                            "import_json" : data,
                            "field_type": "res_users",                           
                            "datetime": datetime.now(),
                            "base_config_id": confid.id,
                        }
                        self.env['sh.import.failed'].create(vals) 
                # ========= CREATE LOG FOR SUCCESSFULLY IMPORT UOM =================
                    
                if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "res_users",
                        "error": "%s Users Imported Successfully" %(count - failed),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
                if failed > 0:
                    vals = {
                        "name": confid.name,
                        "state": "error",
                        "field_type": "res_users",
                        "error": "%s Failed To Import" %(failed),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
                      
                            
            # ========== CREATE LOG FOR ERROR WHICH IS  GENERATE DURING RESOURCE CALENDAR IMPORT  ==============

            else:
                vals = {
                    "name": confid.name,
                    "state": "error",
                    "field_type": "res_users",
                    "error": response.text,
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)
    

    def import_update_res_users(self):
        ''' ============ IMPORT Users ===========   '''
        confid = self.env['sh.import.base'].search([],limit=1)
        print("\n\n========update users")
        if confid.import_user:
            users = confid.users.strip('][').split(', ')
            count=0
            failed=0  
            for user in users[0:5]:
                response = requests.get('''%s/api/public/res.users/%s?query={id,active,active_partner,groups_id{id,name,full_name,display_name},customer,employee,barcode,is_blacklisted,is_moderator,is_published,is_seo_optimized,city,color,comment,contact_address,login,mobile,name,new_password,
                credit_limit,debit,debit_limit,display_name,email,email_formatted,password,phone,state,street,street2,vat,tz,tz_offset,message_is_follower,message_needaction,
                partner_share,sh_customer_reply_notification_on_off,sh_enable_night_mode,sh_job_applicant_notification_on_off,sh_new_notification_on_off,
                sh_portal_user,sh_sale_customer_reply_notif,sh_ticket_assigned_notification_on_off,share,show_in_website,signup_valid,website_published,additional_info,commercial_company_name,
                company_name,function,im_status,parent_name,partner_ledger_label,ref,signup_token,signup_url,website,
                website_url,support_hours,color,credit,total_invoiced,invoice_warn,notification_type,odoobot_state,sale_warn,sh_portal_user_access,trust,
                sale_warn_msg,sign,website_meta_description,website_short_description}&filter=[["company_id","=",1]]''' %(confid.base_url,user))
                if response.status_code == 200:
                    response_json = response.json()     
                    count=0
                    failed=0
                    for data in response_json['result']:
                        try:
                            #  ============= PREAPRE users VALS FOR IMPORT THAT ==============
                            # if data.get('login') and data.get('login')=='admin':
                            #     count += 1
                            #     continue
                            # else:
                            user_vals = confid.process_user_data(data)
                            domain = ['|',('remote_res_user_id', '=', data['id']),('login','=',data['login']),'|',('active','=',True),('active','=',False)]
                            find_user = self.env['res.users'].search(domain)
                                
                            # ============ CHECK IF user EXIST OR NOT ===============
                            if find_user:
                                find_user.write(user_vals)
                            else:
                                self.env['res.users'].create(user_vals)  
                            count += 1
                        
                        except Exception as e:
                            failed += 1
                            vals = {
                                "name": data['id'],
                                "error": e,
                                "import_json" : data,
                                "field_type": "res_users",                           
                                "datetime": datetime.now(),
                                "base_config_id": confid.id,
                            }
                            self.env['sh.import.failed'].create(vals) 
                    # ========= CREATE LOG FOR SUCCESSFULLY IMPORT UOM =================
            confid.users='['+', '.join([str(elem) for elem in users[5:]])+']'        
                        
            if count > 0:              
                vals = {
                    "name": confid.name,
                    "state": "success",
                    "field_type": "res_users",
                    "error": "%s Users Update Successfully" %(count - failed),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)
            if failed > 0:
                vals = {
                    "name": confid.name,
                    "state": "error",
                    "field_type": "res_users",
                    "error": "%s Failed To Import" %(failed),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)
                      

        


    def process_user_data(self,data):
        ''' ============== Prepare SalesPerson ====================== '''
        user_vals = {
            'remote_res_user_id':data.get('id'),
            'active_partner':data.get('active_partner'),
            'employee':data.get('employee'),
            'barcode':data.get('barcode'),
            'is_blacklisted':data.get('is_blacklisted'),
            'is_published':data.get('is_published'),
            'is_seo_optimized':data.get('is_seo_optimized'),
            'city' : data.get('city'),  
            'color':data.get('color'),
            'comment':data.get('comment'),
            'contact_address':data.get('contact_address'),
            'login' : data.get('login'),  
            'mobile':data.get('mobile'),
            'name':data.get('name'),
            # 'new_password':'123',
            'credit_limit' : data.get('credit_limit'),  
            'debit':data.get('debit'),
            'debit_limit':data.get('debit_limit'),
            'display_name':data.get('display_name'),
            'email':data.get('email'),
            'email_formatted':data.get('email_formatted'),
            'phone':data.get('phone'),
            'state':data.get('state').get('sh_api_current_state'),            
            'street':data.get('street'),
            'street2':data.get('street2'),
            'vat':data.get('vat'),
            'tz':data.get('tz').get('sh_api_current_state') if data.get('tz') else 'Asia/Kolkata',
            'tz_offset':data.get('tz_offset'),
            'message_is_follower' : data.get('message_is_follower'),  
            'message_needaction':data.get('message_needaction'),
            'partner_share':data.get('partner_share'),
            'sh_customer_reply_notification_on_off':data.get('sh_customer_reply_notification_on_off'),
            # 'sh_enable_night_mode' : data.get('sh_enable_night_mode'),  
            'sh_job_applicant_notification_on_off':data.get('sh_job_applicant_notification_on_off'),            
            'sh_new_notification_on_off':data.get('sh_new_notification_on_off'),
            'sh_portal_user':data.get('sh_portal_user'),
            'sh_sale_customer_reply_notif':data.get('sh_sale_customer_reply_notif'),
            'sh_ticket_assigned_notification_on_off':data.get('sh_ticket_assigned_notification_on_off'),
            'share':data.get('share'),
            'show_in_website' : data.get('show_in_website'),  
            'signup_valid':data.get('signup_valid'),
            'website_published':data.get('website_published'),
            # 'additional_info':data.get('additional_info'),
            'commercial_company_name':data.get('commercial_company_name'),
            'company_name' : data.get('company_name'),  
            'function':data.get('function'),
            'im_status':data.get('im_status'),
            'parent_name':data.get('parent_name'),
            'ref' : data.get('ref'),  
            'signup_token':data.get('signup_token'),
            'signup_url':data.get('signup_url'),
            'website':data.get('website'),
            'website_url':data.get('website_url'),
            'support_hours' : data.get('support_hours'),  
            'color':data.get('color'),
            'credit':data.get('credit'),            
            'total_invoiced':data.get('total_invoiced'),
            'invoice_warn':data.get('invoice_warn').get('sh_api_current_state') if data.get('invoice_warn') else False,
            'notification_type':data.get('notification_type').get('sh_api_current_state'),
            # 'odoobot_state':data.get('odoobot_state').get('sh_api_current_state'),
            'sale_warn':data.get('sale_warn').get('sh_api_current_state') if data.get('sale_warn') else False, 
            'sh_portal_user_access':data.get('sh_portal_user_access').get('sh_api_current_state') if data.get('sh_portal_user_access') else False,
            'trust':data.get('trust').get('sh_api_current_state') if data.get('trust') else False,
            'sale_warn_msg':data.get('sale_warn_msg'),
            'sign':data.get('sign'),
            'website_meta_description':data.get('website_meta_description'),
            'website_short_description':data.get('website_short_description'),
            'company_id':1,
            'password':'123',
        }    
        # if data.get('groups_id'):
        #     print("\n\n\=====data.get('id')===",data.get('id'),data.get('name'))
        #     print("\n\n\=====data.get('groups_id')===",data.get('groups_id'))
        #     groups=[]
        #     for group in data.get('groups_id'):
        #         find_group=self.env['res.groups'].sudo().search([('full_name','=',group.get('full_name'))],limit=1)
        #         if find_group:
        #             groups.append(find_group.id)
        #     if groups:
        #         user_vals['groups_id']=[6,0,groups]
        return user_vals
    
    