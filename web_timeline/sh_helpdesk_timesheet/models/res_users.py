# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import _, api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    ticket_id = fields.Many2one(related="account_analytic_id.ticket_id", store=True)
