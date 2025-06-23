# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api, Command
from odoo.tools.translate import html_translate
from odoo.exceptions import ValidationError
from datetime import timedelta, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sh_confirm_date = fields.Datetime("Confirmation Date")
    
    @api.model_create_multi
    def create(self,vals_list):
        res = super(SaleOrder,self).create(vals_list)
        # -- THIS CONDITION ADD BECAUSE WE NEED ONLY WEBSITE ORDER CREATION NOTIFICATION----

        if res.website_id:
            for vals in vals_list:
                users = res.env['res.users'].search([])
                listt = []
                for user in users:
                    if user.has_group('sales_team.group_sale_manager') and user != self.env.user:
                        listt.append(user)
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                self.env['user.push.notification'].push_notification(listt,'Sale Order Created','Sale Order Reference %s:'% (res.name),base_url+"/mail/view?model=sale.order&res_id="+str(res.id),'sale.order',res.id,'sale')
        return res

    request_quote_message = fields.Text("Requested Quote Message")  

    def get_dependent_product(self, technical_name, product_list, product):
        if technical_name:
            product=self.env['product.product'].search([('sh_technical_name','=',technical_name),('product_template_variant_value_ids.id','in',product.product_template_variant_value_ids.ids)],limit=1)
            if product:
                product_list.append(product)
                if product.depends:
                    for dependency in product.depends:
                        product_list = self.get_dependent_product(dependency.technical_name, product_list, product)
        
        return product_list
    

    @api.onchange('order_line')
    def onchange_product(self):
        
        for line in self.order_line:
            if line.product_id.depends:
              #recursive 
                for dependency in line.product_id.depends:
                    product_list = []
                    product_list = line.product_id.get_dependent_product_in_variants(
                    dependency.technical_name, product_list, line.product_id)

                    for product_item in product_list:
                        
                        if  product_item.not_unique_product or not self.order_line.filtered(lambda x:x.product_id == product_item):
                            price = 0.00
                            if self.pricelist_id:
                                price = self.pricelist_id.with_context(uom=product_item.uom_id.id)._get_product_price(product_item, 1, False)
                            else:
                                price = product_item.lst_price
                            if product_item:
                                self.order_line = [Command.create({
                                    'product_id': product_item.id,
                                    "product_uom_qty": 1,
                                    "price_unit":price,
                                    })]

    def write(self, vals):
        for rec in self:
            if vals.get('state', False) in ['sale'] and rec.date_order:
                vals.update({
                    'date_order': rec.date_order,
                    'sh_confirm_date': datetime.now(),
                })
        return super(SaleOrder, self).write(vals)