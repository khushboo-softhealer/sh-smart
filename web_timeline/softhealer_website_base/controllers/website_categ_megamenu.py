# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo.http import request
from odoo import http
import json

class ShCategMegaMenu(http.Controller):

    @http.route(['/get_sh_edition_details'], type='json', auth="public", website=True)
    def get_sh_edition_details(self, sh_editions, **post):
        """
        Get Edition details
        """
        edition_obj = request.env['sh.edition'].sudo().search([])
        if sh_editions:
            fields = ['id', 'name']

            dict = {
                'sh_edition_info_details': edition_obj.read(fields),
            }
            if dict:
                return dict
        return {}

    @http.route('/softhealer_website_base/get_app_theme_categories', type='json', auth='public', website=True)
    def get_app_theme_categories(self, **kwargs):
        ecom_category_obj = request.env['product.public.category'].sudo()

        app_domain = [('sh_is_app', '=', True)] + \
            request.website.website_domain()
        app_categories = ecom_category_obj.search(app_domain)

        theme_domain = [('sh_is_theme', '=', True)] + \
            request.website.website_domain()
        theme_categories = ecom_category_obj.search(theme_domain)

        data = request.env["ir.ui.view"].sudo()._render_template(
            'softhealer_website_base.theme_softhealer_base_ecom_megamenu_categ_tmpl', values={
                'app_categories': app_categories,
                'theme_categories': theme_categories,
            })

        values = {
            'data': data
        }
        return values
