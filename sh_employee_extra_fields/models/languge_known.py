# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import api, exceptions, fields, models, _
from odoo.exceptions import UserError, ValidationError

# Language Known Object
class LangugeKnown(models.Model):
    _name = 'language.known'
    _description = 'Sh Language Known'
      
    employee_id = fields.Many2one('hr.employee',string='Employee Reference', required=True, ondelete='cascade', index=True, copy=False)
    
    language =  fields.Many2one('res.lang',string="Language",required=True) 
    can_read = fields.Boolean("Can Read?")
    can_write = fields.Boolean("Can Write?")
    can_speak = fields.Boolean("Can Speak?")
    
# Sh Emp Non Technical Skill
class ShEmpProfessionalExperience(models.Model):    
    _name = "sh.emp.professional.experience"
    _description = 'Sh Emp Professional Experience'
        
    exp_employee_id = fields.Many2one('hr.employee',string='Profession Employee Reference',ondelete='cascade', index=True, copy=False)
    
    job_title_id = fields.Many2one('hr.job',string='Job Reference',ondelete='cascade', index=True, copy=False,required=True)
    location = fields.Char(string='location', index=True, copy=False,required=True)
    start_date = fields.Date(string="Start Date",required=True)
    end_date = fields.Date(string="End Date",required=True)
    experience_cirty = fields.Binary("Experience Certificate")
    