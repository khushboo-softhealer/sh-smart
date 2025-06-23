from email import message
from operator import le
from re import T
from odoo import api, fields, tools, models, _

import base64
import csv
from datetime import date,datetime

class DataImportWizard(models.TransientModel):
    _name = 'sh.import.data.wizard'
    _description = "Import Paypal Data"

    file = fields.Binary(string="File",required=True)   

    def show_success_msg(self,message_dict):
        #open the new success message box    
        view = self.env.ref('sh_import_paypal_data.sh_message_wizard')
        context = dict(self._context or {})

        message = ""
        if len(message_dict['successfully_updated']) > 0:
            message = message + str(len(message_dict['successfully_updated'])) + " " + "Records imported successfully" + "\n"
            

        if len(message_dict['invocied_bt_not_paid']) > 0:
            message = message + str(message_dict['invocied_bt_not_paid']) + " " +  "This rows are invoiced but not paid yet :" +  "\n"

        if len(message_dict['not_invoiced']) > 0:
            message = message + str(message_dict['not_invoiced']) + " " +  "This rows are not invoiced"
        
        if len(message_dict['actual_amount_greater_than_zero']) > 0:
            message = message + str(message_dict['actual_amount_greater_than_zero']) + " " +  "for this rows actual amount is greater than total amount"

        context['message'] = message          
        
        return {
            'name': 'Success',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context,
            }   

    def import_data(self):

        skip_header = True
        successfully_updated = []
        invocied_bt_not_paid = []
        not_invoiced = []
        actual_amount_greater_than_zero = []
        message_dict = {}

        counter = 0

        # try:
        file = str(base64.decodebytes(self.file).decode('utf-8'))
        myreader = csv.reader(file.splitlines())

        for row in myreader:
            counter = counter + 1

            if skip_header:
                skip_header=False
                continue


            if len(row) > 12:
                transaction = self.env['payment.transaction'].search([('provider_reference','=',row[12])],limit = 1)
                if transaction:
                    if transaction.invoice_ids:
                        if transaction.invoice_ids[0].payment_state == 'paid':
                            invoice = transaction.invoice_ids[0]

                            dictt = invoice.invoice_payments_widget
                            
                            if "content" in dictt and len(dictt['content']) > 0:
                                first_payment_dictt = dictt['content'][0]
                                if 'account_payment_id' in first_payment_dictt:
                                    payment = self.env['account.payment'].browse(first_payment_dictt['account_payment_id'])
                                    currency = self.env['res.currency'].search([('name','ilike',row[6])])
                                    if currency:
                                        payment.write({
                                            'currency_of_fees' : currency[0].id,
                                            'paypal_fees' : abs(float(row[8]))
                                        })
                                        successfully_updated.append(counter)

                        else:
                            invocied_bt_not_paid.append(counter)

                    else:
                        not_invoiced.append(counter)
        file = str(base64.decodebytes(self.file).decode('utf-8'))
        myreader = csv.reader(file.splitlines())
        
        dictt = {}
        transaction_list = []
        for row in myreader:
            if len(row) > 4 and row[4] == 'Website Payment':
                transaction = self.env['payment.transaction'].search([('provider_reference','=',row[12])],limit = 1)
                if transaction:
                    transaction_list.append(transaction.id)

            if len(row) > 4 and row[4] == 'General Withdrawal':
                if transaction_list:
                    transaction_list.append(abs(float(row[7].replace(',',''))))
                    dictt[row[0]] = transaction_list
                    transaction_list = []
        
        for key,value in dictt.items():
            date_time_obj = datetime.strptime(key, '%d/%m/%Y')
            
          

            payments = self.env['account.payment'].search([
                                                            ('payment_transaction_id','in',value[:-1]),
                                                            ])
         
            if payments:
                received_amount_obj = self.env['sh.received.amount'].create({
                    'payment_ids' : [(6,0,payments.ids)],
                    'received_amount' : value[-1]
                })

                rtn_value = received_amount_obj.confirm_actual_received_payment()
                if rtn_value == 0:
                    actual_amount_greater_than_zero.append(key)
                    continue

                for payment in payments:
                    
                    if not payment.paypal_bank_transfer_id:
                        
                        line_ids = []
                        
                        bank_journal = self.env.user.company_id.paypal_to_bank_transfer_journal_id
                        bank_account = self.env.user.company_id.paypal_to_bank_transfer_journal_id.profit_account_id

                        
                        journal_items = self.env['account.move.line'].search([('payment_id', '=', payment.id)])
                        journal_item_of_paypal_account = journal_items.filtered(lambda x:x.account_id.id == payment.journal_id.profit_account_id.id)
                        paypal_amount = journal_item_of_paypal_account.debit

                        line_ids.append((0,0,{
                                'account_id':journal_item_of_paypal_account.account_id.id,
                                'credit':paypal_amount,
                                'debit':0.0,
                                'name': ' ',
                                'partner_id':payment.partner_id.id
                            }))
            
                        line_ids.append((0,0,{
                                'account_id':bank_account.id,
                                'credit':0.0,
                                'debit':paypal_amount,
                                'name': ' ',
                                'partner_id':payment.partner_id.id
                            }))
                        
                        move = self.env['account.move'].sudo().create({
                                'date':date.today(),
                                'journal_id':bank_journal.id,
                                'ref': "Payment to Bank Transfer",
                                'company_id':self.env.user.company_id.id,
                                'line_ids':line_ids,
                                
                                
                            })
                        
                        move.action_post()

                        payment.write({
                        'paypal_bank_transfer_id' : move.id
                        })

     
        #for expense we create bill

        vendor_names = self.env.user.company_id.sh_paypal_vendor_ids.mapped('name')
        file = str(base64.decodebytes(self.file).decode('utf-8'))
        myreader = csv.reader(file.splitlines())
        for row in myreader:
            if len(row) > 3 and row[3] in vendor_names:
                
                date_time_obj = datetime.strptime(row[0], '%d/%m/%Y')
                sh_date = date_time_obj.date()
                vendor = self.env['res.partner'].search([('name','=',row[3])],limit=1)

                bill_exist = self.env['account.move'].search([('move_type','=','in_invoice'),('partner_id','=',vendor.id),('invoice_date','=',sh_date)])
                if not bill_exist:

                    product = self.env['product.product'].search([],limit = 1)

                    bill = self.env['account.move'].create({
                        'partner_id' : vendor.id,
                        'move_type':'in_invoice',
                        'invoice_date' : sh_date,
                        'user_id':self.env.user.id,
                    })

                    accounts = product.product_tmpl_id.get_product_accounts(bill.fiscal_position_id)

                    line_vals = {
                        'name' : "Paypal Expense",
                        'quantity' : 1,
                        'price_unit' : abs(float(row[7].replace(',',''))),
                        'account_id' : accounts['expense'].id,
                        'move_id' : bill.id
                    }

                    bill.write({
                            'invoice_line_ids' : [(0,0,line_vals)]
                        })


        message_dict.update({
            'successfully_updated' :successfully_updated,
            'invocied_bt_not_paid' : invocied_bt_not_paid,
            'not_invoiced' : not_invoiced,
            'actual_amount_greater_than_zero' : actual_amount_greater_than_zero
        })
            
        if counter > 1:

            res = self.show_success_msg(message_dict)
            return res