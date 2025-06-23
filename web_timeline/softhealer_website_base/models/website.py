# -*- encoding: utf-8 -*-
# Part of Softhealer Technologies.

import base64

from odoo import fields, models, tools
from odoo.http import request
from odoo.modules.module import get_resource_path
from psycopg2 import sql





# for sitemap imports
import logging
logger = logging.getLogger(__name__)
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.osv.expression import AND, OR, FALSE_DOMAIN, get_unaccent_wrapper

# for sitemap imports



class ShWebsite(models.Model):
    _inherit = "website"

    sh_softhealer_website_expand_warranty_ticket_type_id = fields.Many2one(
        'sh.helpdesk.ticket.type', string='Expand Warranty Ticket Type')

    ## MARKETING
    sh_softhealer_website_default_campaign_id = fields.Many2one(
        'utm.campaign', string='Default Campaign')
    sh_softhealer_website_default_medium_id = fields.Many2one(
        'utm.medium', string='Default Medium')
    sh_softhealer_website_default_source_id = fields.Many2one(
        'utm.source', string='Default Source')
    enable_website_popular_searches = fields.Boolean(
        "Enable Website Popular Searches")

    def get_page(self):
        return request.httprequest.path

    def sh_softhealer_website_default_logo_scrolled(self):
        image_path = get_resource_path(
            'website', 'static/src/img', 'website_logo.svg')
        with tools.file_open(image_path, 'rb') as logo_file:
            return base64.b64encode(logo_file.read())

    sh_softhealer_website_logo_scrolled = fields.Binary(
        'Website Scrolled Logo', default=sh_softhealer_website_default_logo_scrolled, help="Display this logo on the website when header scrolled down.")

    def _search_exact(self, search_details, search, limit, order):
        '''

        PURPOSE BEHIND USING THIS METHOD IS
        WE ADD GLOBAL SEARCH FEATURE IN SH-SMART WEBSITE
        WE USE STANDARD CONTROLLER FOR GET RESULT FOR GLOBAL SEARCH
        STANDARD CONTROLLER USE THIS METHOD FOR SEARCH DATA WITH MODEL'S.

        NOW WE NEED TO ARRANGE SEARCH WITH (products , blogs and pages) SEQUENCE WISE
        SO WE USE THIS METHOD JUST FOR ARRANGE DATA MODEL SEQUENCE WISE

        '''

        # SORT DATA BASED ON MODELS - (product , blog and page)
        search_details = sorted(search_details, key=lambda d: (
            d['model'] != 'product.template', d['model'] != 'blog.post', d['model'] != 'website.page'))

        return super(ShWebsite, self)._search_exact(search_details=search_details, search=search, limit=limit, order=order)


    def _enumerate_pages(self, query_string=None, force=False):
        """
            SOFTHEALER OVERWRITE THIS METHOD TO GENERATE CUSTOM SITEMAP
            # /blog/odoo-1/sierra-tarahumara-1 --> /blog/odoo-1/post/sierra-tarahumara-1
            # /shop/ --> /shop/product/
            FOR WEBSITE 1 ONLY
        """

        """
            SOFTHEALER CUSTOM CODE FOR MOBIHEAL
            TO HIDE /SHOP RELATED ALL ROUTES FROM THE SITEMAP OF MOBIHEAL
            AND WE ARE CONSIDERING WEBSITE ID=3 IS MOBIHEAL HARD CODED

        """
        """ Available pages in the website/CMS. This is mostly used for links
            generation and can be overridden by modules setting up new HTML
            controllers for dynamic pages (e.g. blog).
            By default, returns template views marked as pages.
            :param str query_string: a (user-provided) string, fetches pages
                                     matching the string
            :returns: a list of mappings with two keys: ``name`` is the displayable
                      name of the resource (page), ``url`` is the absolute URL
                      of the same.
            :rtype: list({name: str, url: str})
        """

        router = self.env['ir.http'].routing_map()
        url_set = set()

        sitemap_endpoint_done = set()

        for rule in router.iter_rules():
            if 'sitemap' in rule.endpoint.routing and rule.endpoint.routing['sitemap'] is not True:
                if rule.endpoint.func in sitemap_endpoint_done:
                    continue
                # -------------------------------------------
                # FOR WEBSITE 3 ONLY - MOBIHEAL HARD CODED
                # WE DON'T WANT TO SHOW THE ALL /SHOP AND /SHOP/CATEGORY URL
                # -------------------------------------------
                if self.id == 3 or self.id == 1:
                    if '/shop' in rule.endpoint.routing.get('routes',[]):
                        continue
                # -------------------------------------------
                # FOR WEBSITE 3 ONLY - MOBIHEAL HARD CODED
                # WE DON'T WANT TO SHOW THE ALL /SHOP AND /SHOP/CATEGORY URL
                # -------------------------------------------
                sitemap_endpoint_done.add(rule.endpoint.func)
                func = rule.endpoint.routing['sitemap']
                if func is False:
                    continue
                for loc in func(self.env, rule, query_string):
                    yield loc
                continue

            if not self.rule_is_enumerable(rule):
                continue

            if 'sitemap' not in rule.endpoint.routing:
                logger.warning('No Sitemap value provided for controller %s (%s)' %
                               (rule.endpoint.original_endpoint, ','.join(rule.endpoint.routing['routes'])))

            converters = rule._converters or {}
            if query_string and not converters and (query_string not in rule.build({}, append_unknown=False)[1]):
                continue

            values = [{}]
            # converters with a domain are processed after the other ones
            convitems = sorted(
                converters.items(),
                key=lambda x: (hasattr(x[1], 'domain') and (x[1].domain != '[]'), rule._trace.index((True, x[0]))))

            for (i, (name, converter)) in enumerate(convitems):
                if 'website_id' in self.env[converter.model]._fields and (not converter.domain or converter.domain == '[]'):
                    converter.domain = "[('website_id', 'in', (False, current_website_id))]"

                newval = []
                for val in values:
                    query = i == len(convitems) - 1 and query_string
                    if query:
                        r = "".join([x[1] for x in rule._trace[1:] if not x[0]])  # remove model converter from route
                        query = sitemap_qs2dom(query, r, self.env[converter.model]._rec_name)
                        if query == FALSE_DOMAIN:
                            continue

                    for rec in converter.generate(self.env, args=val, dom=query):
                        # -------------------------------------------
                        # FOR WEBSITE 3 ONLY - MOBIHEAL HARD CODED
                        # WE DON'T WANT TO SHOW THE ALL THE PRODUCT DETAILS PAGE RELATED URLS IN MOBIHEAL 
                        # -------------------------------------------
                        if self.id == 3 or self.id == 1:
                            if rec._name == 'product.template':
                                continue

                        # -------------------------------------------
                        # FOR WEBSITE 3 ONLY - MOBIHEAL HARD CODED
                        # WE DON'T WANT TO SHOW THE ALL THE PRODUCT DETAILS PAGE RELATED URLS IN MOBIHEAL                             
                        # -------------------------------------------
                        newval.append(val.copy())
                        newval[-1].update({name: rec})
                values = newval

            for value in values:
                domain_part, url = rule.build(value, append_unknown=False)
                if not query_string or query_string.lower() in url.lower():

                    # -------------------------------------------
                    # Softhealer custom code START
                    # /blog/odoo-1/sierra-tarahumara-1 --> /blog/odoo-1/post/sierra-tarahumara-1
                    # -------------------------------------------
                    # FOR WEBSITE 1 ONLY 
                    if self.id  == 1:
                        if '/blog/' in url and url.count('/') == 3:
                            forbidden_strings = ["/blog/tag", "/feed"]
                            is_change_blog_url = True
                            for forbidden_str in forbidden_strings:
                                if forbidden_str in url:
                                    is_change_blog_url = False
                                    break
                            if is_change_blog_url:
                                last_slash_index = url.rfind('/')                                
                                # custom code to hide all post of odoo-2 named blog from the sitemap for website 1 only
                                if url[:last_slash_index] == '/blog/odoo-2':
                                    continue
                                # custom code to hide all post of odoo-2 named blog from the sitemap for website 1 only

                                # url = url[:last_slash_index] + '/post' + url[last_slash_index:]


                        # custom code to hide  odoo-2 named blog from the sitemap for website 1 only
                        if '/blog/' in url and url.count('/') == 2 and url == '/blog/odoo-2':
                            continue
                        # custom code to hide odoo-2 named blog from the sitemap for website 1 only


                    #     # -------------------------------------------
                    #     # Softhealer custom code. 
                    #     # /shop/ --> /shop/product/
                    #     # -------------------------------------------
                    #     if '/shop/' in url and '/shop/category/' not in url:
                    #         url = url.replace('/shop/','/shop/product/')

                    # -------------------------------------------
                    # Softhealer custom code END
                    # -------------------------------------------
                    page = {'loc': url}
                    if url in url_set:
                        continue
                    url_set.add(url)
                    yield page

        # '/' already has a http.route & is in the routing_map so it will already have an entry in the xml
        domain = [('url', '!=', '/')]
        if not force:
            domain += [('website_indexed', '=', True), ('visibility', '=', False)]
            # is_visible
            domain += [
                ('website_published', '=', True), ('visibility', '=', False),
                '|', ('date_publish', '=', False), ('date_publish', '<=', fields.Datetime.now())
            ]

        if query_string:
            domain += [('url', 'like', query_string)]

        pages = self._get_website_pages(domain)
        for page in pages:
            record = {'loc': page['url'], 'id': page['id'], 'name': page['name']}
            if page.view_id and page.view_id.priority != 16:
                record['priority'] = min(round(page.view_id.priority / 32.0, 1), 1)
            if page['write_date']:
                record['lastmod'] = page['write_date'].date()
            yield record

    def get_website_page_ids(self):
        if self.env.user.user_has_groups('softhealer_website_base.group_softhealer_website_editor_page'):
            domain = [('url', '!=', False)]
            if self:
                domain = AND([domain, self.website_domain()])
            pages = self.env['website.page'].sudo().search(domain)
            if self:
                pages = pages._get_most_specific_pages()
            return pages.ids
        return super().get_website_page_ids()


