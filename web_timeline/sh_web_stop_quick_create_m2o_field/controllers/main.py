# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import http
from odoo.http import request


class ShCustom(http.Controller):

    @http.route(['/sh_get_models_user_access'], type='json', auth="user", methods=['POST'])
    def sh_get_models_user_access(self, **post):
        user = request.env.user
        data = {
            'model_list':[],
        }
        if user and not user.has_group('sh_web_stop_quick_create_m2o_field.group_sh_stop_quick_create_quick_m2o_field'):
            data.update({
                'has_access':'has_access',
            })
            if request.env.company and request.env.company.sh_model_ids:
                model_list = request.env.company.sh_model_ids.mapped('model')
                if model_list:
                    data.update({
                        'model_list':model_list or [],
                    })
        return data
            