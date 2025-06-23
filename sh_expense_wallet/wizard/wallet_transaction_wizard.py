# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class WalletTransactionWizard(models.TransientModel):

    _name = "sh.wallet.transaction.wizard"
    _description = "Wallet Transaction Wizard"

    date = fields.Date(string="Date", default=fields.Date.today)
    amount = fields.Float(string="Amount")
    desc = fields.Char(string="Description")

    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id,
                                  string='Currency', store=True, depends=["company_id"],)
    company_id = fields.Many2one(
        'res.company', required=True, default=lambda self: self.env.user.company_id)

    @api.constrains('amount')
    def check_amount(self):
        if not self.amount > 0.0:
            raise ValidationError('Please enter positive amount!!!')

    def add_wallet_to_transaction_ids(self):
        active_id = self.env.context.get('active_id')

        active_obj = self.env[self.env.context.get(
            'active_model')].browse(active_id)

        if active_obj and active_obj.user_id:
            if not active_obj.user_id.employee_account_id:
                employee_account = self.env['account.account'].sudo().create({'name': active_obj.user_id.name,
                                                                              'code': self.env['ir.sequence'].next_by_code('employee.account'),
                                                                              'account_type': 'asset_current'
                                                                              })

                active_obj.user_id.write(
                    {'employee_account_id': employee_account.id})

        journal_id = active_obj.company_id.wallet_journal

        if not journal_id:
            raise UserError("Wallet Journal Not Found!")

        line_ids = []

        if not journal_id._get_journal_outbound_outstanding_payment_accounts():
            raise UserError("Debit Account not set in Wallet Journal !")

        line_ids.append((0, 0, {
            'account_id': journal_id._get_journal_outbound_outstanding_payment_accounts()[0].id,
            'debit': 0.0,
            'credit': self.amount,
            'name': 'Wallet Transfer'
        }))

        line_ids.append((0, 0, {
            'account_id': active_obj.user_id.employee_account_id.id,
            'credit': 0.0,
            'debit': self.amount,
            'name': 'Wallet Transfer'
        }))
        move = self.env['account.move'].sudo().create({
            'ref': active_obj.name,
            'date': self.date,
            'journal_id': journal_id.id,
            'line_ids': line_ids
        })
        move.action_post()

        vals = {
            'amount': self.amount,
            'date': self.date,
            'desc': self.desc,
            'wallet_id': active_id
        }
        self.env['sh.wallet.transaction'].create(vals)
