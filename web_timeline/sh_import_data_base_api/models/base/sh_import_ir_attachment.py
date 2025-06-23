# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
import requests
import json
from datetime import datetime
import base64

class InheritImportEmployee(models.Model):
    _inherit = "sh.import.base"    

    import_attachment = fields.Boolean("Import Attachment")
    sh_import_filter_attachment=fields.Boolean("Import Filtered Attachment")  
    sh_from_date_attachment=fields.Datetime("From Date Attachment")
    sh_to_date_attachment=fields.Datetime("To Date Attachment") 
    sh_import_attachment_ids=fields.Char("Attachment ids")
    records_per_page_attachment = fields.Integer("No of Attachment per page")
    current_import_page_attachment = fields.Integer("Attachment Current Page ",default=0) 


    def import_attach_filtered_to_queue(self):
        ''' ========== Import Filtered Attachment 
        between from date and end date ==================  ''' 
        confid = self.env['sh.import.base'].search([],limit=1)  
        if confid.sh_import_filter_attachment:
            response = requests.get('''%s/api/public/ir.attachment?query={id,write_date}&filter=[["write_date",">=","%s"],["write_date","<=","%s"]]''' 
                %(confid.base_url,str(confid.sh_from_date_attachment),str(confid.sh_to_date_attachment)))
            response_json = response.json()
            if response_json.get('result'):
                confid.sh_import_attachment_ids=[r['id'] for r in response_json.get('result')]
    
    
    def import_attach_from_queue(self):   
        ''' ========== Import Attachment ==================  '''
        confid = self.env['sh.import.base'].search([],limit=1)
        if confid.sh_import_filter_attachment and confid.sh_import_attachment_ids:   
            attachs = confid.sh_import_attachment_ids.strip('][').split(', ')
            count=0
            failed=0  
            for attach in attachs[0:50]:
                try:
                    response = requests.get('%s/api/public/ir.attachment/%s?query={*}' %(confid.base_url,attach))           
                    if response.status_code == 200:
                        response_json = response.json()
                        for data in response_json['result']:
                            attchment_vals = confid.process_attchment_data(data)                    
                            domain = [('remote_ir_attachment_id', '=', data['id'])]
                            attachment_obj = self.env['ir.attachment'].search(domain,limit=1) 
                            if attachment_obj:
                                count += 1 
                                attachment_obj = self.env['ir.attachment'].write(attchment_vals)
                            else:
                                attachment_obj = self.env['ir.attachment'].create(attchment_vals) 
                    confid.sh_import_attachment_ids='['+', '.join([str(elem) for elem in attachs[50:]])+']'
                    if count > 0:              
                        vals = {
                            "name": confid.name,
                            "state": "success",
                            "field_type": "attachment",
                            "error": "%s Attachment Imported Successfully" %(count - failed),
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
                except Exception as ex:
                        print(f"Invalid chunk encoding {str(ex)}")

    def import_ir_attachment_cron(self):
        confid = self.env['sh.import.base'].search([],limit=1)
        confid.import_attach_from_queue()
        # if confid.import_attachment:
        #     confid.current_import_page_attachment += 1
        #     response = requests.get('%s/api/public/ir.attachment?query={*}&filter=[["res_model", "=", "blog.post"],["res_id", "=", 30]]&page_size=%s&page=%s' %(confid.base_url,confid.records_per_page_attachment,confid.current_import_page_attachment))           
        #     print("\n\n======response",response)
        #     response_json = response.json()
        #     print("\n\n===response_json",response_json)
        #     if response.status_code == 200:
        #         if 'count' in response_json:
        #             if confid.records_per_page_attachment != response_json['count']:
        #                 confid.import_attachment = False
        #                 confid.current_import_page_attachment = 0
        #         count = 0
        #         failed = 0                
        #         for data in response_json['result']:
        #             attchment_vals = confid.process_attchment_data(data)                    
        #             domain = [('remote_ir_attachment_id', '=', data['id'])]
        #             attachment_obj = self.env['ir.attachment'].search(domain,limit=1) 
        #             print("\n\n\nattchment find object",attachment_obj)
        #             if attachment_obj:
        #                 count += 1 
        #                 attachment_obj = self.env['ir.attachment'].write(attchment_vals)
        #             else:
        #                 # try:
        #                 # if 'res_id' in attchment_vals:
        #                 print("\n\n111111",attchment_vals)
        #                 count += 1 
        #                 attachment_obj = self.env['ir.attachment'].create(attchment_vals) 
        #                 print("==== attachment_obj",attachment_obj)    
        #                 # else:
        #                 #     print("\nn\====attchment_vals==",attchment_vals)                          
        #                 # except Exception as e:                    
        #                 #     failed += 1
        #                 #     vals = {
        #                 #         "name": data['id'],
        #                 #         "error": e,
        #                 #         "import_json" : data,
        #                 #         "field_type": "attachment",                           
        #                 #         "datetime": datetime.now(),
        #                 #         "base_config_id": confid.id,
        #                 #     }
        #                 #     self.env['sh.import.failed'].create(vals)               
        #         if count > 0:              
        #             vals = {
        #                 "name": confid.name,
        #                 "state": "success",
        #                 "field_type": "attachment",
        #                 "error": "%s Attachment Imported Successfully" %(count - failed),
        #                 "datetime": datetime.now(),
        #                 "base_config_id": confid.id,
        #                 "operation": "import"
        #             }
        #             self.env['sh.import.base.log'].create(vals)                   
        #         if failed > 0:
        #             vals = {
        #                 "name": confid.name,
        #                 "state": "error",
        #                 "field_type": "attachment",
        #                 "error": "%s Failed To Import" %(failed),
        #                 "datetime": datetime.now(),
        #                 "base_config_id": confid.id,
        #                 "operation": "import"
        #             }
        #             self.env['sh.import.base.log'].create(vals)

        #     else:
        #         vals = {
        #             "name": confid.name,
        #             "state": "error",
        #             "field_type": "attachment",
        #             "error": response.text,
        #             "datetime": datetime.now(),
        #             "base_config_id": confid.id,
        #             "operation": "import"
        #         }
        #         self.env['sh.import.base.log'].create(vals)

                           
    def process_attchment_data(self,data):
        ''' 
            PREPARE ONE2MANY VALUES FOR ATTACHMENT CONNECTED TO 
            CHATTER OR TASK , TICKET
        '''                
        attchment_vals={
            'remote_ir_attachment_id':data.get('id'),
            # 'access_token':data.get('access_token'),
            # 'checksum':data.get('checksum'),
            # 'datas':data.get('datas_fname'),
            'description':data.get('description'),
            # 'file_size':data.get('file_size'),
            # 'index_content':data.get('index_content'),
            # 'local_url':data.get('local_url'),
            # 'mimetype':data.get('mimetype'),
            'name':data.get('name'),
            'public':data.get('public'),
            # 'res_field':data.get('res_field'),
            'res_model':data.get('res_model'),
            # 'res_name':data.get('res_name'),
            # 'store_fname':data.get('store_fname'),
            'type':data.get('type').get('sh_api_current_state'),  
            # 'url':data.get('url'),
            'datas':data.get('datas').encode(),
            # 'db_datas':data.get('db_datas'),
            'company_id':1,
            # 'res_id' :1,
        }   
        print("\n=========data.get('res_model')",data.get('res_model'))     
        if data.get('res_model'):
            model_name= data.get('res_model')
            field_name="remote_%s_id"%(data.get('res_model').replace(".", "_"))
            if data.get('res_model') =='helpdesk.ticket':
                attchment_vals['res_model'] = 'sh.helpdesk.ticket'
                model_name = 'sh.helpdesk.ticket'
                field_name="remote_sh_%s_id"%(data.get('res_model').replace(".", "_"))  
            if data.get('res_model') =='account.invoice':
                model_name = 'account.move'
                field_name="remote_account_move_id"
            if data.get('res_model') =='account.invoice.line':
                model_name = 'account.move.line'
            data['res_model']=model_name

            checked_field = self.env['ir.model.fields'].sudo().search([('name','=',field_name)])
            print("\n\n======checked_field",checked_field)
            if checked_field and data.get('res_id'):
                print("======checked_field=",checked_field,data.get('id'))
                print("======model_name=",model_name)
                print("======field_name=",field_name)
                res_id_find =self.env[model_name].sudo().search([(field_name,'=',data.get('res_id'))])               
                if res_id_find:
                    print("====res_id_find",res_id_find)
                    attchment_vals.update({
                        'res_id':res_id_find.id,
                    })
        # print("n\n\n",attchment_vals)
        return attchment_vals               
