from odoo import models, fields, api
from odoo.exceptions import ValidationError

class MassUpdateProductCategoryWizard(models.TransientModel):
    _name='sh.update.category.wizard'
    _description="Mass Update Product Category Wizard"

    catagory_ids=fields.Many2one('product.category',string="Product Category")
    product_ids = fields.Many2many('product.template')

    def mass_update_category(self):
        self.product_ids.write({
            'categ_id':self.catagory_ids.id
        })
