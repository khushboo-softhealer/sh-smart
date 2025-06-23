# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
from odoo.tools.translate import html_translate


class Website(models.Model):
    _inherit = "website"

    sh_website_show_terms_conditions_website = fields.Boolean(
        "Show Terms & Conditions in Website?")
    sh_website_tnc_type = fields.Selection([
        ('single', 'Single'),
        ('multiple', 'Multiple')
    ], string='Type', default='single')
    sh_website_tnc_default_check = fields.Boolean("Default Check ?")
    sh_website_tnc_terms_title = fields.Char("Title ", translate=True)
    sh_website_tnc_terms_label = fields.Char("Label", translate=True)
    sh_website_tnc_terms_text = fields.Html(
        "Terms & Conditions", translate=html_translate)
    sh_website_tnc_alert_msg = fields.Html(
        "Alert Message", translate=html_translate)


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    sh_website_show_terms_conditions_website = fields.Boolean(
        related="website_id.sh_website_show_terms_conditions_website",
        string="Show Terms & Conditions in Website?",
        readonly=False)
    sh_website_tnc_type = fields.Selection(
        related="website_id.sh_website_tnc_type",
        string='Type',
        readonly=False)
    sh_website_tnc_default_check = fields.Boolean(
        related="website_id.sh_website_tnc_default_check",
        string="Default Check ?",
        readonly=False)
    sh_website_tnc_terms_title = fields.Char(
        related="website_id.sh_website_tnc_terms_title",
        string="Title ", readonly=False)
    sh_website_tnc_terms_label = fields.Char(
        related="website_id.sh_website_tnc_terms_label",
        string="Label", readonly=False)
    sh_website_tnc_terms_text = fields.Html(
        related="website_id.sh_website_tnc_terms_text",
        string="Terms and Conditions",
        readonly=False)
    sh_website_tnc_alert_msg = fields.Html(
        related="website_id.sh_website_tnc_alert_msg",
        string="Alert Message", readonly=False)
