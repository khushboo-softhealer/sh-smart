# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import api, exceptions, fields, models, _
from odoo.exceptions import UserError, ValidationError

# Employee Religion
class ShEmployeeReligion(models.Model):
    _name = 'sh.employee.religion'
    _description = 'Sh Employee Religion'
    
    name = fields.Char('Name',required=True)    
