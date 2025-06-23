from odoo import models, fields, api

class MassUpdateProductEcommerceCategoryWizard(models.TransientModel):
    _name='sh.update.ecommerce.category.wizard'
    _description="Mass Update Product Ecommerce Category Wizard"

    ecommerce_catagory_ids=fields.Many2many('product.public.category',string="Product Ecommerce Category")
    product_ids = fields.Many2many('product.template')

    def mass_update_ecommerce_category(self):
        if self.ecommerce_catagory_ids:
            self.product_ids.write({
                'public_categ_ids':[(6,0,self.ecommerce_catagory_ids.ids)]
            })
        else:
            self.product_ids.write({
                'public_categ_ids':[(6,0,[])]
            })    
        # for category in self.ecommerce_catagory_ids :
        #     self.product_ids.write({
        #         'public_categ_ids': [(4, category.id)] 
        #     })
