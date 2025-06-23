# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ShSocialMediaPresence(models.Model):
    _name = 'sh.social.media.presence'
    _description = 'social media' 
    _rec_name = "social_media_url"
    
    social_media_url = fields.Text("Social Media URL")
    no_of_followers = fields.Integer("Number of followers")
    no_of_employees = fields.Integer("Number of employees")
    sh_crm_lead_id = fields.Many2one('crm.lead')
    sh_helpdesk_ticket_id = fields.Many2one('sh.helpdesk.ticket')
    res_partner_id = fields.Many2one('res.partner')