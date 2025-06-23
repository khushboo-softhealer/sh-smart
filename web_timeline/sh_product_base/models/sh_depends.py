# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields,api
from odoo.exceptions import ValidationError


class ShDepends(models.Model):
    _name = 'sh.depends'
    _description = "Sh Depends"

    name = fields.Char('Name',required=True)
    technical_name = fields.Char("Technical Name",required=True)
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.company)
    
    # @api.constrains('technical_name')
    # def unique_technical_name(self):
    #     for rec in self:
    #         matched_technical_name = self.search([('id','!=',rec.id),('technical_name','=',rec.technical_name)])
    #         if matched_technical_name:
    #             raise ValidationError("This Technical Name Already exists")
    