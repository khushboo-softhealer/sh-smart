# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
import requests
import json
from datetime import datetime

class InheritImportBase(models.Model):
    _inherit = "sh.import.base"
    
    import_invoice=fields.Boolean("Import Invoice")
    records_per_page_invoice = fields.Integer("No of records per page(invoice)")
    current_import_page_invoice = fields.Integer("Current Page(invoice)",default=0) 
    invoice_ids=fields.Char("Invoices")
    payment_ids=fields.Char("Payments")
    import_payment=fields.Boolean("Import Payment")

    def import_invoice_cron(self):   
        ''' ========== Import Invoice ==================  '''
        confid = self.env['sh.import.base'].search([],limit=1)
        if confid.import_invoice and confid.invoice_ids and confid.invoice_ids!='[]':   
            invoices = confid.invoice_ids.strip('][').split(', ')
            count=0
            failed=0 
            for invoice in invoices[0:10]:
                confid.current_import_page_invoice += 1
                invoice_query ='''%s/api/public/account.invoice/%s?query={*,user_id,message_follower_ids{*},currency_id{name},payment_ids{*,journal_id{id,name,type,code},currency{name},currency_of_fees{name},message_ids{id,subtype_id{*},author_id,body,channel_ids{*},date,display_name,email_from,has_error,layout,mail_activity_type_id{*},message_id,message_type,model,moderation_status,moderator_id,need_moderation,needaction,no_auto_thread,notification_ids,rating_value,record_name,reply_to,res_id,starred,subject},currency_id{name},payment_method_id{*},paypal_bank_transfer_id{*,currency_id{name},dummy_account_id{*,tag_ids{*},tax_ids{*},user_type_id{*}},journal_id{id,name,type,code},line_ids{*,tax_ids{*},account_id{*,tag_ids{*},tax_ids{*},user_type_id{*}},currency_id{name},journal_id{id,name,type,code},tax_line_id{*},
                analytic_line_ids{*}}},destination_account_id{*,tag_ids{*},tax_ids{*},user_type_id{*}},destination_journal_id{id,name,type,code},journal_id{id,name,type,code},partner_bank_account_id{*}},message_ids{id,subtype_id{*},author_id,body,channel_ids{*},date,display_name,email_from,has_error,layout,mail_activity_type_id{*},message_id,message_type,model,moderation_status,
                moderator_id,need_moderation,needaction,no_auto_thread,notification_ids,rating_value,record_name,reply_to,res_id,starred,subject},version_ids{*},account_id{*},journal_id{id,name,type,code},medium_id{*},partner_bank_id{*},source_id{*},
                team_id{*},invoice_line_ids{*,-product_image,currency_id{name},invoice_line_tax_ids{*},account_id{*}}}&order="id asc"&filter=[["company_id","=",1]] ''' %(confid.base_url,invoice)
                response = requests.get(invoice_query)

                # print("n\n\======response",response.json())
                # confid.current_import_page_invoice += 1
                # confid.current_import_page_invoice += 1
                # invoice_query ='''%s/api/public/account.invoice?query={*,-amount_by_group,currency_id{name},payment_ids{*,journal_id{id,name,type,code},currency{name},currency_of_fees{name},message_ids{id,subtype_id{*},author_id,body,channel_ids{*},date,display_name,email_from,has_error,layout,mail_activity_type_id{*},message_id,message_type,model,moderation_status,moderator_id,need_moderation,needaction,no_auto_thread,notification_ids,rating_value,record_name,reply_to,res_id,starred,subject},currency_id{name},payment_method_id{*},paypal_bank_transfer_id{*,currency_id{name},dummy_account_id{*,tag_ids{*},tax_ids{*},user_type_id{*}},journal_id{id,name,type,code},line_ids{*,tax_ids{*},account_id{*,tag_ids{*},tax_ids{*},user_type_id{*}},currency_id{name},journal_id{id,name,type,code},tax_line_id{*},
                # analytic_line_ids{*}}},destination_account_id{*,tag_ids{*},tax_ids{*},user_type_id{*}},destination_journal_id{id,name,type,code},journal_id{id,name,type,code},partner_bank_account_id{*}},message_follower_ids{*,subtype_ids{*,parent_id{*}}},message_ids{id,subtype_id{*},author_id,body,channel_ids{*},date,display_name,email_from,has_error,layout,mail_activity_type_id{*},message_id,message_type,model,moderation_status,
                # moderator_id,need_moderation,needaction,no_auto_thread,notification_ids,rating_value,record_name,reply_to,res_id,starred,subject},version_ids{*},account_id{*},journal_id{id,name,type,code},medium_id{*},partner_bank_id{*},source_id{*},
                # team_id{*},invoice_line_ids{*,-product_image,currency_id{name},invoice_line_tax_ids{*},account_id{*}}}&page_size=%s&page=%s''' %(confid.base_url,confid.records_per_page_invoice,confid.current_import_page_invoice)
                # response = requests.get(invoice_query)
                # print("\\n\n\n",response)
                response_json = response.json()
                if response.status_code==200:
                    if response_json.get('count') and confid.records_per_page_invoice != response_json['count']:
                        confid.import_invoice = False
                        confid.current_import_page_invoice = 0
                    count = 0
                    failed = 0
                    # print("\\n\nn0",json.dumps(response_json,indent=4))
                    for data in response_json.get('result'):
                    # try:
                        # if data.get('sh_invoice_so_count')==0:
                        # print("\n\n========data",data)
                        # print("n\n=invoice====",data.get('id'),data.get('number'))
                        not_import_invoice=False
                        # find_invoice=self.env['account.move'].search([[('remote_account_move_id','=',data.get('id'))]])
                        # if not find_invoice:
                        invoice_status=data.get('state').get('sh_api_current_state')
                        invoice_list,payment_list=confid.process_invoice_data([data])
                        for invoice in invoice_list:
                            if invoice[2]:
                                # print("\n\n====invoice[2]",invoice[2].get('name'))
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
                                    # created_invoice.message_subscribe(partner_ids=[partner
                                    #     for partner in followers_list
                                    #     if partner not in created_invoice.sudo().message_partner_ids.ids])
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


                                if invoice_status == 'open' or invoice_status =='in_payment' or invoice_status =='paid':
                                    if created_invoice.invoice_line_ids:
                                        created_invoice.action_post()
                                if invoice_status == 'cancel':
                                    created_invoice.write({
                                        'state':'cancel',
                                    }) 
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
                                    if created_payment.state!='cancel':
                                        for inv in connected_invoice_ids:
                                            invoice=self.env['account.move'].search([('remote_account_move_id','=',inv)])
                                            if invoice and invoice.state!='cancel':  
                                                # print("\n\n====created_payment.line_ids",created_payment.name ,created_payment.line_ids.mapped('parent_state'))
                                                # print("\n\n====invoice.line_ids",invoice.line_ids.mapped('parent_state'))
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
                        #         "field_type": "invoice",                           
                        #         "datetime": datetime.now(),
                        #         "base_config_id": confid.id,
                        #     }
                        #     self.env['sh.import.failed'].create(vals)
                else:
                    vals = {
                        "name": confid.name,
                        "state": "error",
                        "field_type": "invoice",
                        "error": response.text,
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
            confid.invoice_ids='['+', '.join([str(elem) for elem in invoices[10:]])+']'
            if count > 0:              
                vals = {
                    "name": confid.name,
                    "state": "success",
                    "field_type": "invoice",
                    "error": "%s Import Invoice Successfully" %(count - failed),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)
            if failed > 0:
                vals = {
                    "name": confid.name,
                    "state": "error",
                    "field_type": "invoice",
                    "error": "%s Failed To Import Invoice" %(failed),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)

    def process_account_move_data(self,data):
        ''' ================= Import Account Moves =============  '''
        # print("\n\n\=======data",data)
        invoice_line_list=[]
        for line in data:
            line_vals={}
            if line.get('display_type') and line.get('display_type').get('sh_api_current_state') and line.get('display_type').get('sh_api_current_state')=='line_section' or line.get('display_type').get('sh_api_current_state')=='line_note':
                line_vals={
                    'remote_account_move_line_id':line.get('id'),
                    'name':line.get('name'),
                    'display_type':line.get('display_type').get('sh_api_current_state'),
                }
            else:
                line_vals={
                    'remote_account_move_line_id':line.get('id'),
                    'name':line.get('name'),
                    'display_name':line.get('display_name'),
                    'discount':line.get('discount'),
                    'price_unit':line.get('price_unit'),
                    'quantity':line.get('quantity'),
                    'sequence':line.get('sequence'),
                    'price_subtotal':line.get('price_subtotal'),
                    'price_total':line.get('price_total'),
                    'move_type':line.get('invoice_type').get('sh_api_current_state'),
                    'company_id':1,
                    'tax_ids' : False
                }
                
                if line.get('invoice_line_tax_ids'):
                    line_tax_list=[]
                    for line_tax in line.get('invoice_line_tax_ids'):
                        domain = [('name', '=', line_tax['name']),('amount_type', '=', line_tax['amount_type']['sh_api_current_state']),('type_tax_use', '=', line_tax['type_tax_use']['sh_api_current_state'])]
                        find_tax = self.env['account.tax'].search(domain,limit=1)
                        if find_tax:
                            line_tax_list.append((4,find_tax.id)) 
                    if line_tax_list:
                        line_vals['tax_ids']=line_tax_list

                # print("\n\n===vvvvv=line.get('currency_id')",line.get('currency_id'))         
                if line.get('currency_id'):
                    domain=[('name','=',line.get('currency_id').get('name'))]
                    # print("\n\nn",domain)
                    find_currency_id=self.env['res.currency'].search(domain,limit=1)
                    # print("\n\n=-=--------find_currency_id",find_currency_id)
                    if find_currency_id:
                        line_vals['currency_id']=find_currency_id.id
                        
                        
                # ======== Get partner if already created or create =====
                
                if line.get('partner_id'):
                    domain = [('remote_res_partner_id', '=', line['partner_id'])]
                    find_customer = self.env['res.partner'].search(domain)
                    if find_customer:
                        line_vals['partner_id'] = find_customer.id


                if line.get('product_id'):
                    domain=[('remote_product_product_id','=',line.get('product_id'))]
                    find_product=self.env['product.product'].search(domain,limit=1)
                    if find_product:
                        line_vals['product_id']=find_product.id   
                        # print("\n\n=====line_vals.get('product_id')",line_vals.get('product_id'),line.get('product_id'))
                    # else:
                    #     find_template=self.env['product.template'].search([('remote_product_template_id','=',line.get('product_id').get('product_tmpl_id'))])
                    #     if find_template:
                    #         print("\n\n==========find_template.product_variant_ids.mapped('id')",find_template.product_variant_ids.mapped('id'))
                    #         variant=find_template.product_variant_ids.mapped('id')[-1]   
                    #         print("\nn=======variant",variant)
                    #         line_vals['product_id']=variant  


            if line_vals: 
                # state=line.get('parent_state').get('sh_api_current_state')                      
                move_id=self.env['account.move.line'].search([('remote_account_move_line_id','=',line.get('id'))])
                if move_id:
                    if move_id.reconciled:
                        move_id.with_context(check_move_validity=False).remove_move_reconcile()
                    if move_id.move_id.state!='draft':
                        try :
                            move_id.move_id.button_draft()
                            move_id.write(line_vals)  
                        except Exception as e:
                            print("\n\n===========e==",e)
                    # print("\n\n=====move_id",move_id,move_id.parent_state,state)
                    # if state:
                    #     move_id.write({'parent_state':state})
                else: 
                    invoice_line_list.append((0,0,line_vals)) 

        return invoice_line_list               
    
    def account_move_line_data(self,data):
        line_vals={
            'remote_account_move_line_id':data.get('id'),
            'blocked':data.get('blocked'),
            'tax_exigible':data.get('tax_exigible'),
            'counterpart':data.get('counterpart'),
            'display_name':data.get('display_name'),
            'name':data.get('name'),
            'parent_state':data.get('parent_state'),
            'ref':data.get('ref'),
            'quantity':data.get('quantity'),
            'amount_residual':data.get('amount_residual'),
            'amount_residual_currency':data.get('amount_residual_currency'),
            'balance':data.get('balance'),
            'balance_cash_basis':data.get('balance_cash_basis'),
            'credit':data.get('credit'),
            'credit_cash_basis':data.get('credit_cash_basis'),
            'debit':data.get('debit'),
            'debit_cash_basis':data.get('debit_cash_basis'),
            'tax_base_amount':data.get('tax_base_amount'),
            'internal_note':data.get('internal_note'),
            'narration':data.get('narration'),
            'company_id':1,
        }
        if data.get('date'):
            date_time=datetime.strptime(data.get('date'),'%Y-%m-%d')
            line_vals['date']=date_time    
        
        if data.get('date_maturity'):
            date_time=datetime.strptime(data.get('date_maturity'),'%Y-%m-%d')
            line_vals['date_maturity']=date_time 
            
        if data.get('expected_pay_date'):
            date_time=datetime.strptime(data.get('expected_pay_date'),'%Y-%m-%d')
            line_vals['expected_pay_date']=date_time
            
        if data.get('next_action_date'):
            date_time=datetime.strptime(data.get('next_action_date'),'%Y-%m-%d')
            line_vals['next_action_date']=date_time       

        if data.get('tax_ids'):         
            tax_list=[]
            for line_tax in data.get('tax_ids'):
                domain = [('amount', '=', line_tax['amount']),('type_tax_use', '=', line_tax['type_tax_use']['sh_api_current_state'])]
                find_tax = self.env['account.tax'].search(domain,limit=1)
                if find_tax:
                    tax_list.append((4,find_tax.id)) 
            if tax_list:
                line_vals['tax_ids']=tax_list        
        
        if data.get('currency_id'):
            domain=[('name','=',data.get('currency_id').get('name'))]
            find_currency_id=self.env['res.currency'].search(domain,limit=1)
            if find_currency_id:
                line_vals['currency_id']=find_currency_id.id  
                
        if data.get('partner_id'):         
            domain = [('remote_res_partner_id', '=', data['partner_id']['id'])]
            find_customer = self.env['res.partner'].search(domain)
            if find_customer:
                line_vals['partner_id'] = find_customer.id
            else:
                contact_vals=self.process_contact_data(data['partner_id'])
                partner_id=self.env['res.partner'].create(contact_vals)
                if partner_id:
                    line_vals['partner_id']=partner_id.id         
        
        if data.get('product_id'):
            domain=[('remote_product_product_id','=',data.get('product_id').get('id'))]
            find_product=self.env['product.product'].search(domain,limit=1)
            if find_product:
                line_vals['product_id']=find_product.id   
                # print("\n\n=====line_vals.get('product_id')",line_vals.get('product_id'),data.get('product_id'))
            else:
                find_template=self.env['product.template'].search([('remote_product_template_id','=',data.get('product_id').get('product_tmpl_id'))])
                if find_template:
                    # print("\n\n==========find_template.product_variant_ids.mapped('id')",find_template.product_variant_ids.mapped('id'))
                    variant=find_template.product_variant_ids.mapped('id')[-1]   
                    # print("\nn=======variant",variant)
                    line_vals['product_id']=variant   
       
        if data.get('tax_line_id'):
            domain = [('amount', '=', data.get('tax_line_id')['amount']),('type_tax_use', '=', data.get('tax_line_id')['type_tax_use']['sh_api_current_state'])]
            find_tax = self.env['account.tax'].search(domain,limit=1)
            if find_tax:      
                line_vals['tax_line_id']=find_tax.id
         
        if data.get('analytic_line_ids'):
            analytic_line_list=self.process_timesheet_data(data.get('analytic_line_ids'))
            if analytic_line_list:
                line_vals['analytic_line_ids']=analytic_line_list         
                
        return line_vals
                        
    def account_move_id_data(self,data):
        move_vals={
            'remote_account_move_line_id':data.get('id'),
            'auto_reverse':data.get('auto_reverse'),
            'display_name':data.get('display_name'),
            'ref':data.get('ref'),
            'tax_type_domain':data.get('tax_type_domain'),
            'matched_percentage':data.get('matched_percentage'),
            'amount':data.get('amount'),
            'narration':data.get('narration'),
            'ref':data.get('ref'),
            'tax_type_domain':data.get('tax_type_domain'),
            'company_id':1,
        }   
        if data.get('date'):
            date_time=datetime.strptime(data.get('date'),'%Y-%m-%d')
            move_vals['date']=date_time 
            
        if data.get('reverse_date'):
            date_time=datetime.strptime(data.get('reverse_date'),'%Y-%m-%d')
            move_vals['reverse_date']=date_time      
                                 
        if data.get('currency_id'):
            domain=[('name','=',data.get('currency_id').get('name'))]
            find_currency_id=self.env['res.currency'].search(domain,limit=1)
            if find_currency_id:
                move_vals['currency_id']=find_currency_id.id                             

        if data.get('journal_id') and data.get('journal_id').get('id') and data.get('journal_id').get('id')!=0:
            domain=['|',('remote_account_journal_id','=',data.get('journal_id').get('id')),('code', '=', data['journal_id']['code'])]
            find_journal=self.env['account.journal'].search(domain,limit=1)
            if find_journal:
                move_vals['journal_id']=find_journal.id
            else:
                journal_vals={
                    'remote_account_journal_id':data.get('journal_id').get('id'),
                    'code':data.get('journal_id').get('code'),
                    'name':data.get('journal_id').get('name'),
                    'type':data.get('journal_id').get('type').get('sh_api_current_state'),
                }
                created_journal = self.env['account.journal'].create(journal_vals)
                if created_journal:
                    move_vals['journal_id']=created_journal.id
         
        if data.get('partner_id'):
            domain = [('remote_res_partner_id', '=', data['partner_id']['id'])]
            find_customer = self.env['res.partner'].search(domain)
            if find_customer:
                move_vals['partner_id'] = find_customer.id
            else:
                contact_vals=self.process_contact_data(data['partner_id'])
                partner_id=self.env['res.partner'].create(contact_vals)
                if partner_id:
                    move_vals['partner_id']=partner_id.id       
                               
        if data.get('line_ids'):
            line_list=[]
            for line in data.get('line_ids'):
                line_vals=self.account_move_line_data(line)                          
                line_list.append((0,0,line_vals))     
            if line_list:
                move_vals['line_ids']=line_list                 
                                 
        return move_vals                 
                        
    def process_invoice_data(self,data):
        ''' ================= Import Invoices =============  '''
        invoice_list=[]
        payment_list = []
        # print("\n\n========data",data)
        for invoice in data:
            invoice_vals={
                'remote_account_move_id':invoice.get('id'),
                'name':invoice.get('number'),
                'message_has_error':invoice.get('message_has_error'),
                'message_is_follower':invoice.get('message_is_follower'),
                'message_needaction':invoice.get('message_needaction'),
                'display_name':invoice.get('display_name'),
                'invoice_origin':invoice.get('origin'),
                'ref':invoice.get('reference'),
                'invoice_source_email':invoice.get('source_email'),
                'amount_tax':invoice.get('amount_tax'),
                'amount_tax_signed':invoice.get('amount_tax_signed'),
                'amount_total':invoice.get('amount_total'),
                'amount_total_signed':invoice.get('amount_total_signed'),
                # 'amount_untaxed':invoice.get('amount_untaxed'),
                # 'amount_untaxed_signed':invoice.get('amount_untaxed_signed'),
                # 'amount_residual':invoice.get('residual'),
                # 'amount_residual_signed':invoice.get('residual_signed'),
                # 'amount_paid':invoice.get('total_paid'),
                'move_type':invoice.get('type').get('sh_api_current_state'),
                'access_warning':invoice.get('access_warning'),
                'invoice_outstanding_credits_debits_widget':invoice.get('outstanding_credits_debits_widget'),
                'invoice_payments_widget':invoice.get('payments_widget'),
                'invoice_payment_term_id':1,
                'company_id':1,
            }
            
            if invoice.get('date'):
                date_time=datetime.strptime(invoice.get('date'),'%Y-%m-%d')
                invoice_vals['date']=date_time
                
            if invoice.get('date_due'):
                date_time=datetime.strptime(invoice.get('date_due'),'%Y-%m-%d')
                invoice_vals['invoice_date_due']=date_time
                
            if invoice.get('date_invoice'):
                date_time=datetime.strptime(invoice.get('date_invoice'),'%Y-%m-%d')
                invoice_vals['invoice_date']=date_time
            
            # if invoice.get('message_partner_ids'):
            #     partner_list=[]
            #     for m_partner in invoice.get('message_partner_ids'):
            #         domain = [('remote_res_partner_id', '=',m_partner)]
            #         find_customer = self.env['res.partner'].search(domain)
                    
            #         # ======== CHECK IF PARTNER IS CREATED OR NOT IF CREATE THEN RETURN ELSE CREATE =======
            #         if find_customer:
            #             partner_list.append((4,find_customer.id))
            #     if partner_list:            
            #         invoice_vals['message_partner_ids']=partner_list
                    
            if invoice.get('user_id'):
                domain_by_id = [('remote_res_user_id','=',invoice.get('user_id'))]
                find_user_id=self.env['res.users'].search(domain_by_id)
                if find_user_id:   
                    invoice_vals['invoice_user_id']=find_user_id.id


            if invoice.get('project_task_id'):
                project_task_list=[]
                for task in invoice.get('project_task_id'):
                    domain=[('remote_project_task_id','=',task)]
                    find_task=self.env['project.task'].search(domain)
                    if find_task:        
                        project_task_list.append((4,find_task.id))    
                if project_task_list:
                    invoice_vals['project_task_id']=project_task_list          
            
            if invoice.get('responsible_user_ids'):
                user_list=[]
                for user in invoice.get('responsible_user_ids'):
                    if user and user!=0:
                        domain_by_id = [('remote_res_user_id','=',invoice['user_id'])]
                        find_user_id=self.env['res.users'].search(domain_by_id)
                        if find_user_id:
                            user_list.append((4,find_user_id.id))
                if user_list:
                    invoice_vals['responsible_user_ids']=user_list
                    
            if invoice.get('sh_invoice_task_ids'):
                invoice_task_list=[]
                for task in invoice.get('sh_invoice_task_ids'):
                    domain=[('remote_project_task_id','=',task)]
                    find_task=self.env['project.task'].search(domain)
                    if find_task:           
                        invoice_task_list.append((4,find_task.id))
                if invoice_task_list:
                    invoice_vals['sh_invoice_task_ids']=invoice_task_list
            
            if invoice.get('sh_ticket_ids'):
                ticket_list=[]
                for ticket in invoice.get('sh_ticket_ids'):
                    domain=[('remote_sh_helpdesk_ticket_id','=',ticket)]      
                    find_ticket = self.env['sh.helpdesk.ticket'].search(domain)
                    if find_ticket:
                        ticket_list.append((4,find_ticket.id))  
                if ticket_list:
                    invoice_vals['sh_ticket_ids']=ticket_list   
                    
            if invoice.get('version_ids'):
                version_list=[]
                for version in invoice.get('version_ids'):
                    domain=[('remote_sh_version_id','=',version.get('id'))]
                    find_version=self.env['sh.version'].search(domain)
                    if find_version:
                        version_list.append((4,find_version.id))
                    else:
                        version_vals={
                            'remote_sh_version_id':version.get('id'),
                            'display_name':version.get('display_name'),
                            'name':version.get('name'), 
                            'company_id':1,                       
                        }
                        created_version=self.env['sh.version'].create(version_vals)
                        if created_version:
                            version_list.append((4,created_version.id))
                if version_list:
                    invoice_vals['version_ids']=version_list       

            if invoice.get('currency_id'):                       
                domain=[('name','=',invoice.get('currency_id').get('name'))]
                find_currency_id=self.env['res.currency'].search(domain,limit=1)
                if find_currency_id:
                    invoice_vals['currency_id']=find_currency_id.id
                                            
            # ======== Get partner if already created or create =====
            if invoice.get('partner_id'):
                domain = [('remote_res_partner_id', '=', invoice['partner_id'])]
                find_customer = self.env['res.partner'].search(domain)
                if find_customer:
                    invoice_vals['partner_id'] = find_customer.id
            
            # ============== Manage Journal ==========
            if invoice.get('journal_id') and invoice.get('journal_id').get('id') and invoice.get('journal_id').get('id')!=0:
                domain=['|',('remote_account_journal_id','=',invoice.get('journal_id').get('id')),('code', '=', invoice['journal_id']['code'])]
                find_journal=self.env['account.journal'].search(domain,limit=1)
                if find_journal:
                    invoice_vals['journal_id']=find_journal.id
                else:
                    journal_vals={
                    'remote_account_journal_id':invoice.get('journal_id').get('id'),
                    'code':invoice.get('journal_id').get('code'),
                    'name':invoice.get('journal_id').get('name'),
                    'type':invoice.get('journal_id').get('type').get('sh_api_current_state'),
                    }
                    created_journal = self.env['account.journal'].create(journal_vals)
                    if created_journal:
                        invoice_vals['journal_id']=created_journal.id
                    

            if invoice.get('medium_id') and invoice.get('medium_id').get('id') and invoice.get('medium_id').get('id')!=0:
                domain = ['|', ('remote_medium_id', '=', invoice['medium_id']['id']),('name', '=', invoice['medium_id']['name'])]
                find_rec = self.env['utm.medium'].search(domain,limit=1)
                if find_rec:
                    invoice_vals['medium_id'] = find_rec.id
                else:
                    medium_vals = {
                        'remote_medium_id': invoice['medium_id']['id'],
                        'name': invoice['medium_id']['name'],
                        'display_name': invoice['medium_id']['display_name'],
                        'active': invoice['medium_id']['active'],
                    }
                    created_rec = self.env['utm.medium'].create(medium_vals)
                    if created_rec:
                        invoice_vals['medium_id'] = created_rec.id

            # ======== Get partner if already created or create =====

            if invoice.get('partner_shipping_id'):
                domain = [('remote_res_partner_id', '=', invoice['partner_shipping_id'])]
                find_customer = self.env['res.partner'].search(domain)
                if find_customer:
                    invoice_vals['partner_shipping_id'] = find_customer.id       

            if invoice.get('responsible_user_id') and invoice.get('responsible_user_id') and invoice.get('responsible_user_id')!=0:
                domain_by_id = [('remote_res_user_id','=',invoice['responsible_user_id'])]
                find_user_id=self.env['res.users'].search(domain_by_id)
                if find_user_id:
                    invoice_vals['responsible_user_id']=find_user_id.id 
                
            if invoice.get('source_id') and invoice.get('source_id').get('id') and invoice.get('source_id').get('id')!=0:
                domain = ['|', ('remote_source_id', '=', invoice.get('source_id').get('id')),
                          ('name', '=', invoice.get('source_id').get('name'))]
                find_rec = self.env['utm.source'].search(domain)
                if find_rec:
                    invoice_vals['source_id'] = find_rec.id
                else:
                    source_vals = {
                        'remote_source_id': invoice.get('source_id').get('id'),
                        'name': invoice.get('source_id').get('name'),
                        'display_name': invoice.get('source_id').get('display_name'),
                    }
                    created_rec = self.env['utm.source'].create(source_vals)
                    if created_rec:
                        invoice_vals['source_id'] = created_rec.id
                        
            if invoice.get('team_id'):
                domain=[('remote_crm_team_id','=',invoice.get('team_id').get('id'))]    
                find_crm_team_id=self.env['crm.team'].search(domain)
                
                # =========== CHECK IF CREATED TEAM OR NOT IF CREATE THEN RETURN ELSE CREATE AND RETURN =============
                if find_crm_team_id:
                    invoice_vals['team_id']=find_crm_team_id.id 
                else:
                    team_vals=self.process_crm_team_data(invoice['team_id'])       
                    team_id=self.env['crm.team'].create(team_vals)
                    if team_id:
                        invoice_vals['team_id']=team_id.id          
                        
            if invoice.get('user_id') and invoice.get('user_id')!=0:
                domain_by_id = [('remote_res_user_id','=',invoice['user_id'])]
                find_user_id=self.env['res.users'].search(domain_by_id)
                if find_user_id:
                    invoice_vals['user_id']=find_user_id.id      

            # if invoice.get('message_ids'):    
            #     message_list = []
            #     message_list_create=[]
            #     remain_mail=[]           
            #     for message in invoice.get('message_ids'):   
            #         if message['id']:             
            #             domain = [('remote_mail_message_id','=',message['id'])]
            #             find_message = self.env['mail.message'].search(domain,limit=1)                    
            #             if find_message:
            #                 message_list.append((4,find_message.id))
            #             else:
            #                 remain_mail.append(message)
            #     if remain_mail:
            #         message_list_create = self.process_message_data(remain_mail)
            #         if message_list_create:
            #             for message in message_list_create:
            #                 if message[2].get('model') and message[2].get('model')=='account.invoice':
            #                     message[2]['model']='account.move'                                             
                                
            #     invoice_vals['message_ids']=message_list+message_list_create                           

            if invoice.get('timesheet_ids'):
                timesheet_list=self.process_timesheet_data(invoice.get('timesheet_ids'))
                if timesheet_list:
                    invoice_vals['timesheet_ids']=timesheet_list 
                                       
            # ======== Prepare Invoice lines ==========
            if invoice.get('invoice_line_ids'):
                if len(invoice.get('invoice_line_ids'))<=100:
                    invoice_line_list = self.process_account_move_data(invoice.get('invoice_line_ids'))
                    if invoice_line_list:
                        invoice_vals['invoice_line_ids']= invoice_line_list
            
            if invoice.get('message_follower_ids'):
                # follower_ids=[]
                # for follower in invoice.get('message_follower_ids'):
                #     if follower.get('partner_id'):
                #         domain = [('remote_res_partner_id', '=', follower.get('partner_id'))]
                #         find_customer = self.env['res.partner'].search(domain)
                #         if find_customer:
                #             follower_ids.append(find_customer.id)
                invoice_vals['message_follower_ids']= invoice.get('message_follower_ids')

            if invoice.get('paypal_bank_transfer_id'):
                domain=[('remote_account_move_id','=',invoice.get('paypal_bank_transfer_id').get('id'))] 
                find_move=self.env['account.move'].search(domain)
                if find_move:
                    invoice_vals['paypal_bank_transfer_id']= find_move.id

            print("\n\n========invoice.get('payment_ids')",invoice.get('payment_ids'))

            if invoice.get('payment_ids'):

                payment_ids=self.process_account_payment_data(invoice.get('payment_ids'))                
                payment_list+=payment_ids
            invoice_list.append((0,0,invoice_vals))

        return invoice_list,payment_list
     
     
    def process_invoice_id_data(self,invoice):
        ''' ================= Import Invoices =============  '''

        invoice_vals={
            'remote_account_move_id':invoice.get('id'),
            'name':invoice.get('number'),
            'message_has_error':invoice.get('message_has_error'),
            'message_is_follower':invoice.get('message_is_follower'),
            'message_needaction':invoice.get('message_needaction'),
            'display_name':invoice.get('display_name'),
            'invoice_origin':invoice.get('origin'),
            'ref':invoice.get('reference'),
            'invoice_source_email':invoice.get('source_email'),
            'amount_tax':invoice.get('amount_tax'),
            'amount_tax_signed':invoice.get('amount_tax_signed'),
            'amount_total':invoice.get('amount_total'),
            'amount_total_signed':invoice.get('amount_total_signed'),
            # 'amount_untaxed':invoice.get('amount_untaxed'),
            # 'amount_untaxed_signed':invoice.get('amount_untaxed_signed'),
            # 'amount_residual':invoice.get('residual'),
            # 'amount_residual_signed':invoice.get('residual_signed'),
            # 'amount_paid':invoice.get('total_paid'),
            'move_type':invoice.get('type').get('sh_api_current_state'),
            'access_warning':invoice.get('access_warning'),
            'invoice_outstanding_credits_debits_widget':invoice.get('outstanding_credits_debits_widget'),
            'invoice_payments_widget':invoice.get('payments_widget'),
            'invoice_payment_term_id':1,
            'company_id':1,
        }
        
        if invoice.get('date'):
            date_time=datetime.strptime(invoice.get('date'),'%Y-%m-%d')
            invoice_vals['date']=date_time
            
        if invoice.get('date_due'):
            date_time=datetime.strptime(invoice.get('date_due'),'%Y-%m-%d')
            invoice_vals['invoice_date_due']=date_time
            
        if invoice.get('date_invoice'):
            date_time=datetime.strptime(invoice.get('date_invoice'),'%Y-%m-%d')
            invoice_vals['invoice_date']=date_time
        
        # if invoice.get('message_partner_ids'):
        #     partner_list=[]
        #     for m_partner in invoice.get('message_partner_ids'):
        #         domain = [('remote_res_partner_id', '=',m_partner)]
        #         find_customer = self.env['res.partner'].search(domain)
                
        #         # ======== CHECK IF PARTNER IS CREATED OR NOT IF CREATE THEN RETURN ELSE CREATE =======
        #         if find_customer:
        #             partner_list.append((4,find_customer.id))
        #     if partner_list:            
        #         invoice_vals['message_partner_ids']=partner_list
                
        if invoice.get('project_task_id'):
            project_task_list=[]
            for task in invoice.get('project_task_id'):
                domain=[('remote_project_task_id','=',task)]
                find_task=self.env['project.task'].search(domain)
                if find_task:        
                    project_task_list.append((4,find_task.id))    
            if project_task_list:
                invoice_vals['project_task_id']=project_task_list  
                
        if invoice.get('responsible_user_ids'):
            user_list=[]
            for user in invoice.get('responsible_user_ids'):
                if user and user!=0:
                    domain_by_id = [('remote_res_user_id','=',invoice['user_id'])]
                    find_user_id=self.env['res.users'].search(domain_by_id)
                    if find_user_id:
                        user_list.append((4,find_user_id.id))

            if user_list:
                invoice_vals['responsible_user_ids']=user_list
                
        if invoice.get('sh_invoice_task_ids'):
            invoice_task_list=[]
            for task in invoice.get('sh_invoice_task_ids'):
                domain=[('remote_project_task_id','=',task)]
                find_task=self.env['project.task'].search(domain)
                if find_task:           
                    invoice_task_list.append((4,find_task.id))
            if invoice_task_list:
                invoice_vals['sh_invoice_task_ids']=invoice_task_list
        
        if invoice.get('sh_ticket_ids'):
            ticket_list=[]
            for ticket in invoice.get('sh_ticket_ids'):
                domain=[('remote_sh_helpdesk_ticket_id','=',ticket)]      
                find_ticket = self.env['sh.helpdesk.ticket'].search(domain)
                if find_ticket:
                    ticket_list.append((4,find_ticket.id))
            if ticket_list:
                invoice_vals['sh_ticket_ids']=ticket_list   
                
        if invoice.get('version_ids'):
            version_list=[]
            for version in invoice.get('version_ids'):
                domain=[('remote_sh_version_id','=',version.get('id'))]
                find_version=self.env['sh.version'].search(domain)
                if find_version:
                    version_list.append((4,find_version.id))
                else:
                    version_vals={
                        'remote_sh_version_id':version.get('id'),
                        'display_name':version.get('display_name'),
                        'name':version.get('name'), 
                        'company_id':1,                       
                    }
                    created_version=self.env['sh.version'].create(version_vals)
                    if created_version:
                        version_list.append((4,created_version.id))
            if version_list:
                invoice_vals['version_ids']=version_list                  
                
        if invoice.get('currency_id'):                       
            domain=[('name','=',invoice.get('currency_id').get('name'))]
            find_currency_id=self.env['res.currency'].search(domain,limit=1)
            # print("\nn\======find_currency_id",find_currency_id)
            if find_currency_id:
                invoice_vals['currency_id']=find_currency_id.id
        # print("\n\n=====invoice_vals",invoice_vals)
                                        
        # ======== Get partner if already created or create =====
        if invoice.get('partner_id'):
            domain = [('remote_res_partner_id', '=', invoice['partner_id'])]
            find_customer = self.env['res.partner'].search(domain)
            if find_customer:
                invoice_vals['partner_id'] = find_customer.id
        
        # ============== Manage Journal ==========
        if invoice.get('journal_id') and invoice.get('journal_id').get('id') and invoice.get('journal_id').get('id')!=0:
            domain=['|',('remote_account_journal_id','=',invoice.get('journal_id').get('id')),('code', '=', invoice['journal_id']['code'])]
            find_journal=self.env['account.journal'].search(domain,limit=1)
            if find_journal:
                invoice_vals['journal_id']=find_journal.id
            else:
                journal_vals={
                'remote_account_journal_id':invoice.get('journal_id').get('id'),
                'code':invoice.get('journal_id').get('code'),
                'name':invoice.get('journal_id').get('name'),
                'type':invoice.get('journal_id').get('type').get('sh_api_current_state'),
                }
                created_journal = self.env['account.journal'].create(journal_vals)
                if created_journal:
                    invoice_vals['journal_id']=created_journal.id
                
        if invoice.get('medium_id') and invoice.get('medium_id').get('id') and invoice.get('medium_id').get('id')!=0 :
            domain = ['|', ('remote_medium_id', '=', invoice['medium_id']['id']),('name', '=', invoice['medium_id']['name'])]
            find_rec = self.env['utm.medium'].search(domain,limit=1)
            if find_rec:
                invoice_vals['medium_id'] = find_rec.id
            else:
                medium_vals = {
                    'remote_medium_id': invoice['medium_id']['id'],
                    'name': invoice['medium_id']['name'],
                    'display_name': invoice['medium_id']['display_name'],
                    'active': invoice['medium_id']['active'],
                }
                created_rec = self.env['utm.medium'].create(medium_vals)
                if created_rec:
                    invoice_vals['medium_id'] = created_rec.id

        # ======== Get partner if already created or create =====
        if invoice.get('partner_shipping_id'):
            domain = [('remote_res_partner_id', '=', invoice['partner_shipping_id'])]
            find_customer = self.env['res.partner'].search(domain)
            if find_customer:
                invoice_vals['partner_shipping_id'] = find_customer.id      

        if invoice.get('responsible_user_id'):
            domain_by_id = [('remote_res_user_id','=',invoice['responsible_user_id'])]
            find_user_id=self.env['res.users'].search(domain_by_id)
            if find_user_id:
                invoice_vals['responsible_user_id']=find_user_id.id 
            
        if invoice.get('source_id') and invoice.get('source_id').get('id') and invoice.get('source_id').get('id')!=0:
            domain = ['|', ('remote_source_id', '=', invoice.get('source_id').get('id')),
                        ('name', '=', invoice.get('source_id').get('name'))]
            find_rec = self.env['utm.source'].search(domain)
            if find_rec:
                invoice_vals['source_id'] = find_rec.id
            else:
                source_vals = {
                    'remote_source_id': invoice.get('source_id').get('id'),
                    'name': invoice.get('source_id').get('name'),
                    'display_name': invoice.get('source_id').get('display_name'),
                }
                created_rec = self.env['utm.source'].create(source_vals)
                if created_rec:
                    invoice_vals['source_id'] = created_rec.id
                    
        if invoice.get('team_id'):
            domain=[('remote_crm_team_id','=',invoice.get('team_id').get('id'))]    
            find_crm_team_id=self.env['crm.team'].search(domain)
            
            # =========== CHECK IF CREATED TEAM OR NOT IF CREATE THEN RETURN ELSE CREATE AND RETURN =============
            if find_crm_team_id:
                invoice_vals['team_id']=find_crm_team_id.id 
            else:
                team_vals=self.process_crm_team_data(invoice['team_id'])       
                team_id=self.env['crm.team'].create(team_vals)
                if team_id:
                    invoice_vals['team_id']=team_id.id          
                    
        if invoice.get('user_id'):
            domain_by_id = [('remote_res_user_id','=',invoice['user_id'])]
            find_user_id=self.env['res.users'].search(domain_by_id)
            if find_user_id:
                invoice_vals['user_id']=find_user_id.id                   
            
        # if invoice.get('message_ids'):
        #     message_list = []
        #     message_list_create=[]
        #     remain_mail=[]           
        #     for message in invoice.get('message_ids'):   
        #         if message['id']:             
        #             domain = [('remote_mail_message_id','=',message['id'])]
        #             find_message = self.env['mail.message'].search(domain,limit=1)                    
        #             if find_message:
        #                 message_list.append((4,find_message.id))
        #             else:
        #                 remain_mail.append(message)
        #     if remain_mail:
        #         message_list_create = self.process_message_data(remain_mail)
        #         if message_list_create:
        #             for message in message_list_create:
        #                 if message[2].get('model') and message[2].get('model')=='account.invoice':
        #                     message[2]['model']='account.move'                                             
                            
        #     invoice_vals['message_ids']=message_list+message_list_create 
            
        if invoice.get('timesheet_ids'):
            timesheet_list=self.process_timesheet_data(invoice.get('timesheet_ids'))
            if timesheet_list:
                invoice_vals['timesheet_ids']=timesheet_list 
                                    
        # ======== Prepare Invoice lines ==========
                            
        if invoice.get('invoice_line_ids'):
            invoice_line_list = self.process_account_move_data(invoice.get('invoice_line_ids'))
            if invoice_line_list:
                invoice_vals['invoice_line_ids']= invoice_line_list
        
        if invoice.get('paypal_bank_transfer_id'):
            domain=[('remote_account_move_id','=',invoice.get('paypal_bank_transfer_id').get('id'))] 
            find_move=self.env['account.move'].search(domain)
            if find_move:
                invoice_vals['paypal_bank_transfer_id']= find_move.id
                       
        return invoice_vals
    
