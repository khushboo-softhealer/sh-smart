# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
from datetime import datetime
import requests
import json

class ImportTask(models.Model):
    _inherit = "sh.import.base"
    

    import_link_task_product=fields.Boolean("Link Task Product")
    records_per_task_product = fields.Integer("No of Task Product per Page")
    current_import_page_task_product = fields.Integer("Current Task Product Page",default=0) 
    sh_task_ids = fields.Char("Tasks")

    def link_task_product_cron(self):
        ''' ========== Import Projects Task ============ '''
        
        confid = self.env['sh.import.base'].search([],limit=1)
        if confid.import_link_task_product:
            confid.current_import_page_task_product += 1
            # response = requests.get('''%s/api/public/project.task?query={id,sh_ticket_ids,parent_id,sh_product_id{id,related_sub_task},message_follower_ids{*},product_template_id{id,related_task}}&page_size=%s&page=%s&filter=[["company_id","=",1]]''' %(confid.base_url,confid.records_per_task_product,confid.current_import_page_task_product))
            
            response = requests.get('''%s/api/public/project.task?query={id,account_invoice_id,sh_ticket_ids,parent_id,sh_product_id{id,related_sub_task},message_follower_ids{*},product_template_id{id,related_task}}&page_size=%s&page=%s&filter=[["company_id","=",1]]''' %(confid.base_url,confid.records_per_task_product,confid.current_import_page_task_product))


            response_json = response.json()
            if response.status_code==200:
                # if 'count' in response_json and confid.records_per_page_task != response_json['count'] : 
                #     confid.import_link_task_product = False
                #     confid.current_import_page_task = 0
                count = 0
                failed = 0
                print("\n\n===response_json['result']",response_json['result'])
                for data in response_json['result']:
                    if data.get('id') and data.get('id')!=0 :
                        if data.get('sh_product_id') or data.get('product_template_id') or data.get('message_follower_ids') or data.get('sh_ticket_ids') or data.get('parent_id'):

                            followers_list=[]
                            if data.get('message_follower_ids'):
                                for follower in data.get('message_follower_ids'):
                                    if follower.get('partner_id'):
                                        domain = [('remote_res_partner_id', '=', follower.get('partner_id'))]
                                        find_customer = self.env['res.partner'].search(domain)
                                        if find_customer:
                                            followers_list.append(find_customer.id)
                                

                            domain = [('remote_project_task_id', '=', data['id'])]
                            find_task = self.env['project.task'].search(domain)
                            if followers_list:
                                find_task.message_subscribe(partner_ids=[partner
                                    for partner in followers_list
                                    if partner not in find_task.sudo().message_partner_ids.ids])


                            find_product_variant=False
                            find_product_template=False
                            if data.get('sh_product_id') and data.get('sh_product_id').get('id') and data.get('sh_product_id').get('id')!=0:
                                find_product_variant=self.env['product.product'].search([('remote_product_product_id','=',data.get('sh_product_id').get('id'))])
                                find_variant_task=self.env['project.task'].search([('remote_project_task_id','=',data.get('sh_product_id').get('related_sub_task'))])
                                if find_product_variant:
                                    print("========link ===== 2 ======")
                                    find_task.write({
                                        'sh_product_id':find_product_variant.id,
                                    })
                                    if find_variant_task:
                                        find_product_variant.write({
                                            # 'related_task':find_task.id,
                                            'related_sub_task':find_variant_task.id,
                                        })
                            
                            
                            if data.get('product_template_id'):
                                find_product_template=self.env['product.template'].search([('remote_product_template_id','=',data.get('product_template_id'))])
                                find_parent_task=self.env['project.task'].search([('remote_project_task_id','=',data.get('product_template_id').get('related_task'))])
                                if find_product_template:
                                    print("========link ===== 1 ======")
                                    find_task.write({
                                        'product_template_id':find_product_template.id,
                                    })
                                    if find_parent_task:
                                        find_product_template.write({
                                            'related_task':find_parent_task.id,
                                        })  
                                
                           
                            
                            # try:
                            print("=====find_product_template===",find_product_template)
                            print("=====find_product_variant===",find_product_variant)
                            if find_task:
                                if data.get('account_invoice_id') and  data.get('account_invoice_id')!=0:
                                    domain=[('remote_account_move_id','=',data.get('account_invoice_id'))]
                                    find_account_move_line = self.env['account.move'].search(domain)
                                    if find_account_move_line:
                                        find_task.account_move_id=find_account_move_line.id





                                # if find_product_template:
                                #     print("========link ===== 1 ======")
                                #     find_task.write({
                                #         'product_template_id':find_product_template.id,
                                #     })
                                #     find_product_template.write({
                                #         'related_task':find_task.id,
                                #     })  
                                # if find_product_variant:
                                #     print("========link ===== 2 ======")
                                #     find_task.write({
                                #         'sh_product_id':find_product_variant.id,
                                #     })
                                #     find_product_variant.write({
                                #         # 'related_task':find_task.id,
                                #         'related_sub_task':find_task.id,
                                #     })  

                                if data.get('sh_ticket_ids'):
                                    sh_ticket_list=[]
                                    for ticket in data.get('sh_ticket_ids'):
                                        domain=[('remote_sh_helpdesk_ticket_id','=',ticket)]
                                        find_ticket = self.env['sh.helpdesk.ticket'].search(domain)
                                        if find_ticket:
                                            sh_ticket_list.append(find_ticket.id)
                                    if sh_ticket_list:
                                        find_task.write({
                                            'sh_ticket_ids':[(6,0,sh_ticket_list)]
                                        })
                                if data.get('parent_id'):
                                    domain = [('remote_project_task_id', '=', data.get('parent_id'))]
                                    related_task = self.env['project.task'].search(domain)
                                    if related_task:
                                        find_task.write({
                                            'parent_id':related_task.id
                                        })

                        count += 1
                    
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
                        "field_type": "task",
                        "error": "%s Task Line with Product Successfully" %(count - failed),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
                if failed > 0:
                    vals = {
                        "name": confid.name,
                        "state": "error",
                        "field_type": "task",
                        "error": "%s Failed To Link" %(failed),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)

            else:
                vals = {
                    "name": confid.name,
                    "state": "error",
                    "field_type": "task",
                    "error": response.text,
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)  
                

    def link_task_product_from_queue(self):
        ''' ========== Import Projects Task ============ '''
        
        confid = self.env['sh.import.base'].search([],limit=1)
        if confid.import_link_task_product and confid.sh_task_ids:
            sh_task_ids = confid.sh_task_ids.strip('][').split(', ')  
            for task in sh_task_ids[0:300]:
                # confid.current_import_page_task_product += 1
                response = requests.get('''%s/api/public/project.task/%s?query={id,account_invoice_id,timesheet_ids,sh_ticket_ids,parent_id,sh_product_id{id,related_sub_task},message_follower_ids{*},product_template_id{id,related_task}}''' %(confid.base_url,task))
                response_json = response.json()
                if response.status_code==200:
                    # if 'count' in response_json and confid.records_per_page_task != response_json['count'] : 
                    #     confid.import_link_task_product = False
                    #     confid.current_import_page_task = 0
                    count = 0
                    failed = 0
                    print("\n\n===response_json['result']",response_json['result'])
                    for data in response_json['result']:
                        if data.get('id') and data.get('id')!=0 :
                            if data.get('sh_product_id') or data.get('product_template_id') or data.get('message_follower_ids') or data.get('sh_ticket_ids') or data.get('parent_id')  or data.get('timesheet_ids') :

                                followers_list=[]
                                if data.get('message_follower_ids'):
                                    for follower in data.get('message_follower_ids'):
                                        if follower.get('partner_id'):
                                            domain = [('remote_res_partner_id', '=', follower.get('partner_id'))]
                                            find_customer = self.env['res.partner'].search(domain)
                                            if find_customer:
                                                followers_list.append(find_customer.id)
                                    

                                domain = [('remote_project_task_id', '=', data['id'])]
                                find_task = self.env['project.task'].search(domain)
                                if followers_list:
                                    find_task.message_subscribe(partner_ids=[partner
                                        for partner in followers_list
                                        if partner not in find_task.sudo().message_partner_ids.ids])



                                find_product_variant=False
                                find_product_template=False
                                if data.get('sh_product_id') and data.get('sh_product_id').get('id') and data.get('sh_product_id').get('id')!=0:
                                    find_product_variant=self.env['product.product'].search([('remote_product_product_id','=',data.get('sh_product_id').get('id'))])
                                    find_variant_task=self.env['project.task'].search([('remote_project_task_id','=',data.get('sh_product_id').get('related_sub_task'))])
                                    if find_product_variant:
                                        print("========link ===== 2 ======")
                                        find_task.write({
                                            'sh_product_id':find_product_variant.id,
                                        })
                                        if find_variant_task:
                                            find_product_variant.write({
                                                # 'related_task':find_task.id,
                                                'related_sub_task':find_variant_task.id,
                                            })
                                
                                
                                if data.get('product_template_id'):
                                    find_product_template=self.env['product.template'].search([('remote_product_template_id','=',data.get('product_template_id'))])
                                    find_parent_task=self.env['project.task'].search([('remote_project_task_id','=',data.get('product_template_id').get('related_task'))])
                                    if find_product_template:
                                        print("========link ===== 1 ======")
                                        find_task.write({
                                            'product_template_id':find_product_template.id,
                                        })
                                        if find_parent_task:
                                            find_product_template.write({
                                                'related_task':find_parent_task.id,
                                            })  
                                    
                                
                                
                                # try:
                                print("=====find_product_template===",find_product_template)
                                print("=====find_product_variant===",find_product_variant)
                                if find_task:
                                    if data.get('account_invoice_id') and data.get('account_invoice_id')!=0:
                                        domain=[('remote_account_move_id','=',data.get('account_invoice_id'))]
                                        find_account_move_line = self.env['account.move'].search(domain)
                                        if find_account_move_line:
                                            find_task.account_move_id=find_account_move_line.id

                                    # if find_product_template:
                                    #     print("========link ===== 1 ======")
                                    #     find_task.write({
                                    #         'product_template_id':find_product_template.id,
                                    #     })
                                    #     find_product_template.write({
                                    #         'related_task':find_task.id,
                                    #     })  
                                    # if find_product_variant:
                                    #     print("========link ===== 2 ======")
                                    #     find_task.write({
                                    #         'sh_product_id':find_product_variant.id,
                                    #     })
                                    #     find_product_variant.write({
                                    #         # 'related_task':find_task.id,
                                    #         'related_sub_task':find_task.id,
                                    #     })  

                                    if data.get('sh_ticket_ids'):
                                        sh_ticket_list=[]
                                        for ticket in data.get('sh_ticket_ids'):
                                            domain=[('remote_sh_helpdesk_ticket_id','=',ticket)]
                                            find_ticket = self.env['sh.helpdesk.ticket'].search(domain)
                                            if find_ticket:
                                                sh_ticket_list.append(find_ticket.id)
                                        if sh_ticket_list:
                                            find_task.write({
                                                'sh_ticket_ids':[(6,0,sh_ticket_list)]
                                            })
                                    if data.get('parent_id'):
                                        domain = [('remote_project_task_id', '=', data.get('parent_id'))]
                                        related_task = self.env['project.task'].search(domain)
                                        if related_task:
                                            find_task.write({
                                                'parent_id':related_task.id
                                            })  

                            count += 1
                        
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
            confid.sh_task_ids='['+', '.join([str(elem) for elem in sh_task_ids[30:]])+']'        
            if count > 0:              
                vals = {
                    "name": confid.name,
                    "state": "success",
                    "field_type": "task",
                    "error": "%s Task Line with Product Successfully" %(count - failed),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)
            if failed > 0:
                vals = {
                    "name": confid.name,
                    "state": "error",
                    "field_type": "task",
                    "error": "%s Failed To Link" %(failed),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)

    