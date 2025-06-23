# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import _, api, fields, models

class ShHelpDeskTicket(models.Model):
    
    _inherit = 'sh.helpdesk.ticket'

    custom_website_form_company = fields.Char(string="Company Name")
    custom_website_form_url = fields.Char(string="Website Form URL")
    custom_website_form_ref_by = fields.Char(string="Reference By")
    custom_website_form_country_id = fields.Many2one('res.country',string="Country Id")
    custom_website_form_contact_no = fields.Char(string="Contact No.")

    custom_website_form_campaign_id = fields.Many2one("utm.campaign",string='Campaign')
    custom_website_form_medium_id = fields.Many2one("utm.medium",string='Medium')
    custom_website_form_source_id = fields.Many2one("utm.source",string='Source')