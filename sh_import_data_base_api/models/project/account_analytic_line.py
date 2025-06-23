# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class AccountAnalyticline(models.Model):
    _inherit = 'account.analytic.line'
    
    remote_account_analytic_line_id = fields.Char("Remote Timesheet ID",copy=False)