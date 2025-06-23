# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import _, models, fields
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def get_default_partner_categ(self):
        if self.env.user.company_id.sh_partner_categ:
            return self.env.user.company_id.sh_partner_categ.id
        else:
            return False

    partner_category_id = fields.Many2one(
        "partner.category", string="Partner Category", default=get_default_partner_categ, tracking=True)

    def action_mass_update_partner_category_wizard(self):
        if not self.user_has_groups('sh_partner_category.group_partner_category'):
            raise UserError(_(
                "User has not access to update product category please check User Rights."))
        context = {'default_sh_partners': self.env.context.get('active_ids')}
        return {
            'name':'Mass Update Partner Category',
            'res_model':'sh.partner.category.action.wizard',
            'view_mode':'form',
            'view_id': self.env.ref('sh_partner_category.sh_mass_action_partner_category_wizard').id,
            'target': 'new',
            'type':'ir.actions.act_window',
            'context': context
        }
    
    def action_mass_auto_assign_partner_category(self):
        context = self.env.context.get('active_ids')
        res_partner_obj = self.search([('id','in',context)])
        partner_categ_obj = self.env['partner.category'].search([])       
        for partner in res_partner_obj:              
            total_amount=partner.total_invoiced
            for partner_category in partner_categ_obj:                
                from_amount=partner_category.from_invoice_amount
                to_amount = partner_category.to_invoice_amount               
                if from_amount <= total_amount and to_amount >= total_amount:                    
                    partner.partner_category_id = partner_category            
