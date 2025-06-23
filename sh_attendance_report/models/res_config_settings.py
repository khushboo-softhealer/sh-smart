# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models, api
from datetime import datetime


class ResCompany(models.Model):
    _inherit = 'res.company'

    sh_notify_user_email = fields.Char("Notify User Email Addresses")


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_notify_user_email = fields.Char(
        "Notify User Email Addresses", related='company_id.sh_notify_user_email', readonly=False)
