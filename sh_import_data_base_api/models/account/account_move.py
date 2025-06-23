# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, api
import requests

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    remote_account_move_id = fields.Char("Remote Invoice ID",copy=False)

    def mass_update_sale_person(self):
        if self.env.context and self.env.context.get('active_ids'):
            find_invoice=self.env['account.move'].browse([r for r in self.env.context.get('active_ids')])
            for invoice in find_invoice:
                confid = self.env['sh.import.base'].search([],limit=1)
                response = requests.get('''%s/api/public/account.invoice?query={id,user_id}&filter=[["id","=",%s]]''' %(confid.base_url,int(invoice.remote_account_move_id)))
                response_json = response.json()
                for data in response_json.get('result'):
                    if data.get('user_id'):
                        find_invoice=self.env['account.move'].search([('remote_account_move_id','=',data.get('id'))])
                        if find_invoice:
                            if data.get('user_id'):
                                domain_by_id = [('remote_res_user_id','=',data.get('user_id'))]
                                find_user_id=self.env['res.users'].search(domain_by_id)
                                if find_user_id:   
                                    query = """
                                        UPDATE account_move
                                            SET invoice_user_id = %s WHERE id = %s
                                    """
                                    self.env.cr.execute(query, [find_user_id.id,find_invoice.id])





    
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    remote_account_move_line_id = fields.Char("Remote Invoice line ID",copy=False)
    
    def _check_reconciliation(self):
        for line in self:
            if line.matched_debit_ids or line.matched_credit_ids:
                print("You cannot do this modification on a reconciled journal entry. "
                    "You can just change some non legal fields or you must unreconcile first.\n")
                    #   "Journal Entry (id): %s (%s)"% (line.move_id.name, line.move_id.id))
    
class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    remote_account_payment_id = fields.Char("Remote Invoice Payment ID",copy=False)
    
class AccountPaymentMethod(models.Model):
    _inherit = 'account.payment.method'

    @api.model
    def _get_payment_method_information(self):
        res= super()._get_payment_method_information()
        print("\n\n_get_payment_method_information",res)
        res['electronic'] = {'mode': 'multi', 'domain': [('type', 'in', ('bank', 'cash'))]}
        return res
    
class AccountAccount(models.Model):
    _inherit = 'account.account'
    
    remote_account_account_id = fields.Char("Remote Account ID",copy=False)
    
class AccountAccountTag(models.Model):
    _inherit = 'account.account.tag'
    
    remote_account_account_tag_id = fields.Char("Remote Account Tag ID",copy=False)
    
    
class AccountJournal(models.Model):
    _inherit = 'account.journal'
    
    remote_account_journal_id = fields.Char("Remote Account Journal ID",copy=False)

class AccountPaymentMethod(models.Model):
    _inherit = 'account.payment.method'
    
    remote_account_payment_method_id = fields.Char("Remote Account Payment Method ID",copy=False)