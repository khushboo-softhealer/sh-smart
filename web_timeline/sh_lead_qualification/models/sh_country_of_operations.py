# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, api


class ShCountryofOperations(models.Model):
    _name = 'sh.country.of.operations'
    _description = 'Country of Operations' 
    _rec_name = "country_id"
    
    country_id = fields.Many2one('res.country',string="Origin")
    country_group_ids = fields.Many2many('res.country.group', string='Group of countries')
    country_type = fields.Selection([('developed,', 'Developed'),
            ('devleoping', 'Devleoping'),
            ('underdeveloped', 'Underdeveloped')
        ],
        string="Country Type")
    sh_helpdesk_ticket_id = fields.Many2one('sh.helpdesk.ticket')
    res_partner_id = fields.Many2one('res.partner')
    
    
    @api.onchange('country_id')
    def _onchange_account_type(self):
        country_group = self.env['res.country.group'].search([('country_ids','in',[self.country_id.id])])
        self.write({
            'country_group_ids':[(6,0, country_group.ids)],
            'country_type' : self.country_id.country_type
            })
        
