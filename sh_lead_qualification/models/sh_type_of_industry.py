# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ShTypeofIndustry(models.Model):
    _name = 'sh.type.of.industry'
    _description = 'Type of Industry'
    
    name = fields.Char("Industry")