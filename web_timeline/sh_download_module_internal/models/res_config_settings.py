# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import _, api, fields, models

class ShResConfigSetting(models.TransientModel):
    _inherit = "res.config.settings"

    sh_billing_activity = fields.Many2one(related="company_id.sh_billing_activity",string="Billing Activity",readonly=False)

class ResCompany(models.Model):
    _inherit = 'res.company'
    
    sh_billing_activity = fields.Many2one('mail.activity.type',string="Billing Activity")