# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class PredefinedMessage(models.Model):
    _name = 'sh.predefined.reason'
    _description = "Predefined Reason"
    _rec_name = 'name'

    name = fields.Char('Reason',required=True)
