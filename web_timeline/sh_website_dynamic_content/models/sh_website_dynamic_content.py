# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import _, api, fields, models


class ShWebsiteDynamicContent(models.Model):
    _name = "sh.website.dynamic.content"
    _description = "Website Dynamic Content"
    _order="sequence, name, create_date DESC"

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer("Sequence")
    website_id = fields.Many2one("website","Website",ondelete="cascade")
    html_body = fields.Html(string="Content")
