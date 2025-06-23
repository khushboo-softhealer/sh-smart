# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

import base64
import json
import requests
import werkzeug

from odoo import http,_
from odoo.http import request
from odoo.tools import html2plaintext


class HelpdeskTicketController(http.Controller):

    @http.route('/odoo-hosted-on-portal', type='json', auth='user')
    def odoo_hosted_on_portal(self, **kw):
        dic = {}
        if kw.get('edition_id') and kw.get('edition_id') != 'tick_edition':
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

    @http.route('/support_ticket', type='json', auth="user",csrf=False)
    def helpdesk_ticket(self, **post):
        dic = {}

        token = post.get('recaptcha_token_response')
        
        ip_addr = request.httprequest.remote_addr
        recaptcha_result = request.env['ir.http']._verify_recaptcha_token(ip_addr, token, 'verify_so_portal_ticket')

        is_human = False
        if recaptcha_result in ['is_human', 'no_secret']:
            is_human = True
            pass

        if not is_human:
            if recaptcha_result == 'wrong_secret':
                return json.dumps({'success' : False,
                                    'error_message': _("The reCaptcha private key is invalid."),})
            
            elif recaptcha_result == 'wrong_token':
                return json.dumps({'success' : False,
                                    'error_message': _("The reCaptcha token is invalid."),})
            
            elif recaptcha_result == 'timeout':
                    return json.dumps({'success' : False,
                                        'error_message': _("Your request has timed out, please retry."),})
            
            elif recaptcha_result == 'bad_request':
                return json.dumps({'success' : False,
                                    'error_message': _("The request is invalid or malformed."),})
            
            else:
                return json.dumps({'success' : False,
                                    'error_message': _("Suspicious activity detected by Google reCaptcha."),})

                
        if not post.get('subject'):
            dic.update({
                'success':False,
                'error_message': 'Please enter subject'
            })
            return json.dumps(dic)
        if post.get('ticket_type') and post.get('ticket_type') == 'tick_type':
            dic.update({
                'success':False,
                'error_message': 'Please select ticket type'
            })
            return json.dumps(dic)
        if post.get('edition') and post.get('edition') == 'tick_edition':
            dic.update({
                'success':False,
                'error_message': 'Please select edition'
            })
            return json.dumps(dic)
        if post.get('host') and post.get('host') == 'host_on':
            dic.update({
                'success':False,
                'error_message': 'Please select odoo hosted on'
            })
            return json.dumps(dic)
        if not post.get('description'):
            dic.update({
                'success':False,
                'error_message': 'Please enter description'
            })
            return json.dumps(dic)
        ticket_vals = {}
        if post.get('subject'):
            ticket_vals.update({
                'email_subject':post.get('subject')
            })
        if post.get('ticket_type') and post.get('ticket_type') != 'tick_type':
            ticket_vals.update({
                'ticket_type':int(post.get('ticket_type'))
            })
        if post.get('edition') and post.get('edition') != 'tick_edition':
            ticket_vals.update({
                'sh_edition_id':int(post.get('edition'))
            })
        if post.get('host') and post.get('host') != 'host_on':
            ticket_vals.update({
                'sh_odoo_hosted_id':int(post.get('host'))
            })
        if post.get('description'):
            ticket_vals.update({
                'description':post.get('description')
            })
        if post.get('custom_form_check_url'):
            ticket_vals.update({
                'custom_website_form_url': post.get('custom_form_check_url')
            })
        if post.get('product'):
            product_id = request.env['product.product'].browse(int(post.get('product')))
            if product_id:
                ticket_vals.update({
                    'product_ids':[(4,product_id.id)]
                })
                if product_id.product_template_attribute_value_ids:
                    version_attribute_id = product_id.product_template_attribute_value_ids.sudo().filtered(
                        lambda x: x.attribute_id.name == 'Version')
                    if version_attribute_id:
                        version_id = request.env['sh.version'].sudo().search(
                            [('name', '=', version_attribute_id.name)], limit=1)
                        if version_id:
                            ticket_vals.update({
                                'sh_version_id':version_id.id
                            })
        if post.get('ref'):
            ticket_vals.update({
                'store_reference':post.get('ref')
            })
        if post.get('category'):
            helpdesk_categ_id = request.env['sh.helpdesk.category'].sudo().search([('category_id','=',int(post.get('category')))],limit=1)
            if helpdesk_categ_id:
                ticket_vals.update({
                    'category_id':helpdesk_categ_id.id
                })
        if 'email_subject' in ticket_vals and 'ticket_type' in ticket_vals and 'sh_edition_id' in ticket_vals and 'sh_odoo_hosted_id' in ticket_vals and 'description' in ticket_vals:
            ticket_vals.update({
                'partner_id':request.env.user.partner_id.id,
                'email': request.env.user.partner_id.email,
                'sh_email_from':'From SO Portal'
            })
            ticket_id = request.env['sh.helpdesk.ticket'].sudo().create(ticket_vals)
            if post.get('formData'):
                for attachment in post.get('formData'):
                    attachment_id = request.env['ir.attachment'].sudo().create({
                        'name': attachment.get('filename'),
                        'res_model': 'sh.helpdesk.ticket',
                        'res_id': ticket_id.id,
                        'datas': attachment.get('data'),
                        'public': True,
                        'mimetype':attachment.get('type')
                    })
            sale_order_id = request.env['sale.order'].sudo().browse(int(post.get('order_id')))
            if sale_order_id:
                if sale_order_id.invoice_ids:
                    report = 'account.account_invoices'
                    pdf = request.env['ir.actions.report'].sudo()._render_qweb_pdf(report, [sale_order_id.invoice_ids[0].id])
                    result = base64.b64encode(pdf[0])
                    request.env['ir.attachment'].sudo().create({
                        'name': 'Invoice Copy',
                        'res_model': 'sh.helpdesk.ticket',
                        'res_id': ticket_id.id,
                        'datas': result,
                        'public': True,
                    })
            dic.update({
                'success':True,
                'success_message': 'Your '+ticket_id.name+' has been created successfully.'
            })
        return json.dumps(dic)
        