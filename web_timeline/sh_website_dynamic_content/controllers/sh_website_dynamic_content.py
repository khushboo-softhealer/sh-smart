# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website

class ShWebsiteDynamicContent(Website):

    @http.route('/sh_website_dynamic_content/get_content/<model("sh.website.dynamic.content"):content>', type="json", auth="public", website=True)
    def _get_content(self, content):
        html_body=""
        if content and content.exists():
            html_body = content.html_body
        return html_body
