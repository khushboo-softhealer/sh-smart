from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ExpenseWallet(models.Model):
    _name = 'sh.wallet'
    _description = "Wallet"

    name = fields.Char(readonly=True)
    user_id = fields.Many2one('res.users', string="Emoloyee", required=True)
    wallet_amount = fields.Float(
        string="Wallet Amount", required=True, compute="_compute_wallet_amount")
    desc = fields.Char(string="Description")
    transaction_ids = fields.One2many('sh.wallet.transaction', 'wallet_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id,
                                  string='Currency', store=True, depends=["company_id"],)
    company_id = fields.Many2one(
        'res.company', required=True, default=lambda self: self.env.user.company_id)

    @api.constrains('user_id')
    def _check_user_id(self):
        for data in self:
            if self.search([('id', '!=', data.id), ('user_id', '=', data.user_id.id)]):
                raise ValidationError(_('This Employee Already exists!!!'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals.update(
                {'name': self.env['ir.sequence'].next_by_code('wallet.entry')})
        res = super(ExpenseWallet, self).create(vals_list)
        return res

    @api.depends('transaction_ids', 'transaction_ids.amount')
    def _compute_wallet_amount(self):
        for rec in self:
            rec.wallet_amount = 0
            for transaction in rec.transaction_ids:
                rec.wallet_amount = rec.wallet_amount+transaction.amount
