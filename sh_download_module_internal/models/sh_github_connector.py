# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ShGithubConnector(models.Model):
    _inherit = "sh.github.connector"

    billing_activity_user_ids = fields.Many2many(
        'res.users',
        'sh_github_connector_billing_user_activity',
        'sh_user_id',
        'sh_github_connector_id',
        string='Billing Activity Assign To',
        help='''Activity create for the users when the module is downloaded for the Project'''
    )
