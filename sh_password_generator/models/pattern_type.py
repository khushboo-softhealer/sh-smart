# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models


class Type(models.Model):
    _name = 'pattern.type'
    _description = "Pattern Type"

    name=fields.Char("Name")
