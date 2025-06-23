from odoo import api, exceptions, fields, models, _

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    paypal_fees = fields.Float(string = "Fees")
    currency_of_fees = fields.Many2one('res.currency',string = "Currency")
    paypal_bank_transfer_id = fields.Many2one('account.move',string = "Paypal Bank Transfer")