class ShWebsiteVisitor(models.Model):
    _inherit='website.visitor'

    def _upsert_visitor(self, access_token, force_track_values=None):
        """ Based on the given `access_token`, either create or return the
        related visitor if exists, through a single raw SQL UPSERT Query.

        It will also create a tracking record if requested, in the same query.

        :param access_token: token to be used to upsert the visitor
        :param force_track_values: an optional dict to create a track at the
            same time.
        :return: a tuple containing the visitor id and the upsert result (either
            `inserted` or `updated).
        """
        create_values = {
            'access_token': access_token,
            'lang_id': 1,
            # Note that it's possible for the GEOIP database to return a country
            # code which is unknown in Odoo
            'country_code': request.geoip.get('country_code'),
            'website_id': 1,
            'timezone': self._get_visitor_timezone() or None,
            'write_uid': self.env.uid,
            'create_uid': self.env.uid,
            # If the access_token is not a 32 length hexa string, it means that the
            # visitor is linked to a logged in user, in which case its partner_id is
            # used instead as the token.
            'partner_id': None if len(str(access_token)) == 32 else access_token,
        }
        query = """
            INSERT INTO website_visitor (
                partner_id, access_token, last_connection_datetime, visit_count, lang_id,
                website_id, timezone, write_uid, create_uid, write_date, create_date, country_id)
            VALUES (
                %(partner_id)s, %(access_token)s, now() at time zone 'UTC', 1, %(lang_id)s,
                %(website_id)s, %(timezone)s, %(create_uid)s, %(write_uid)s,
                now() at time zone 'UTC', now() at time zone 'UTC', (
                    SELECT id FROM res_country WHERE code = %(country_code)s
                )
            )
            ON CONFLICT (access_token)
            DO UPDATE SET
                last_connection_datetime=excluded.last_connection_datetime,
                visit_count = CASE WHEN website_visitor.last_connection_datetime < NOW() AT TIME ZONE 'UTC' - INTERVAL '8 hours'
                                    THEN website_visitor.visit_count + 1
                                    ELSE website_visitor.visit_count
                                END
            RETURNING id, CASE WHEN create_date = now() at time zone 'UTC' THEN 'inserted' ELSE 'updated' END AS upsert
        """

        if force_track_values:
            create_values['url'] = force_track_values['url']
            create_values['page_id'] = force_track_values.get('page_id')
            query = sql.SQL("""
                WITH visitor AS (
                    {query}, %(url)s AS url, %(page_id)s AS page_id
                ), track AS (
                    INSERT INTO website_track (visitor_id, url, page_id, visit_datetime)
                    SELECT id, url, page_id::integer, now() at time zone 'UTC' FROM visitor
                )
                SELECT id, upsert from visitor;
            """).format(query=sql.SQL(query))

        self.env.cr.execute(query, create_values)
        return self.env.cr.fetchone()


    # def _upsert_visitor(self, access_token, force_track_values=None):
    #     # visitor_id, upsert = super()._upsert_visitor(access_token, force_track_values=force_track_values)
    #     res = self._upsert_visitor(access_token, force_track_values)
    #     print(f"\n\n\n\t--------------> 329 res",res)
    #     print(f"\n\n\n\t--------------> 330 request.lang",request.lang)
    #     return res


    # def _get_visitor_from_request(self,force_create=False, force_track_values=None):
    #     print(f"\n\n\n\t--------------> 284 request.env.user.name",request.env.user.name)
    #     # print(f"\n\n\n\t--------------> 285 request.name",request.lang.name)

    #     res = super()._get_visitor_from_request(force_create,force_track_values)
    #     print(f"\n\n\n\t--------------> 329 res",res)
    #     return res
        