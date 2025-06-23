# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

import base64
import datetime

from itertools import islice

from odoo.addons.website.controllers.main import Website
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_blog.controllers.main import WebsiteBlog
from odoo.addons.http_routing.models.ir_http import url_for
from odoo.addons.http_routing.models.ir_http import slug
import re,logging
_logger = logging.getLogger(__name__)
from textwrap import shorten

from odoo import http, fields
from odoo.http import request
from odoo.tools import html_escape as escape
from odoo.addons.website.controllers.main import QueryURL
from odoo.tools import sql
from random import sample

LOC_PER_SITEMAP = 45000
SITEMAP_CACHE_TIME = datetime.timedelta(hours=12)


class ShWebsiteAutoComplete(Website):

    @http.route()
    def website_info(self, **kwargs):
        ### Redirect URL 
        return request.redirect('/')

    @http.route('/website/snippet/autocomplete', type='json', auth='public', website=True)
    def autocomplete(self, search_type=None, term=None, order=None, limit=5, max_nb_chars=999, options=None):
        """
        Returns list of results according to the term and options

        :param str search_type: indicates what to search within, 'all' matches all available types
        :param str term: search term written by the user
        :param str order:
        :param int limit: number of results to consider, defaults to 5
        :param int max_nb_chars: max number of characters for text fields
        :param dict options: options map containing
            allowFuzzy: enables the fuzzy matching when truthy
            fuzzy (boolean): True when called after finding a name through fuzzy matching

        :returns: dict (or False if no result) containing
            - 'results' (list): results (only their needed field values)
                    note: the monetary fields will be strings properly formatted and
                    already containing the currency
            - 'results_count' (int): the number of results in the database
                    that matched the search query
            - 'parts' (dict): presence of fields across all results
            - 'fuzzy_search': search term used instead of requested search
        """

        '''

            PURPOSE BEHIND OVERRIDE THIS CONTROLLER IS
            STANDARD SORT THE SEARCH DATA BASED ON NAME
            BUT AS PER OUR NEED WE ALREADY SORTED DATA BASED ON MODEL
            SO NO NEED TO RE-SORT THE DATA

        '''
        order = self._get_search_order(order)
        options = options or {}

        if 'display_currency' not in options:
            options['display_currency'] = request.website.currency_id

        results_count, search_results, fuzzy_term = request.website._search_with_fuzzy(
            search_type, term, limit, order, options)
        
        if not results_count:
            return {
                'results': [],
                'results_count': 0,
                'parts': {},
            }
        term = fuzzy_term or term
        search_results = request.website._search_render_results(
            search_results, limit)

        mappings = []
        results_data = []
        for search_result in search_results:
            results_data += search_result['results_data']
            mappings.append(search_result['mapping'])

        # --------------------------------------------------------------------------------------------------
        # STANDARD SORT DATA WITH NAME BUT WE NEED TO SORT WITH MODELS SO NO NEED TO USE THIS CODE
        # --------------------------------------------------------------------------------------------------
        # if search_type == 'all':
        #     # Only supported order for 'all' is on name
        #     results_data.sort(key=lambda r: r.get('name', ''),
        #                       reverse='name desc' in order)
        # --------------------------------------------------------------------------------------------------
        # STANDARD SORT DATA WITH NAME BUT WE NEED TO SORT WITH MODELS SO NO NEED TO USE THIS CODE
        # --------------------------------------------------------------------------------------------------

        search_term = fuzzy_term or term

        # Popular searches code start
        website = request.website
        if website and website.enable_website_popular_searches:
            if results_count and search_type and search_term and len(search_term) >= 5:
                domain = [('name', '=', search_term.strip())]
                domain += website.website_domain()

                PopularSearches = request.env['sh.website.popular.searches']
                searches = PopularSearches.search(domain)
                if searches:
                    searches[0].searches_count += 1
                else:
                    PopularSearches.create({'name': search_term.strip(),
                                            'search_type': search_type,
                                            'website_id': website.id,
                                            'searches_count': 1})
        # Popular searches code end

        results_data = results_data[:limit]
        result = []

        # this code for sorting results by Header name first, then after anther result.
        results_data = sorted(results_data, key=lambda r: (
            term.lower().strip() in r.get('name', '').lower().strip()), reverse=True)

        
        for record in results_data:
            mapping = record['_mapping']
            mapped = {
                '_fa': record.get('_fa'),
            }
            curr_pricelist = request.website.pricelist_id
            pro_id = record.get('id')
            
            if pro_id and curr_pricelist and curr_pricelist.currency_id:
                product = request.env['product.template'].browse(pro_id)
                monetary_options = {'display_currency': curr_pricelist.currency_id}
                product_list = []
                total_price = 0
                
                for dependency in product.sudo().product_variant_id.sudo().depends:
                    product_list = product.sudo().product_variant_id.sudo().get_dependent_product_in_variants(
                        dependency.sudo().technical_name, product_list, product.product_variant_id)

                if product_list:
                    for lst in product_list:
                        combination = lst.sudo()._get_combination_info_variant(pricelist=curr_pricelist)
                        total_price = total_price + combination['price']

                if product.sudo().product_variant_id:
                    variant_list_price = product.sudo().product_variant_id.sudo()._get_combination_info_variant(pricelist=curr_pricelist)
                    total_price = total_price + variant_list_price['price']

                    list_price = request.env['ir.qweb.field.monetary'].value_to_html(
                        total_price, monetary_options
                    )

                    record.update({
                        'price':list_price,
                    })

            for mapped_name, field_meta in mapping.items():
                value = record.get(field_meta.get('name'))
                if not value:
                    mapped[mapped_name] = ''
                    continue
                field_type = field_meta.get('type')
                if field_type == 'text':
                    if value and field_meta.get('truncate', True):
                        value = shorten(value, max_nb_chars, placeholder='...')
                    if field_meta.get('match') and value and term:
                        pattern = '|'.join(map(re.escape, term.split()))
                        if pattern:
                            parts = re.split(
                                f'({pattern})', value, flags=re.IGNORECASE)
                            if len(parts) > 1:
                                value = request.env['ir.ui.view'].sudo()._render_template(
                                    "website.search_text_with_highlight",
                                    {'parts': parts}
                                )
                                field_type = 'html'

                if field_type not in ('image', 'binary') and ('ir.qweb.field.%s' % field_type) in request.env:
                    opt = {}
                    if field_type == 'monetary':
                        opt['display_currency'] = options['display_currency']
                    value = request.env[('ir.qweb.field.%s' %
                                         field_type)].value_to_html(value, opt)
                mapped[mapped_name] = escape(value)
            result.append(mapped)

        return {
            'results': result,
            'results_count': results_count,
            'parts': {key: True for mapping in mappings for key in mapping},
            'fuzzy_search': fuzzy_term,
        }

    @http.route('/sh_website/popular_searches', type='json', auth='public', website=True)
    def popular_searches(self, min_search_count=100):
        """
        METHOD OF SOFTHEALER TECHNOLOGIES

        This function returns a list of popular searches on a website with a minimum search count and
        filters based on user permissions.

        :param min_search_count: This parameter is an optional integer value that sets the minimum
        number of searches required for a search term to be considered "popular". By default, it is set
        to 100, defaults to 100 (optional)
        :return: a list of dictionaries containing the name, searches_count, and is_published fields of
        popular searches on the website that have a searches_count greater than or equal to the
        specified min_search_count and are published. If the user is an admin or website designer, the
        is_published filter is ignored. The list is empty if no popular searches meet the criteria.
        """
        website = request.website
        searches = []
        if website.enable_website_popular_searches:

            domain = [('searches_count', '>=', min_search_count),
                      ('is_published', '=', True)]
            if request.env.user._is_admin() or request.env.user.has_group("website.group_website_designer"):
                domain = [('searches_count', '>=', min_search_count)]

            if website:
                domain += website.website_domain()

            searches = request.env['sh.website.popular.searches'].search_read(
                domain, fields=['name', 'searches_count', 'is_published'])

        return searches
    

    @http.route()
    def sitemap_xml_index(self, **kwargs):

        current_website = request.website
        Attachment = request.env['ir.attachment'].sudo()
        View = request.env['ir.ui.view'].sudo()
        mimetype = 'application/xml;charset=utf-8'
        content = None
        
        
        # Softhealer Custom Code
        sh_current_website_domain_without_forward_slash_in_last = current_website.domain
        # sh_current_website_domain[-1] == '/'
        if sh_current_website_domain_without_forward_slash_in_last and sh_current_website_domain_without_forward_slash_in_last.endswith('/'):
            sh_current_website_domain_without_forward_slash_in_last = sh_current_website_domain_without_forward_slash_in_last[:-1]
        # Softhealer Custom Code


        # print("\n\n\n ======= sitemap_xml_index ====>", current_website)
        # print("\n\n\n ======= request.httprequest.url_root[:-1] ====>", request.httprequest.url_root[:-1])
        # print("\n\n\n ======= request.httprequest.url_root ====>", request.httprequest.url_root)
        # print("\n\n\n ======= current_website.domain ====>", current_website.domain)


        def create_sitemap(url, content):
            return Attachment.create({
                'raw': content.encode(),
                'mimetype': mimetype,
                'type': 'binary',
                'name': url,
                'url': url,
            })
        dom = [('url', '=', '/sitemap-%d.xml' % current_website.id), ('type', '=', 'binary')]
        sitemap = Attachment.search(dom, limit=1)
        if sitemap:
            # Check if stored version is still valid
            create_date = fields.Datetime.from_string(sitemap.create_date)
            delta = datetime.datetime.now() - create_date
            if delta < SITEMAP_CACHE_TIME:
                content = base64.b64decode(sitemap.datas)

        if not content:
            # Remove all sitemaps in ir.attachments as we're going to regenerated them
            dom = [('type', '=', 'binary'), '|', ('url', '=like', '/sitemap-%d-%%.xml' % current_website.id),
                   ('url', '=', '/sitemap-%d.xml' % current_website.id)]
            sitemaps = Attachment.search(dom)
            sitemaps.unlink()

            pages = 0
            locs = request.website.with_user(request.website.user_id)._enumerate_pages()
            while True:

                # Softhealer Custom Code
                values = {
                    'locs': islice(locs, 0, LOC_PER_SITEMAP),
                    'url_root': sh_current_website_domain_without_forward_slash_in_last,
                }
                # Softhealer Custom Code
                
                # values = {
                #     'locs': islice(locs, 0, LOC_PER_SITEMAP),
                #     'url_root': request.httprequest.url_root[:-1],
                # }

                # Softhealer Custom Code
                _logger.warning("@1 sitemap_xml_index ---> %s" % request.httprequest.url_root)
                _logger.warning("@1 sh_current_website_domain_without_forward_slash_in_last ---> %s" % sh_current_website_domain_without_forward_slash_in_last)

                # Softhealer Custom Code
                
                urls = View._render_template('website.sitemap_locs', values)
                if urls.strip():
                    content = View._render_template('website.sitemap_xml', {'content': urls})
                    pages += 1
                    last_sitemap = create_sitemap('/sitemap-%d-%d.xml' % (current_website.id, pages), content)
                else:
                    break

            if not pages:
                return request.not_found()
            elif pages == 1:
                # rename the -id-page.xml => -id.xml
                last_sitemap.write({
                    'url': "/sitemap-%d.xml" % current_website.id,
                    'name': "/sitemap-%d.xml" % current_website.id,
                })
            else:
                # TODO: in master/saas-15, move current_website_id in template directly
                pages_with_website = ["%d-%d" % (current_website.id, p) for p in range(1, pages + 1)]

                # Sitemaps must be split in several smaller files with a sitemap index

                # content = View._render_template('website.sitemap_index_xml', {
                #     'pages': pages_with_website,
                #     'url_root': request.httprequest.url_root,
                # })
                # Softhealer Custom Code
                content = View._render_template('website.sitemap_index_xml', {
                    'pages': pages_with_website,
                    'url_root': sh_current_website_domain_without_forward_slash_in_last + '/',
                })
                # Softhealer Custom Code
                # Softhealer Custom Code
                _logger.warning("@2 sitemap_xml_index ---> %s" % request.httprequest.url_root)
                _logger.warning("@2 sh_current_website_domain_without_forward_slash_in_last ---> %s" % sh_current_website_domain_without_forward_slash_in_last)

                # Softhealer Custom Code

                create_sitemap('/sitemap-%d.xml' % current_website.id, content)

        return request.make_response(content, [('Content-Type', mimetype)])

    

