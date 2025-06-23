# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import _, api, fields, models

class ShResConfigSettings(models.TransientModel):
    _inherit="res.config.settings"

    enable_website_popular_searches=fields.Boolean(related='website_id.enable_website_popular_searches',readonly=False)