from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    wallet_journal = fields.Many2one(
        "account.journal", string="Wallet Journal")


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    wallet_journal = fields.Many2one(
        'account.journal', related="company_id.wallet_journal", string="Wallet Journal", readonly=False)
