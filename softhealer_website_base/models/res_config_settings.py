# -*- encoding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ShResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    sh_softhealer_website_expand_warranty_ticket_type_id = fields.Many2one(
        'sh.helpdesk.ticket.type', string='Expand Warranty Ticket Type', related="website_id.sh_softhealer_website_expand_warranty_ticket_type_id", readonly=False)

    sh_softhealer_website_logo_scrolled = fields.Binary(
        related='website_id.sh_softhealer_website_logo_scrolled',
        readonly=False)

    enable_website_popular_searches = fields.Boolean(
        related='website_id.enable_website_popular_searches', readonly=False)

    ## MARKETING
    sh_softhealer_website_default_campaign_id = fields.Many2one(
        'utm.campaign', string='Default Campaign', related="website_id.sh_softhealer_website_default_campaign_id", readonly=False)
    sh_softhealer_website_default_medium_id = fields.Many2one(
        'utm.medium', string='Default Medium', related="website_id.sh_softhealer_website_default_medium_id", readonly=False)
    sh_softhealer_website_default_source_id = fields.Many2one(
        'utm.source', string='Default Source', related="website_id.sh_softhealer_website_default_source_id", readonly=False)
