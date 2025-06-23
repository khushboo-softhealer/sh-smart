# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields,api


class DynamicPriceProduct(models.Model):
    _inherit = 'product.template'

    
    def write(self, values):
        result = super(DynamicPriceProduct, self).write(values)
        if values.get('list_price') and not values.get('sh_sales_price_with_depends'):
            self.sh_custom_update_price_with_depends(self)
        return result
    

    euro_price_duplicate = fields.Float("Euro Price(D)")

    sh_sales_price_with_depends = fields.Monetary(string="Sales Price with Depends")

    def sh_custom_update_price_with_depends(self, product):
        # pricelist = self.env['website'].get_current_website().sudo().pricelist_id
        product_list = []
        total_price = product.list_price
        for dependency in product.product_variant_id.depends:
            product_list = product.product_variant_id.get_dependent_product_in_variants(
                dependency.technical_name, product_list, product.product_variant_id)
        
        if product_list:
            for lst in product_list: 
                combination = lst.product_tmpl_id.list_price #lst._get_combination_info_variant(pricelist=pricelist)
                total_price = total_price + combination
            product.write({
                'sh_sales_price_with_depends':total_price,
            })
        else:
            product.write({
                'sh_sales_price_with_depends':total_price,
            })
