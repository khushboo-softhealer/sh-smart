# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models


class ShProductPriceList(models.Model):
    _inherit = 'product.pricelist'

    """
        INHERITED BY SOFTHEALER TECHNOLOGIES.
        
        To set image in Pricelist.
    """

    sh_website_sale_popup_pricelist_image = fields.Binary(string="Popup Image")
