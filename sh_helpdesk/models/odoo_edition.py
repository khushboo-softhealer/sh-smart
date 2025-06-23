# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class ShEdition(models.Model):
    _name = 'sh.edition'
    _description = 'Edition'

    name = fields.Char('Edition')

