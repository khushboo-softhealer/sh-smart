# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class MailFollowers(models.Model):
    _inherit = 'mail.followers'

    remote_mail_followers_id = fields.Char("Remote Mail Followers ID",copy=False)
    