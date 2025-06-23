# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import api, fields, models, _
from odoo.addons.http_routing.models.ir_http import slug, unslug
from odoo.addons.website.models import ir_http
from odoo.http import request
from odoo.tools.translate import html_translate
from odoo.osv import expression


class ProductTemplate(models.Model):
    _inherit = "product.template",

    def _search_get_detail(self, website, order, options):
        ## PURPOSE FOR INHERIT METHOD
        ## IN ORDER TO GET SEARCH WORK WITH PRODUCT TECHNICAL NAME
        result = super()._search_get_detail(website, order, options)
        search_fields = result.get('search_fields')
        search_fields.append('sh_technical_name')
        return result

    def update_template_meta_image_url(self):
        for rec in self:
            if rec:
                rec.update({
                    'website_meta_og_img': '/web/image/product.template/'+ str(rec.id) +'/image_1024'
                })

    def update_variant_image(self):
        for rec in self:
            product = self.env['product.product'].search([('product_tmpl_id','=',rec.id)])
            product.update({
                'image_1920': rec.image_1920
            })

    ## Custom redirect to store URL
    def sh_get_website_redirect(self):
        for product in self:
            if product.id:
                sh_website_url = "https://store.softhealer.com/shop/%s" % slug(product)
                return {
                    'name': ('Website URL'),
                    'type': 'ir.actions.act_url',
                    'url': sh_website_url,
                    'target': 'new'
                }


class ProductProduct(models.Model):
    _inherit = "product.product",

    def check_variant_has_post(self, product_id):
        if product_id and product_id.sh_blog_post_id:
            return True
        return False

    ## Custom redirect to store URL
    def sh_get_website_redirect(self):
        for product in self:
            attributes = ','.join(str(x) for x in product.product_template_attribute_value_ids.ids)
            sh_website_url = "https://store.softhealer.com%s#attr=%s" % (product.product_tmpl_id.website_url, attributes)
            return {
                'name': ('Website URL'),
                'type': 'ir.actions.act_url',
                'url': sh_website_url,
                'target': 'new'
            }
    


    