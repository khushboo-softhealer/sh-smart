# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
import re
import base64
import json
import requests
import werkzeug
import phonenumbers
import logging

from odoo import _, http
from odoo.http import request
from odoo.tools import html2plaintext
from odoo.exceptions import ValidationError, UserError
from odoo.addons.phone_validation.tools import phone_validation

_logger = logging.getLogger(__name__)

class HelpdeskTicketController(http.Controller):

    @http.route('/softhealer_website_base/website_create_ticket_page', type='json', auth="public", methods=['POST'], website=True, sitemap=False)
    def website_create_ticket_page(self, **kwargs):
        dic = {}

        try:
            # Google reCaptcha verification
            if not request.env['ir.http']._verify_request_recaptcha_token('sh_recaptcha_demo_form'):
                return json.dumps({'error_msg': _("Suspicious activity detected by Google reCaptcha."),
                                    'recaptch_msg': _("Suspicious activity detected by Google reCaptcha.")})

            # Validate email format
            email = kwargs.get('solution_page_custom_website_form_email', '').strip()
            if email:
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_pattern, email):
                    dic.update({
                        'error_msg': 'Invalid email format.',
                        'email_msg': 'Please enter a valid email address.'
                    })
                    return json.dumps(dic)

            # FIELD VALIDATION
            if not kwargs.get('solution_page_custom_website_form_partner_name', ''):
                dic.update({
                    'name_msg': 'Please enter your name.',
                    'error_msg': 'Please enter your name.'
                })
                return json.dumps(dic)

            if not kwargs.get('solution_page_custom_website_form_company', ''):
                dic.update({
                    'error_msg': 'Please enter your company name.',
                    'company_msg': 'Please enter your company name.'
                })
                return json.dumps(dic)

            if not email:
                dic.update({
                    'error_msg': 'Please enter your email address.',
                    'email_msg': 'Please enter your email address.'
                })
                return json.dumps(dic)

            country_id = kwargs.get('solution_page_custom_website_form_country', '').strip()
            if not country_id:
                dic.update({
                    'error_msg': 'Please select your country.',
                    'country_msg': 'Please select your country.'
                })
                return json.dumps(dic)

            # Fetch the country record
            country = request.env['res.country'].sudo().search([('code','=',country_id)],limit=1)
            if not country.exists():
                dic.update({
                    'error_msg': 'Invalid country selected.',
                    'country_msg': 'Invalid country selected.'
                })
                return json.dumps(dic)
            
            contact = kwargs.get('solution_page_custom_website_form_contact_no', '').strip()
            if not contact:
                return json.dumps({
                    'error_msg': 'Please enter contact no.',
                    'contact_no_msg': 'Please enter contact no.'})

            try:
                pn = phonenumbers.parse(contact, region=country.code or None, keep_raw_input=True)
                if not phonenumbers.is_valid_number(pn):
                    return json.dumps({'error_msg': 'Please enter valid contact no', 'contact_no_msg': 'Please enter valid contact no'})
            except phonenumbers.NumberParseException as e:
                return json.dumps({'error_msg': 'Please enter valid contact no', 'contact_no_msg': 'Please enter valid contact no'})

            if not kwargs.get('solution_page_custom_website_form_description', '').strip():
                dic.update({
                    'error_msg': 'Please enter your requirements.',
                    'description_msg': 'Please enter your requirements.'
                })
                return json.dumps(dic)


            # Create or update partner
            partner_id = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)
            _logger.info('\n\n\n CUSTOM partner_id ==== %s' % (partner_id))
            if not partner_id:
                partner_id = request.env['res.partner'].sudo().create({
                    'name': kwargs.get('solution_page_custom_website_form_partner_name'),
                    'company_type': 'person',
                    'email': email,
                    'country_id': country.id,
                    'mobile': kwargs.get('solution_page_custom_website_form_contact_no')
                })
            _logger.info('\n\n\n CUSTOM partner_id 22 ==== %s' % (partner_id))
            # Create the ticket
            ticket_dict = {
                'partner_id': partner_id.id,
                'custom_website_form_company': kwargs.get('solution_page_custom_website_form_company'),
                'email': partner_id.email,
                'custom_website_form_country_id': country.id,  # Set the country for the ticket
                'custom_website_form_contact_no' :f"+{country.phone_code} {kwargs.get('solution_page_custom_website_form_contact_no')}",
                'custom_website_form_url': kwargs.get('custom_form_check_url'),
                'description': kwargs.get('solution_page_custom_website_form_description')
            }
            _logger.info('\n\n\n CUSTOM ticket_dict ==== %s' % (ticket_dict))
            
            campaign_name = kwargs.get('custom_form_utm_campaign')
            medium_name = kwargs.get('custom_form_utm_medium')
            source_name = kwargs.get('custom_form_utm_source')
            # First Priority
            if campaign_name:
                # campaign = request.env['utm.mixin'].sudo()._find_or_create_record('utm.campaign',campaign_name)
                campaign = request.env['utm.campaign'].sudo().search([('name','=',campaign_name)],limit=1)
                print(f"\n\n\n\t--------------> 132 campaign",campaign)
                if campaign : 
                    ticket_dict.update({'custom_website_form_campaign_id':campaign.id})
                    print(f"\n\n\n\t--------------> 134 campaign.name",campaign.name)
            if medium_name:
                # medium = request.env['utm.mixin'].sudo()._find_or_create_record('utm.medium',medium_name)
                medium = request.env['utm.medium'].sudo().search([('name','=',medium_name)],limit=1)
                print(f"\n\n\n\t--------------> 138 medium",medium)
                if medium : 
                    ticket_dict.update({'custom_website_form_medium_id':medium.id})
                    print(f"\n\n\n\t--------------> 140 medium.name",medium.name)
            if source_name:
                # source = request.env['utm.mixin'].sudo()._find_or_create_record('utm.source',source_name)
                source = request.env['utm.source'].sudo().search([('name','=',source_name)],limit=1)

                print(f"\n\n\n\t--------------> 146 source",source)
                if source : 
                    ticket_dict.update({'custom_website_form_source_id':source.id})
                    print(f"\n\n\n\t--------------> 147 source.name",source.name)
            # Second Priority
            for field in ['campaign', 'medium', 'source']:
                if not ticket_dict.get(f'custom_website_form_{field}_id'):
                    default_id = getattr(request.website, f"sh_softhealer_website_default_{field}_id", False)
                    if default_id:
                        ticket_dict[f'custom_website_form_{field}_id'] = default_id.id
            _logger.info('\n\n\n CUSTOM ticket_dict 2 ==== %s' % (ticket_dict))


            ticket = request.env['sh.helpdesk.ticket'].sudo().create(ticket_dict)
            _logger.info('\n\n\n CUSTOM ticket ==== %s' % (ticket))

            return json.dumps({'ticket': ticket.name})

        except (ValidationError, UserError) as e:
            return json.dumps({'error': str(e)})
        except Exception as e:
            # Catch any unexpected errors
            return json.dumps({'error': f"Unexpected error occurred: {str(e)}"})

    @http.route('/softhealer_website_base/get_countries', type='json', auth="public", methods=['POST'], website=True, sitemap=False)
    def get_countries(self, **kwargs):
        countries = request.env['res.country'].search_read([], ['id', 'name','image_url','phone_code','code'])
        # _logger.info('\n\n\n CUSTOM LOGGER ==== %s' % (countries))
        return countries

