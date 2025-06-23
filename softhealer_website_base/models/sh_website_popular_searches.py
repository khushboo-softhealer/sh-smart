# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models


class ShWebsitePopularSearches(models.Model):
    _name = "sh.website.popular.searches"
    _inherit = "website.published.multi.mixin"
    _description = "Website Popular Searches"

    name = fields.Char(string="Name", required=True)
    search_type = fields.Char(string="Search Type")
    searches_count = fields.Integer(string="Search Count")
