# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import _, api, fields, models


class ShWebsite(models.Model):
    _inherit = 'website'

    enable_website_popular_searches=fields.Boolean("Enable Website Popular Searches")
