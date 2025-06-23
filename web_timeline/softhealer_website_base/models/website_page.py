# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models


class ShWebsitePAge(models.Model):
    _inherit = 'website.page'

    # def sh_action_page_code_editor_view(self):
        # return False
    #     if self.view_id:
    #         return {"res_model": self.view_id._name,
    #                 "res_id": self.view_id.id,
    #                 "name": "Edit Page",
    #                 "type": "ir.actions.act_window",
    #                 "views": [(self.env.ref('softhealer_website_base.sh_website_editor_view_form').id, 'form')],
    #                 "view_mode": "form",
    #                 "target": "new", }
