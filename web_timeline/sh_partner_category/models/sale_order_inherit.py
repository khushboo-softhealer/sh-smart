# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import _, models, fields

class SaleOrderPartnerCateg(models.Model):
    _inherit='sale.order'


    sh_partner_category_id = fields.Many2one(
        "partner.category", string="Partner Category", tracking=True)
    

    def action_mass_auto_assign_partner_category(self):
        context = self.env.context.get('active_ids')
        sale_obj = self.search([('id','in',context)])
        partner_categ_obj = self.env['partner.category'].search([])       
        for partner in sale_obj:              
            total_amount=partner.partner_id.total_invoiced
            for partner_category in partner_categ_obj:                
                from_amount=partner_category.from_invoice_amount
                to_amount = partner_category.to_invoice_amount               
                if from_amount <= total_amount and to_amount >= total_amount:                    
                    partner.sh_partner_category_id = partner_category  

