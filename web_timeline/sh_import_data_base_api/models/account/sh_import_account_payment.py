# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
import requests
import json
from datetime import datetime

class InheritImportBase(models.Model):
    _inherit = "sh.import.base"
    
    def auto_import_account_payment(self):
        confid = self.env['sh.import.base'].search([],limit=1)
        failed=0
        count=0
        if confid.import_payment and  confid.payment_ids:
            payment_ids = confid.payment_ids.strip('][').split(', ')  
            for pay in payment_ids[0:30]:
                payment=confid.import_account_payment(pay)
                if payment:
                    domain=[('remote_account_payment_id','=',payment.get('remote_account_payment_id'))]
                    already_payment = self.env['account.payment'].search(domain,limit=1)
                    connected_invoice_ids=[]
                    if 'invoice_ids' in  payment:
                        connected_invoice_ids=payment.get('invoice_ids')
                        del payment['invoice_ids']
                    state='draft'
                    if already_payment:
                        if payment.get('state')=='cancelled':
                            state='cancel'
                            payment['state']='draft'
                        if payment.get('state') in ['posted','sent','reconciled']:
                            state='posted'
                            
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
            
                    if created_payment and connected_invoice_ids:   
                        if created_payment.state=='posted':
                            for inv in connected_invoice_ids:
                                invoice=self.env['account.move'].search([('remote_account_move_id','=',inv)])
                                if invoice and invoice.state not in ['cancel','draft']:  
                                    lines = (created_payment.line_ids + invoice.line_ids).filtered(
                                        lambda l: l.account_id.account_type == 'asset_receivable' and not l.reconciled)
                                    lines.reconcile()
                    count+=1 
                else:
                    failed+=1
                                       
            confid.payment_ids='['+', '.join([str(elem) for elem in payment_ids[30:]])+']'
            
            if count > 0:              
                vals = {
                    "name": confid.name,
                    "state": "success",
                    "field_type": "invoice",
                    "error": "%s Payment Update Successfully" %(count),
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
                    "error": "%s Failed To Update" %(failed),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals) 
        
    def import_account_payment(self,payment_id):
        if payment_id:
            response = requests.get('''%s/api/public/account.payment/%s?query={*,currency_id{name},currency{name},currency_of_fees{name},message_ids{id,subtype_id{*},author_id,body,channel_ids{*},date,display_name,email_from,has_error,layout,mail_activity_type_id{*},message_id,message_type,model,moderation_status,moderator_id,need_moderation,needaction,no_auto_thread,notification_ids,rating_value,record_name,reply_to,res_id,starred,subject},currency_id{name},payment_method_id{*},paypal_bank_transfer_id{*,currency_id{name},dummy_account_id{*,tag_ids{*},tax_ids{*},user_type_id{*}},journal_id{id,name,type,code},line_ids{*,tax_ids{*},account_id{*,tag_ids{*},tax_ids{*},user_type_id{*}},currency_id{name},journal_id{id,name,type,code},tax_line_id{*},
                    analytic_line_ids{*}}},destination_account_id{*,tag_ids{*},tax_ids{*},user_type_id{*}},destination_journal_id{id,name,type,code},journal_id{id,name,type,code},partner_bank_account_id{*}}
                ''' %(self.base_url,payment_id))
            if response.status_code == 200:
                response_json = response.json()
                for data in response_json.get('result'):
                    payment_data=self.process_account_payment_id_data(data)
                    print("\n\n======payment_data",payment_data)
                return payment_data


    def process_account_payment_id_data(self,data):
        ''' ============== PREPARE VALUES FOR IMPORT ACCOUNT PAYMENT WHICH ARE CONNECTED WITH INVOICE ============== '''
        # print("\n\n\nn0",data)
        payment_vals={
            'remote_account_payment_id':data.get('id'),
            'message_has_error':data.get('message_has_error'),
            'message_is_follower':data.get('message_is_follower'),
            'message_needaction':data.get('message_needaction'),
            'show_partner_bank_account':data.get('show_partner_bank_account'),
            'display_name':data.get('display_name'),
            'name':data.get('name'),
            'payment_method_code':data.get('payment_method_code'),
            'payment_reference':data.get('payment_reference'),
            'paypal_fees':data.get('paypal_fees'),
            'message_has_error_counter':data.get('message_has_error_counter'),
            'message_needaction_counter':data.get('message_needaction_counter'),
            'invoice_ids':data.get('invoice_ids'), 
            'actual_received_amount':data.get('actual_received_amount'),
            'amount':data.get('amount'),
            'partner_type':data.get('partner_type').get('sh_api_current_state'),
            'payment_type':data.get('payment_type').get('sh_api_current_state'),
            'state':data.get('state').get('sh_api_current_state'),
            'company_id':1,
        }
        if data.get('payment_date'):
            date_time=datetime.strptime(data.get('payment_date'),'%Y-%m-%d')
            payment_vals['date']=date_time
        
        # ============== Check cashier is exist or not if exist then return else create ==============
        if data.get('cashier'):
            domain_by_id = [('remote_user_id','=',data['cashier']['id'])]
            find_user_id=self.env['res.users'].search(domain_by_id)
            if find_user_id:
                payment_vals['user_id']=find_user_id.id 

        # if data.get('message_partner_ids'):
        #     partner_list=[]
        #     for m_partner in data.get('message_partner_ids'):
        #         domain = [('remote_res_partner_id', '=',m_partner)]
        #         find_customer = self.env['res.partner'].search(domain)
                
        #         # ======== CHECK IF PARTNER IS CREATED OR NOT IF CREATE THEN RETURN ELSE CREATE =======
        #         if find_customer:
        #             partner_list.append((4,find_customer.id))
        #     if partner_list:            
        #         payment_vals['message_partner_ids']=partner_list 

        if data.get('currency_id'):
            domain=[('name','=',data.get('currency_id').get('name'))]
            find_currency_id=self.env['res.currency'].search(domain,limit=1)
            if find_currency_id:
                payment_vals['currency_id']=find_currency_id.id  

        if data.get('currency'):
            domain=[('name','=',data.get('currency').get('name'))]
            find_currency_id=self.env['res.currency'].search(domain,limit=1)
            if find_currency_id:
                payment_vals['currency']=find_currency_id.id   
                        
        if data.get('currency_of_fees'):
            domain=[('name','=',data.get('currency_of_fees').get('name'))]
            find_currency_id=self.env['res.currency'].search(domain,limit=1)
            if find_currency_id:
                payment_vals['currency_of_fees']=find_currency_id.id             

        if data.get('destination_account_id'):
            domain=['|',('remote_account_account_id','=',data.get('destination_account_id').get('id')),('code','=',data.get('destination_account_id').get('code'))]
            find_account=self.env['account.account'].search(domain)
            if find_account:
                payment_vals['destination_account_id']=find_account.id
                        
        
        # ============ Connect Journal with Payment if already exist then return otherwise create ====================
        if data.get('destination_journal_id') and data.get('destination_journal_id').get('id') and data.get('destination_journal_id').get('id')!=0:
            domain=['|',('remote_account_journal_id','=',data.get('destination_journal_id').get('id')),('code', '=', data['destination_journal_id']['code'])]
            find_journal=self.env['account.journal'].search(domain)
            if find_journal:
                payment_vals['destination_journal_id']=find_journal.id
            else:
                journal_vals={
                'remote_account_journal_id':data.get('destination_journal_id').get('id'),
                'code':data.get('destination_journal_id').get('code'),
                'name':data.get('destination_journal_id').get('name'),
                'type':data.get('destination_journal_id').get('type').get('sh_api_current_state'),
                }
                created_journal = self.env['account.journal'].create(journal_vals)
                if created_journal:
                    payment_vals['destination_journal_id']=created_journal.id
        
        # ============ Connect Journal with Payment if already exist then return otherwise create ====================
        if data.get('journal_id') and data.get('journal_id').get('id') and data.get('journal_id').get('id')!=0:
            domain=['|',('remote_account_journal_id','=',data.get('journal_id').get('id')),('code', '=', data['journal_id']['code'])]
            find_journal=self.env['account.journal'].search(domain)
            if find_journal:
                payment_vals['journal_id']=find_journal.id 
            else:
                journal_vals={
                'remote_account_journal_id':data.get('journal_id').get('id'),
                'code':data.get('journal_id').get('code'),
                'name':data.get('journal_id').get('name'),
                'type':data.get('journal_id').get('type').get('sh_api_current_state'),
                }
                created_journal = self.env['account.journal'].create(journal_vals)
                if created_journal:
                    payment_vals['journal_id']=created_journal.id  
            
        
        if data.get('partner_id'):
            domain = [('remote_res_partner_id', '=', data['partner_id'])]
            find_customer = self.env['res.partner'].search(domain)
            if find_customer:
                payment_vals['partner_id'] = find_customer.id

        # ================= CHECK PAYMENT METHOD WHICH IS CONNECTED WITH ACCOUNT PAYMENT =============
        if data.get('payment_method_id'):
            domain=['|',('remote_account_payment_method_id','=',data.get('payment_method_id').get('id')),('code','=',data.get('payment_method_id').get('code'))]
            find_payment_method=self.env['account.payment.method'].search(domain,limit=1)
            if find_payment_method:
                payment_vals['payment_method_id']=find_payment_method.id
            else:
                payment_method_vals={
                    'remote_account_payment_method_id':data.get('payment_method_id').get('id'),
                    'code':data.get('payment_method_id').get('code'),
                    'name':data.get('payment_method_id').get('name'),
                    'display_name':data.get('payment_method_id').get('display_name'),
                    'payment_type':data.get('payment_method_id').get('payment_type').get('sh_api_current_state'),
                }
                if payment_method_vals:
                    created_payment_method=self.env['account.payment.method'].create(payment_method_vals)
                    if created_payment_method:
                        payment_vals['payment_method_id']=created_payment_method.id                
        
        # =========== Mapped Writeoff account with name or id if not match any then create new account ============
        # if data.get('writeoff_account_id') and data.get('writeoff_account_id').get('id') and data.get('writeoff_account_id').get('id')!=0:
        #     domain=['|',('remote_account_account_id','=',data.get('writeoff_account_id').get('id')),('name','=',data.get('writeoff_account_id').get('name'))]
        #     find_account=self.env['account.account'].search(domain)
        #     if find_account:
        #         payment_vals['writeoff_account_id']=find_account.id

        # ========== CHECK CONNCTED PARTNER IS EXIST OR NOT  =====================
        if payment_vals.get('journal_id') and payment_vals.get('payment_method_id')  :
            
            self._cr.execute('''select id from account_payment_method_line where journal_id = %s and payment_method_id = %s ''',
                [payment_vals.get('journal_id'),payment_vals.get('payment_method_id')])
            payment_method_line = self._cr.dictfetchall()    
            
            if payment_method_line:
                payment_vals['payment_method_line_id']=payment_method_line[0].get('id')   
                
        # if data.get('message_ids'):
        #     message_list=self.process_message_data(data.get('message_ids'))
        #     if message_list:
        #         payment_vals['message_ids']=message_list   
                    
             
        return payment_vals


    def process_account_payment_data(self,payment):
        ''' ============== PREPARE VALUES FOR IMPORT ACCOUNT PAYMENT WHICH ARE CONNECTED WITH INVOICE ============== '''
        payment_list=[]
        # print("\n\n\nn0",payment)
        for data in payment:
            payment_vals={
                'remote_account_payment_id':data.get('id'),
                'message_has_error':data.get('message_has_error'),
                'message_is_follower':data.get('message_is_follower'),
                'message_needaction':data.get('message_needaction'),
                'show_partner_bank_account':data.get('show_partner_bank_account'),
                'display_name':data.get('display_name'),
                'name':data.get('name'),
                'payment_method_code':data.get('payment_method_code'),
                'payment_reference':data.get('payment_reference'),
                'paypal_fees':data.get('paypal_fees'),
                'message_has_error_counter':data.get('message_has_error_counter'),
                'message_needaction_counter':data.get('message_needaction_counter'),
                'invoice_ids':data.get('invoice_ids'), 
                'actual_received_amount':data.get('actual_received_amount'),
                'amount':data.get('amount'),
                'partner_type':data.get('partner_type').get('sh_api_current_state'),
                'payment_type':data.get('payment_type').get('sh_api_current_state'),
                'state':data.get('state').get('sh_api_current_state'),
                'company_id':1,
            }
            if data.get('payment_date'):
                date_time=datetime.strptime(data.get('payment_date'),'%Y-%m-%d')
                payment_vals['date']=date_time
            
            # ============== Check cashier is exist or not if exist then return else create ==============
            if data.get('cashier'):
                domain_by_id = [('remote_user_id','=',data['cashier']['id'])]
                find_user_id=self.env['res.users'].search(domain_by_id)
                if find_user_id:
                    payment_vals['user_id']=find_user_id.id 

            # if data.get('message_partner_ids'):
            #     partner_list=[]
            #     for m_partner in data.get('message_partner_ids'):
            #         domain = [('remote_res_partner_id', '=',m_partner)]
            #         find_customer = self.env['res.partner'].search(domain)
                    
            #         # ======== CHECK IF PARTNER IS CREATED OR NOT IF CREATE THEN RETURN ELSE CREATE =======
            #         if find_customer:
            #             partner_list.append((4,find_customer.id))
            #     if partner_list:            
            #         payment_vals['message_partner_ids']=partner_list 

            if data.get('currency_id'):
                domain=[('name','=',data.get('currency_id').get('name'))]
                find_currency_id=self.env['res.currency'].search(domain,limit=1)
                if find_currency_id:
                    payment_vals['currency_id']=find_currency_id.id  

            if data.get('currency'):
                domain=[('name','=',data.get('currency').get('name'))]
                find_currency_id=self.env['res.currency'].search(domain,limit=1)
                if find_currency_id:
                    payment_vals['currency']=find_currency_id.id   
                          
            if data.get('currency_of_fees'):
                domain=[('name','=',data.get('currency_of_fees').get('name'))]
                find_currency_id=self.env['res.currency'].search(domain,limit=1)
                if find_currency_id:
                    payment_vals['currency_of_fees']=find_currency_id.id             

            if data.get('destination_account_id'):
                domain=['|',('remote_account_account_id','=',data.get('destination_account_id').get('id')),('code','=',data.get('destination_account_id').get('code'))]
                find_account=self.env['account.account'].search(domain)
                if find_account:
                    payment_vals['destination_account_id']=find_account.id
                          
            
            # ============ Connect Journal with Payment if already exist then return otherwise create ====================
            if data.get('destination_journal_id') and data.get('destination_journal_id').get('id') and data.get('destination_journal_id').get('id')!=0:
                domain=['|',('remote_account_journal_id','=',data.get('destination_journal_id').get('id')),('code', '=', data['destination_journal_id']['code'])]
                find_journal=self.env['account.journal'].search(domain)
                if find_journal:
                    payment_vals['destination_journal_id']=find_journal.id
                else:
                    journal_vals={
                    'remote_account_journal_id':data.get('destination_journal_id').get('id'),
                    'code':data.get('destination_journal_id').get('code'),
                    'name':data.get('destination_journal_id').get('name'),
                    'type':data.get('destination_journal_id').get('type').get('sh_api_current_state'),
                    }
                    created_journal = self.env['account.journal'].create(journal_vals)
                    if created_journal:
                        payment_vals['destination_journal_id']=created_journal.id
            
            # ============ Connect Journal with Payment if already exist then return otherwise create ====================
            if data.get('journal_id') and data.get('journal_id').get('id') and data.get('journal_id').get('id')!=0:
                domain=['|',('remote_account_journal_id','=',data.get('journal_id').get('id')),('code', '=', data['journal_id']['code'])]
                find_journal=self.env['account.journal'].search(domain)
                if find_journal:
                    payment_vals['journal_id']=find_journal.id 
                else:
                    journal_vals={
                    'remote_account_journal_id':data.get('journal_id').get('id'),
                    'code':data.get('journal_id').get('code'),
                    'name':data.get('journal_id').get('name'),
                    'type':data.get('journal_id').get('type').get('sh_api_current_state'),
                    }
                    created_journal = self.env['account.journal'].create(journal_vals)
                    if created_journal:
                        payment_vals['journal_id']=created_journal.id  
             
            
            if data.get('partner_id'):
                domain = [('remote_res_partner_id', '=', data['partner_id'])]
                find_customer = self.env['res.partner'].search(domain)
                if find_customer:
                    payment_vals['partner_id'] = find_customer.id

            # ================= CHECK PAYMENT METHOD WHICH IS CONNECTED WITH ACCOUNT PAYMENT =============
            if data.get('payment_method_id'):
                domain=['|',('remote_account_payment_method_id','=',data.get('payment_method_id').get('id')),('code','=',data.get('payment_method_id').get('code'))]
                find_payment_method=self.env['account.payment.method'].search(domain,limit=1)
                if find_payment_method:
                    payment_vals['payment_method_id']=find_payment_method.id
                else:
                    payment_method_vals={
                        'remote_account_payment_method_id':data.get('payment_method_id').get('id'),
                        'code':data.get('payment_method_id').get('code'),
                        'name':data.get('payment_method_id').get('name'),
                        'display_name':data.get('payment_method_id').get('display_name'),
                        'payment_type':data.get('payment_method_id').get('payment_type').get('sh_api_current_state'),
                    }
                    if payment_method_vals:
                        created_payment_method=self.env['account.payment.method'].create(payment_method_vals)
                        if created_payment_method:
                            payment_vals['payment_method_id']=created_payment_method.id                
            
            # =========== Mapped Writeoff account with name or id if not match any then create new account ============
            # if data.get('writeoff_account_id') and data.get('writeoff_account_id').get('id') and data.get('writeoff_account_id').get('id')!=0:
            #     domain=['|',('remote_account_account_id','=',data.get('writeoff_account_id').get('id')),('name','=',data.get('writeoff_account_id').get('name'))]
            #     find_account=self.env['account.account'].search(domain)
            #     if find_account:
            #         payment_vals['writeoff_account_id']=find_account.id

            # ========== CHECK CONNCTED PARTNER IS EXIST OR NOT  =====================
            if payment_vals.get('journal_id') and payment_vals.get('payment_method_id')  :
                
                self._cr.execute('''select id from account_payment_method_line where journal_id = %s and payment_method_id = %s ''',
                    [payment_vals.get('journal_id'),payment_vals.get('payment_method_id')])
                payment_method_line = self._cr.dictfetchall()    
                
                if payment_method_line:
                    payment_vals['payment_method_line_id']=payment_method_line[0].get('id')   
                    
            # if data.get('message_ids'):
            #     message_list=self.process_message_data(data.get('message_ids'))
            #     if message_list:
            #         payment_vals['message_ids']=message_list   
                     
            payment_list.append(payment_vals) 
        print("\\n============cccccccccccccpayment_list",payment_list)
        return payment_list