# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
from datetime import datetime
import requests
import json

class Importproduct(models.Model):
    _inherit = "sh.import.base"

    import_product_link=fields.Boolean("Link Products")
    records_per_product_link = fields.Integer("No of Product per Page")
    current_import_page_product_link = fields.Integer("Current Product Page",default=0) 
    sh_products_ids = fields.Char("Tasks")

    def link_products_cron(self):
        ''' ========== Import Projects Task ============ '''
        
        confid = self.env['sh.import.base'].search([],limit=1)
        if confid.import_product_link:
            confid.current_import_page_product_link += 1
            # response = requests.get('''%s/api/public/product.product?query={id,image_medium,alternative_product_ids,individual_modules,optional_product_ids,accessory_product_ids,
            # product_variant_id,product_variant_ids}&page_size=%s&page=%s&filter=[["company_id","=",1]]''' 
            #     %(confid.base_url,confid.records_per_product_link,confid.current_import_page_product_link))
            # response = requests.get('''%s/api/public/product.product?query={id,sh_blog_post_ids}&page_size=%s&page=%s&filter=[["company_id","=",1]]''' 
            #     %(confid.base_url,confid.records_per_product_link,confid.current_import_page_product_link))
            # response_json = response.json()
            response = requests.get('''%s/api/public/product.template?query={id,image}&page_size=%s&page=%s&filter=[["company_id","=",1]]''' 
                %(confid.base_url,confid.records_per_product_link,confid.current_import_page_product_link))
            response_json = response.json()
            # print("\n\nn--------response_json",response_json)
            if response.status_code==200:
    
                count = 0
                failed = 0
                print("\n\n===response_json['result']",response_json['result'])
                updated_product=[]
                for data in response_json['result']:
                    count+=1
                    if data.get('id') and data.get('id')!=0 :
                        find_pro_tmpl=self.env['product.template'].search([('remote_product_template_id','=',data.get('id'))])
                        if find_pro_tmpl and data.get('image'):
                            updated_product.append(find_pro_tmpl.id)
                            find_pro_tmpl.write({
                                'image_1920':data.get('image'),
                            })

                        # find_product=self.env['product.product'].search([('remote_product_product_id','=',data.get('id'))],limit=1)
                        
                        # if find_product and data.get('sh_blog_post_ids'):
                        #     blog_list=[]
                        #     for blog in data.get('sh_blog_post_ids'):
                        #         find_blog=self.env['blog.post'].browse(blog)
                        #         if find_blog:
                        #             blog_list.append(find_blog.id)
                        #     if blog_list:
                        #         find_product.write({'sh_blog_post_ids':[(6,0,blog_list)]})
                        
                        
                        # print("\n\==============data",data)
                        # alternative_product=[]
                        # if data.get('alternative_product_ids'):
                        #     for product in data.get('alternative_product_ids'):
                        #         find_product_tmpl=self.env['product.template'].search([('remote_product_template_id','=',product)],limit=1) 
                        #         if find_product_tmpl:
                        #             alternative_product.append(find_product_tmpl.id)  
                        # individual_modules=[]
                        # if data.get('individual_modules'):
                        #     for product in data.get('individual_modules'):
                        #         find_product_tmpl=self.env['product.template'].search([('remote_product_template_id','=',product)],limit=1) 
                        #         if find_product_tmpl:
                        #             individual_modules.append(find_product_tmpl.id) 

                        # optional_product_ids=[]
                        # if data.get('optional_product_ids'):
                        #     for product in data.get('optional_product_ids'):
                        #         find_product_tmpl=self.env['product.template'].search([('remote_product_template_id','=',product)],limit=1) 
                        #         if find_product_tmpl:
                        #             optional_product_ids.append(find_product_tmpl.id) 

                        # accessory_product_ids=[]
                        # if data.get('accessory_product_ids'):
                        #     for product in data.get('accessory_product_ids'):
                        #         find_product_var=self.env['product.product'].search([('remote_product_product_id','=',product)],limit=1) 
                        #         if find_product_var:
                        #             accessory_product_ids.append(find_product_var.id)  
                        
                        # variant_id=False
                        # if data.get('product_variant_id'):
                        #     variant_id=self.env['product.product'].search([('remote_product_product_id','=',data.get('product_variant_id'))],limit=1) 

                        # product_variant_ids=[]
                        # if data.get('product_variant_ids'):
                        #     for product in data.get('product_variant_ids'):
                        #         find_product_var=self.env['product.product'].search([('remote_product_product_id','=',product)],limit=1) 
                        #         if find_product_var:
                        #             product_variant_ids.append(find_product_var.id)  

                        # valid_archived_variant_ids=[]
                        # if data.get('valid_archived_variant_ids'):
                        #     for product in data.get('valid_archived_variant_ids'):
                        #         find_product_var=self.env['product.product'].search([('remote_product_product_id','=',product)],limit=1) 
                        #         if find_product_var:
                        #             valid_archived_variant_ids.append(find_product_var.id)  

                        # valid_existing_variant_ids=[]
                        # if data.get('valid_existing_variant_ids'):
                        #     for product in data.get('valid_existing_variant_ids'):
                        #         find_product_var=self.env['product.product'].search([('remote_product_product_id','=',product)],limit=1) 
                        #         if find_product_var:
                        #             valid_existing_variant_ids.append(find_product_var.id)  


                        # vals={
                        #     'alternative_product_ids': alternative_product,  
                        #     'individual_modules':individual_modules,
                        #     'optional_product_ids':optional_product_ids,
                        #     'accessory_product_ids':accessory_product_ids,
                        #     'image_1920':data.get('image_medium') ,
                        #     # 'product_variant_ids':product_variant_ids,
                        #     # 'valid_archived_variant_ids':valid_archived_variant_ids,
                        #     # 'valid_existing_variant_ids':valid_existing_variant_ids,
                        #     # 'product_variant_id':variant_id.id,
                        # }
                        # find_product.write(vals)

                    
                    # except Exception as e:
                    #     failed += 1
                    #     vals = {
                    #         "name": data['id'],
                    #         "error": e,
                    #         "import_json" : data,
                    #         "field_type": "task",                           
                    #         "datetime": datetime.now(),
                    #         "base_config_id": confid.id,
                    #     }
                    #     self.env['sh.import.failed'].create(vals) 
                    
                if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "product",
                        "error": "%s Product Update Successfully" %(updated_product),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
                if failed > 0:
                    vals = {
                        "name": confid.name,
                        "state": "error",
                        "field_type": "product",
                        "error": "%s Product Not Update" %(failed),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)

            else:
                vals = {
                    "name": confid.name,
                    "state": "error",
                    "field_type": "product",
                    "error": response.text,
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)  
                