# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    show_in_website = fields.Boolean(string="Show in website")
