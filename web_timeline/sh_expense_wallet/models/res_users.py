from odoo import models, fields


class Users(models.Model):
    _inherit = "res.users"

    employee_account_id = fields.Many2one(
        'account.account', string="Employee Account")
