# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields

class ShScale(models.Model):
    _name='sh.scale'
    _description="Sh Scale"

    name = fields.Char("Scale")
    days=fields.Integer('Days')
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.company)