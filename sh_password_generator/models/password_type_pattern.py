# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models


class PasswordTypePattern(models.Model):
    _name = 'password.type.pattern'
    _description = "PWD Pattern Type"

    password_wiz_id = fields.Many2one('password.generator.wizard',string="Password Wizard Id")
    name = fields.Char("Title",required=1)
    password_length = fields.Integer("Password Length")
    pattern_type_ids = fields.Many2many('pattern.type')
