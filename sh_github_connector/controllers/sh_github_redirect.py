# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import http, _
from odoo.http import request
import werkzeug
import werkzeug.utils
from odoo.exceptions import UserError


class Redirects(http.Controller):

    @http.route("/sh_github_connector/auth", auth="public",website=True, methods=['get','post'])
    def sh_github_connector_auth(self, **kwargs):
        '''Controller to get the Access token from Gihub'''
        if 'code' in kwargs:
            connector_obj = request.env['sh.github.connector'].sudo().search([('id', '=', int(kwargs.get('state')))], limit=1)
            if connector_obj:
                connector_obj.generate_access_token(kwargs.get('code'))
            return werkzeug.utils.redirect("/")
        raise UserError(_("Could not receive code, check credentials"))
