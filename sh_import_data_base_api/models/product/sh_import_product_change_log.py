# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
import requests
import json
from datetime import datetime

class InheritImportBase(models.Model):
    _inherit = "sh.import.base"
    
    import_product_change_log = fields.Boolean("Import Products Change Log")    
    change_log_ids=fields.Char("Changes Logs")


    def update_change_log(self):
            config = self.env['sh.import.base'].search([],limit=1)
            if config.import_product_change_log:
                logs = config.change_log_ids.strip('][').split(', ')
                count=0
                failed=0           
                for log in logs[0:200]:
                    response = requests.get('%s/api/public/product.change.log/%s?query={*}'%(config.base_url,log))            
                    if response.status_code == 200:
                        response_json = response.json()
                        if 'count' in response_json:
                            if config.records_per_page != response_json['count']:
                                config.import_product = False
                                config.current_import_page = 0
                        for data in response_json['result']:
                            # try:                              
                            if data['id'] != 0 and data['product_variant_id']!=False:
                                created_log = self.env['product.change.log'].search([('remote_product_change_log_id','=',data['id'])])
                                if created_log:                                    
                                    count += 1
                                else:
                                    obj =self.env['product.product'].sudo().search([('remote_product_product_id','=',data['product_variant_id'])])                                    
                                    if obj:
                                        vals={}
                                        vals.update({
                                            'remote_product_change_log_id':data['id'],
                                            'product_variant_id':obj.id,                                
                                            'log_type':data['log_type']['sh_api_current_state'],
                                            'version':data['version'],
                                            'details':data['details']
                                        })
                                        if data['date']:
                                            vals.update({
                                                'date':data['date'],
                                            })
                                        log =self.env['product.change.log'].create(vals)
                                        count += 1                                                               
                            

                            elif data['id'] != 0 and data['product_id']!=False:
                                created_log = self.env['product.change.log'].search([('remote_product_change_log_id','=',data['id'])])
                                if created_log:                                   
                                    count += 1
                                else:
                                    obj =self.env['product.template'].sudo().search([('remote_product_template_id','=',data['product_id'])])                                    
                                    if obj:
                                        vals={}
                                        vals.update({
                                            'remote_product_change_log_id':data['id'],
                                            'product_id':obj.id,                                
                                            'log_type':data['log_type']['sh_api_current_state'],
                                            'version':data['version'],
                                            'details':data['details']
                                        })
                                        if data['date']:
                                            vals.update({
                                                'date':data['date'],
                                            })
                                        log =self.env['product.change.log'].create(vals)
                                        count += 1                                                              
                            # except Exception as e:                    
                            #     failed += 1
                            #     vals = {
                            #         "name": data['id'],
                            #         "error": e,
                            #         "import_json" : data,
                            #         "field_type": "product",                           
                            #         "datetime": datetime.now(),
                            #         "base_config_id": config.id,
                            #     }
                            #     self.env['sh.import.failed'].create(vals) 
                config.change_log_ids='['+', '.join([str(elem) for elem in logs[200:]])+']' 
                if count > 0:              
                    vals = {
                        "name": config.name,
                        "state": "success",
                        "field_type": "product",
                        "error": "%s Product Change Log Successfully" %(count - failed),
                        "datetime": datetime.now(),
                        "base_config_id": config.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)                   
                if failed > 0:
                    vals = {
                        "name": config.name,
                        "state": "error",
                        "field_type": "product",
                        "error": "%s Failed To Import" %(failed),
                        "datetime": datetime.now(),
                        "base_config_id": config.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)

                # else:
                #     vals = {
                #         "name": config.name,
                #         "state": "error",
                #         "field_type": "product",
                #         "error": response.text,
                #         "datetime": datetime.now(),
                #         "base_config_id": config.id,
                #         "operation": "import"
                #     }
                #     self.env['sh.import.base.log'].create(vals)
                                    