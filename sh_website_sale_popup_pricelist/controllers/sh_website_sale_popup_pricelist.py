# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies

from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request

from werkzeug.urls import url_decode, url_encode, url_parse

class ShWebsiteSalePopupPricelistWebsiteSale(WebsiteSale):

    @http.route('/sh_website_sale_popup_pricelist/get_pricelist_available_for_popup', auth='public', type='json', website=True)
    def get_pricelist_available_for_popup(self,stored_pricelist):
        """
            Check session data if sh_website_sale_popup_current_pl is not set then check popup pricelist config setting.
            get available pricelist from website and return Pricelist.
        """
        values = []
        show_popup = True
        available_pricelists = request.website.get_pricelist_available()
        
        if stored_pricelist:
            if int(stored_pricelist) in available_pricelists.ids:
                show_popup = False

        if show_popup and request.website.is_sh_website_sale_popup_pricelist:
            show_image = request.website.viewref('sh_website_sale_popup_pricelist.sh_website_sale_popup_pricelist_website_sale_pricelist_list').active
            pricelist = request.website.get_pricelist_available(show_visible=True)
            if pricelist:
                for pl in pricelist:
                    values.append({"id": pl.id, "name": pl.currency_id.name, "show_image": show_image})
        return values




    @http.route(['/sh_website_sale_popup_pricelist/change_pricelist/<model("product.pricelist"):pricelist>'], type='http', auth="public", website=True, sitemap=False)
    def sh_website_sale_popup_pricelist_pricelist_change(self, pricelist, **post):
        website = request.env['website'].get_current_website()
        redirect_url = request.httprequest.referrer

        # ------------------------------------------------
        # SOFTHEALER CUSTOM CODE HERE IN ORDER TO REDIRECT PROPER PLACE
        # WHEN PRICELIST CHANGE.
        # for help check standard odoo route:
        # @http.route(['/shop/change_pricelist/<model("product.pricelist"):pricelist>'], type='http', auth="public", website=True, sitemap=False)
        # def pricelist_change(self, pricelist, **post):
        # we have issue when share product URL with attribute at that time
        # that attribute not kept when change pricelist to fix this issue
        # we have added redirect url from javascript side.
        # for ex, http://localhost:8084/shop/customizable-desk-9#attr=2,3
        # ------------------------------------------------
        if post.get('redirect',False):
            redirect_url = post.get('redirect',False)

        # ------------------------------------------------
        # SOFTHEALER CUSTOM CODE HERE IN ORDER TO REDIRECT PROPER PLACE
        # WHEN PRICELIST CHANGE.            
        # ------------------------------------------------            

        if (pricelist.selectable or pricelist == request.env.user.partner_id.property_product_pricelist) \
                and website.is_pricelist_available(pricelist.id):
            if redirect_url and request.website.is_view_active('website_sale.filter_products_price'):
                decoded_url = url_parse(redirect_url)
                args = url_decode(decoded_url.query)
                min_price = args.get('min_price')
                max_price = args.get('max_price')
                if min_price or max_price:
                    previous_price_list = request.website.get_current_pricelist()
                    try:
                        min_price = float(min_price)
                        args['min_price'] = min_price and str(
                            previous_price_list.currency_id._convert(min_price, pricelist.currency_id, request.website.company_id, fields.Date.today(), round=False)
                        )
                    except (ValueError, TypeError):
                        pass
                    try:
                        max_price = float(max_price)
                        args['max_price'] = max_price and str(
                            previous_price_list.currency_id._convert(max_price, pricelist.currency_id, request.website.company_id, fields.Date.today(), round=False)
                        )
                    except (ValueError, TypeError):
                        pass
                    redirect_url = decoded_url.replace(query=url_encode(args)).to_url()
            request.session['website_sale_current_pl'] = pricelist.id
            request.website.sale_get_order(update_pricelist=True)
        return request.redirect(redirect_url or '/shop')


