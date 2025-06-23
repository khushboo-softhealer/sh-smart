# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import http, _
from odoo.addons.website_hr_recruitment.controllers.main import WebsiteHrRecruitment
from odoo.http import request

class ShWebsiteHrRecruitmentMobiheal(WebsiteHrRecruitment):

    @http.route()
    def jobs(self, country=None, department=None, office_id=None, contract_type_id=None, **kwargs):
        response = super().jobs(country, department, office_id, contract_type_id,**kwargs)
        theme_id = request.website.sudo().theme_id
        if theme_id and theme_id.name.startswith('theme_mobiheal_website') and response.status_code == 200:
            return request.render("theme_mobiheal_website.sh_jobs_mobiheal_index", response.qcontext)
        return response