class SofthealerWebsiteBaseShop(WebsiteSale):
    
    @http.route()
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        """
        INHERITED BY SOFTHEALER
        To redirect url to softhealer store
        """
        res = super(SofthealerWebsiteBaseShop, self).shop(
            page, category, search, min_price, max_price, ppg, **post)
        # if request.website and request.website.domain != 'https://store.softhealer.com':
        #     url = 'https://store.softhealer.com' + url_for(request.httprequest.path)
        #     return request.redirect(url, code=301, local=False)
        return res
    
    @http.route()
    def old_product(self, product, category='', search='', **kwargs):
        """
        INHERITED BY SOFTHEALER
        To redirect url to softhealer store
        """
        # product_url = "/shop/" + slug(product)
        # if request.website and request.website.domain != 'https://store.softhealer.com':
        #     url = 'https://store.softhealer.com' + url_for(product_url)
        #     return request.redirect(url, code=301, local=False)
        return super(SofthealerWebsiteBaseShop, self).old_product(product, category, search, **kwargs)
    
    @http.route()
    def product(self, product, category='', search='', **kwargs):
        """
        INHERITED BY SOFTHEALER
        To redirect url to softhealer store
        """
        # product_url = "/shop/" + slug(product)
        # if request.website and request.website.domain != 'https://store.softhealer.com':
        #     url = 'https://store.softhealer.com' + url_for(product_url)
        #     return request.redirect(url, code=301, local=False)
        return super(SofthealerWebsiteBaseShop, self).product(product, category, search, **kwargs)

