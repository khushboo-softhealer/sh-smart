# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

import logging
from datetime import datetime
from odoo import models,fields,api
_logger = logging.getLogger(__name__)

class HelpdeskTicketcrmleadextra(models.Model):
    _inherit = 'sh.helpdesk.ticket'
    
    partner_name = fields.Char(string="Company Name")
    website = fields.Char('Website')
    sh_country_of_operations_ids = fields.One2many('sh.country.of.operations','sh_helpdesk_ticket_id',string="Country of operations")
    sh_social_media_presence_ids = fields.One2many('sh.social.media.presence', 'sh_helpdesk_ticket_id', string="Social media presence")
    google_reviews = fields.Text(string="Google Review")
    google_rating = fields.Text(string="Google Rating")
    service_review = fields.Text(string="Product/Service Review")
    service_rating = fields.Text(string="Service Rating")
    year_of_establishment = fields.Text(string="Year of establishment")
    type_of_industry_id = fields.Many2one('sh.type.of.industry',string='Type of industry')
    career_page_analysis = fields.Text(string="Career page analysis")
    lead_source = fields.Selection([('referral,', 'Referral'),
            ('social_media', 'Social Media'),
            ('webinar', 'webinar/event'),
            ('cold_outreach', 'Cold outreach'),
            ('website_form', 'website form'),
        ],
        string="Lead source")
    customer_history = fields.Selection([('past_customer,', 'Past customer'),
            ('past_interacted', 'Past interacted'),
            ('new_customer', 'New customer')
        ],
        string="Customer history")
    client_type = fields.Selection([('btob,', 'B2B'),
            ('btob', 'B2C')
        ],
        string="Client type")
    
    updated_by = fields.Many2one('res.users', string="Updated by", readonly=True)
    updated_on = fields.Datetime(string="Updated on", readonly=True)
    
    # @api.model_create_multi
    # def create(self, values):
    #     res = super(HelpdeskTicketcrmleadextra, self).create(values)
    #     try:
    #         for rec in res:
    #             if rec.partner_id and rec.partner_id.parent_id:
    #                 rec.partner_id.parent_id.write({
    #                 'name':rec.partner_name or rec.partner_id.parent_id.name,
    #                 'website': rec.website,
    #                 'google_reviews':rec.google_reviews,
    #                 'google_rating':rec.google_rating,
    #                 'service_review':rec.service_review,
    #                 'service_rating':rec.service_rating,
    #                 'year_of_establishment':rec.year_of_establishment,
    #                 'type_of_industry_id':rec.type_of_industry_id.id,
    #                 'career_page_analysis':rec.career_page_analysis,
    #                 'lead_source':rec.lead_source,
    #                 'customer_history':rec.customer_history,
    #                 'client_type':rec.client_type,
    #                 'sh_country_of_operations_ids':[(6,0, rec.sh_country_of_operations_ids.ids)],
    #                 'sh_social_media_presence_ids':[(6,0, rec.sh_social_media_presence_ids.ids)]
    #                 })
    #             elif rec.partner_id and rec.partner_id.is_company:
    #                 rec.partner_id.write({
    #                 'name':rec.partner_name or rec.partner_id.name,
    #                 'website': rec.website,
    #                 'google_reviews':rec.google_reviews,
    #                 'google_rating':rec.google_rating,
    #                 'service_review':rec.service_review,
    #                 'service_rating':rec.service_rating,
    #                 'year_of_establishment':rec.year_of_establishment,
    #                 'type_of_industry_id':rec.type_of_industry_id.id,
    #                 'career_page_analysis':rec.career_page_analysis,
    #                 'lead_source':rec.lead_source,
    #                 'customer_history':rec.customer_history,
    #                 'client_type':rec.client_type,
    #                 'sh_country_of_operations_ids':[(6,0, rec.sh_country_of_operations_ids.ids)],
    #                 'sh_social_media_presence_ids':[(6,0, rec.sh_social_media_presence_ids.ids)]
    #                 })
    #     except Exception as e:
    #          _logger.exception("partner company not created on ticket create: %s" % e)
    #     return res

    @api.model_create_multi  
    def create(self, values):  
        res = super(HelpdeskTicketcrmleadextra, self).create(values)  
        try:  
            for rec in res:  
                update_values = {}   

                # Add only non-falsy values  
                for field in ['website', 'google_reviews', 'google_rating', 'service_review',  
                                'service_rating', 'year_of_establishment', 'lead_source',  
                                'career_page_analysis', 'customer_history', 'client_type']:  
                    if getattr(rec, field):  
                        update_values[field] = getattr(rec, field)  

                if rec.type_of_industry_id:  
                    update_values['type_of_industry_id'] = rec.type_of_industry_id.id  

                if rec.sh_country_of_operations_ids:  
                    update_values['sh_country_of_operations_ids'] = [(6, 0, rec.sh_country_of_operations_ids.ids)]  

                if rec.sh_social_media_presence_ids:  
                    update_values['sh_social_media_presence_ids'] = [(6, 0, rec.sh_social_media_presence_ids.ids)]  
                

                if rec.partner_id.parent_id:  
                        rec.partner_id.parent_id.write(update_values)  
                elif rec.partner_id.is_company:  
                        rec.partner_id.write(update_values)
        except Exception as e:  
            _logger.exception("Partner company not updated on ticket creation: %s", e)  

        return res  
    
    # def write(self,vals):
    #     key_list = [
    #         'partner_name', 'website', 'sh_country_of_operations_ids',
    #         'sh_social_media_presence_ids', 'google_reviews', 'google_rating',
    #         'service_review', 'service_rating', 'year_of_establishment',
    #         'type_of_industry_id', 'career_page_analysis', 'lead_source',
    #         'customer_history', 'client_type'
    #     ]
    #     keys_to_update = vals.copy()
    #     for key in keys_to_update.keys():
    #         if key in key_list:
    #             vals.update({
    #                 'updated_by':self.env.user.id,
    #                 'updated_on':datetime.now()  
    #             })  
    #     res = super(HelpdeskTicketcrmleadextra, self).write(vals)
    #     if not self.env.context.get('update_by_contact'):
    #         key_list = [
    #             'partner_name', 'website', 'sh_country_of_operations_ids',
    #             'sh_social_media_presence_ids', 'google_reviews', 'google_rating',
    #             'service_review', 'service_rating', 'year_of_establishment',
    #             'type_of_industry_id', 'career_page_analysis', 'lead_source',
    #             'customer_history', 'client_type'
    #         ]
    #         keys_to_update = vals.copy()
    #         for key in keys_to_update.keys():
    #             if key in key_list:
    #                 for rec in self:
    #                     partner = self.env['res.partner'].search(['|',('id','=',rec.partner_id.id),('id','in',rec.partner_id.child_ids.ids)])
    #                     if partner and partner.parent_id:
    #                         partner.parent_id.write({
    #                         'name':rec.partner_name or partner.parent_id.name,
    #                         'website': rec.website,
    #                         'google_reviews':rec.google_reviews,
    #                         'google_rating':rec.google_rating,
    #                         'service_review':rec.service_review,
    #                         'service_rating':rec.service_rating,
    #                         'year_of_establishment':rec.year_of_establishment,
    #                         'type_of_industry_id':rec.type_of_industry_id.id,
    #                         'career_page_analysis':rec.career_page_analysis,
    #                         'lead_source':rec.lead_source,
    #                         'customer_history':rec.customer_history,
    #                         'client_type':rec.client_type,
    #                         'sh_country_of_operations_ids':[(6,0, rec.sh_country_of_operations_ids.ids)],
    #                         'sh_social_media_presence_ids':[(6,0, rec.sh_social_media_presence_ids.ids)]
    #                         })
    #                     elif partner and partner.is_company:
    #                         partner.write({
    #                         'name':rec.partner_name or partner.name,
    #                         'website': rec.website,
    #                         'google_reviews':rec.google_reviews,
    #                         'google_rating':rec.google_rating,
    #                         'service_review':rec.service_review,
    #                         'service_rating':rec.service_rating,
    #                         'year_of_establishment':rec.year_of_establishment,
    #                         'type_of_industry_id':rec.type_of_industry_id.id,
    #                         'career_page_analysis':rec.career_page_analysis,
    #                         'lead_source':rec.lead_source,
    #                         'customer_history':rec.customer_history,
    #                         'client_type':rec.client_type,
    #                         'sh_country_of_operations_ids':[(6,0, rec.sh_country_of_operations_ids.ids)],
    #                         'sh_social_media_presence_ids':[(6,0, rec.sh_social_media_presence_ids.ids)]
    #                         })
    #     return res

    def write(self, vals):
        key_list = [
            'partner_name', 'website', 'sh_country_of_operations_ids',
            'sh_social_media_presence_ids', 'google_reviews', 'google_rating',
            'service_review', 'service_rating', 'year_of_establishment',
            'type_of_industry_id', 'career_page_analysis', 'lead_source',
            'customer_history', 'client_type'
        ]

        # Update timestamp only if relevant fields are changing
        if any(key in vals for key in key_list):
            vals.update({
                'updated_by': self.env.user.id,
                'updated_on': datetime.now()
            })

        res = super().write(vals)

        if not self.env.context.get('update_by_contact'):
            for rec in self:
                partner = rec.partner_id.parent_id if rec.partner_id.parent_id else rec.partner_id if rec.partner_id.is_company else None

                if partner:
                    update_vals = {
                        field: getattr(rec, field)
                        for field in key_list if field in vals and getattr(rec, field)
                    }

                    if 'type_of_industry_id' in vals and rec.type_of_industry_id:
                        update_vals['type_of_industry_id'] = rec.type_of_industry_id.id

                    if 'sh_country_of_operations_ids' in vals and rec.sh_country_of_operations_ids:
                        update_vals['sh_country_of_operations_ids'] = [(6, 0, rec.sh_country_of_operations_ids.ids)]

                    if 'sh_social_media_presence_ids' in vals and rec.sh_social_media_presence_ids:
                        update_vals['sh_social_media_presence_ids'] = [(6, 0, rec.sh_social_media_presence_ids.ids)]

                    if update_vals:
                        partner.write(update_vals)

        return res
    
    # @api.onchange('partner_id')
    # def onchange_partner_id(self):
    #     res = super().onchange_partner_id()
    #     for rec in self:
    #         if rec.partner_id.parent_id:
    #             rec.update({
    #             'partner_name':rec.partner_id.parent_id.name,
    #             'website': rec.partner_id.parent_id.website,
    #             'google_reviews':rec.partner_id.parent_id.google_reviews,
    #             'google_rating':rec.partner_id.parent_id.google_rating,
    #             'service_review':rec.partner_id.parent_id.service_review,
    #             'service_rating':rec.partner_id.parent_id.service_rating,
    #             'year_of_establishment':rec.partner_id.parent_id.year_of_establishment,
    #             'type_of_industry_id':rec.partner_id.parent_id.type_of_industry_id.id,
    #             'career_page_analysis':rec.partner_id.parent_id.career_page_analysis,
    #             'lead_source':rec.partner_id.parent_id.lead_source,
    #             'customer_history':rec.partner_id.parent_id.customer_history,
    #             'client_type':rec.partner_id.parent_id.client_type,
    #             'sh_country_of_operations_ids':[(6,0, rec.partner_id.parent_id.sh_country_of_operations_ids.ids)],
    #             'sh_social_media_presence_ids':[(6,0, rec.partner_id.parent_id.sh_social_media_presence_ids.ids)]
    #             })
    #         elif rec.partner_id.is_company:
    #             rec.update({
    #             'partner_name':rec.partner_id.name,
    #             'website': rec.partner_id.website,
    #             'google_reviews':rec.partner_id.google_reviews,
    #             'google_rating':rec.partner_id.google_rating,
    #             'service_review':rec.partner_id.service_review,
    #             'service_rating':rec.partner_id.service_rating,
    #             'year_of_establishment':rec.partner_id.year_of_establishment,
    #             'type_of_industry_id':rec.partner_id.type_of_industry_id.id,
    #             'career_page_analysis':rec.partner_id.career_page_analysis,
    #             'lead_source':rec.partner_id.lead_source,
    #             'customer_history':rec.partner_id.customer_history,
    #             'client_type':rec.partner_id.client_type,
    #             'sh_country_of_operations_ids':[(6,0, rec.partner_id.sh_country_of_operations_ids.ids)],
    #             'sh_social_media_presence_ids':[(6,0, rec.partner_id.sh_social_media_presence_ids.ids)]
    #             })
    #     return res

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        super().onchange_partner_id()
        for rec in self:
            partner = rec.partner_id.parent_id if rec.partner_id.parent_id else rec.partner_id if rec.partner_id.is_company else None
            
            if partner:
                update_vals = {
                    field: getattr(partner, field)
                    for field in [
                        'partner_name', 'website', 'google_reviews', 'google_rating',
                        'service_review', 'service_rating', 'year_of_establishment',
                        'career_page_analysis', 'lead_source', 'customer_history', 'client_type'
                    ]
                    if getattr(partner, field)
                }

                if partner.type_of_industry_id:
                    update_vals['type_of_industry_id'] = partner.type_of_industry_id.id

                if partner.sh_country_of_operations_ids:
                    update_vals['sh_country_of_operations_ids'] = [(6, 0, partner.sh_country_of_operations_ids.ids)]

                if partner.sh_social_media_presence_ids:
                    update_vals['sh_social_media_presence_ids'] = [(6, 0, partner.sh_social_media_presence_ids.ids)]

                if update_vals:
                    rec.update(update_vals)
