from odoo import fields, models


class WalletTransaction(models.Model):
    _name = 'sh.wallet.transaction'
    _description = "Wallet Transaction"

    date = fields.Date(string="Date", default=fields.Date.today)
    amount = fields.Float(string="Amount")
    wallet_id = fields.Many2one('sh.wallet')
    desc = fields.Char(string="Description")
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id,
                                  string='Currency', store=True, depends=["company_id"],)
    company_id = fields.Many2one(
        'res.company', required=True, default=lambda self: self.env.user.company_id)
