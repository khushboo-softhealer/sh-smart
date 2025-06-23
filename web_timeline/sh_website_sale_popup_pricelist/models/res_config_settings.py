# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models


class ShResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    """
        INHERITED BY SOFTHEALER TECHNOLOGIES.

        field bool : is_sh_website_sale_popup_pricelist for show pricelist popup,
        field text : sh_website_sale_popup_pricelist_pages_url for set page urls in which page popup is Show.
    """

    is_sh_website_sale_popup_pricelist = fields.Boolean(
        string="Show Pricelist Popup", related='website_id.is_sh_website_sale_popup_pricelist', readonly=False)
    sh_website_sale_popup_pricelist_pages_url=fields.Text(string="Pages URL",related='website_id.sh_website_sale_popup_pricelist_pages_url',readonly=False)
