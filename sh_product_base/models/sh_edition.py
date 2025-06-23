# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields

class ShEdition(models.Model):
    _name='sh.edition'
    _description="Sh Edition"

    name=fields.Char('Name',required="1")
    active = fields.Boolean(default=True)
    sh_display_in_frontend = fields.Boolean('Display At Frontend ?')
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.company)