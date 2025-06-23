# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    sh_invoice_recurring_order_id = fields.Many2one(
        "sh.invoice.recurring", string="Recurring Order")
