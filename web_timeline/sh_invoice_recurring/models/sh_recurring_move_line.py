# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class RecurringMoveLine(models.Model):
    _name = 'sh.recurring.move.line'
    _description="Recurring Move Line"

    name = fields.Char()
    account_id = fields.Many2one('account.account', required=True)
    partner_id = fields.Many2one('res.partner')
    debit = fields.Float(string='Debit')
    credit = fields.Float(string='Credit')
    recurring_id = fields.Many2one('sh.invoice.recurring', string='Order Reference',
                                   required=True, ondelete='cascade', index=True, copy=False)
