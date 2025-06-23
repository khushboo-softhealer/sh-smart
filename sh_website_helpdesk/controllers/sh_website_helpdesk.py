# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

import base64
import json
import requests
import werkzeug

from odoo import http
from odoo.http import request
from odoo.tools import html2plaintext


import logging
import requests

from odoo import api, models, _
from odoo.http import request
from odoo.exceptions import UserError, ValidationError

logger = logging.getLogger(__name__)





class HelpdeskTicketController(http.Controller):

    @http.route('/support', type='http', auth="public",  website=True)
    def helpdesk(self, **post):
        google_recaptcha = bool(request.env['ir.config_parameter'].sudo().get_param('google_recaptcha'))
        google_captcha_site_key = request.env['ir.config_parameter'].sudo().get_param('site_key')
        ticket_attachment_size = int(request.env['ir.config_parameter'].sudo().get_param('attachment_size'))
        # google_recaptcha = request.env['ir.default'].get(
        #     'res.config.settings', 'google_recaptcha')
        # google_captcha_site_key = request.env['ir.default'].get(
        #     'res.config.settings', 'site_key')
        # ticket_attachment_size = request.env['ir.default'].get(
        #     'res.config.settings', 'attachment_size')
        if ticket_attachment_size is None:
            ticket_attachment_size = 0

        # ------------------------------------
        # Get ticket type from URL Query params
        # in order to use it in contact us page or any href link
        # ------------------------------------
        ticket_type = {}
        if post.get('ticket_type'):
            if post.get('ticket_type') == 'technical_support':
                ticket_type.update({'ticket_type': 1})
            if post.get('ticket_type') == 'new_customization':
                ticket_type.update({'ticket_type': 3})
            if post.get('ticket_type') == 'demo_request':
                ticket_type.update({'ticket_type': 4})
        # ------------------------------------
        # Get ticket type from URL Query params
        # in order to use it in contact us page or any href link
        # ------------------------------------
        if request.website.sudo().theme_id and request.website.sudo().theme_id.sudo().name == "theme_mobiheal_website":
            return request.render("sh_website_helpdesk.theme_mobiheal_website_helpdesk_form", {
                'google_recaptcha': google_recaptcha,
                'google_captcha_site_key': google_captcha_site_key,
                'file_size': ticket_attachment_size,
                'ticket_type': ticket_type})
        return request.render("sh_website_helpdesk.helpdesk_form", {
            'google_recaptcha': google_recaptcha,
            'google_captcha_site_key': google_captcha_site_key,
            'file_size': ticket_attachment_size,
            'ticket_type': ticket_type})

    @http.route('/ticket-type', type='json', auth='public')
    def ticket_type(self, **kw):
        dic = {}
        if kw.get('type_id') and kw.get('type_id') != 'type':
            type_id = request.env['sh.helpdesk.ticket.type'].sudo().search(
                [('id', '=', kw.get('type_id'))], limit=1)
            if type_id:
                if type_id.sh_invoice:
                    dic.update({
                        'invoice': True
                    })
                else:
                    dic.update({
                        'invoice': False
                    })
                if type_id.sh_product:
                    dic.update({
                        'product': True
                    })
                else:
                    dic.update({
                        'product': False
                    })
            else:
                dic.update({
                    'invoice': False,
                    'product': False
                })
        else:
            dic.update({
                'invoice': False,
                'product': False
            })
        return json.dumps(dic)

    @http.route('/product-data', type='json', auth='public')
    def product_data(self, **kw):
        dic = {}

        if kw.get('category_id') and kw.get('category_id') != 'category':
            category_id = request.env['sh.helpdesk.category'].sudo().browse(
                int(kw.get('category_id')))
            if category_id and category_id.category_id and category_id.sh_product_options:
                dic.update({
                    'products': html2plaintext(category_id.sh_product_options),
                    'status': True
                })
        elif kw.get('category_id') and kw.get('category_id') == 'category':
            dic.update({
                'status': False,
                'products': '',
            })

        return json.dumps(dic)

    @http.route('/ticket-data', type='json', auth='public')
    def ticket_data(self, **kw):
        dic = {}
        if request.env.user and request.env.user.login != 'public':
            dic.update({
                'login_user': '1'
            })
            if request.env.user.partner_id and not request.env.user.sudo()._is_public():
                if request.env.user.partner_id.name:
                    dic.update({
                        'name': request.env.user.partner_id.name,
                    })
                if request.env.user.partner_id.email:
                    dic.update({
                        'email': request.env.user.partner_id.email,
                    })
                if request.env.user.partner_id.mobile:
                    dic.update({
                        'mobile': request.env.user.partner_id.mobile,
                    })
        else:
            dic.update({
                'login_user': '0',
            })
        return json.dumps(dic)

    @http.route('/odoo-hosted-on', type='json', auth='public')
    def odoo_hosted_on(self, **kw):
        dic = {}
        if kw.get('edition_id') and kw.get('edition_id') != 'odoo_edition':
            edition_id = request.env['sh.edition'].sudo().search(
                [('id', '=', int(kw.get('edition_id')))])
            if edition_id:
                domain = [('sh_edtion_id', '=', edition_id.id)]
                hosted_dic = request.env["sh.odoo.hosted.on"].sudo().search_read(domain, [
                    'id', 'name'])
                if hosted_dic:
                    dic.update({
                        'hosted_ids': hosted_dic
                    })
                else:
                    dic.update({
                        'hosted_ids': []
                    })
        return json.dumps(dic)

    @http.route('/check-validation', type='json', auth='public',website=True)
    def check_validation(self, **kw):
        dic = {}
        if kw.get('contact_name') == '':
            dic.update({
                'name_msg': 'Name is Required.'
            })
        if kw.get('email') == '':
            dic.update({
                'email_msg': 'Email is Required.'
            })

        if kw.get('category') and kw.get('category') == 'category':
            dic.update({
                'category_msg': 'Category is Required.'
            })
        if kw.get('ticket_type'):
            if kw.get('ticket_type') == 'type':
                dic.update({
                    'type_msg': 'Ticket Type is Required.'
                })
            else:
                type_id = request.env['sh.helpdesk.ticket.type'].sudo().search(
                    [('id', '=', kw.get('ticket_type'))], limit=1)
                if type_id.sh_product and kw.get('products') == 'product':
                    dic.update({
                        'products_msg': 'Products is Required.'
                    })
                if type_id.sh_invoice and kw.get('files') == '':
                    dic.update({
                        'invoice_msg': 'Invoice proof is Required.'
                    })
        if kw.get('edition') == 'odoo_edition':
            if kw.get('ticket_type'):
                if kw.get('ticket_type') != 'type':
                    ticket_type_id = request.env['sh.helpdesk.ticket.type'].sudo().search(
                        [('id', '=', kw.get('ticket_type'))], limit=1)
                    if ticket_type_id and ticket_type_id.sh_edition_required:
                        dic.update({
                            'edition_msg': 'Edition is Required.'
                        })
        if not kw.get('odoo_hosted') or kw.get('odoo_hosted') == 'odoo_hosted_on':
            if kw.get('ticket_type'):
                if kw.get('ticket_type') != 'type':
                    ticket_type_id = request.env['sh.helpdesk.ticket.type'].sudo().search(
                        [('id', '=', kw.get('ticket_type'))], limit=1)
                    if ticket_type_id and ticket_type_id.sh_required_odoo_hosted:
                        dic.update({
                            'error_hosted_msg': 'Odoo Hosted On is Required.'
                        })
        if kw.get('version') == 'odoo_version':
            if kw.get('ticket_type'):
                if kw.get('ticket_type') != 'type':
                    ticket_type_id = request.env['sh.helpdesk.ticket.type'].sudo().search(
                        [('id', '=', kw.get('ticket_type'))], limit=1)
                    if ticket_type_id and ticket_type_id.sh_version_required:
                        dic.update({
                            'version_msg': 'Version is Required.'
                        })

        version_id = False
        if kw.get('products') and kw.get('products') != '' or kw.get('products') != 'product' and kw.get('version') and kw.get('version') != 'odoo_version':
            if kw.get('version') and kw.get('version') != 'odoo_version':
                version_id = request.env['sh.version'].sudo().browse(
                    int(kw.get('version')))
                if version_id:
                    # multi_products_value = kw.get('products')
                    if kw.get('products') and kw.get('products') != 'product':
                        multi_products = request.env['product.template'].sudo().browse(
                            int(kw.get('products')))
                        if multi_products:
                            variant_ids = []
                            exist_version = False
                            for product in multi_products:
                                version_attribute = request.env['product.attribute'].sudo().search(
                                    [('name', 'ilike', 'Version')], limit=1)
                                if version_attribute:
                                    version_values = product.attribute_line_ids.sudo().filtered(
                                        lambda x: x.attribute_id.id == version_attribute.id)
                                    if version_values:
                                        if version_id and version_values.value_ids:
                                            for value in version_values.value_ids:
                                                if value.name == version_id.name:
                                                    exist_version = True
                                if product.product_variant_ids:
                                    for variant in product.product_variant_ids:
                                        if variant.id not in variant_ids:
                                            variant_ids.append(variant.id)
                            dic.update({
                                'exist': exist_version
                            })

        # comment by code by kishan ghelani
        # google_recaptcha = request.website.google_recaptcha
        # google_recaptcha = request.env['ir.default'].get(
        #     'res.config.settings', 'google_recaptcha')
        # google_recaptcha = bool(request.env['ir.config_parameter'].sudo().get_param('google_recaptcha'))
        # if google_recaptcha:
        #     if kw.get('g-recaptcha-response') == '':
        #         dic.update({
        #             'google_captcha_msg': 'Please Validate reCaptcha.'
        #         })
        

        
        return json.dumps(dic)

    @http.route('/support/ticket/submit',methods=['POST'], type="http", auth="public", website=True, csrf=False)
    def helpdesk_process_ticket(self, **kwargs):
        if kwargs:

            # code by kishan ghelani

            ip_addr = request.httprequest.remote_addr
            
            # token = request.params.pop('recaptcha_token_response', False)
            token = kwargs.get('recaptcha_token_response',False)
            
            recaptcha_result = request.env['ir.http']._verify_recaptcha_token(ip_addr, token, 'sh_recaptcha_demo_form')
            is_human = False
            if recaptcha_result in ['is_human', 'no_secret']:
                # return True
                is_human = True
                pass

            if not is_human:
                if recaptcha_result == 'wrong_secret':
                    # raise ValidationError(_("The reCaptcha private key is invalid."))
                    return http.request.render('sh_website_helpdesk.helpdesk_thank_you', 
                                            {'error_msg': 'The reCaptcha private key is invalid', })
                
                elif recaptcha_result == 'wrong_token':
                    # raise ValidationError(_("The reCaptcha token is invalid."))
                    return http.request.render('sh_website_helpdesk.helpdesk_thank_you', 
                                            {'error_msg': 'The reCaptcha token is invalid.', })
                
                elif recaptcha_result == 'timeout':
                    # raise UserError(_("Your request has timed out, please retry."))
                    return http.request.render('sh_website_helpdesk.helpdesk_thank_you', 
                                            {'error_msg': 'Your request has timed out, please retry.', })
                
                elif recaptcha_result == 'bad_request':
                    # raise UserError(_("The request is invalid or malformed."))
                    return http.request.render('sh_website_helpdesk.helpdesk_thank_you', 
                                            {'error_msg': 'The request is invalid or malformed.', })
                
                else:
                    # return False
                    return http.request.render('sh_website_helpdesk.helpdesk_thank_you', {'error_msg': 'Suspicious activity detected by Google reCaptcha.', })


            # if not request.env['ir.http']._verify_request_recaptcha_token('sh_recaptcha_demo_form'):    

            #     return http.request.render('sh_website_helpdesk.helpdesk_thank_you', {'error_msg': 'Suspicious activity detected by Google reCaptcha.', })

            google_recaptcha = bool(request.env['ir.config_parameter'].sudo().get_param('google_recaptcha'))
            # google_recaptcha = request.env['ir.default'].get(
            #     'res.config.settings', 'google_recaptcha')
            values = {}
            for field_name, field_value in kwargs.items():
                values[field_name] = field_value
            # if google_recaptcha:
            #     google_captcha_site_key = request.env['ir.config_parameter'].sudo().get_param('site_key')

                
            #     # google_captcha_site_key = request.website.site_key
            #     # Redirect them back if they didn't answer the captcha
            #     if 'g-recaptcha-response' not in values:
            #         return werkzeug.utils.redirect("/support")

            #     payload = {'secret': google_captcha_site_key,
            #                'response': str(values['g-recaptcha-response'])}
            #     response_json = requests.post(
            #         "https://www.google.com/recaptcha/api/siteverify", data=payload).json()

            ticket_dic = {'ticket_from_website': True,
                          'company_id': request.website.sudo().company_id.id}

            login_user = request.env.user
            # if login_user and login_user.login != 'public':
            if not login_user._is_public(): #login_user and login_user.login != 'public':
                ticket_dic.update({'partner_id': login_user.partner_id.id, 'partner_ids': [
                    (6, 0, [login_user.partner_id.id])]})
            else:
                partner_id = request.env['res.partner'].sudo().search(
                    [('email', '=', kwargs.get('email'))], limit=1)
                if not partner_id:
                    partner_id = request.env['res.partner'].sudo().create({
                        'name': kwargs.get('contact_name'),
                        'company_type': 'person',
                        'email': kwargs.get('email'),
                        'mobile': kwargs.get('mobile'),
                    })
                if partner_id:
                    ticket_dic.update(
                        {'partner_id': partner_id.id, 'partner_ids': [(6, 0, [partner_id.id])]})
            version_id = False
            if kwargs.get('version') and kwargs.get('version') != 'odoo_version':
                version_id = request.env['sh.version'].sudo().browse(
                    int(kwargs.get('version')))
                if version_id:
                    ticket_dic.update({
                        'sh_version_id': version_id.id,
                    })
            if kwargs.get('sh_multiple_products') and kwargs.get('sh_multiple_products') != '' and kwargs.get('sh_multiple_products') != 'product':
                product_users = []
                multi_products = request.env['product.template'].sudo().browse(
                    int(kwargs.get('sh_multiple_products')))
                if multi_products:
                    variant_ids = []
                    for product in multi_products:
                        # if product.resposible_user_id and product.resposible_user_id.id not in product_users:
                        #     product_users.append(
                        #         product.resposible_user_id.id)
                        if product.product_variant_ids:
                            for variant in product.product_variant_ids:
                                if variant.product_template_attribute_value_ids:
                                    for attribute_value in variant.product_template_attribute_value_ids:
                                        if version_id and attribute_value.name == version_id.name and variant.id not in variant_ids:
                                            variant_ids.append(
                                                variant.id)
                    if variant_ids:
                        ticket_dic.update({
                            'product_ids': [(6, 0, variant_ids)]
                        })
                # if product_users:
                #     ticket_dic.update({
                #         'sh_user_ids': [(6, 0, product_users)]
                #     })

            if request.website.sudo().company_id.sh_default_team_id and request.website.sudo().company_id.sh_default_user_id:
                ticket_dic.update({
                    'team_id': request.website.sudo().company_id.sh_default_team_id.id,
                    'team_head': request.website.sudo().company_id.sh_default_team_id.team_head.id,
                    'user_id': request.website.sudo().company_id.sh_default_user_id.id,
                })
            if kwargs.get('edition') and kwargs.get('edition') != 'odoo_edition':
                ticket_dic.update({
                    'sh_edition_id': int(kwargs.get('edition')),
                })
            if kwargs.get('hosted') and kwargs.get('hosted') != 'odoo_hosted_on':
                ticket_dic.update({
                    'sh_odoo_hosted_id': int(kwargs.get('hosted')),
                })
            if kwargs.get('contact_name'):
                ticket_dic.update({
                    'person_name': kwargs.get('contact_name'),
                })
            if kwargs.get('email'):
                ticket_dic.update({
                    'email': kwargs.get('email'),
                })
            if kwargs.get('mobile'):
                ticket_dic.update({
                    'mobile_no': kwargs.get('mobile'),
                })
            if kwargs.get('category') and kwargs.get('category') != 'category':
                ticket_dic.update({
                    'category_id': int(kwargs.get('category')),
                })
            # if kwargs.get('subcategory') and kwargs.get('subcategory')!='subcategory':
            #     ticket_dic.update({
            #         'sub_category_id': int(kwargs.get('subcategory')),
            #     })
            if kwargs.get('ticket_type') and kwargs.get('ticket_type') != 'type':
                ticket_dic.update({
                    'ticket_type': int(kwargs.get('ticket_type')),
                })
            if kwargs.get('subject') and kwargs.get('subject') != 'ticket_subject':
                ticket_dic.update({
                    'subject_id': int(kwargs.get('subject')),
                })
            if kwargs.get('description'):
                ticket_dic.update({
                    'description': kwargs.get('description'),
                })
            if kwargs.get('priority') and kwargs.get('priority') != 'ticket_priority':
                ticket_dic.update({
                    'priority': int(kwargs.get('priority')),
                })
            ticket_dic.update({'state': 'customer_replied'})
            
            if kwargs.get('ticket_form_url'):
                ticket_dic.update({'custom_website_form_url': kwargs.get('ticket_form_url') })
            if request.website:
                ticket_dic.update({'website_id': request.website.id})
            
            ticket = request.env['sh.helpdesk.ticket'].sudo().create(
                ticket_dic)
            if ticket:
                attachment_ids = []
                if 'file' in request.params:
                    attached_files = request.httprequest.files.getlist(
                        'file')
                    for attachment in attached_files:
                        result = base64.b64encode(attachment.read())
                        if result:
                            attachment_id = request.env['ir.attachment'].sudo().create({
                                'name': ticket.name+" "+attachment.filename,
                                'res_model': 'sh.helpdesk.ticket',
                                'res_id': ticket.id,
                                'datas': result,
                                'public': True,
                            })
                            attachment_ids.append(attachment_id.id)
                if 'invoice_file' in request.params:
                    invoice_attached_files = request.httprequest.files.getlist(
                        'invoice_file')
                    for invoice_attachment in invoice_attached_files:
                        result = base64.b64encode(invoice_attachment.read())
                        if result:
                            invoice_attachment_id = request.env['ir.attachment'].sudo().create({
                                'name': ticket.name+" "+invoice_attachment.filename,
                                'res_model': 'sh.helpdesk.ticket',
                                'res_id': ticket.id,
                                'datas': result,
                                'public': True,
                            })
                            attachment_ids.append(invoice_attachment_id.id)
                if attachment_ids:
                    ticket.attachment_ids = [(6, 0, attachment_ids)]
                    kwargs = {}
                return http.request.render('sh_website_helpdesk.helpdesk_thank_you', {'success_msg': 'Your ticket '+str(ticket.name) + ' has been sent successfully.'})
        else:
            return http.request.render('sh_website_helpdesk.helpdesk_thank_you', {'error_msg': 'Please Go to out support page.', })
