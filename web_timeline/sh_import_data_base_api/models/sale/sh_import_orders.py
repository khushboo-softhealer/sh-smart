# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
import requests
import json
from datetime import datetime
import time
import logging
_logger = logging.getLogger(__name__)

class InheritImportBase(models.Model):
    _inherit = "sh.import.base"
    
    import_order=fields.Boolean("Import Orders")
    records_per_page_so = fields.Integer("No of records per page(SO)")
    current_import_page_so = fields.Integer("Current Page(SO)",default=0) 
    sh_import_filter_order=fields.Boolean("Import Filtered Orders")  
    sh_from_date=fields.Datetime("From Date(SO)")
    sh_to_date=fields.Datetime("To Date(SO)") 
    sh_import_order_ids=fields.Char("Order ids")
    
    def import_order_filtered_to_queue(self):
        ''' ========== Import Filtered Ordered 
        between from date and end date ==================  ''' 
        confid = self.env['sh.import.base'].search([],limit=1)  
        if confid.sh_import_filter_order:
            response = requests.get('''%s/api/public/sale.order?query={id,write_date}&filter=[["write_date",">=","%s"],["write_date","<=","%s"],["company_id","=",1]]''' 
                %(confid.base_url,str(confid.sh_from_date),str(confid.sh_to_date)))
            response_json = response.json()
            if response_json.get('result'):
                confid.sh_import_order_ids=[r['id'] for r in response_json.get('result')]
    
    def find_missing_order(self):
        # all_orders = self.env['sh.attendance.modification.request'].search([]).mapped('remote_sh_attendance_modification_request_id')
        # confid = self.env['sh.import.base'].search([],limit=1)
        # response = requests.get(f'''%s/api/public/sh.attendance.modification.request?missing=%s''' 
        #         %(confid.base_url,all_orders))
        # response_json = response.json()
        # if 'result' in response_json:
        #     self.sh_import_attendance_ids = response_json['result']


        # all_users = self.env['res.users'].search([]).mapped('remote_res_user_id')
        # print("\n\n=====all_users",all_users)
        # confid = self.env['sh.import.base'].search([],limit=1)
        # response = requests.get(f'''%s/api/public/res.users?missing=%s''' 
        #     %(confid.base_url,all_users))
        # response_json = response.json()
        # print("\n\n==response_json",response_json)
        # if 'result' in response_json:
        #     self.users = response_json['result']


        all_applications = self.env['hr.applicant'].search([]).filtered(lambda p: p.remote_hr_applicant_id ).mapped('remote_hr_applicant_id')
        print("all_applications",all_applications, len(all_applications))
        confid = self.env['sh.import.base'].search([],limit=1)
        response = requests.get(f'''%s/api/public/hr.applicant?missing=%s''' 
                %(confid.base_url,all_applications))
        response_json = response.json()
        if 'result' in response_json:
            self.application_ids = response_json['result']

        # all_orders = self.env['sale.order.line'].search([]).mapped('remote_sale_order_line_id')
        # confid = self.env['sh.import.base'].search([],limit=1)
        # response = requests.get(f'''%s/api/public/sale.order.line?missing=%s''' 
        #         %(confid.base_url,all_orders))
        # response_json = response.json()
        # if 'result' in response_json:
        #     self.sh_import_order_ids = response_json['result']


        # all_orders = self.env['sh.helpdesk.ticket'].search([]).mapped('remote_sh_helpdesk_ticket_id')
        # confid = self.env['sh.import.base'].search([],limit=1)
        # response = requests.get(f'''%s/api/public/helpdesk.ticket?missing=%s''' 
        #         %(confid.base_url,all_orders))
        # response_json = response.json()
        # if 'result' in response_json:
        #     self.sh_import_ticket_ids = response_json['result']


        # all_contact = self.env['res.partner'].search([]).mapped('remote_res_partner_id')
        # confid = self.env['sh.import.base'].search([],limit=1)
        # response = requests.get(f'''%s/api/public/res.partner?missing=%s''' 
        #     %(confid.base_url,all_contact))
        # response_json = response.json()
        # print("\n\n==response_json",response_json)
        # if 'result' in response_json:
        #     self.sh_import_partner_ids = response_json['result']

        # all_product = self.env['product.template'].search([('remote_product_template_id','!=','')]).mapped('remote_product_template_id')
        # confid = self.env['sh.import.base'].search([],limit=1)
        # response = requests.get(f'''%s/api/public/product.template?missing=%s''' 
        #     %(confid.base_url,all_product))
        # response_json = response.json()
        # print("\n\n==response_json",response_json)
        # if 'result' in response_json:
        #     self.sh_import_product_ids = response_json['result']

        # all_users = self.env['hr.employee'].search([]).mapped('remote_hr_employee_id')
        # confid = self.env['sh.import.base'].search([],limit=1)
        # response = requests.get(f'''%s/api/public/hr.employee?missing=%s''' 
        #     %(confid.base_url,all_users))
        # response_json = response.json()
        # print("\n\n==response_json",response_json)
        # if 'result' in response_json:
        #     self.sh_employees = response_json['result']



        # users = self.env['crm.lead'].search([]).mapped('remote_crm_lead_id')
        # confid = self.env['sh.import.base'].search([],limit=1)
        # response = requests.get(f'''%s/api/public/crm.lead?missing=%s''' 
        #         %(confid.base_url,users))
        # response_json = response.json()
        # if 'result' in response_json:
        #     self.sh_import_crm_ids = response_json['result']

        # changes_log = self.env['product.change.log'].search([]).mapped('remote_product_change_log_id')
        # confid = self.env['sh.import.base'].search([],limit=1)
        # response = requests.get(f'''%s/api/public/product.change.log?missing=%s''' 
        #         %(confid.base_url,changes_log))
        # response_json = response.json()
        # if 'result' in response_json:
        #     self.change_log_ids = response_json['result']

        # all_invoice = self.env['account.move'].search([]).mapped('remote_account_move_id')
        # confid = self.env['sh.import.base'].search([],limit=1)
        # response = requests.get(f'''%s/api/public/account.invoice?missing=%s''' 
        #     %(confid.base_url,all_invoice))
        # response_json = response.json()
        # if 'result' in response_json:
        #     self.invoice_ids = response_json['result']
        
        # all_payment = self.env['account.payment'].search([]).mapped('remote_account_payment_id')
        # confid = self.env['sh.import.base'].search([],limit=1)
        # response = requests.get(f'''%s/api/public/account.payment?missing=%s''' 
        #     %(confid.base_url,all_payment))
        # response_json = response.json()
        # if 'result' in response_json:
        #     self.payment_ids = response_json['result']

        # all_task = self.env['project.task'].search([]).mapped('remote_project_task_id')
        # confid = self.env['sh.import.base'].search([],limit=1)
        # response = requests.get(f'''%s/api/public/project.task?missing=%s''' 
        #     %(confid.base_url,all_task))
        # response_json = response.json()
        # if 'result' in response_json:
        #     self.sh_import_task_ids = response_json['result']

        # all_messages = self.env['mail.message'].search([]).mapped('remote_mail_message_id')
        # confid = self.env['sh.import.base'].search([],limit=1)
        # response = requests.get(f'''%s/api/public/mail.message?missing=%s''' 
        #     %(confid.base_url,all_messages))
        # response_json = response.json()
        # if 'result' in response_json:
        #     self.message_ids = response_json['result']


        # all_product = self.env['product.product'].search([]).mapped('remote_product_product_id')
        # confid = self.env['sh.import.base'].search([],limit=1)
        # response = requests.get(f'''%s/api/public/product.product?missing=%s''' 
        #     %(confid.base_url,all_product))
        # response_json = response.json()
        # if 'result' in response_json:
        #     self.sh_import_product_ids = response_json['result']
        # print("n\n\n123123")
        # all_leave = self.env['ir.attachment'].search([]).mapped('remote_ir_attachment_id')
        # confid = self.env['sh.import.base'].search([],limit=1)
        # response = requests.get(f'''%s/api/public/ir.attachment?missing=%s''' 
        #     %(confid.base_url,all_leave))
        # response_json = response.json()
        # if 'result' in response_json:
        #     self.sh_import_attachment_ids = response_json['result']

        # all_timesheet = self.env['account.analytic.line'].search([]).mapped('remote_account_analytic_line_id')
        # confid = self.env['sh.import.base'].search([],limit=1)
        # response = requests.get(f'''%s/api/public/account.analytic.line?missing=%s''' 
        #     %(confid.base_url,all_timesheet))
        # response_json = response.json()
        # if 'result' in response_json:
        #     self.timesheet_ids = response_json['result']
        

    def import_sale_order_missing_fields(self):
        confid = self.env['sh.import.base'].search([],limit=1)  
        if confid.import_order:
            confid.current_import_page_so += 1
            response = requests.get('''%s/api/public/sale.order?query={id,timeline,odoo_version,estimated_hrs}&page_size=%s&page=%s&filter=["|",["odoo_version","!=",False],["estimated_hrs",">",0]]''' 
                %(confid.base_url,confid.records_per_page_so,confid.current_import_page_so))
            count=0
            failed=0
            response_json = response.json()
            if response_json.get('count') and confid.records_per_page_so != response_json['count']:
                confid.import_order = False
                confid.current_import_page_so = 0
            if response_json.get('result'):
                _logger.info("response_json['result']", response_json['result'])
                for data in response_json['result']:
                    domain = [('remote_sale_order_id', '=', data['id'])]
                    find_order = self.env['sale.order'].search(domain)
                    if find_order:
                        count+=1
                        _logger.info('find_order', find_order)
                        if data.get('odoo_version'):
                            domain=[('remote_sh_version_id','=',data.get('odoo_version'))]
                            find_version=self.env['sh.version'].search(domain)
                            if find_version:
                                query = """
                                    UPDATE sale_order
                                        SET odoo_version = %s WHERE id = %s
                                """
                                self.env.cr.execute(query, [find_version.id,find_order.id])
                        if data.get('timeline') and data.get('estimated_hrs'):
                            query = """
                                UPDATE sale_order
                                    SET timeline = %s , estimated_hrs = %s WHERE id = %s
                            """
                            self.env.cr.execute(query, [data.get('timeline'),data.get('estimated_hrs'),find_order.id])
                        elif data.get('timeline'):
                            query = """
                                UPDATE sale_order
                                    SET timeline = %s WHERE id = %s
                            """
                            self.env.cr.execute(query, [data.get('timeline'),find_order.id])
                        elif data.get('estimated_hrs'):
                            query = """
                                UPDATE sale_order
                                    SET estimated_hrs = %s WHERE id = %s
                            """
                            self.env.cr.execute(query, [data.get('estimated_hrs'),find_order.id])

                        _logger.info('Updated Order', find_order)
                    else:
                        _logger.info('Not Updated Order', find_order)
                        failed+=1
                if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "order",
                        "error": "%s Order Update Successfully" %(count - failed),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
                   
                if failed > 0:
                    vals = {
                        "name": confid.name,
                        "state": "error",
                        "field_type": "order",
                        "error": "%s Failed Not Update Update" %(failed),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)

    def update_sale_order_missing_fields(self):
        confid = self.env['sh.import.base'].search([],limit=1)  
        if confid.sh_import_filter_order and confid.sh_import_order_ids:   
            orders = confid.sh_import_order_ids.strip('][').split(', ')
            count=0
            failed=0  
            order_count=confid.records_per_page_so
            for order in orders[0:order_count]:
                response = requests.get('''%s/api/public/sale.order/%s?query={id,timeline,odoo_version,estimated_hrs}''' 
                    %(confid.base_url,order))
                response_json = response.json()
                if response_json.get('result'):
                    _logger.info("response_json['result']", response_json['result'])
                    for data in response_json['result']:
                        domain = [('remote_sale_order_id', '=', data['id'])]
                        find_order = self.env['sale.order'].search(domain)
                        if find_order:
                            count+=1
                            _logger.info('find_order', find_order)
                            if data.get('odoo_version'):
                                domain=[('remote_sh_version_id','=',data.get('odoo_version'))]
                                find_version=self.env['sh.version'].search(domain)
                                if find_version:
                                    query = """
                                        UPDATE sale_order
                                            SET odoo_version = %s WHERE id = %s
                                    """
                                    self.env.cr.execute(query, [find_version.id,find_order.id])
                            if data.get('timeline') and data.get('estimated_hrs'):
                                query = """
                                    UPDATE sale_order
                                        SET timeline = %s , estimated_hrs = %s WHERE id = %s
                                """
                                self.env.cr.execute(query, [data.get('timeline'),data.get('estimated_hrs'),find_order.id])
                            elif data.get('timeline'):
                                query = """
                                    UPDATE sale_order
                                        SET timeline = %s WHERE id = %s
                                """
                                self.env.cr.execute(query, [data.get('timeline'),find_order.id])
                            elif data.get('estimated_hrs'):
                                query = """
                                    UPDATE sale_order
                                        SET estimated_hrs = %s WHERE id = %s
                                """
                                self.env.cr.execute(query, [data.get('estimated_hrs'),find_order.id])

                            _logger.info('Updated Order', find_order)
                        else:
                            _logger.info('Not Updated Order', find_order)
                            failed+=1
            confid.sh_import_order_ids='['+', '.join([str(elem) for elem in orders[order_count:]])+']'
            if count > 0:              
                vals = {
                    "name": confid.name,
                    "state": "success",
                    "field_type": "order",
                    "error": "%s Order Update Successfully" %(count - failed),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)
                
            if failed > 0:
                vals = {
                    "name": confid.name,
                    "state": "error",
                    "field_type": "order",
                    "error": "%s Failed Not Update Update" %(failed),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)



    def get_currency_values(self):
        confid = self.env['sh.import.base'].search([],limit=1)  
        if confid.sh_import_filter_order:
            response = requests.get('''%s/api/public/res.currency?query={id,rate,name,rate_ids{id,name,rate}}''' 
                %(confid.base_url))
            
            response_json = response.json()
            if response_json.get('result'):
                for data in response_json['result']:
                    domain=[('name','=',data.get('name'))]
                    find_currency_id=self.env['res.currency'].search(domain,limit=1)
                    find_currency_id.write({
                        'rate_ids' : False
                    })
                    for currency_rate in data['rate_ids']:
                        rate_vals = {
                            'company_rate' : currency_rate['rate'],
                            'name' : currency_rate['name'],
                            'currency_id' : find_currency_id.id
                        }
                        self.env['res.currency.rate'].create(rate_vals)
    
    def import_order_from_queue(self):   
        ''' ========== Import Sale_orders ==================  '''
        confid = self.env['sh.import.base'].search([],limit=1)
        if confid.sh_import_filter_order and confid.sh_import_order_ids:   
            orders = confid.sh_import_order_ids.strip('][').split(', ')
            count=0
            failed=0  
            for order in orders[0:20]:
                # try:
                    so_query='''%s/api/public/sale.order/%s?query={*,medium_id{*},sale_order_option_ids{*},message_ids{id,subtype_id{*},author_id,body,channel_ids{*},date,display_name,email_from,has_error,layout,mail_activity_type_id{*},message_id,message_type,model,moderation_status,moderator_id,need_moderation,needaction,no_auto_thread,notification_ids,rating_value,record_name,reply_to,res_id,starred,subject},currency_id{name},sh_replied_status_id{*},
                invoice_ids{*,user_id,currency_id{name},payment_ids{*,journal_id{id,name,type,code},currency{name},currency_of_fees{name},message_ids{id,subtype_id{*},author_id,body,channel_ids{*},date,display_name,email_from,has_error,layout,mail_activity_type_id{*},message_id,message_type,model,moderation_status,moderator_id,need_moderation,needaction,no_auto_thread,notification_ids,rating_value,record_name,reply_to,res_id,starred,subject},currency_id{name},payment_method_id{*},paypal_bank_transfer_id{*,currency_id{name},dummy_account_id{*,tag_ids{*},tax_ids{*},user_type_id{*}},journal_id{id,name,type,code},line_ids{*,tax_ids{*},account_id{*,tag_ids{*},tax_ids{*},user_type_id{*}},currency_id{name},journal_id{id,name,type,code},tax_line_id{*},
                analytic_line_ids{*}}},destination_account_id{*,tag_ids{*},tax_ids{*},user_type_id{*}},destination_journal_id{id,name,type,code},journal_id{id,name,type,code},partner_bank_account_id{*}},message_follower_ids{*},message_ids{id,subtype_id{*},author_id,body,channel_ids{*},date,display_name,email_from,has_error,layout,mail_activity_type_id{*},message_id,message_type,model,moderation_status,
                moderator_id,need_moderation,needaction,no_auto_thread,notification_ids,rating_value,record_name,reply_to,res_id,starred,subject},version_ids{*},account_id{*},journal_id{id,name,type,code},medium_id{*},partner_bank_id{*},source_id{*},
                team_id{*},invoice_line_ids{*,-product_image,product_id{id,product_tmpl_id},currency_id{name},invoice_line_tax_ids{*},account_id{*}}},opportunity_id{*,tag_ids{*},lost_reason{*},medium_id{*},
                source_id{*},stage_id{*},state_id{name,code},team_id{*},message_ids{id,subtype_id{*},author_id,body,channel_ids{*},date,display_name,email_from,has_error,layout,mail_activity_type_id{*},message_id,message_type,model,moderation_status,moderator_id,need_moderation,needaction,no_auto_thread,notification_ids,rating_value,record_name,reply_to,res_id,starred,subject}},
                sh_bank_account_id{*},sh_edition_id{*},sh_odoo_hosted_id{*,sh_edtion_id{*}},sh_partner_category_id{*},sh_replied_status_id{*},source_id{*},team_id{*},
                message_follower_ids{*},order_line{*,product_id{id,product_tmpl_id},tax_id{name,amount_type,amount,type_tax_use},currency_id{name},analytic_line_ids{*},invoice_lines{*,invoice_line_tax_ids{*},account_id{*,tag_ids{*},tax_ids{*}, user_type_id{*}},currency_id{name}},tax_id{*},product_uom{id,name,uom_type,factor,rounding,category_id{*}}}
                }''' %(confid.base_url,order)
                    response = requests.get(so_query)
                    response_json = response.json()
                    if response.status_code==200:
                        already_order=False
                        payment_list=[]
                        for data in response_json.get('result'):
                            print("\n==========",data.get('id'),data.get('name'))
                            not_import_invoice=False
                            # try:
                            domain = ['|',('remote_sale_order_id', '=', data['id']),('name', '=', data['name'])]
                            already_order = self.env['sale.order'].search(domain)
                            order_vals=self.process_order_data(data)
                            invoice_dict={}
                            if order_vals:
                                followers_list=[]
                                # if 'message_follower_ids' in order_vals:
                                #     followers_list = order_vals['message_follower_ids']
                                #     del order_vals['message_follower_ids']
                                if already_order:
                                    already_order.write(order_vals)
                                    if followers_list:
                                        already_order.message_subscribe(partner_ids=[partner
                                            for partner in followers_list
                                            if partner not in already_order.sudo().message_partner_ids.ids])
                                else:
                                    created_so=self.env['sale.order'].create(order_vals)
                                    if followers_list:
                                        created_so.message_subscribe(partner_ids=[partner
                                            for partner in followers_list
                                            if partner not in created_so.sudo().message_partner_ids.ids])
                                if data.get('invoice_ids'):
                                    for invoice in data.get('invoice_ids'):
                                        invoice_dict[str(invoice.get('id'))]=invoice.get('state').get('sh_api_current_state')

                                    invoice_list,payment_list=confid.process_invoice_data(data.get('invoice_ids'))
                                    print("\n\n=======invoice_list",invoice_list,len(invoice_list))
                                    print("\n\n=======payment_list",payment_list,len(payment_list))
                                    for invoice in invoice_list:
                                        if invoice[2]:
                                            find_invoice=self.env['account.move'].search([('remote_account_move_id','=',invoice[2].get('remote_account_move_id'))])
                                            followers_list=[]
                                            if 'message_follower_ids' in invoice[2]:
                                                followers_list = invoice[2]['message_follower_ids']
                                                del invoice[2]['message_follower_ids']
                                            
                                            if not find_invoice:
                                                created_invoice = self.env['account.move'].create(invoice[2])
                                            else: 
                                                find_invoice.write(invoice[2])
                                                created_invoice=find_invoice
                                            if followers_list:


                                                for follower in followers_list:
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
                                                                if partner not in created_invoice.sudo().message_partner_ids.ids]
                                                            # print("\n\n=======find_customer",find_customer)
                                                            # print("\nn\======part_list",part_list)
                                                            created_invoice.sudo().message_subscribe(partner_ids=part_list)
                                                            find_follower=self.env['mail.followers'].search([('partner_id','=',find_customer.id),('res_model','=','account.move'),('res_id','=',created_invoice.id)])
                                                            # print("\n\n========find_follower",find_follower)
                                                            if find_follower:
                                                                find_follower.update({
                                                                    'subtype_ids':  [(6,0,subtype_list)],
                                                                })
                                            if invoice_dict[str(created_invoice.remote_account_move_id)] in ['open','in_payment','paid']:
                                                if created_invoice.invoice_line_ids:
                                                    created_invoice.action_post()
                                            if invoice_dict[str(created_invoice.remote_account_move_id)] == 'cancel':
                                                created_invoice.write({
                                                    'state':'cancel',
                                                }) 
                                                # created_invoice.action_invoice_cancel()
                                        else:
                                            not_import_invoice=True
                                # ======================================================
                                # CONNECT SALE ORDER AND INVOICE ( CREATE ENTRY ON 
                                # MANY2MANY TABLE sale_order_line_invoice_rel)
                                # ======================================================
                                for invoice in data.get('invoice_ids'):
                                    if invoice.get('invoice_line_ids') and len(invoice.get('invoice_line_ids'))<=100:
                                        for invoice_line in invoice.get('invoice_line_ids'):
                                            sale_lines=invoice_line.get("sale_line_ids")
                                            invoice_line_id=invoice_line.get('id')
                                            invoice_line = self.env['account.move.line'].search([('remote_account_move_line_id','=',invoice_line_id)])        
                                            if invoice_line:
                                                for line in sale_lines:
                                                    related_soline = self.env['sale.order.line'].search([('remote_sale_order_line_id','=',line)])        
                                                    if related_soline:
                                                        self.env.cr.execute(""" SELECT * from sale_order_line_invoice_rel where invoice_line_id=%s and order_line_id=%s """ , [invoice_line.id,related_soline.id])
                                                        find_relation = self._cr.dictfetchall()
                                                        if not find_relation:
                                                            self.env.cr.execute(""" INSERT INTO sale_order_line_invoice_rel (invoice_line_id, order_line_id) VALUES (%s, %s);""" , [invoice_line.id,related_soline.id])
                                                            self.env.cr.commit() 
                                                            self.env.cr.flush()    
                                                            related_soline.state=related_soline.order_id.state
                                                            related_soline._compute_qty_invoiced()
                                                            related_soline._compute_invoice_status()
                                                            related_soline.order_id._compute_invoice_status()             
                            
                                    else:
                                        not_import_invoice=True

                                # ======================================================
                                # CREATE PAYMENT WHICH ARE RELATED TO INVOICE
                                # ======================================================
                                if not not_import_invoice:
                                    for payment in payment_list:
                                        print("\n\n===========payment",payment)
                                        domain=[('remote_account_payment_id','=',payment.get('remote_account_payment_id'))]
                                        already_payment = self.env['account.payment'].search(domain,limit=1)
                                        connected_invoice_ids=[]
                                        if payment.get('invoice_ids'):
                                            connected_invoice_ids=payment.get('invoice_ids')
                                            del payment['invoice_ids']
                                        state='draft'
                                        if already_payment:
                                            if payment.get('state')=='cancelled':
                                                state='cancel'
                                                payment['state']='draft'
                                            if payment.get('state') in ['posted','sent','reconciled']:
                                                state='posted'
                                            # if payment.get('state') not  in ['posted','sent','reconciled']:
                                            #     already_payment.write(payment)
                                            
                                            # if already_payment.state!='posted' and state=='posted':
                                            #     already_payment.action_post()
                                            # elif already_payment.state!='cancel' and state=='cancel':
                                            #     already_payment.action_cancel()
                                            created_payment=already_payment
                                        else:
                                            if payment.get('state') in ['posted','sent','reconciled']:
                                                state='posted'
                                                payment['state']='draft'
                                            elif payment.get('state')=='cancelled':
                                                state='cancel'
                                                payment['state']='draft'
                                            created_payment = self.env['account.payment'].create(payment)
                                            if created_payment.state!='posted' and state=='posted':
                                                created_payment.action_post()
                                            elif created_payment.state!='cancel' and state=='cancel':
                                                created_payment.action_cancel()   
                                        # ======================================================
                                        # CONNECT INVOICE AND PAYMENT ( INVOICE AND PAYMENT 
                                        # JOURNAL ENTRY RECONCILE )
                                        # ======================================================
                                        if created_payment and connected_invoice_ids: 
                                            print("\n\n====created_payment",created_payment,created_payment.state) 
                                            print("\n\n======connected_invoice_ids",connected_invoice_ids) 
                                            if created_payment.state=='posted':
                                                for inv in connected_invoice_ids:
                                                    invoice=self.env['account.move'].search([('remote_account_move_id','=',inv)])
                                                    print("\n\n====invoice",invoice,invoice.state)
                                                    if invoice and invoice.state!='cancel':  
                                                        lines = (created_payment.line_ids + invoice.line_ids).filtered(
                                                                lambda l: l.account_id.account_type == 'asset_receivable' and not l.reconciled)
                                                        print("\n\n===lines",lines)
                                                        lines.reconcile()             
                                                
                                
                        count += 1
                    else:
                        vals = {
                            "name": confid.name,
                            "state": "error",
                            "field_type": "order",
                            "error": response.text,
                            "datetime": datetime.now(),
                            "base_config_id": confid.id,
                            "operation": "import"
                        }
                        self.env['sh.import.base.log'].create(vals)
                # except Exception as e:
                #     failed += 1
                #     vals = {
                #         "name": data['id'],
                #         "error": e,
                #         "import_json" : data,
                #         "field_type": "order",                           
                #         "datetime": datetime.now(),
                #         "base_config_id": confid.id,
                #     }
                #     self.env['sh.import.failed'].create(vals)
            confid.sh_import_order_ids='['+', '.join([str(elem) for elem in orders[20:]])+']'
            if count > 0:              
                vals = {
                    "name": confid.name,
                    "state": "success",
                    "field_type": "order",
                    "error": "%s Update Order Successfully" %(count - failed),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)
            if failed > 0:
                vals = {
                    "name": confid.name,
                    "state": "error",
                    "field_type": "order",
                    "error": "%s Failed To Update" %(failed),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)

            
    
    
    def import_orders_cron(self):   
        ''' ========== Import Sale_orders ==================  '''
        confid = self.env['sh.import.base'].search([],limit=1)
        if confid.import_order:
            confid.current_import_page_so += 1
            so_query='''%s/api/public/sale.order?query={*,medium_id{*},sale_order_option_ids{*},message_ids{id,subtype_id{*},author_id,body,channel_ids{*},date,display_name,email_from,has_error,layout,mail_activity_type_id{*},message_id,message_type,model,moderation_status,moderator_id,need_moderation,needaction,no_auto_thread,notification_ids,rating_value,record_name,reply_to,res_id,starred,subject},currency_id{name},sh_replied_status_id{*},
        invoice_ids{*,user_id,currency_id{name},payment_ids{*,journal_id{id,name,type,code},currency{name},currency_of_fees{name},message_ids{id,subtype_id{*},author_id,body,channel_ids{*},date,display_name,email_from,has_error,layout,mail_activity_type_id{*},message_id,message_type,model,moderation_status,moderator_id,need_moderation,needaction,no_auto_thread,notification_ids,rating_value,record_name,reply_to,res_id,starred,subject},currency_id{name},payment_method_id{*},paypal_bank_transfer_id{*,currency_id{name},dummy_account_id{*,tag_ids{*},tax_ids{*},user_type_id{*}},journal_id{id,name,type,code},line_ids{*,tax_ids{*},account_id{*,tag_ids{*},tax_ids{*},user_type_id{*}},currency_id{name},journal_id{id,name,type,code},tax_line_id{*},
        analytic_line_ids{*}}},destination_account_id{*,tag_ids{*},tax_ids{*},user_type_id{*}},destination_journal_id{id,name,type,code},journal_id{id,name,type,code},partner_bank_account_id{*}},message_follower_ids{*},message_ids{id,subtype_id{*},author_id,body,channel_ids{*},date,display_name,email_from,has_error,layout,mail_activity_type_id{*},message_id,message_type,model,moderation_status,
        moderator_id,need_moderation,needaction,no_auto_thread,notification_ids,rating_value,record_name,reply_to,res_id,starred,subject},version_ids{*},account_id{*},journal_id{id,name,type,code},medium_id{*},partner_bank_id{*},source_id{*},
        team_id{*},invoice_line_ids{*,-product_image,product_id{id,product_tmpl_id},currency_id{name},invoice_line_tax_ids{*},account_id{*}}},opportunity_id{*,tag_ids{*},lost_reason{*},medium_id{*},
        source_id{*},stage_id{*},state_id{name,code},team_id{*},message_ids{id,subtype_id{*},author_id,body,channel_ids{*},date,display_name,email_from,has_error,layout,mail_activity_type_id{*},message_id,message_type,model,moderation_status,moderator_id,need_moderation,needaction,no_auto_thread,notification_ids,rating_value,record_name,reply_to,res_id,starred,subject}},
        sh_bank_account_id{*},sh_edition_id{*},sh_odoo_hosted_id{*,sh_edtion_id{*}},sh_partner_category_id{*},sh_replied_status_id{*},source_id{*},team_id{*},
        message_follower_ids{*},order_line{*,product_id{id,product_tmpl_id},tax_id{name,amount_type,amount,type_tax_use},currency_id{name},analytic_line_ids{*},invoice_lines{*,invoice_line_tax_ids{*},account_id{*,tag_ids{*},tax_ids{*}, user_type_id{*}},currency_id{name}},tax_id{*},product_uom{id,name,uom_type,factor,rounding,category_id{*}}}
        }&page_size=%s&page=%s&order="id asc"&filter=[["company_id","=",1],["create_date",">=","01/01/2022 00:00:00"]]''' %(confid.base_url,confid.records_per_page_so,confid.current_import_page_so)
            response = requests.get(so_query)
            response_json = response.json()
            if response.status_code==200:
                if response_json.get('count') and confid.records_per_page_so != response_json['count']:
                    confid.import_order = False
                    confid.current_import_page_so = 0
                count = 0
                failed = 0
                already_order=False
                payment_list=[]
                for data in response_json.get('result'):
                    # print("\n==========",data.get('id'),data.get('name'))
                    not_import_invoice=False
                    # try:
                    domain = ['|',('remote_sale_order_id', '=', data['id']),('name', '=', data['name'])]
                    already_order = self.env['sale.order'].search(domain)
                    order_vals=self.process_order_data(data)
                    invoice_dict={}
                    if order_vals:
                        # followers_list=[]
                        # if 'message_follower_ids' in order_vals:
                        #     followers_list = order_vals['message_follower_ids']
                        #     del order_vals['message_follower_ids']

                        if already_order:
                            already_order.write(order_vals)

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
                                                if partner not in already_order.sudo().message_partner_ids.ids]
                                            # print("\n\n=======find_customer",find_customer)
                                            # print("\nn\======part_list",part_list)
                                            already_order.sudo().message_subscribe(partner_ids=part_list)
                                            find_follower=self.env['mail.followers'].search([('partner_id','=',find_customer.id),('res_model','=','sale.order'),('res_id','=',already_order.id)])
                                            # print("\n\n========find_follower",find_follower)
                                            if find_follower:
                                                find_follower.update({
                                                    'subtype_ids':  [(6,0,subtype_list)],
                                                })

                        else:
                            created_so=self.env['sale.order'].create(order_vals)
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
                                                if partner not in created_so.sudo().message_partner_ids.ids]
                                            # print("\n\n=======find_customer",find_customer)
                                            # print("\nn\======part_list",part_list)
                                            created_so.sudo().message_subscribe(partner_ids=part_list)
                                            find_follower=self.env['mail.followers'].search([('partner_id','=',find_customer.id),('res_model','=','sale.order'),('res_id','=',created_so.id)])
                                            # print("\n\n========find_follower",find_follower)
                                            if find_follower:
                                                find_follower.update({
                                                    'subtype_ids':  [(6,0,subtype_list)],
                                                })


                        if data.get('invoice_ids'):
                            for invoice in data.get('invoice_ids'):
                                invoice_dict[str(invoice.get('id'))]=invoice.get('state').get('sh_api_current_state')

                            invoice_list,payment_list=confid.process_invoice_data(data.get('invoice_ids'))
                            # print("\n\n=======99999999999")    

                            for invoice in invoice_list:
                                if invoice[2]:
                                    find_invoice=self.env['account.move'].search([('remote_account_move_id','=',invoice[2].get('remote_account_move_id'))])
                                    followers_list=[]
                                    if 'message_follower_ids' in invoice[2]:
                                        followers_list = invoice[2]['message_follower_ids']
                                        del invoice[2]['message_follower_ids']
                                    
                                    if not find_invoice:
                                        created_invoice = self.env['account.move'].create(invoice[2])
                                    else: 
                                        find_invoice.write(invoice[2])
                                        created_invoice=find_invoice
                                    if followers_list:
                                        # follower_ids=[]
                                        for follower in followers_list:
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
                                                        if partner not in created_invoice.sudo().message_partner_ids.ids]
                                                    created_invoice.sudo().message_subscribe(partner_ids=part_list)
                                                    find_follower=self.env['mail.followers'].search([('partner_id','=',find_customer.id),('res_model','=','account.move'),('res_id','=',created_invoice.id)])
                                                    if find_follower:
                                                        find_follower.update({
                                                            'subtype_ids':  [(6,0,subtype_list)],
                                                        })

                                  
                                    if invoice_dict[str(created_invoice.remote_account_move_id)] in ['open','in_payment','paid']:
                                        if created_invoice.invoice_line_ids:
                                            created_invoice.action_post()
                                    if invoice_dict[str(created_invoice.remote_account_move_id)] == 'cancel':
                                        created_invoice.write({
                                            'state':'cancel',
                                        }) 
                                        # created_invoice.action_invoice_cancel()
                                else:
                                    not_import_invoice=True
                        # ======================================================
                        # CONNECT SALE ORDER AND INVOICE ( CREATE ENTRY ON 
                        # MANY2MANY TABLE sale_order_line_invoice_rel)
                        # ======================================================
                        for invoice in data.get('invoice_ids'):
                            if invoice.get('invoice_line_ids') and len(invoice.get('invoice_line_ids'))<=100:
                                for invoice_line in invoice.get('invoice_line_ids'):
                                    sale_lines=invoice_line.get("sale_line_ids")
                                    invoice_line_id=invoice_line.get('id')
                                    invoice_line = self.env['account.move.line'].search([('remote_account_move_line_id','=',invoice_line_id)])        
                                    if invoice_line:
                                        for line in sale_lines:
                                            related_soline = self.env['sale.order.line'].search([('remote_sale_order_line_id','=',line)])        
                                            if related_soline:
                                                self.env.cr.execute(""" SELECT * from sale_order_line_invoice_rel where invoice_line_id=%s and order_line_id=%s """ , [invoice_line.id,related_soline.id])
                                                find_relation = self._cr.dictfetchall()
                                                if not find_relation:
                                                    self.env.cr.execute(""" INSERT INTO sale_order_line_invoice_rel (invoice_line_id, order_line_id) VALUES (%s, %s);""" , [invoice_line.id,related_soline.id])
                                                    self.env.cr.commit() 
                                                    self.env.cr.flush()    
                                                    related_soline.state=related_soline.order_id.state
                                                    related_soline._compute_qty_invoiced()
                                                    related_soline._compute_invoice_status()
                                                    related_soline.order_id._compute_invoice_status()             
                    
                            else:
                                not_import_invoice=True

                        # ======================================================
                        # CREATE PAYMENT WHICH ARE RELATED TO INVOICE
                        # ======================================================
                        if not not_import_invoice:
                            for payment in payment_list:
                                domain=[('remote_account_payment_id','=',payment.get('remote_account_payment_id'))]
                                already_payment = self.env['account.payment'].search(domain,limit=1)
                                connected_invoice_ids=[]
                                if payment.get('invoice_ids'):
                                    connected_invoice_ids=payment.get('invoice_ids')
                                    del payment['invoice_ids']
                                state='draft'
                                if already_payment:
                                    if payment.get('state')=='cancelled':
                                        state='cancel'
                                        payment['state']='draft'
                                    if payment.get('state') in ['posted','sent','reconciled']:
                                        state='posted'
                                    # if payment.get('state') not  in ['posted','sent','reconciled']:
                                    #     already_payment.write(payment)
                                    
                                    # if already_payment.state!='posted' and state=='posted':
                                    #     already_payment.action_post()
                                    # elif already_payment.state!='cancel' and state=='cancel':
                                    #     already_payment.action_cancel()
                                    created_payment=already_payment
                                else:
                                    if payment.get('state') in ['posted','sent','reconciled']:
                                        state='posted'
                                        payment['state']='draft'
                                    elif payment.get('state')=='cancelled':
                                        state='cancel'
                                        payment['state']='draft'
                                    created_payment = self.env['account.payment'].create(payment)
                                    if created_payment.state!='posted' and state=='posted':
                                        created_payment.action_post()
                                    elif created_payment.state!='cancel' and state=='cancel':
                                        created_payment.action_cancel()   
                                # ======================================================
                                # CONNECT INVOICE AND PAYMENT ( INVOICE AND PAYMENT 
                                # JOURNAL ENTRY RECONCILE )
                                # ======================================================
                                if created_payment and connected_invoice_ids: 
                                    # print("\n\n====created_payment",created_payment.line_ids.parent_state)  
                                    if created_payment.state=='posted':
                                        for inv in connected_invoice_ids:
                                            invoice=self.env['account.move'].search([('remote_account_move_id','=',inv)])

                                            if invoice and invoice.state!='cancel':  
                                                lines = (created_payment.line_ids + invoice.line_ids).filtered(
                                                        lambda l: l.account_id.account_type == 'asset_receivable' and not l.reconciled)
                                                lines.reconcile()               
                    count += 1
                    # except Exception as e:
                    #     failed += 1
                    #     vals = {
                    #         "name": data['id'],
                    #         "error": e,
                    #         "import_json" : data,
                    #         "field_type": "order",                           
                    #         "datetime": datetime.now(),
                    #         "base_config_id": confid.id,
                    #     }
                    #     self.env['sh.import.failed'].create(vals)
                if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "order",
                        "error": "%s Order Imported Successfully" %(count - failed),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
                if failed > 0:
                    vals = {
                        "name": confid.name,
                        "state": "error",
                        "field_type": "order",
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
                    "field_type": "order",
                    "error": response.text,
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)      
                        
    def process_order_line_data(self,data):
        ''' ================= Import sale order lines=============  '''
        order_line_list=[]
        for line in data:            
            line_vals={}
            if line.get('id') and line.get('id')!=0:
                if line.get('display_type') and line.get('display_type').get('sh_api_current_state') and line.get('display_type').get('sh_api_current_state')=='line_section' or line.get('display_type').get('sh_api_current_state')=='line_note':
                    line_vals={
                        'remote_sale_order_line_id':line.get('id'),
                        'display_type':line.get('display_type').get('sh_api_current_state'),
                        'name':line.get('name'),
                        'company_id':1,
                    }
                else:
                    line_vals={
                        'remote_sale_order_line_id':line.get('id'),
                        'display_type':line.get('display_type').get('sh_api_current_state'),
                        'name':line.get('name'),
                        'is_downpayment':line.get('is_downpayment'),
                        'is_expense':line.get('is_expense'),
                        'is_service':line.get('is_service'),
                        'product_updatable':line.get('product_updatable'),
                        'display_name':line.get('display_name'),
                        'name_short':line.get('name_short'),
                        'customer_lead':line.get('customer_lead'),
                        'discount':line.get('discount'),
                        'price_reduce':line.get('price_reduce'),
                        'price_tax':line.get('price_tax'),
                        'price_unit':line.get('price_unit'),
                        'product_uom_qty':line.get('product_uom_qty'),
                        'qty_invoiced':line.get('qty_invoiced'),
                        'qty_to_invoice':line.get('qty_to_invoice'),
                        'sequence':line.get('sequence'),
                        'price_reduce_taxexcl':line.get('price_reduce_taxexcl'),
                        'price_reduce_taxinc':line.get('price_reduce_taxinc'),
                        'price_subtotal':line.get('price_subtotal'),
                        'price_total':line.get('price_total'),
                        'untaxed_amount_invoiced':line.get('untaxed_amount_invoiced'),
                        'untaxed_amount_to_invoice':line.get('untaxed_amount_to_invoice'),
                        'invoice_status':line.get('invoice_status').get('sh_api_current_state'),
                        'so_state':line.get('so_state').get('sh_api_current_state'),
                        'state':line.get('state').get('sh_api_current_state'),
                        'company_id':1,
                        'tax_id':False,
                    }
                    if line.get('so_order_date'):
                        date_time=datetime.strptime(line.get('so_order_date'),'%Y-%m-%d-%H-%M-%S')
                        date_time=date_time.strftime('%Y-%m-%d %H:%M:%S')
                        line_vals['so_order_date']=date_time
                    
                    if line.get('currency_id'):
                        domain=[('name','=',line.get('currency_id').get('name'))]
                        find_currency_id=self.env['res.currency'].search(domain,limit=1)
                        if find_currency_id:
                            line_vals['currency_id']=find_currency_id.id

                    # =================  Get Product if created ===================
                    if line.get('product_id'):
                        domain=[('remote_product_product_id','=',line.get('product_id').get('id'))]
                        find_product=self.env['product.product'].search(domain,limit=1)
                        if find_product:
                            line_vals['product_id']=find_product.id   
                            # print("\n\n=====line_vals.get('product_id')",line_vals.get('product_id'),line.get('product_id'))
                        else:
                            find_template=self.env['product.template'].search([('remote_product_template_id','=',line.get('product_id').get('product_tmpl_id'))])
                            if find_template:
                                # print("\n\n==========find_template.product_variant_ids.mapped('id')",find_template.product_variant_ids.mapped('id'))
                                variant=find_template.product_variant_ids.mapped('id')[-1]   
                                # print("\nn=======variant",variant)
                                line_vals['product_id']=variant

                    if line.get('project_id'):             
                        domain=[('remote_project_project_id','=',line.get('project_id'))]
                        find_project=self.env['project.project'].search(domain)
                        if find_project:            
                            line_vals['project_id']=find_project.id      
                            
                    if line.get('salesman_id') and line.get('salesman_id')!=0:
                        domain_by_id = [('remote_res_user_id','=',line['salesman_id'])]
                        find_user_id=self.env['res.users'].search(domain_by_id)
                        if find_user_id:
                            line_vals['salesman_id']=find_user_id.id 
                         

                    if line.get('task_id'):
                        domain=[('remote_project_task_id','=',line.get('task_id'))]
                        find_task=self.env['project.task'].search(domain)
                        if find_task:        
                            line_vals['task_id']=find_task.id          
                    
                    if line.get('analytic_line_ids'):
                        analytic_line_list=self.process_timesheet_data(line.get('analytic_line_ids'))
                        if analytic_line_list:
                            line_vals['analytic_line_ids']=analytic_line_list
                                
                    if line.get('sale_order_option_ids'):
                        order_option_list=[]
                        for order_option in line.get('sale_order_option_ids'):
                            order_option_vals={
                                'remote_sale_order_option_id':order_option.get('id'),
                                'display_name':order_option.get('display_name'),
                                'discount':order_option.get('discount'),
                                'price_unit':order_option.get('price_unit'),
                                'quantity':order_option.get('quantity'),
                                'sequence':order_option.get('sequence'),
                                'name':order_option.get('name'),
                            }
                            if order_option.get('product_id'):
                                domain=[('remote_product_product_id','=',order_option.get('product_id'))]
                                find_product=self.env['product.product'].search(domain)
                                if find_product:
                                    order_option_vals['product_id']=find_product.id   
                                    
                                
                            order_option_list.append((0,0,order_option_vals))    
                        if order_option_list:
                            line_vals['sale_order_option_ids']=order_option_list   
                            
                    # ==============  Import line tax ===================
                    
                    if line.get('tax_id'):
                        tax_list = self.process_tax(line['tax_id'])
                        print("nn\n\n\n",tax_list)
                        if tax_list:
                            line_vals['tax_id'] = tax_list
                    else:
                        line_vals['tax_id'] = [(6,0,[])]
            print("n\n\n",line_vals)
            if line_vals and line_vals.get('product_id'):
                order_line=self.env['sale.order.line'].search([('remote_sale_order_line_id','=',line.get('id'))])
                if order_line:
                    del line_vals['display_type']
                    if order_line.state!='draft':
                        order_line.write({'state':'draft'})
                    order_line.write(line_vals)
                else:
                    order_line_list.append((0,0,line_vals)) 
        return order_line_list                

    def process_order_data(self,data):
        ''' ================= Import Orders =============  '''
        domain = ['|',('remote_sale_order_id', '=', data['id']),('name', '=', data['name'])]
        already_order = self.env['sale.order'].search(domain)
        if already_order.state!='draft':
            already_order.action_draft()
        
        order_vals = {
            'remote_sale_order_id':data.get('id'),
            'cart_recovery_email_sent':data.get('cart_recovery_email_sent'),
            'is_abandoned_cart':data.get('is_abandoned_cart'),
            'is_expired':data.get('is_expired'),
            'message_has_error':data.get('message_has_error'),
            'message_is_follower':data.get('message_is_follower'),
            'message_needaction':data.get('message_needaction'),
            'only_services':data.get('only_services'),
            'pricelist_alert':data.get('pricelist_alert'),
            'require_payment':data.get('require_payment'),
            'sh_original_module_send':data.get('sh_original_module_send'),   
            'client_order_ref':data.get('client_order_ref'),
            'display_name':data.get('display_name'),
            'name':data.get('name'),
            'origin':data.get('origin'),
            'reference':data.get('reference'),
            'responsible_user_names':data.get('responsible_user_names'),
            'signed_by':data.get('signed_by'),
            'type_name':data.get('type_name'),
            'amount_undiscounted':data.get('amount_undiscounted'),
            'currency_rate':data.get('currency_rate'),
            'timesheet_count':data.get('timesheet_count'),
            'cart_quantity':data.get('cart_quantity'),
            'expense_count':data.get('expense_count'),
            'invoice_count':data.get('invoice_count'),
            'message_has_error_counter':data.get('message_has_error_counter'),
            'message_needaction_counter':data.get('message_needaction_counter'),
            'sale_ticket_count':data.get('sale_ticket_count'),
            'tasks_count':data.get('tasks_count'),
            'amount_tax':data.get('amount_tax'),
            'amount_total':data.get('amount_total'),
            'amount_untaxed':data.get('amount_untaxed'),    
            'invoice_status':data.get('invoice_status').get('sh_api_current_state'),
            'sh_custom_module_conflict':data.get('sh_custom_module_conflict').get('sh_api_current_state'),
            'sh_deployment_required':data.get('sh_deployment_required').get('sh_api_current_state'),
            'sh_invoice_verified':data.get('sh_invoice_verified').get('sh_api_current_state'),
            'sh_latest_update':data.get('sh_latest_update').get('sh_api_current_state'),
            'sh_need_to_setup_environment':data.get('sh_need_to_setup_environment').get('sh_api_current_state'),
            'state':data.get('state').get('sh_api_current_state'),
            'access_warning':data.get('access_warning'),
            'note':data.get('note'),
            'request_quote_message':data.get('request_quote_message'), 
            'sh_replied_status':data.get('sh_replied_status').get('sh_api_current_state'),
            'responsible_user_names':data.get('responsible_user_names'),     
            'company_id':1,
            'payment_term_id':1,
            # 'sale_order_template_id':1,
        }
        # ======== Get partner if already created or create ==========
        
        if data.get('effective_date'):
            date_time=datetime.strptime(data.get('effective_date'),'%Y-%m-%d')
            order_vals['effective_date']=date_time
            
        if data.get('expected_date'):
            date_time=datetime.strptime(data.get('expected_date'),'%Y-%m-%d-%H-%M-%S')
            date_time=date_time.strftime('%Y-%m-%d %H:%M:%S')
            order_vals['expected_date']=date_time
            
        if data.get('date_order'):
            date_time=datetime.strptime(data.get('date_order'),'%Y-%m-%d-%H-%M-%S')
            date_time=date_time.strftime('%Y-%m-%d %H:%M:%S')
            order_vals['date_order']=date_time

        if data.get('validity_date'):
            date_time=datetime.strptime(data.get('validity_date'),'%Y-%m-%d')
            order_vals['validity_date']=date_time

        # if data.get('message_partner_ids'):
        #     partner_list=[]
        #     for partner in data.get('message_partner_ids'):
        #         if partner and partner!=0:
        #             domain = [('remote_res_partner_id', '=', partner)]
        #             find_customer = self.env['res.partner'].search(domain)
        #             if find_customer:
        #                 partner_list.append((4,find_customer.id))
        #     if partner_list:
        #         order_vals['message_partner_ids']=partner_list  

        if data.get('project_ids'):
            project_list=[]
            for project in data.get('project_ids'):
                domain=[('remote_project_project_id','=',project)]
                find_project=self.env['project.project'].search(domain)
                if find_project:
                    project_list.append((4,find_project.id))    
            if project_list:
                order_vals['project_ids']=project_list
            
        if data.get('sh_responsible_user_ids'):
            user_list=[]
            for user in data.get('sh_responsible_user_ids'):
                if user and user!=0:
                    domain_by_id = [('remote_res_user_id','=',user)]
                    find_user_id=self.env['res.users'].search(domain_by_id)
                    if find_user_id:
                        user_list.append(find_user_id.id)
            if user_list:
                order_vals['sh_responsible_user_ids']=[(6,0,user_list)]
            
        if data.get('sh_sale_ticket_ids'):
            ticket_list=[]
            for ticket in data.get('sh_sale_ticket_ids'):
                if ticket and ticket!=0:
                    domain = [('remote_sh_helpdesk_ticket_id', '=', ticket)]   
                    find_ticket = self.env['sh.helpdesk.ticket'].search(domain)
                    if find_ticket:
                        ticket_list.append((4,find_ticket.id))
            if ticket_list:
                order_vals['sh_sale_ticket_ids']=ticket_list   
                     
        if data.get('tag_ids'):
            tag_list=[]
            for tag in data.get('tag_ids'):         
                domain_by_id=[('remote_crm_tag_id','=',tag.get('id'))]
                already_crm_tag_id = self.env['crm.tag'].search(domain_by_id,limit=1)
                domain_by_name=[('name','=',tag.get('name'))]
                already_crm_tag_name = self.env['crm.tag'].search(domain_by_name,limit=1)
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
                    if crm_tag_id:
                        tag_list.append((4,crm_tag_id.id))                  
            if tag_list:
                order_vals['tag_ids']=tag_list          
                
        if data.get('tasks_ids'):
            task_list=[]
            for task in data.get('tasks_ids'):
                domain=[('remote_project_task_id','=',task)]
                find_task=self.env['project.task'].search(domain)
                if find_task:
                    task_list.append((4,find_task.id))
            if task_list:
                order_vals['tasks_ids']=task_list
        
        if data.get('timesheet_ids'):
            timesheet_list=[]
            for timesheet in data.get('timesheet_ids'):
                domain=[('remote_account_analytic_line_id','=',timesheet)]
                find_timesheet=self.env['account.analytic.line'].search(domain)
                if find_timesheet:
                    timesheet_list.append((4,find_timesheet.id))
            if timesheet_list:
                order_vals['timesheet_ids']=timesheet_list
                
        if data.get('currency_id'):   
            domain=[('name','=',data.get('currency_id').get('name'))]
            find_currency_id=self.env['res.currency'].search(domain,limit=1)
            if find_currency_id:
                order_vals['currency_id']=find_currency_id.id

        if data.get('medium_id') and data.get('medium_id').get('id') and data.get('medium_id').get('id')!=0:
            domain = ['|', ('remote_medium_id', '=', data['medium_id']['id']),
                          ('name', '=', data['medium_id']['name'])]
            find_rec = self.env['utm.medium'].search(domain,limit=1)
            if find_rec:
                order_vals['medium_id'] = find_rec.id
            else:
                medium_vals = {
                    'remote_medium_id': data['medium_id']['id'],
                    'name': data['medium_id']['name'],
                    'display_name': data['medium_id']['display_name'],
                    'active': data['medium_id']['active'],
                }
                created_rec = self.env['utm.medium'].create(medium_vals)
                if created_rec:
                    order_vals['medium_id'] = created_rec.id

        if data.get('opportunity_id') and data.get('opportunity_id').get('id') and data.get('opportunity_id').get('id')!=0:
            domain = [('remote_crm_lead_id', '=', data.get('opportunity_id')['id'])]
            find_lead = self.env['crm.lead'].search(domain)
            if find_lead:
                order_vals['opportunity_id']=find_lead.id
            else:
                lead_vals=self.process_lead_data(data.get('opportunity_id'))
                if lead_vals:
                    create_lead=self.env['crm.lead'].create(lead_vals)
                    if create_lead:
                        order_vals['opportunity_id']=create_lead.id    

        if data.get('partner_id') and data['partner_id']!=0:
            domain = [('remote_res_partner_id', '=', data['partner_id'])]
            find_customer = self.env['res.partner'].search(domain)
            if find_customer:
                order_vals['partner_id'] = find_customer.id
        
        if data.get('partner_invoice_id') and data['partner_invoice_id']!=0:
            domain = [('remote_res_partner_id', '=', data['partner_invoice_id'])]
            find_customer = self.env['res.partner'].search(domain)
            if find_customer:
                order_vals['partner_invoice_id'] = find_customer.id
        
        if data.get('partner_shipping_id') and data['partner_shipping_id']!=0:
            domain = [('remote_res_partner_id', '=', data['partner_shipping_id'])]
            find_customer = self.env['res.partner'].search(domain)
            if find_customer:
                order_vals['partner_shipping_id'] = find_customer.id        
                
                
        if data.get('pricelist_id'):
            domain = [('remote_product_pricelist_id', '=', data.get('pricelist_id'))]
            find_pricelist = self.env['product.pricelist'].search(domain)        
            if find_pricelist:
                order_vals['pricelist_id']=find_pricelist.id 

        if data.get('responsible_user_id') and data['responsible_user_id']!=0:
            domain_by_id = [('remote_res_user_id','=',data['responsible_user_id'])]
            find_user_id=self.env['res.users'].search(domain_by_id)
            if find_user_id:
                order_vals['responsible_user_id']=find_user_id.id    

        if data.get('sh_edition_id'):
            domain=[('remote_sh_edition_id','=',data.get('sh_edition_id').get('id'))]
            find_edition=self.env['sh.edition'].search(domain)
            if find_edition:
                order_vals['sh_edition_id']=find_edition.id        
            else:
                edition_vals={
                    'remote_sh_edition_id':data.get('sh_edition_id').get('id'),
                    'active':data.get('sh_edition_id').get('active'),
                    'sh_display_in_frontend':data.get('sh_edition_id').get('sh_display_in_frontend'),
                    'display_name':data.get('sh_edition_id').get('display_name'),
                    'name':data.get('sh_edition_id').get('name'),
                    'company_id':1,
                }    
                created_edition=self.env['sh.edition'].create(edition_vals)
                if created_edition:
                    order_vals['sh_edition_id']=created_edition.id 

        # if data.get('sh_odoo_hosted_id') and data.get('sh_odoo_hosted_id').get('id') and data.get('sh_odoo_hosted_id').get('id')!=0:
        #     domain=[('remote_sh_odoo_hosted_id','=',data.get('sh_odoo_hosted_id').get('id'))]
        #     find_odoo_hosted=self.env['sh.odoo.hosted.on'].search(domain)
        #     if find_odoo_hosted:
        #         order_vals['sh_odoo_hosted_id']=find_odoo_hosted.id
        #     else:
        #         odoo_hosted_vals={
        #             'remote_sh_odoo_hosted_id':data.get('sh_odoo_hosted_id').get('id'),
        #             'active':data.get('sh_odoo_hosted_id').get('active'),
        #             'sh_display_in_frontend':data.get('sh_odoo_hosted_id').get('sh_display_in_frontend'),
        #             'display_name':data.get('sh_odoo_hosted_id').get('display_name'),
        #             'name':data.get('sh_odoo_hosted_id').get('name'),
        #             'company_id':1,
        #         }

        #         if data.get('sh_odoo_hosted_id').get('sh_edtion_id') and data.get('sh_odoo_hosted_id').get('sh_edtion_id').get('id')!=0:
        #             domain=[('remote_sh_edition_id','=',data.get('sh_odoo_hosted_id').get('sh_edtion_id').get('id'))]
        #             find_edition=self.env['sh.edition'].search(domain)
        #             if find_edition:
        #                 odoo_hosted_vals['sh_edtion_id']=find_edition.id        
        #             else:
        #                 edition_vals={
        #                     'remote_sh_edition_id':data.get('sh_odoo_hosted_id').get('sh_edition_id').get('id'),
        #                     'active':data.get('sh_odoo_hosted_id').get('sh_edition_id').get('active'),
        #                     'sh_display_in_frontend':data.get('sh_odoo_hosted_id').get('sh_edition_id').get('sh_display_in_frontend'),
        #                     'display_name':data.get('sh_odoo_hosted_id').get('sh_edition_id').get('display_name'),
        #                     'name':data.get('sh_odoo_hosted_id').get('sh_edition_id').get('name'),
        #                     'company_id':1,
        #                 }    
        #                 created_edition=self.env['sh.edition'].create(edition_vals)
        #                 if created_edition:
        #                     odoo_hosted_vals['sh_edtion_id']=created_edition.id   
        #         created_odoo_host=self.env['sh.odoo.hosted.on'].create(odoo_hosted_vals)  
        #         if created_odoo_host:
        #             order_vals['sh_odoo_hosted_id']=created_odoo_host.id   
                    
        if data.get('sh_partner_category_id'):
            domain=['|',('remote_partner_category_id','=',data.get('sh_partner_category_id').get('id')),('name','=',data.get('sh_partner_category_id').get('name'))]    
            find_partner_category=self.env['partner.category'].search(domain)
            if find_partner_category:
                order_vals['sh_partner_category_id']=find_partner_category.id              
            else:
                category_vals={
                    'remote_partner_category_id':data.get('sh_partner_category_id').get('id'),
                    'display_name':data.get('sh_partner_category_id').get('display_name'),
                    'from_invoice_amount':data.get('sh_partner_category_id').get('from_invoice_amount'),
                    'name':data.get('sh_partner_category_id').get('name'),
                    'sequence':data.get('sh_partner_category_id').get('sequence'),
                    'to_invoice_amount':data.get('sh_partner_category_id').get('to_invoice_amount'),
                }    
                created_category=self.env['partner.category'].create(category_vals)
                if created_category:
                    order_vals['sh_partner_category_id']=created_category.id            
            
        if data.get('sh_replied_status_id'):        
            domain=[('remote_sh_replied_status_id','=',data.get('sh_replied_status_id').get('id'))]    
            find_replied_status=self.env['sh.replied.status'].search(domain)
            if find_replied_status:
                order_vals['sh_replied_status_id']=find_replied_status.id       
            else:
                replied_staus_vals={
                    'remote_sh_replied_status_id':data.get('sh_replied_status_id').get('id'),
                    'display_name':data.get('sh_replied_status_id').get('display_name'), 
                    'name':data.get('sh_replied_status_id').get('name'),
                    'sequence':data.get('sh_replied_status_id').get('sequence'), 
                    'sh_closed':data.get('sh_replied_status_id').get('sh_closed'),
                    'sh_customer_replied':data.get('sh_replied_status_id').get('sh_customer_replied'), 
                    'sh_running':data.get('sh_replied_status_id').get('sh_running'), 
                    'sh_staff_replied':data.get('sh_replied_status_id').get('sh_staff_replied'),
                    'company_id':1,
                }  
                create_replied_staus=self.env['sh.replied.status'].create(replied_staus_vals)
                if create_replied_staus:
                    order_vals['sh_replied_status_id']=create_replied_staus.id      
                
        if data.get('sh_task_id'):
            domain=[('remote_project_task_id','=',data.get('sh_task_id'))]
            find_task=self.env['project.task'].search(domain)
            if find_task:
                order_vals['sh_task_id']=find_task.id      
                
        if data.get('source_id') and data.get('source_id').get('id') and data.get('source_id').get('id') != 0:
            domain = ['|', ('remote_source_id', '=', data.get('source_id').get('id')),
                        ('name', '=', data.get('source_id').get('name'))]
            find_rec = self.env['utm.source'].search(domain)
            if find_rec:
                order_vals['source_id'] = find_rec.id
            else:
                source_vals = {
                    'remote_source_id': data.get('source_id').get('id'),
                    'name': data.get('source_id').get('name'),
                    'display_name': data.get('source_id').get('display_name'),
                }
                created_source = self.env['utm.source'].create(source_vals)
                if created_source:
                    order_vals['source_id'] = created_source.id           
       
        if data.get('team_id'):
            domain=[('remote_crm_team_id','=',data.get('team_id').get('id'))]    
            find_crm_team_id=self.env['crm.team'].search(domain)
            
            # =========== CHECK IF CREATED TEAM OR NOT IF CREATE THEN RETURN ELSE CREATE AND RETURN =============
            if find_crm_team_id:
                order_vals['team_id']=find_crm_team_id.id 
            else:
                team_vals=self.process_crm_team_data(data['team_id'])       
                team_id=self.env['crm.team'].create(team_vals)
                if team_id:
                    order_vals['team_id']=team_id.id

        if data.get('user_id') and data['user_id'] and data['user_id']!=0:
            domain_by_id = [('remote_res_user_id','=',data['user_id']),'|',('active','=',True),('active','=',False)]
            find_user_id=self.env['res.users'].search(domain_by_id)
            if find_user_id:
                order_vals['user_id']=find_user_id.id       
                                      
        # if data.get('message_follower_ids'):
        #     follower_ids=[]
        #     for follower in data.get('message_follower_ids'):
        #         if follower.get('partner_id'):
        #             domain = [('remote_res_partner_id', '=', follower.get('partner_id'))]
        #             find_customer = self.env['res.partner'].search(domain)
        #             if find_customer:
        #                 follower_ids.append(find_customer.id)
        #     order_vals['message_follower_ids']= follower_ids      

        if data.get('sale_order_option_ids'):
            order_option_list=[]
            for order_option in data.get('sale_order_option_ids'):
                order_option_vals={
                    'remote_sale_order_option_id':order_option.get('id'),
                    'display_name':order_option.get('display_name'),
                    'discount':order_option.get('discount'),
                    'price_unit':order_option.get('price_unit'),
                    'quantity':order_option.get('quantity'),
                    'sequence':order_option.get('sequence'),
                    'name':order_option.get('name'),
                }
                if order_option.get('product_id'):
                    domain=[('remote_product_product_id','=',order_option.get('product_id'))]
                    find_product=self.env['product.product'].search(domain)
                    if find_product:
                        order_option_vals['product_id']=find_product.id   
                        
                    
                order_option_list.append((0,0,order_option_vals))    
            if order_option_list:
                order_vals['sale_order_option_ids']=order_option_list         
                            
        # ======= Prepare orderlines ==================
        if data.get('order_line'):
            order_line_list=self.process_order_line_data(data.get('order_line'))
            if order_line_list:
                order_vals['order_line']=order_line_list   
        if 'partner_id' in order_vals and order_vals['partner_id']:
            return order_vals
        return False
    
