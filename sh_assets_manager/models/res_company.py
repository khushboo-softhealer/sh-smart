# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    user_id = fields.Many2one('res.users', string=' Responsible Person')
