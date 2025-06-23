# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models

class Http(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        result = super(Http, self).session_info()
        user = self.env.user
        allow_group = self.env.ref('sh_hide_follow_button.group_show_follow_button', raise_if_not_found=False)
        result['sh_show_follow_button'] = allow_group and allow_group in user.groups_id
        return result
