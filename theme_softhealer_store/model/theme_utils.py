# -*- coding: utf-8 -*-

from odoo import api, models


class theme_utils(models.AbstractModel):
    _inherit = 'theme.utils'

    @api.model
    def _reset_default_config(self):
        self.disable_view('theme_softhealer_store.theme_softhealer_header_custom_global_search')
        self.disable_view('theme_softhealer_store.theme_softhealer_store_template_softhealer_custom_footer')
        self.disable_view('theme_softhealer_store.sh_custom_footer_copyright_tmpl')

        super()._reset_default_config()
