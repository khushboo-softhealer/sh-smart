# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from audioop import add
from odoo import http, _ , tools
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.sale.controllers.variant import VariantController
from odoo.addons.http_routing.models.ir_http import slug
import json
from collections import OrderedDict
from mimetypes import guess_extension, guess_type

class CreateTicketFromPopup(http.Controller):

    """
    For create ticket and customization related request for product detail page
    """
    @http.route(['/helpdesk/helpdesk_create_ticket'], type='json', auth="public", methods=['POST'], website=True)
    def helpdesk_create_ticket(self, **post):

        partner_obj = request.env['res.partner'].sudo()
        helpdesk_ticket_obj = request.env['sh.helpdesk.ticket'].sudo()
        version = request.env['sh.version'].sudo().search([('name','=',post.get('version'))],limit=1)
        partner_vals = {}
        validation_msg = {}
        success_msg = {}

        ### Validations
        if post.get('user_email','') and not tools.single_email_re.match(post.get('user_email','')):
            validation_msg.update({'email_validation':'email_not_valid'})

        if validation_msg:
            return validation_msg

        ### Success
        if post and not validation_msg:
            new_partner = False
            if post.get('name',''):
                partner_vals.update({'name':post.get('name','')})

            if post.get('user_email',''):
                partner_vals.update({'email':post.get('user_email','')})
            
            if post.get('contact_no',''):
                partner_vals.update({'phone':post.get('contact_no','')})
            
            if request.env.user._is_public():
                new_partner = partner_obj.create(partner_vals)
            else:
                partner_id = post.get('partner_id','')
                if partner_id in ['', "", False, 0]:
                    partner_id = False
                else:
                    partner_id = int(partner_id)
                new_partner = partner_obj.browse(partner_id)

            if post.get('product_id',''):
                product_id = post.get('product_id','')
                if product_id in ['', "", False, 0]:
                    product_id = False
                else:
                    product_id = int(product_id)

            if new_partner:

                new_helpdesk_ticket = helpdesk_ticket_obj.create({
                    'partner_id':new_partner.id,
                    'sh_version_id':version.id if version else False,
                    'description':post.get('message'),
                    'product_ids':[(6,0,[product_id])],
                    'custom_website_form_url' : post.get('sh_ecommerce_website_sale_ticket_url')
                })
                
                print('\n\n new_helpdesk_ticket',new_helpdesk_ticket)
                if new_helpdesk_ticket:

                    attachments_record_list = []
                    for attachments_base64 in post.get('attachment_base64_list'):
                        extension = guess_extension(guess_type(attachments_base64)[0])
                        file_name = new_helpdesk_ticket.name + str(extension)
                        attachments_record = request.env['ir.attachment'].sudo().create({
                            'name':file_name,
                            'datas':attachments_base64.split(',')[1],
                            'res_model':'helpdesk.ticket',
                            'public':True,
                            })
                        attachments_record_list.append(attachments_record.id)
                    new_helpdesk_ticket.attachment_ids = [(6, 0, attachments_record_list)]

                    get_ticket_type = False
                    if post.get('btn_origin','') == 'technical_support':
                        get_ticket_type = request.env['sh.helpdesk.ticket.type'].sudo().search([('name','=','Technical Support With Purchased App')],limit=1)
                    
                    if post.get('btn_origin','') == 'demo_support':
                        get_ticket_type = request.env['sh.helpdesk.ticket.type'].sudo().search([('name','=','Demo Request')],limit=1)
                        get_tag_ids = request.env['sh.helpdesk.tags'].sudo().search([('name','=','Demo')],limit=1)
                        new_helpdesk_ticket.tag_ids = [(6,0,get_tag_ids.ids)] if get_tag_ids else []

                    if post.get('btn_origin','') == 'new_customization':
                        get_ticket_type = request.env['sh.helpdesk.ticket.type'].sudo().search([('name','=','New Customization')],limit=1)
                    
                    if get_ticket_type:
                        new_helpdesk_ticket.ticket_type = get_ticket_type.id if get_ticket_type else False

                    get_odoo_categories = request.env['sh.helpdesk.category'].sudo().search([('name','=','Odoo')],limit=1)

                    new_helpdesk_ticket.category_id = get_odoo_categories.id if get_odoo_categories else False

                    if request.env.user.company_id.sh_default_team_id:
                        new_helpdesk_ticket.onchange_team()
                    new_helpdesk_ticket.onchange_category()
                    # new_helpdesk_ticket.onchange_partner_id()
                    success_msg.update({
                        'ticket_success':'ticket_success',
                        'ticket_name':new_helpdesk_ticket.name,
                    })
                    return success_msg

class WebsiteSaleDetailPage(VariantController):
    @http.route()
    def get_combination_info_website(self, product_template_id, product_id, combination, add_qty, **kw):
        res = super(WebsiteSaleDetailPage,self).get_combination_info_website(product_template_id,product_id,combination,add_qty,**kw) 
        if res and res.get('product_id', False):
            sh_product_id = res.get('product_id', False)
            get_product = request.env['product.product'].sudo().browse(sh_product_id)
            
            ###### Product Blog Display
            
            if get_product and get_product.sh_blog_post_ids:
                res.update(
                    {'product_variant_desc': get_product.sh_blog_post_ids[0].content})
            else:
                res.update(
                    {'product_variant_desc': None})
                
            ###### Product Blog Display

            ###### Change LOG

            if get_product.product_variant_change_log_id:
                change_log_html = request.env['ir.ui.view']._render_template("sh_ecommerce.sh_ecommerce_change_log_common_tmpl", {
                    'change_logs': get_product.product_variant_change_log_id,
                })
                res.update({'change_log_html': change_log_html})

            ###### Change LOG

            ###### Module Information

            product_list = []
            for dependency in get_product.depends:
                product_list = get_product.get_dependent_product_in_variants(
                    dependency.technical_name, product_list, get_product)
                
            module_info_html = request.env['ir.ui.view']._render_template("sh_ecommerce.sh_ecommerce_module_information_common_tmpl", {
                'sh_technical_name':get_product.sh_technical_name if get_product.sh_technical_name else None,
                'sh_versions':get_product.product_version if get_product.product_version else None,
                'last_updated_date':get_product.last_updated_date if get_product.last_updated_date else None,
                'editions':get_product.sh_edition_ids.mapped('name') if get_product.sh_edition_ids else [],
                'depends_product_list':product_list if product_list else [],
                'required_apps':get_product.required_apps.mapped('name') if get_product.required_apps else [],
                'license':get_product.license.name if get_product.license else None,
                'public_categ_ids':get_product.public_categ_ids if get_product.public_categ_ids else []
            })
            res.update({'module_info_html': module_info_html})
            
            ###### Module Information


            ##### PRICE Calculation
            total_price = 0.0
            pricelist = request.website.get_current_pricelist()

            if product_list:
                for rec in product_list: 
                    combination = rec._get_combination_info_variant(pricelist=pricelist)
                    total_price = total_price + combination['price']

                total_price = total_price + res.get('list_price')

            res.update({'price':total_price})

            
            ##### PRICE Calculation
        return res

    