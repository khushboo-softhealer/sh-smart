# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class ShVersion(models.Model):
    _name = 'sh.version'
    _description = "Sh Version"

    name = fields.Char('Name')
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.company)