# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import api, exceptions, fields, models, _
from odoo.exceptions import UserError, ValidationError

# Sh Degree
class ShDegree(models.Model):    
    _name = "sh.degree" 
    _description = "Sh Degree"
    
    name = fields.Char("Name",required=True)

# Sh Education Qualification
class ShEducationQualification(models.Model):    
    _name = "sh.education.qualification"
    _description = "Sh Education Qualification"
        
    edu_employee_id = fields.Many2one('hr.employee',string='Profession Employee Reference',ondelete='cascade', index=True, copy=False)
    
    degree_id = fields.Many2one('sh.degree',string='Degree',ondelete='cascade', index=True, copy=False,required=True)
    institutes = fields.Char(string='Institutes',required=True)
    score = fields.Char(string='Score',required=True)
    quo_year = fields.Date(string="Qualification Year",required=True)
    transcript = fields.Binary("Transcripts")
    
# Sh Certification
class ShCertification(models.Model):    
    _name = "sh.certification"
    _description = "Sh Certification"
        
    cert_employee_id = fields.Many2one('hr.employee',string='Profession Employee Reference',ondelete='cascade', index=True, copy=False)
    
    course = fields.Char(string='Course Name',required=True)
    level_completion = fields.Char(string='Score',required=True)
    comp_year = fields.Date(string="Qualification Year",required=True)
    certificate = fields.Binary("Certificates")    
       