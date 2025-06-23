# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, api
from datetime import date, datetime


class WarningMessage(models.Model):
    _name = 'sh.warning.message'
    _description = 'Warning Message'

    name = fields.Char()
    description = fields.Char()
    user_id = fields.Many2one('res.users')
    res_model = fields.Char()
    res_id = fields.Integer()
    sh_create_date = fields.Date()
    is_checked = fields.Boolean()

    def checked_the_warning(self):
        self.write({
            'is_checked': True
        })
