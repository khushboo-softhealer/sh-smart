# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models,fields

class Country(models.Model):
    _inherit = 'res.country'
    
    country_type = fields.Selection([('developed,', 'Developed'),
            ('devleoping', 'Devleoping'),
            ('underdeveloped', 'Underdeveloped')
        ],
        string="Country Type")