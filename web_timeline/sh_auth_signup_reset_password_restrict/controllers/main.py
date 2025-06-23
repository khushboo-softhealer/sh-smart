# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import http, _
from odoo.addons.web.controllers.home import Home
from odoo.exceptions import ValidationError
from odoo.http import request





class AuthSignupHome(Home):
    @http.route()
    def web_auth_reset_password(self, *args, **kw):
        """
        stop reset password when user is Internal user.
        """
        qcontext = self.get_auth_signup_qcontext()
        new_user = request.env['res.users'].sudo().search([('login', '=', qcontext.get('login')),('share','=',False)], limit=1)
        if new_user:
            if new_user.sudo().partner_id:
                new_user.sudo().partner_id.sudo().signup_cancel()
            raise ValidationError(_("You can't Reset Password."))
        
        return super().web_auth_reset_password(*args, **kw)
       