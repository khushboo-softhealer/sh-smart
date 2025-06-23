# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models


class ServerTag(models.Model):
    _name = 'server.tag'
    _description = "Server Tag"

    name = fields.Char(string='Server Tag Name')
