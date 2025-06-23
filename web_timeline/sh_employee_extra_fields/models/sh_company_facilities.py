# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import api, exceptions, fields, models, _
from odoo.exceptions import UserError, ValidationError

# Company Facilities
class ShCompanyFacilities(models.Model):    
    _name = "sh.company.facilities"    
    _description = 'Sh Company Facilities'
    
    name = fields.Char('Name',required=True)   