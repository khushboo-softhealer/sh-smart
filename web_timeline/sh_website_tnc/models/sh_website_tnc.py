# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ShWebsiteTncMulti(models.Model):
    _name = 'sh.website.tnc.multi'
    _description = 'Website TnC Multi'
    _order = 'id desc'

    name = fields.Char(string='Title', required=True)
    sh_website_multi_tnc_label = fields.Char(string='Label')
    sh_website_multi_default_check = fields.Boolean(string='Default Check ?')
    sh_website_multi_tnc_terms_text = fields.Html(
        string='Terms and Conditions')