class SofthealerWebsiteBaseBlog(WebsiteBlog):
    
    @http.route()
    def old_blog_post(self, blog, blog_post, **post):
        #### Blog post compatible controller inherit by softhealer
        #### URL redirect to softhealer store
        # if request.website and request.website.domain != 'https://store.softhealer.com' and not blog.sh_is_this_career_blog:
            
        #     ### GET products from blog post
        #     request.env.cr.execute("""select product_product_id from blog_post_product_product_rel where blog_post_id =%s""",[blog_post.id])
        #     res = request.env.cr.dictfetchall()
        #     products= request.env['product.product'].sudo().browse([r['product_product_id'] for r in res])

        #     ### GET highest version Product
        #     value = products.product_template_attribute_value_ids.sorted(key='name', reverse=True)
            
        #     final_product = False
        #     for rec in products:
        #         if value and value[0].id == rec.product_template_attribute_value_ids.id:
        #             final_product = rec
            
        #     ### if product find get new blog post id and redirect url 
        #     if final_product and final_product.sudo().sh_blog_post_id:
        #         blog = final_product.sudo().sh_blog_post_id.sudo().blog_id
        #         blog_post = final_product.sudo().sh_blog_post_id
        #         blog_url = "/blog/" + slug(blog) + "/" +  slug(blog_post)
        #         url = 'https://store.softhealer.com' + url_for(blog_url)
        #         return request.redirect(url, code=301, local=False)
        
        #return super(SofthealerWebsiteBaseBlog, self).old_blog_post(blog, blog_post, tag_id,page,enable_editor, **post)
        return super(SofthealerWebsiteBaseBlog, self).old_blog_post(blog, blog_post, **post)
    
    @http.route()
    def blog_post(self, blog, blog_post, tag_id=None, page=1, enable_editor=None, **post):
        #### Blog post controller inherit by softhealer
        #### URL redirect to softhealer store
        # if request.website and request.website.domain != 'https://store.softhealer.com' and not blog.sh_is_this_career_blog:
        #     url = 'https://store.softhealer.com' + url_for(request.httprequest.path)
        #     return request.redirect(url, code=301, local=False)
        
        related_blogs = request.env['blog.post'].sudo().search([
            ('blog_id','=',blog.id),
            ('is_published','=',True),
            ('id','!=',blog_post.id)])
        
        random_blogs = sample(list(related_blogs), min(4, len(related_blogs)))
        response = super(SofthealerWebsiteBaseBlog, self).blog_post(
            blog, blog_post, tag_id, page, enable_editor, **post
        )
        if hasattr(response, 'qcontext'):
            response.qcontext['random_blogs'] = random_blogs
        return response
