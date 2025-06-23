from odoo import fields, models,api
from odoo.exceptions import RedirectWarning, UserError, ValidationError

class ReceivedAmount(models.TransientModel):
    _name = 'sh.received.amount'
    _description = 'Received Amount'

    # currency_id = fields.Many2one('res.currency', default=lambda self: self.env.user.currency_id,
    #                               string='Currency', store=True, depends=["company_id"],)   
    # company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id, string='Company', readonly=True)
    received_amount = fields.Float(string = "Received Amount")
    payment_ids = fields.Many2many('account.payment',string = "Payments")

    def confirm_actual_received_payment(self):
        if not self.env.user.company_id.loss_account_id or not self.env.user.company_id.profit_account_id or not self.env.user.company_id.paypal_fees_account_id or not self.env.user.company_id.paypal_to_bank_transfer_journal_id:
            raise UserError("Please select default account in settings")
        if not self.payment_ids:
            self.payment_ids = self.env['account.payment'].browse(self.env.context.get('active_id')).ids
        total_actual_received = self.received_amount
        total_paypal_fees = 0
        total_old_debit = 0
        for acc_payment in self.payment_ids:
            paypal_fees_currency_rates = acc_payment.currency_of_fees.rate_ids

            if paypal_fees_currency_rates:
                paypal_fees_currency_rates = self.env['res.currency.rate'].search([('name','=',acc_payment.date),('id','in',paypal_fees_currency_rates.ids)],limit = 1)

            paypal_fees = acc_payment.paypal_fees
            if paypal_fees > 0 and not acc_payment.currency_of_fees:
                raise UserError("Currency not found for paypal fees")

            if paypal_fees > 0 and not paypal_fees_currency_rates:
                raise UserError("Currency rate not found for paypal fees")
        
            if paypal_fees_currency_rates.rate != 0:
                paypal_fees = (acc_payment.paypal_fees / paypal_fees_currency_rates.rate)

            amount_currency_rates = acc_payment.currency_id.rate_ids
            if amount_currency_rates:
                amount_currency_rates = self.env['res.currency.rate'].search([('name','=',acc_payment.date),('id','in',amount_currency_rates.ids)],order ="name desc",limit = 1)

            if not amount_currency_rates:
                raise UserError("Currency rate not found for amount")

            amount = acc_payment.amount
            if amount_currency_rates.rate !=0:
                amount = (acc_payment.amount) / amount_currency_rates.rate


            total_paypal_fees = total_paypal_fees + paypal_fees
            total_old_debit = total_old_debit + amount

        
        if total_actual_received > (total_old_debit - total_paypal_fees):
            
            return 0

        for acc_payment in self.payment_ids:
            
            acc_payment.action_cancel()
            acc_payment.action_draft()

            amount_currency_rates = acc_payment.currency_id.rate_ids
            if amount_currency_rates:
                amount_currency_rates = self.env['res.currency.rate'].search([('name','=',acc_payment.date),('id','in',amount_currency_rates.ids)],order ="name desc",limit = 1)

            if not amount_currency_rates:
                raise UserError("Currecy rate not found for amount")

            old_debit = acc_payment.amount
            if amount_currency_rates.rate !=0:
                old_debit = (acc_payment.amount) / amount_currency_rates.rate


            paypal_fees_currency_rates = acc_payment.currency_of_fees.rate_ids
            if paypal_fees_currency_rates:
                paypal_fees_currency_rates = self.env['res.currency.rate'].search([('name','=',acc_payment.date),('id','in',paypal_fees_currency_rates.ids)],order ="name desc",limit = 1)
        
            paypal_fees = acc_payment.paypal_fees
            if paypal_fees_currency_rates.rate != 0:
                paypal_fees = (acc_payment.paypal_fees / paypal_fees_currency_rates.rate)

            acc_payment.write({
            'actual_received_amount':total_actual_received
            })
            acc_payment.action_post()
            total_actual_received = total_actual_received - (old_debit - paypal_fees)


