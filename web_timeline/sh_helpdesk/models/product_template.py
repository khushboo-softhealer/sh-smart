# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, api

class Product(models.Model):
    _inherit = 'product.template'

    @api.model_create_multi
    def create(self, vals_list):
        res = super(Product, self).create(vals_list)
        for rec in res:
            if rec.categ_id:
                helpdesk_category_ids = self.env['sh.helpdesk.category'].sudo().search([('category_id','=',rec.categ_id.id)])
                if helpdesk_category_ids:
                    for category in helpdesk_category_ids:
                        category.update_products()
        return res

    def write(self, vals):
        res = super(Product, self).write(vals)
        for rec in self:
            if 'is_published' in vals:
                if rec.categ_id:
                    helpdesk_category_ids = self.env['sh.helpdesk.category'].sudo().search([('category_id','=',rec.categ_id.id)])
                    if helpdesk_category_ids:
                        for category in helpdesk_category_ids:
                            category.update_products()
        return res