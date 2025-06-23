# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.


from odoo import models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def _search_get_detail(self, website, order, options):
        """
            INHERITED BY SOFTHEALER
            ==> In order to add tag domain in base_domain and return
            if user click on tag
        """

        result = super(ProductTemplate, self)._search_get_detail(
            website, order, options)
        # --------------------------------------------------------------------
        # softhealer custom code start here
        # --------------------------------------------------------------------
        base_domain = result.get('base_domain', [])
        
        ### Price Filter
        price_attr = options.get('price','')
        if price_attr == 'Paid':
            base_domain = base_domain or []
            base_domain.append([
                ('list_price','>',0)
            ])
        if price_attr == 'Free':
            base_domain = base_domain or []
            base_domain.append([
                ('list_price','<=',0)
            ])
        
        ### Most Downloaded Filter
        if options.get('most_downloaded',False):
            base_domain = base_domain or []
            base_domain.append([
                ('sh_product_counter','>',0)
            ])

        result.update({'base_domain': base_domain})
        # --------------------------------------------------------------------
        # softhealer custom code ends here
        # --------------------------------------------------------------------
        return result

    def _get_sales_prices(self, pricelist):
        res = super(ProductTemplate, self)._get_sales_prices(pricelist=pricelist)

        for rec in res:
            
            template = self.browse(rec)
            if res[rec] and template.product_variant_id:
                total_price = 0.0
                product_list = []

                for dependency in template.product_variant_id.depends:
                    product_list = template.product_variant_id.get_dependent_product_in_variants(
                        dependency.technical_name, product_list, template.product_variant_id)
                
                if product_list:
                    for lst in product_list: 
                        combination = lst._get_combination_info_variant(pricelist=pricelist)
                        total_price = total_price + combination['price']

                    if res[rec].get('base_price',False):
                        total_price = total_price + res[rec].get('base_price')
                    else:
                        total_price = total_price + res[rec].get('price_reduce')
                else:
                    if res[rec].get('base_price',False):
                        total_price = total_price + res[rec].get('base_price')
                    else:
                        total_price = total_price + res[rec].get('price_reduce')
                res[rec].update({
                    'price_reduce':total_price
                })
        return res