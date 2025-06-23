# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo.http import request
from odoo import http
import uuid
from odoo.osv import expression
from ast import literal_eval
from odoo.addons.http_routing.models.ir_http import slug


def generate_slider_tab_token():
    ran_num = str(uuid.uuid4().int)
    token = int(ran_num[:5] + ran_num[-5:])
    return str(token)


class Main(http.Controller):

    # --------------------------------------------------------------------------
    # Prepare Products Vals
    # --------------------------------------------------------------------------

    def _prepare_product_vals(self, products):
        fields = ['id', 'name', 'website_url', 'description_sale','sh_product_counter']
        res = {}
        res.update({
            'products': products.read(fields),
        })

        FieldMonetary = request.env['ir.qweb.field.monetary']
        monetary_options = {
            'display_currency': request.website.get_current_pricelist().currency_id,
        }

#         rating = request.website.viewref('website_sale.product_comment').active

        for res_product, product in zip(res['products'], products):
            combination_info = product._get_combination_info(
                only_template=True)
            res_product.update(combination_info)
            res_product['list_price'] = FieldMonetary.value_to_html(
                res_product['list_price'], monetary_options)
            res_product['price'] = FieldMonetary.value_to_html(
                res_product['price'], monetary_options)
            # Product Variant
            res_product['product_variant_id'] = product._get_first_possible_variant_id()

            # In Wish
            res_product['in_wish'] = product._is_in_wishlist()

            # Ribbon
            res_product['ribbon_id'] = product.website_ribbon_id.id if product.website_ribbon_id else False
            res_product['ribbon_bg_color'] = product.website_ribbon_id.bg_color if product.website_ribbon_id else ""
            res_product['ribbon_text_color'] = product.website_ribbon_id.text_color if product.website_ribbon_id else ''
            res_product['ribbon_html_class'] = product.website_ribbon_id.html_class if product.website_ribbon_id else ''
            res_product['ribbon_html'] = product.website_ribbon_id.html if product.website_ribbon_id else ''

            # ecommerce Category
            res_product['category'] = ', '.join(
                map(lambda x: (x.name or ''), product.public_categ_ids))

            # Rating
