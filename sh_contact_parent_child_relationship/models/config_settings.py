# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'
    
    sh_common_mail_domains_ids = fields.Many2many(
        'sh.common.mail.domains', string="Common Mail domains")
    
class HelpdeskSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    
    sh_common_mail_domains_ids = fields.Many2many(
        'sh.common.mail.domains', string='Common Mail domains', related='company_id.sh_common_mail_domains_ids', readonly=False)