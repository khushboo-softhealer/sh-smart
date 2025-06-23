# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies

from werkzeug import urls
from werkzeug.exceptions import NotFound

from odoo import models, http,_
from odoo.addons.http_routing.models.ir_http import RequestUID
from odoo.exceptions import AccessError, MissingError
from odoo.http import request


class Website(models.Model):
    _inherit = 'website'

    @staticmethod
    def _get_product_sort_mapping():
        return [
            ('website_sequence asc', _('Featured')),
            ('create_date desc', _('Newest Arrivals')),
            ('name asc', _('Name (A-Z)')),
            ('sh_sales_price_with_depends asc', _('Price - Low to High')),
            ('sh_sales_price_with_depends desc', _('Price - High to Low')),
            ('sh_product_counter desc', _('Most Downloaded')),
        ]

    def _get_canonical_url_localized(self, lang, canonical_params):
        """
            Overrides By SOfthealer Technologies

            set up product website URL in blog post canonical url
        """
        self.ensure_one()
        try:
            # Re-match the controller where the request path routes.
            rule, args = self.env['ir.http']._match(request.httprequest.path)
            
            if "blog_post" not in args:
                return super()._get_canonical_url_localized(lang, canonical_params)

            # Softhealer Custom code for set product website URL in blog post canonical url.
            product_url = False
            for key, val in list(args.items()):
                if isinstance(val, models.BaseModel):
                    if isinstance(val._uid, RequestUID):
                        args[key] = val = val.with_user(request.uid)
                    if val.env.context.get('lang') != lang.code:
                        args[key] = val = val.with_context(lang=lang.code)
                    if val._name == "blog.post" and val.sh_product_id.website_url:
                        product_url = val.sh_product_id.product_tmpl_id.website_url
                        
            router = http.root.get_db_router(request.db).bind('')

            path = router.build(rule.endpoint, args)
            if product_url:
                path = product_url

        except (NotFound, AccessError, MissingError):
            # The build method returns a quoted URL so convert in this case for consistency.
            path = urls.url_quote_plus(request.httprequest.path, safe='/')
            
        if lang != self.default_lang_id:
            path = f'/{lang.url_code}{path if path != "/" else ""}'
        canonical_query_string = f'?{urls.url_encode(canonical_params)}' if canonical_params else ''
        return self.get_base_url() + path + canonical_query_string
