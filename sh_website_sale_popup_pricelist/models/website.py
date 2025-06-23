# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models


class ShWebsite(models.Model):
    _inherit = 'website'

    """
        INHERITED BY SOFTHEALER TECHNOLOGIES.

        field bool : is_sh_website_sale_popup_pricelist for show pricelist popup,
        field text : sh_website_sale_popup_pricelist_pages_url for set page urls in which page popup is Show.
    """

    is_sh_website_sale_popup_pricelist = fields.Boolean(
        string="Show Pricelist Popup")
    sh_website_sale_popup_pricelist_pages_url = fields.Text(string="Page Name")
