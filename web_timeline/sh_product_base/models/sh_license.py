# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api

class Shlicense(models.Model):
    _name = 'sh.license'
    _description = "Sh license"
    
    name = fields.Char('Name')
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.company)