# -*- encoding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class WebsiteSale(models.Model):
    _inherit = "product.public.category"

    sh_is_app = fields.Boolean(
        string='Is App ?',
    )

    sh_is_theme = fields.Boolean(
        string='Is Theme ?',
    )

    sh_svg_text = fields.Text(
        string='Svg Code',
    )
    