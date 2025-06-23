# -*- coding: utf-8 -*-

from ast import literal_eval
from collections import OrderedDict
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, MissingError
from odoo.osv import expression
from lxml import etree, html
import logging
from random import randint

_logger = logging.getLogger(__name__)


class WebsiteSnippetFilter(models.Model):
    _inherit = 'website.snippet.filter'


    def _render(self, template_key, limit, search_domain=None, with_sample=False):
        """
            INHERIT BY SOFTHEALER
            THIS IS PATCH TO FIX DISPLAY CAREER RELATED BLOG IN CAREER PAGE

        """
        
        if template_key == 'theme_softhealer_website.dynamic_filter_template_blog_post_sh_softhealer_website_custom' or template_key == 'theme_softhealer_website.dynamic_filter_template_blog_post_sh_image_gird':
            records = self.sh_website_blog_snippet_filter_patch_prepare_values(limit, search_domain)
            is_sample = with_sample and not records
            if is_sample:
                records = self._prepare_sample(limit)
            content = self.env['ir.qweb'].with_context(inherit_branding=False)._render(template_key, dict(
                records=records,
                is_sample=is_sample,
            ))
            return [etree.tostring(el, encoding='unicode') for el in html.fromstring('<root>%s</root>' % str(content)).getchildren()]


        return super()._render(template_key,limit,search_domain,with_sample)


    def sh_website_blog_snippet_filter_patch_prepare_values(self, limit=None, search_domain=None):
        """
            MADE BY SOFTHEALER TO CALLED FROM ABVOE METHOD
            THIS IS PATCH TO FIX DISPLAY CAREER RELATED BLOG IN CAREER PAGE

        """
        self.ensure_one()

        # TODO adapt in master: the "limit" field is there to prevent loading
        # an arbitrary number of records asked by the client side. It was
        # however set to 6 for a blog post filter, probably thinking it was a
        # default limit and not a max limit. That means that configuring a
        # higher limit via the editor (which allows up to 16) was not working.
        # As a stable fix, this was made to bypass the max limit if it is under
        # 16, and only for newly configured snippets.
        max_limit = max(self.limit, 200) if self.env.context.get('_bugfix_force_minimum_max_limit_to_16') else self.limit
        limit = limit and min(limit, max_limit) or max_limit

        if self.filter_id:
            filter_sudo = self.filter_id.sudo()
            domain = filter_sudo._get_eval_domain()
            if 'website_id' in self.env[filter_sudo.model_id]:
                domain = expression.AND([domain, self.env['website'].get_current_website().website_domain()])
            if 'company_id' in self.env[filter_sudo.model_id]:
                website = self.env['website'].get_current_website()
                domain = expression.AND([domain, [('company_id', 'in', [False, website.company_id.id])]])
            if 'is_published' in self.env[filter_sudo.model_id]:
                domain = expression.AND([domain, [('is_published', '=', True)]])
            if search_domain:
                domain = expression.AND([domain, search_domain])
            
            # -------------------------------------------
            # Softhealer custom code here
            # -------------------------------------------                
            # Softhealer Patch
            domain = search_domain
            if not domain:
                domain = []
            if 'is_published' in self.env[filter_sudo.model_id]:
                domain = expression.AND([domain, [('is_published', '=', True)]])            
            # Softhealer Patch
            # -------------------------------------------
            # Softhealer custom code here
            # -------------------------------------------  
            try:
                records = self.env[filter_sudo.model_id].with_context(**literal_eval(filter_sudo.context)).search(
                    domain,
                    order=','.join(literal_eval(filter_sudo.sort)) or None,
                    limit=limit
                )
                return self._filter_records_to_values(records)
            except MissingError:
                _logger.warning("The provided domain %s in 'ir.filters' generated a MissingError in '%s'", domain, self._name)
                return []
        elif self.action_server_id:
            try:
                return self.action_server_id.with_context(
                    dynamic_filter=self,
                    limit=limit,
                    search_domain=search_domain,
                ).sudo().run() or []
            except MissingError:
                _logger.warning("The provided domain %s in 'ir.actions.server' generated a MissingError in '%s'", search_domain, self._name)
                return []
            