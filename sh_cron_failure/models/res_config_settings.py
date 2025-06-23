# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import _, api, fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    sh_cron_notify_users = fields.Many2many('res.users',string='Cron Notify User',relation="rel_user_crone_notify",
        column1="notify_user_id",
        column2="res_user_id")

class ResConfig(models.TransientModel):
    _inherit = "res.config.settings"


    sh_cron_notify_users = fields.Many2many('res.users',related='company_id.sh_cron_notify_users',readonly=False)

