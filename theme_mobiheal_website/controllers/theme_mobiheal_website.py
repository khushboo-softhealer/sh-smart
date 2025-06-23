# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.


from odoo import http
from odoo.http import request

class mobiheal_website_controller(http.Controller):


    @http.route(['/terms-and-condition'], type='http', auth="public", website=True, sitemap=True)
    def theme_mobiheal_website_terms_condition(self, **post):

        return request.render("theme_mobiheal_website.theme_mobiheal_website_terms_condition_tmpl", {})


    @http.route(['/privacy-policy'], type='http', auth="public", website=True, sitemap=True)
    def theme_mobiheal_website_privacy_policy(self, **post):

        return request.render("theme_mobiheal_website.theme_mobiheal_website_privacy_policy_tmpl", {})