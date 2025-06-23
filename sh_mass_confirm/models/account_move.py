# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def sh_mass_invoice_confirm(self):
        account_invoice_obj = self.env['account.move']
        active_ids = self.env.context.get('active_ids')
        if active_ids:
            search_invoice_rec = account_invoice_obj.search([
                ('id', 'in', active_ids)
            ])
            if search_invoice_rec:
                for record in search_invoice_rec:
                    record.action_post()
