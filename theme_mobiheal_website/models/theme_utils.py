# -*- coding: utf-8 -*-

from odoo import api, models


class theme_utils(models.AbstractModel):
    _inherit = 'theme.utils'

    @api.model
    def _reset_default_config(self):
        self.disable_view('theme_mobiheal_website.mb_mobiheal_footer_custom')
        self.disable_view('theme_mobiheal_website.sh_template_header_magazine')

        super()._reset_default_config()
