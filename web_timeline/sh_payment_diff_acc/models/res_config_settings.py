from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    loss_account_id = fields.Many2one(
        'account.account', string="Default Loss Account")
    profit_account_id = fields.Many2one(
        'account.account', string="Defalut Profit Account")
    paypal_fees_account_id = fields.Many2one(
        'account.account',string = "Default Paypal fees Account"
    )
    paypal_to_bank_transfer_journal_id = fields.Many2one(
        'account.journal',string = "Paypal to Bank transfer Journal"
    )
    sh_paypal_vendor_ids = fields.Many2many('res.partner',string = "Vendors")

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    loss_account_id = fields.Many2one(
        'account.account', string="Default Loss Account", related="company_id.loss_account_id", readonly=False)
    profit_account_id = fields.Many2one(
        'account.account', string="Default Profit Account", related="company_id.profit_account_id", readonly=False)
    paypal_fees_account_id = fields.Many2one(
       'account.account',string = "Default Paypal fees Account",related = "company_id.paypal_fees_account_id",readonly = False
    )
    paypal_to_bank_transfer_journal_id = fields.Many2one(
        'account.journal',string = "Paypal to Bank transfer Journal",related = "company_id.paypal_to_bank_transfer_journal_id",readonly = False
    )
    sh_paypal_vendor_ids = fields.Many2many('res.partner',related = "company_id.sh_paypal_vendor_ids",readonly = False)