#             res_product['rating'] = ''
#             if rating:
            res_product['rating'] = request.env["ir.ui.view"].sudo()._render_template('portal_rating.rating_widget_stars_static', values={
                'rating_avg': product.rating_avg,
                'rating_count': product.rating_count,
            })
            
            res_product['price'] = request.env["ir.ui.view"].sudo()._render_template('sh_ecommerce_snippet.sh_ecommerce_snippet_price_tmpl', values={
                'combination_info': combination_info,
                'website':request.website,
            })

        return res.get('products')

    # --------------------------------------------------------------------------
    # Prepare Products Vals
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Get Products
    # --------------------------------------------------------------------------

    @http.route('/sh_ecommerce_snippet/get_products', type='json', auth='public', website=True)
    def get_products(self, item_template=False, categs_ids=False, filter_id=False, options={}, **kwargs):
        ProductTemplate = request.env['product.template']
        res = {}
        data = ''
        filter = False

        # --------------------------------------------------------------------------
        # Prepare Options
        res.update({
            'display_add_to_cart': options.get('display_add_to_cart', False),
            'display_description': options.get('display_description', False),
            'display_wishlist': options.get('display_wishlist', False),
            'display_price': options.get('display_price', False),
            'display_rating': False,
            'display_category': options.get('display_category', False),
        })
        order = options.get(
            'order', "is_published desc, website_sequence ASC, id desc")
        limit = options.get('limit', False)

        # --------------------------------------------------------------------------
        # Prepare domain and order from filters
        if filter_id:
            default_domain = [
                ('sale_ok', '=', True),
                ('website_published', '=', True),
            ] + request.website.website_domain()

            filter = request.env['sh.ecom.s.filter'].sudo().search(
                [('id', '=', filter_id)], limit=1)

        # Default Behavior
        is_show_tab_local = True
        is_show_slider_local = False
        if filter:
            is_show_tab_local = filter.is_show_tab
            is_show_slider_local = filter.is_show_slider

        # ========================================
        # Prepare Tabs
        # ========================================
        list_tabs_dic = []
        tab_token_pair_dic = {}

        if filter and filter.tab_product_line:
            for tab in filter.tab_product_line:
                token = generate_slider_tab_token()
                nav_tab_dic = {
                    'id': tab.id,
                    'name': tab.name,
                    'href': '#nav_tab_' + token,
                }
                
                list_tabs_dic.append(nav_tab_dic)
                tab_token_pair_dic.update({
                    tab.id: token
                })

        # ========================================
        # Prepare Tabs
        # ========================================

        # ========================================
        # Prepare Tab pane/ Tab Content
        # ========================================
        list_tab_panes_dic = []
        if filter and filter.tab_product_line:
            is_first_tab_with_content = True
            tabs = filter.tab_product_line

            # ---------------------------
            # FOR SINGLE TAB
            # ---------------------------
            if options.get('tab_id', False):
                tab_id = options.get('tab_id')
                tabs = filter.tab_product_line.filtered(
                    lambda line: line.id == tab_id)
            # ---------------------------
            # FOR SINGLE TAB
            # ---------------------------

            for tab in tabs:
                tab_pane_dic = {
                    'id': tab.id,
                    'name': tab.name,
                    'id_tab_pane': 'nav_tab_' + tab_token_pair_dic.get(tab.id),
                    'categ_name':tab.categ_id.name if tab.categ_id else False, 
                    'categ_url':"/shop/category/%s" % slug(tab.categ_id) if tab.categ_id else False,
                
                }

                tab_content = []
                if is_first_tab_with_content and filter.filter_type == 'manual' and tab.product_tmpl_ids:
                    tab_content = self._prepare_product_vals(
                        tab.product_tmpl_ids)
                    
                elif is_first_tab_with_content and filter.filter_type == 'domain':
                    # --------------------------------------------------------------------------
                    # Prepare domain and order from filters
                    if tab.filter_id.sudo():
                        default_domain = [
                            ('sale_ok', '=', True),
                            ('website_published', '=', True),
                        ] + request.website.website_domain()

                        filter_sudo = tab.filter_id.sudo()
                        domain = filter_sudo._get_eval_domain()
                        domain = expression.AND([domain, default_domain])
                        order = ','.join(literal_eval(
                            filter_sudo.sort)) or 'is_published desc, website_sequence ASC, id desc'

                        limit = None
                        if tab.limit > 0:
                            limit = tab.limit

                        # --------------------------------------------------------------------------
                        # Find Products
                        products = ProductTemplate.search(
                            domain,
                            limit=limit,
                            order=order
                        )
                        if products:
                            tab_content = self._prepare_product_vals(products)
                tab_pane_dic.update({
                    'list_products_dic': tab_content
                })

                # ==================================
                # No TAB THINGS
                if is_show_tab_local:
                    is_first_tab_with_content = False
                else:
                    is_first_tab_with_content = True

                # No TAB THINGS
                # ==================================
                list_tab_panes_dic.append(tab_pane_dic)
                
                # list_tab_panes_dic[0].update({
                #     'categ_id':tab.categ_id
                # })

        # ==================================
        # NO TAB THINGS
        if not is_show_tab_local and list_tab_panes_dic:
            list_tab_panes_dic_single = list_tab_panes_dic[0]
            list_products_dic_single_tab = []
            for tab_pane_dic in list_tab_panes_dic:
                list_products_dic = tab_pane_dic.get("list_products_dic", [])
                for product_dic in list_products_dic:
                    list_products_dic_single_tab.append(product_dic)

            list_tab_panes_dic_single.update({
                'list_products_dic': list_products_dic_single_tab,
            })

            list_tab_panes_dic = [list_tab_panes_dic_single]
            list_tabs_dic = []

        res.update({
            'list_tabs_dic': list_tabs_dic,
            'list_tab_panes_dic': list_tab_panes_dic,
            'row_classes': 'owl-carousel owl-theme' if is_show_slider_local else 'row',
            'column_classes': 'item' if is_show_slider_local else options.get('column_class', 'col-md-4')
        })

        data = request.env["ir.ui.view"].sudo(
        )._render_template(item_template, values=res)

        values = {
            'data': data
        }

        if filter:
            values.update({
                'items':    filter.items,
                'autoplay': filter.autoplay,
                'speed':    filter.speed,
                'loop':     filter.loop,
                'nav':      filter.nav,
                'is_show_slider_local': is_show_slider_local,
            })

        return values
