# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields

class HREeployee(models.Model):
    _inherit = 'hr.employee'
    
    sh_rmm_employee_id = fields.Char("RMM Employee Code")