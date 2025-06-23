# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models, _, api

class TypeofStyle(models.Model):
    _name = 'sh.style'

    name = fields.Char(string = "Name",required=True)
    description = fields.Text(string="Description")
    sequence = fields.Integer(string = "Sequence",default=10)
    active = fields.Boolean(default=True,)
