# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import _, api, fields, models

class ShResConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_finance_manager = fields.Many2many(related='company_id.sh_finance_manager',string="Finance Manager",readonly=False)



class ShResCompany(models.Model):
    _inherit='res.company'

    sh_finance_manager = fields.Many2many('res.users',string="Finance Manager",relation='sh_ot_config_finance_rel',column1='config_id',column2='user_id',domain=lambda self: [('groups_id', 'in', [self.env.ref('account.group_account_manager').id])])