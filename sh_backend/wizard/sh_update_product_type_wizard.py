from odoo import models, fields, api

class MassUpdateProductTypeWizard(models.TransientModel):
    _name='sh.update.product.type.wizard'
    _description="Mass Update Product Type Wizard"

    product_type_id = fields.Selection([
        ('consu', 'Consumable'),
        ('service', 'Service')], string='Product Type', default='consu', required=True)
    product_ids = fields.Many2many('product.template')

    def mass_update_product_type(self):
        self.product_ids.write({
            'type': self.product_type_id
        })
