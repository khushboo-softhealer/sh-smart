# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models

class AccountFiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    state_type = fields.Selection(
        string='State Type',
        selection=[
            ('inter_state', 'Inter State'),
            ('intra_state', 'Intra State')
        ]
    )
    