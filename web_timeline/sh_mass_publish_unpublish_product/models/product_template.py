# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import _, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def sh_action_publish_product(self):
        context = self.env.context.get('active_ids')
        products_obj = self.search([('id', 'in', context)])

        for product in products_obj:
            if self.env.user.has_group('sh_product_base.group_product_tags_manager'):
                product.write({'is_published': True})
            else:
                raise ValidationError(
                    'You are not Authorised to perform this action !')

    def sh_action_unpublish_product(self):
        context = self.env.context.get('active_ids')
        products_obj = self.search([('id', 'in', context)])

        for product in products_obj:
            if self.env.user.has_group('sh_product_base.group_product_tags_manager'):
                product.write({'is_published': False})
            else:
                raise ValidationError(
                    'You are not Authorised to perform this action !')
