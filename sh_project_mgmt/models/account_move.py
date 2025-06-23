# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from datetime import datetime, timedelta, time, date
from odoo.exceptions import ValidationError
from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = "account.move"

    sh_analytic_account_id = fields.Many2one("account.analytic.account",string="Analytic Account")

    def update_analytic(self):
        print("\n\n\n---------")
        create_analytic_line = False
        if self.sh_analytic_account_id:
            for line in self.invoice_line_ids:
                if not line.analytic_distribution:
                    create_analytic_line = True
                    line.sudo().write({'analytic_distribution':{self.sh_analytic_account_id.id:100}})

            if create_analytic_line:
                self.env['account.move.line'].sudo()._create_analytic_lines()