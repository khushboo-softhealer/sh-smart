
# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
import requests
import json
import pytz
import datetime
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
import logging
_logger = logging.getLogger(__name__)

class InheritImportBase(models.Model):
    _inherit = "sh.import.base"

    import_message = fields.Boolean("Import Message")
    records_per_page_message = fields.Integer("No of Message per page")
    current_import_page_message = fields.Integer("Message Current Page ",default=0)
    message_ids=fields.Char("Messages")


    def process_mail_message_ids(self):
        # active_ids = self.env['mail.message'].browse(self.env.context.get('active_ids'))
        # print("N\n\n",active_ids)
        # if active_ids:
        confid = self.env['sh.import.base'].search([],limit=1)
        # if confid.import_message and confid.message_ids:
        if confid.import_message:
            confid.current_import_page_message += 1
            query='%s/api/public/mail.message?query={*,-author_avatar,tracking_value_ids{*}}&order="id asc"&filter=[["model", "=", "crm.lead"]]&page_size=%s&page=%s' %(confid.base_url,confid.records_per_page_message,confid.current_import_page_message)
            # print("\n\n=====query",query)
            response = requests.get(query) 
            # message_ids = confid.message_ids.strip('][').split(', ')  
            # for message in message_ids[0:300]:
            # for active_id in active_ids:
                # response = requests.get('''%s/api/public/mail.message/%s?query={id,message_id,author_id}''' %(confid.base_url,message))
            response_json = response.json() 
            print("\n\n====response_json",response_json)
            if response.status_code == 200:
                count = 0
                failed = 0                
                for data in response_json['result']:
                    domain = [('remote_mail_message_id', '=', data['id'])]
                    message_obj = self.env['mail.message'].search(domain,limit=1) 
                    print("message_obj find message_obj",message_obj)
                    author = False
                    if data.get('author_id'):
                        print("\n\n====message.get('author_id')",data.get('author_id'))
                        domain = [('remote_res_partner_id', '=', data['author_id'])]
                        find_customer = self.env['res.partner'].search(domain,limit=1)
                        if find_customer:
                            author = find_customer.id

                    if message_obj:
                        message_obj.write({
                            'message_id':data.get('message_id'),
                            'author_id':author
                        })
                        count += 1 
                    else:
                        failed+=1 
                if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "attachment",
                        "error": "%s Messages Imported Successfully" %(count - failed),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)                   
                if failed > 0:
                    vals = {
                        "name": confid.name,
                        "state": "error",
                        "field_type": "attachment",
                        "error": "%s Failed To Import" %(failed),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
            # confid.message_ids='['+', '.join([str(elem) for elem in message_ids[300:]])+']'              













    def import_mail_messages_cron(self):
        
        confid = self.env['sh.import.base'].search([],limit=1)
        # if confid.import_message:
        confid.current_import_page_message += 1

        # query='%s/api/public/mail.message?query={*,-author_avatar,tracking_value_ids{*}}&order="id asc"&&filter=[["write_date",">=","%s"],["write_date","<=","%s"],["model","=","helpdesk.ticket"]]' %(confid.base_url,str(confid.sh_from_date_task),str(confid.sh_to_date_task))
        # # print("\n\n=====query",query)
        # response = requests.get(query) 
        message_ids = confid.message_ids.strip('][').split(', ')  
        _logger.info('Messages',message_ids[0:confid.records_per_page_message])
        for message in message_ids[0:confid.records_per_page_message]:
        # for active_id in active_ids:
            response = requests.get('''%s/api/public/mail.message/%s?query={*,-author_avatar,tracking_value_ids{*}}''' %(confid.base_url,message))          
            if response.status_code == 200:
                response_json = response.json()
                # if 'count' in response_json:
                #     if confid.records_per_page_message != response_json['count']:
                #         confid.import_message = False
                #         confid.current_import_page_message = 0
                count = 0
                failed = 0                
                for data in response_json['result']:
                    message_vals = confid.process_message_data(data)                    
                    _logger.info('  ==== message_vals',message_vals)
                    domain = [('remote_mail_message_id', '=', data['id'])]
                    message_obj = self.env['mail.message'].search(domain,limit=1) 
                    print("message_obj find message_obj",message_obj)
                    if message_obj:
                        _logger.info('----- inside if ')
                        count += 1 
                        self.env['mail.message'].write(message_vals)
                        if data.get('child_ids') and message_obj:
                            for child in data.get('child_ids'):
                                find_message=self.env['mail.message'].search([('remote_mail_message_id', '=',child)],limit=1) 
                                if find_message:
                                    find_message.parent_id= message_obj.id 
                    else:
                        _logger.info('----- inside Else ')
                        # try:
                        if 'res_id' in message_vals:
                            print("message_vals",message_vals)
                            message_obj = self.env['mail.message'].sudo().create(message_vals) 
                            if data.get('child_ids') and message_obj:
                                for child in data.get('child_ids'):
                                    find_message=self.env['mail.message'].search([('remote_mail_message_id', '=',child)],limit=1) 
                                    if find_message:
                                        find_message.parent_id= message_obj.id 
                            count += 1 
                        # else:
                        #     print("\nn\====attchment_vals==",attchment_vals)                          
                        # except Exception as e:                    
                        #     failed += 1
                        #     vals = {
                        #         "name": data['id'],
                        #         "error": e,
                        #         "import_json" : data,
                        #         "field_type": "attachment",                           
                        #         "datetime": datetime.now(),
                        #         "base_config_id": confid.id,
                        #     }
                        #     self.env['sh.import.failed'].create(vals)               
                if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "attachment",
                        "error": "%s Messages Imported Successfully" %(count - failed),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)                   
                if failed > 0:
                    vals = {
                        "name": confid.name,
                        "state": "error",
                        "field_type": "attachment",
                        "error": "%s Failed To Import" %(failed),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
                confid.message_ids='['+', '.join([str(elem) for elem in message_ids[confid.records_per_page_message:]])+']'              
            else:
                vals = {
                    "name": confid.name,
                    "state": "error",
                    "field_type": "attachment",
                    "error": response.text,
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)



    def import_mail_message_from_queue(self):
        ''' ========== Import Projects Task ============ '''
        
        confid = self.env['sh.import.base'].search([],limit=1)
        if confid.import_message and confid.message_ids:
            message_ids = confid.message_ids.strip('][').split(', ')  
            for message in message_ids[0:300]:
                # confid.current_import_page_task_product += 1
                query='%s/api/public/mail.message/%s?query={*,-author_avatar,tracking_value_ids{*}}&order="id asc"' %(confid.base_url,message)
                # print("\n\n=====query",query)
                response = requests.get(query)           
                if response.status_code == 200:
                    response_json = response.json()
                    # if 'count' in response_json:
                    #     if confid.records_per_page_message != response_json['count']:
                    #         confid.import_message = False
                    #         confid.current_import_page_message = 0
                    count = 0
                    failed = 0                
                    for data in response_json['result']:
                        # print("\n\n======data",data)
                        message_vals = confid.process_message_data(data)   
                        # print("\n\n======message_vals",message_vals)                 
                        domain = [('remote_mail_message_id', '=', data['id'])]
                        message_obj = self.env['mail.message'].search(domain,limit=1) 
                        print("message_obj find message_obj",message_obj)
                        if message_obj:
                            count += 1 
                            message_obj = self.env['mail.message'].write(message_vals)
                        else:
                            # try:
                            # print("\n\n\n",message_vals)
                            if 'res_id' in message_vals:
                                # print("message_vals",message_vals)
                                message_obj = self.env['mail.message'].sudo().create(message_vals) 
                                count += 1 
                                print("==== message_obj",message_obj)    
                            # else:
                            #     print("\nn\====attchment_vals==",attchment_vals)                          
                            # except Exception as e:                    
                            #     failed += 1
                            #     vals = {
                            #         "name": data['id'],
                            #         "error": e,
                            #         "import_json" : data,
                            #         "field_type": "attachment",                           
                            #         "datetime": datetime.now(),
                            #         "base_config_id": confid.id,
                            #     }
                            #     self.env['sh.import.failed'].create(vals)  
            confid.message_ids='['+', '.join([str(elem) for elem in message_ids[300:]])+']'              
            if count > 0:              
                vals = {
                    "name": confid.name,
                    "state": "success",
                    "field_type": "attachment",
                    "error": "%s Messages Imported Successfully" %(count - failed),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)                   
            if failed > 0:
                vals = {
                    "name": confid.name,
                    "state": "error",
                    "field_type": "attachment",
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
                "field_type": "attachment",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals)



    def process_message_data(self,message):
        ''' ============= Prepare Message related task list =============  '''
          
        # date = message.get('date')
        # local = pytz.timezone('Asia/Kolkata')
        # naive = datetime.strptime(date, "%Y-%m-%d-%H-%M-%S")
        # local_dt = local.localize(naive, is_dst=None)
        # utc_dt = local_dt.astimezone(pytz.utc)
        # create_date = utc_dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

        print("\n\n\n",json.dumps(message,indent=4))

        message_vals={
            'remote_mail_message_id':message.get('id'),
            'body':message.get('body'), 
            'display_name':message.get('display_name'),
            'email_from':message.get('email_from'), 
            'has_error':message.get('has_error'),
            'message_id':message.get('message_id'),
            'message_type':message.get('message_type').get('sh_api_current_state'),       
            'model':message.get('model'),
            # 'needaction':message.get('needaction'), 
            'rating_value':message.get('rating_value'),
            'record_name':message.get('record_name'), 
            'reply_to':message.get('reply_to'),
            # 'res_id':message.get('res_id'), 
            # 'starred':message.get('starred'),
            'subject':message.get('subject'),
            'description':message.get('description'),
        }

        if message.get('parent_id'):
            find_message=self.env['mail.message'].search([('remote_mail_message_id','=',message.get('parent_id'))],limit=1)      
            if find_message:
                message_vals['parent_id']=find_message.id

        if message.get('subtype_id'):
            find_subtype=self.env['mail.message.subtype'].search([('remote_mail_message_subtype_id','=',message.get('subtype_id'))],limit=1)      
            if find_subtype:
                message_vals['subtype_id']=find_subtype.id

        if message.get('date'):
            date_time=datetime.strptime(message.get('date'),'%Y-%m-%d-%H-%M-%S')
            date_time=date_time.strftime('%Y-%m-%d %H:%M:%S')
            message_vals['date']=date_time
        if message_vals['model'] == 'helpdesk.ticket':
            message_vals['model'] = 'sh.helpdesk.ticket'
        if message_vals['model'] == 'account.invoice':
            message_vals['model'] = 'account.move'
        if message_vals['model'] == 'account.invoice.line':
            message_vals['model'] = 'account.move.line'
            
        field_name="remote_%s_id"%(message_vals.get('model').replace(".", "_"))
        if field_name == 'remote_hr_leave_id':
            field_name = 'remote_leave_id'
        checked_field = self.env['ir.model.fields'].sudo().search([('name','=',field_name)])
        # print("\n======checked_field=",checked_field,message.get('id'))
        # print("\n======model_name=",message_vals['model'])
        # print("======field_name=",field_name)
        
        if checked_field and message.get('res_id') and message.get('model'):
            # print("\n\n\n111111111111111111111")
            res_id_find =self.env[message_vals['model']].sudo().search([(field_name,'=',message.get('res_id'))],limit=1)               
            # print("====res_id_find",res_id_find)
            if res_id_find:
                message_vals.update({
                    'res_id':res_id_find.id,
                })
        tracking_list=[]
        if message.get('tracking_value_ids'):
            # print("=======message.get('tracking_value_ids')",message.get('tracking_value_ids'))
            for tracking in message.get('tracking_value_ids'):
                find_tracking=self.env['mail.tracking.value'].search([('remote_mail_tracking_value_id','=',tracking.get('id'))])
                tracking_vals={
                    'remote_mail_tracking_value_id':tracking.get('id'),
                    'new_value_char':tracking.get('new_value_char'),
                    'new_value_float':tracking.get('new_value_float'),
                    'new_value_integer':tracking.get('new_value_integer'),
                    'new_value_monetary':tracking.get('new_value_monetary'),
                    'new_value_text':tracking.get('new_value_text'),
                    'old_value_char':tracking.get('old_value_char'),
                    'old_value_float':tracking.get('old_value_float'),
                    'old_value_integer':tracking.get('old_value_integer'),
                    'old_value_monetary':tracking.get('old_value_monetary'),
                    'old_value_text':tracking.get('old_value_text'),
                }
                if tracking.get('new_value_datetime'):
                    date_time=datetime.strptime(tracking.get('new_value_datetime'),'%Y-%m-%d-%H-%M-%S')
                    date_time=date_time.strftime('%Y-%m-%d %H:%M:%S')
                    tracking_vals['new_value_datetime']=date_time
                if tracking.get('old_value_datetime'):
                    date_time=datetime.strptime(tracking.get('old_value_datetime'),'%Y-%m-%d-%H-%M-%S')
                    date_time=date_time.strftime('%Y-%m-%d %H:%M:%S')
                    tracking_vals['old_value_datetime']=date_time
                if tracking.get('field'):    
                    checked_field = self.env['ir.model.fields'].sudo().search([('name','=',tracking.get('field')),('model','=',message_vals['model'])])
                    # print("======checked_field",checked_field)
                    if checked_field:
                        tracking_vals['field']=checked_field.id 
                        tracking_vals['field_desc']=checked_field.field_description 
                if tracking_vals.get('field'):
                
                    if find_tracking:
                        find_tracking.write(tracking_vals)
                    else:
                        tracking_list.append((0,0,tracking_vals))

            if tracking_list:
                message_vals['tracking_value_ids']=tracking_list


        # ======== Get User if already created or create =========
        # if message.get('user_id') and message.get('user_id').get('id') and message.get('user_id').get('active'):
        #     domain_by_id = [('remote_res_user_id','=',message['user_id']['id'])]
        #     find_user_id=self.env['res.users'].search(domain_by_id)
        #     domain_by_login = [('login','=',message['user_id']['login'])]
        #     find_user_login=self.env['res.users'].search(domain_by_login)
        #     if find_user_id:
        #         message_vals['user_id']=find_user_id.id 
        #     elif find_user_login:
        #         message_vals['user_id']=find_user_login.id 
        #     else:
        #         user_vals=self.process_user_data(message['user_id'])       
        #         user_id=self.env['res.users'].create(user_vals)
        #         if user_id:
        #             message_vals['user_id']=user_id.id
                    
        # ======== Get Partner if already created or create =========
    
        if message.get('author_id'):
            print("\n\n====message.get('author_id')",message.get('author_id'))
            domain = [('remote_res_partner_id', '=', message['author_id'])]
            find_customer = self.env['res.partner'].search(domain,limit=1)
            if find_customer:
                message_vals['author_id'] = find_customer.id
            print("\n\n=======partner",find_customer,find_customer.name)
        else:
            message_vals['author_id'] = False
            # else:
            #     contact_vals=self.process_contact_data(message['author_id'])
            #     partner_id=self.env['res.partner'].create(contact_vals)
            #     if partner_id:
            #         message_vals['author_id']=partner_id.id

        # ======== Get Partner if already created or create =========
    
        if message.get('partner_ids'):
            partner_ids=[]
            for partner in message.get('partner_ids'):
                domain = [('remote_res_partner_id', '=', partner)]
                find_customer = self.env['res.partner'].search(domain,limit=1)
                if find_customer:
                    partner_ids.append((4,find_customer.id))
                # else:
                #     contact_vals=self.process_contact_data(partner)
                #     partner_id=self.env['res.partner'].create(contact_vals)
                #     if partner_id:
                #         partner_ids.append((4,partner_id.id))  
            if partner_ids:
                message_vals['partner_ids']=partner_ids  
                
        # ======== Get Partner if already created or create =========
    
        if message.get('starred_partner_ids'):
            s_partner_ids=[]
            for s_partner in message.get('starred_partner_ids'):
                domain = [('remote_res_partner_id', '=', s_partner)]
                find_customer = self.env['res.partner'].search(domain,limit=1)
                if find_customer:
                    s_partner_ids.append((4,find_customer.id))
                else:
                    contact_vals=self.process_contact_data(s_partner)
                    partner_id=self.env['res.partner'].create(contact_vals)
                    if partner_id:
                        s_partner_ids.append((4,partner_id.id))  
            if s_partner_ids:
                message_vals['starred_partner_ids']=s_partner_ids                      
                

        return message_vals