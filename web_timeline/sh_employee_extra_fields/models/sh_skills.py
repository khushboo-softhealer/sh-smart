# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import api, exceptions, fields, models, _
from odoo.exceptions import UserError, ValidationError

# Sh Emp Technical Skill
class ShEmpTechnicalSkill(models.Model):    
    _name = "sh.emp.technical.skill"    
    _description = 'Sh Emp Technical Skill'
    
    employee_id = fields.Many2one('hr.employee',string='Employee Reference', required=True, ondelete='cascade', index=True, copy=False)
    skill_id = fields.Many2one('sh.technical.skill',string='Skill Reference', required=True, ondelete='cascade', index=True, copy=False)
    level = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'Minimum'),
        ('3', 'High'),
        ('4', 'Maximum'),
        ('5', 'Max'),
        ],string="Level")
    
# Sh Technical Skill
class ShTechnicalSkill(models.Model):    
    _name = "sh.technical.skill"  
    _description = 'Sh Technical Skill'  
    
    name = fields.Char('Name',required=True) 

# Sh Emp Non Technical Skill
class ShEmpNonTechnicalSkill(models.Model):    
    _name = "sh.emp.non.technical.skill"    
    _description = 'Sh Emp Non Technical Skill'
    
    employee_id = fields.Many2one('hr.employee',string='Employee Reference', required=True, ondelete='cascade', index=True, copy=False)
    non_tec_skill_id = fields.Many2one('sh.non.technical.skill',string='Non Technical Skill Reference', required=True, ondelete='cascade', index=True, copy=False)
    level = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'Minimum'),
        ('3', 'High'),
        ('4', 'Maximum'),
        ('5', 'Max'),
        ],string="Level")

# Sh Non Technical Skill
class ShNonTechnicalSkill(models.Model):    
    _name = "sh.non.technical.skill"  
    _description = 'Sh Non Technical Skill'  
    
    name = fields.Char('Name',required=True) 

