# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

class Company(models.Model):
    _inherit = "res.company"

    def write(self, vals):
        for rec in self:
            for each_key,each_val in vals.items():

                #find field in fields model
                sh_field = self.env['ir.model.fields'].sudo().search([('name','=',each_key)],limit=1)
                if sh_field:
                    if sh_field.ttype == 'many2many':
                        if each_val and each_val[0] and each_val[0][2] and sh_field.relation:
                            each_val_list  = each_val[0][2]
                            model_name = sh_field.relation
                            data = self.env[model_name].sudo().search([('id','in',each_val_list)])
                            if data:
                                each_val = ''
                                for each_data in data:
                                   each_val +=  each_data.name

                    if sh_field.ttype == 'many2one':
                        if each_val and sh_field.relation:
                            model_name = sh_field.relation
                            data = self.env[model_name].sudo().browse(int(each_val))
                            if data:
                                each_val =  data.name
                            
                    
                    self.env['sh.multi.company.change.log'].sudo().create({
                        'company_id':rec.id,
                        'field_name':each_key,
                        'new_value':each_val,
                        'label':sh_field.field_description,
                        'user_id':self.env.uid,
                        'change_date':fields.Datetime.now()
                    })
                
        


        return super(Company, self).write(vals)




class MultiCompanyChangeLog(models.Model):
    _name = "sh.multi.company.change.log"
    _description = "Multi Company Chane Log"

    name = fields.Char("Ref",default='New')
    company_id = fields.Many2one("res.company",string="Company")
    field_name = fields.Char("Field Technical Name")
    new_value = fields.Char("Set Value")
    label = fields.Char("Label")
    change_date = fields.Datetime("Update Time")
    user_id = fields.Many2one("res.users",string="Updated By")


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sh.company.change.log') or 'New'
                result = super(MultiCompanyChangeLog, self).create(vals_list)
        return result