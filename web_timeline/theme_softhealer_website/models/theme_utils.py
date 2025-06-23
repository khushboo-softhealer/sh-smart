# -*- coding: utf-8 -*-

from odoo import api, models


class theme_utils(models.AbstractModel):
    _inherit = 'theme.utils'

    @api.model
    def _reset_default_config(self):

        self.disable_view('theme_softhealer_website.global_search_template_header_default')
        self.disable_view('theme_softhealer_website.user_dropdown')
        self.disable_view('theme_softhealer_website.template_softhealer_custom_footer')
        self.disable_view('theme_softhealer_website.sh_custom_footer_copyright_tmpl')

        super()._reset_default_config()
