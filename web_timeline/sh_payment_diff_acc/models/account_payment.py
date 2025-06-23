from operator import mod
from odoo import fields, models,api
from odoo.exceptions import RedirectWarning, UserError, ValidationError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    actual_received_amount = fields.Monetary(string="Received Amount",currency_field='currency_id')
    currency = fields.Many2one('res.currency', default=lambda self: self.env.user.currency_id,
                                  string='Currency', store=True, depends=["company_id"],)   
    # company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id, string='Company', readonly=True)

    def actual_received_pay(self):

        for rec in self:

            if not rec.company_id.loss_account_id or not rec.company_id.profit_account_id or not rec.company_id.paypal_fees_account_id or not rec.company_id.paypal_to_bank_transfer_journal_id:
                raise UserError("Please select default loss, profit and paypal fees account in settings")

        return {
            'name': 'Actual Received Amount',
            'res_model': 'sh.received.amount',
            'view_mode': 'form',
            'view_id': self.env.ref('sh_payment_diff_acc.sh_received_amount_view_form').id,
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {'default_payment_ids': [(6, 0, self.env.context.get('active_ids'))]}
        }

    # def action_post(self):
        
    #     if self.payment_type == 'inbound':
    #         aml_obj = self.env['account.move.line'].with_context(check_move_validity=False)
    #         debit_move_line = self.move_id.line_ids.filtered(lambda x:x.debit > 0)
    #         liquidity_aml_dict = {
                
    #             'move_id' : self.move_id.id,
    #             'name': '',
    #         }
    #         old_debit =debit_move_line.debit

    #         paypal_fees_currency_rates = self.currency_of_fees.rate_ids
    #         if paypal_fees_currency_rates:
    #             paypal_fees_currency_rates = self.env['res.currency.rate'].search([('name','=',self.date),('id','in',paypal_fees_currency_rates.ids)],order ="name desc",limit = 1)
            
    #         paypal_fees = round(self.paypal_fees,2)
            
    #         if paypal_fees_currency_rates.rate != 0:
    #             paypal_fees = round((self.paypal_fees / paypal_fees_currency_rates.rate),2)
            
    #         self.actual_received_amount = round(self.actual_received_amount ,2)
    #         if self.actual_received_amount != 0:
                
    #             if self.actual_received_amount >= (old_debit - paypal_fees):
                    
    #                 debit_move_line.update({
    #                     'debit': old_debit - paypal_fees
    #                 })
                    
                    
    #                 liquidity_aml_dict.update({
    #                     'account_id':self.company_id.paypal_fees_account_id.id,
    #                     'debit':paypal_fees
    #                 })
                    
    #                 aml_obj.create(liquidity_aml_dict)

    #                 self.actual_received_amount = old_debit - paypal_fees
                    

    #             else:
                    
    #                 debit_move_line.update({
    #                     'debit': self.actual_received_amount
    #                 })

    #                 liquidity_aml_dict.update({
    #                     'account_id':self.company_id.loss_account_id.id,
    #                     'debit':old_debit - paypal_fees - self.actual_received_amount 
    #                 })

    #                 aml_obj.create(liquidity_aml_dict)

    #                 liquidity_aml_dict.update({
    #                     'account_id':self.company_id.paypal_fees_account_id.id,
    #                     'debit':paypal_fees
    #                 })
                    
    #                 aml_obj.create(liquidity_aml_dict)
                
    #     return super(AccountPayment,self).action_post()

    # @api.onchange('payment_difference_handling','payment_difference')
    # def default_account(self):
        
    #     if self.payment_difference_handling == 'reconcile':
    #         if self.payment_difference > 0.0 and self.company_id.loss_account_id:
    #            self.writeoff_account_id = self.company_id.loss_account_id.id
            
    #         if self.payment_difference < 0.0 and self.company_id.profit_account_id:
    #             self.writeoff_account_id = self.company_id.profit_account_id.id

    #     else:
    #         self.writeoff_account_id = False

class AccountRegisterPayments(models.TransientModel):
    _inherit = 'account.payment.register'

    @api.onchange('payment_difference_handling','payment_difference')
    def default_account(self):
        
        acc_payment = self.env[self.env.context.get('active_model')].browse(self.env.context.get('active_id'))

        if self.payment_difference_handling == 'reconcile':
            if self.payment_difference > 0.0 and acc_payment.company_id.loss_account_id:
               self.writeoff_account_id = acc_payment.company_id.loss_account_id.id
            
            if self.payment_difference < 0.0 and acc_payment.company_id.profit_account_id:
                self.writeoff_account_id = acc_payment.company_id.profit_account_id.id

        else:
            self.writeoff_account_id = False