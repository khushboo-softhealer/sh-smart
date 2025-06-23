# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

import logging
from datetime import datetime
from odoo import models,fields

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    partner_name = fields.Char(string="Company Name", tracking=True)
    sh_country_of_operations_ids = fields.One2many('sh.country.of.operations','res_partner_id',string="Country of operations", tracking=True)
    sh_social_media_presence_ids = fields.One2many('sh.social.media.presence', 'res_partner_id', string="Social media presence", tracking=True)
    google_reviews = fields.Text(string="Google Review", tracking=True)
    google_rating = fields.Text(string="Google Rating", tracking=True)
    service_review = fields.Text(string="Product/Service Review", tracking=True)
    service_rating = fields.Text(string="Service Rating", tracking=True)
    year_of_establishment = fields.Text(string="Year of establishment", tracking=True)
    type_of_industry_id = fields.Many2one('sh.type.of.industry',string='Type of industry', tracking=True)
    career_page_analysis = fields.Text(string="Career page analysis", tracking=True)
    lead_source = fields.Selection([('referral,', 'Referral'),
            ('social_media', 'Social Media'),
            ('webinar', 'webinar/event'),
            ('cold_outreach', 'Cold outreach'),
            ('website_form', 'website form'),
        ],
        string="Lead source", tracking=True)
    customer_history = fields.Selection([('past_customer,', 'Past customer'),
            ('past_interacted', 'Past interacted'),
            ('new_customer', 'New customer')
        ],
        string="Customer history", tracking=True)
    client_type = fields.Selection([('btob,', 'B2B'),
            ('btob', 'B2C')
        ],
        string="Client type", tracking=True)
    
    updated_by = fields.Many2one('res.users', string="Updated by", readonly=True, tracking=True)
    updated_on = fields.Datetime(string="Updated on", readonly=True, tracking=True)
        
    def write(self,vals):
        """This code write for when change Lead qualification page
        Updated_by(User) and updated_on(datetime) automatic added.
        """
        res = super(ResPartner, self).write(vals)
        key_list = [
            'name', 'website', 'sh_country_of_operations_ids',
            'sh_social_media_presence_ids', 'google_reviews', 'google_rating',
            'service_review', 'service_rating', 'year_of_establishment',
            'type_of_industry_id', 'career_page_analysis', 'lead_source',
            'customer_history', 'client_type'
        ]
        keys_to_update = vals.copy()
        for key in keys_to_update.keys():
            if key in key_list:
                vals.update({
                    'updated_by':self.env.user.id,
                    'updated_on':datetime.now()  
                })   
        key_list = [
            'name', 'website', 'sh_country_of_operations_ids',
            'sh_social_media_presence_ids', 'google_reviews', 'google_rating',
            'service_review', 'service_rating', 'year_of_establishment',
            'type_of_industry_id', 'career_page_analysis', 'lead_source',
            'customer_history', 'client_type'
        ]
        keys_to_update = vals.copy()
        for key in keys_to_update.keys():
            if key in key_list:
                for rec in self:
                    ticket_ids = self.env['sh.helpdesk.ticket'].search(['|',('partner_id','=',rec.id),('partner_id','in',rec.child_ids.ids)])
                    if ticket_ids:
                        country_operations_ids = []
                        social_media_ids = []
                        for ticket in ticket_ids:
                            for res in rec.sh_country_of_operations_ids:
                                country = ticket.sh_country_of_operations_ids.with_context(create_country_by_contact=True).create({
                                    'country_id':res.country_id.id,
                                    'country_group_ids':[(6,0,res.country_group_ids.ids)],
                                    'country_type':res.country_type,
                                    'sh_helpdesk_ticket_id':ticket.id
                                })
                                country_operations_ids.append(country.id)
                            for social in rec.sh_social_media_presence_ids:
                                social_media = ticket.sh_social_media_presence_ids.with_context(create_sm_by_contact=True).create({
                                    'social_media_url':social.social_media_url,
                                    'no_of_followers':social.no_of_followers,
                                    'no_of_employees':social.no_of_employees,
                                    'sh_helpdesk_ticket_id':ticket.id
                                })
                                social_media_ids.append(social_media.id)
                            ticket.with_context(update_by_contact=True).write({
                                'partner_name':rec.name,
                                'website': rec.website,
                                'google_reviews':rec.google_reviews,
                                'google_rating':rec.google_rating,
                                'service_review':rec.service_review,
                                'service_rating':rec.service_rating,
                                'year_of_establishment':rec.year_of_establishment,
                                'type_of_industry_id':rec.type_of_industry_id.id,
                                'career_page_analysis':rec.career_page_analysis,
                                'lead_source':rec.lead_source,
                                'customer_history':rec.customer_history,
                                'client_type':rec.client_type,
                                'sh_country_of_operations_ids':[(6,0, country_operations_ids)],
                                'sh_social_media_presence_ids':[(6,0, social_media_ids)]
                            })
                            country_operations_ids = []
                            social_media_ids = []
            return res
