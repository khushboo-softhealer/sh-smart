
# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_sh_lognote_posted_for_delete_depends_products = fields.Boolean(default=False)

    # def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
    #     #### Check product has blog or not

    #     sh_product = self.env['product.product'].browse(product_id).exists()
    #     check_product_blog = sh_product.check_variant_has_post(sh_product)
    #     self.clear_caches()
    #     if not check_product_blog:
    #         value = {'sh_blog_post_not_exists': 'sh_blog_post_not_exists'}
    #         if sh_product and sh_product.product_template_attribute_value_ids and sh_product.product_template_attribute_value_ids[0]:
    #             value.update({'product_varsion':sh_product.product_template_attribute_value_ids[0].name})
    #         return value
        
    #     #### Check product has blog or not
        
    #     res = super(SaleOrder, self)._cart_update(
    #         product_id, line_id, add_qty, set_qty, **kwargs)

    #     if self.order_line and res.get('line_id') in self.order_line.ids:
    #         get_current_line = self.env['sale.order.line'].browse(
    #             res.get('line_id'))
    #         product_list = []
    #         for dependency in get_current_line.product_id.depends:
    #             product_list = get_current_line.product_id.get_dependent_product_in_variants(
    #                 dependency.technical_name, product_list, get_current_line.product_id)

    #         if product_list:
    #             for product in product_list:
    #                 if self.order_line and product:
    #                     get_line = self.order_line.filtered(
    #                         lambda x: x.product_id.id == product.id)
    #                     if not get_line:
    #                         self.env['sale.order.line'].create(
    #                             {'product_id': product.id, 'order_id': self.id})
    #     return res
    

    def _cart_update(self, *args, **kwargs):
        product_id  = kwargs['product_id']
        sh_product = self.env['product.product'].browse(product_id).exists()
        check_product_blog = sh_product.check_variant_has_post(sh_product)
        self.clear_caches()
        if not check_product_blog:
            value = {'sh_blog_post_not_exists': 'sh_blog_post_not_exists'}
            if sh_product and sh_product.product_template_attribute_value_ids and sh_product.product_template_attribute_value_ids[0]:
                value.update({'product_varsion':sh_product.product_template_attribute_value_ids[0].name})
            return value
        
        #### Check product has blog or not
        
        res = super(SaleOrder, self)._cart_update(*args, **kwargs)

        if self.order_line and res.get('line_id') in self.order_line.ids:
            get_current_line = self.env['sale.order.line'].browse(
                res.get('line_id'))
            product_list = []
            for dependency in get_current_line.product_id.depends:
                product_list = get_current_line.product_id.get_dependent_product_in_variants(
                    dependency.technical_name, product_list, get_current_line.product_id)

            if product_list:
                for product in product_list:
                    if self.order_line and product:
                        get_line = self.order_line.filtered(
                            lambda x: x.product_id.id == product.id)
                        if not get_line:
                            self.env['sale.order.line'].create(
                                {'product_id': product.id, 'order_id': self.id})
                            
        return res
    