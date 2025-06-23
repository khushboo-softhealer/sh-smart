# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, models, fields

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def action_variant_details_update(self):
        return {
            'name':
            'Mass Update',
            'res_model':
            'sh.product.variant.update.wizard',
            'view_mode':
            'form',
            'context': {
                'default_product_template_ids':
                [(6, 0, self.env.context.get('active_ids'))]
            },
            'view_id':
            self.env.ref(
                'sh_update_template_to_variant.model_product_template_variant_details_wizard_form_view'
            ).id,
            'target':
            'new',
            'type':
            'ir.actions.act_window'
        }

    @api.model
    def default_get(self, fields):
        result = super(ProductTemplate, self).default_get(fields)
        category = self.env['product.category'].search([('name', '=', 'Odoo')], limit=1)
        if category:
            result['categ_id'] = category.id
        return result
