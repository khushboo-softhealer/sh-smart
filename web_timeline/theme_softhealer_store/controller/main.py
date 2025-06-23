# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import http, _ , tools
from odoo.http import request
from odoo.addons.website.controllers.main import Website
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.sale.controllers.variant import VariantController
from mimetypes import guess_extension, guess_type
import json

class CreateTicketFromPopup(http.Controller):

    @http.route('/theme_softhealer_store/get_posts', type='json', auth='public', website=True)
    def get_testimonial_posts(self, item_template=False, **kwargs):
        ShTestimonial = request.env['sh.testimonial'].sudo()
        testimonials = ShTestimonial.search([('active', '=', 'True')])
        values = {}
        testimonial_list = []
        position = 0

        for rec in testimonials:
            position = position + 1
            if rec.sh_image:
                image_base64 = rec.sh_image
                image = image_base64
                image = image.decode('utf-8')
            if rec:
                testimonial = request.env['ir.ui.view']._render_template(item_template, {
                    'partner_image': 'data:image/png;base64,' + image if rec.sh_image else '',
                    'partner_name': rec.name,
                    'priority': rec.priority,
                    'comment': rec.comment,
                    'function': rec.function,
                    'position': position,
                    'classes': 'active' if position == 1 else 'inactive',
                })
                testimonial_list.append(testimonial)
        
        if testimonial_list:
            values = {
                'data': testimonial_list
            }
        return values

    """
    For create ticket and customization related request for product detail page
    """
    @http.route(['/helpdesk/helpdesk_create_ticket'], type='json', auth="public", methods=['POST'], website=True)
    def helpdesk_create_ticket(self, **post):
        validation = False
        ip_addr = request.httprequest.remote_addr
        token = request.params.pop('recaptcha_token_response', False)
        recaptcha_result = request.env['ir.http']._verify_recaptcha_token(ip_addr, token, 'sh_recaptcha_demo_form')
        if recaptcha_result in ['is_human', 'no_secret']:
            validation = True
        
        if not validation:
            if recaptcha_result == 'wrong_secret':
                return {'recaptcha_msg':'The reCaptcha private key is invalid.'}
            elif recaptcha_result == 'wrong_token':
                return {'recaptcha_msg':'The reCaptcha token is invalid.'}
            elif recaptcha_result == 'timeout':
                return {'recaptcha_msg':'Your request has timed out, please retry.'}
            elif recaptcha_result == 'bad_request':
                return {'recaptcha_msg':'The request is invalid or malformed.'}
            else:
                return {'recaptcha_msg':'Suspicious activity detected by Google reCaptcha.'}
        
 
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
            utm_campaign = False
            utm_medium = False
            utm_source = False
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

            if post.get('sh_edition',''):
                sh_edition = post.get('sh_edition','')
                if sh_edition in ['', "", False, 0]:
                    sh_edition = False
                else:
                    sh_edition = int(sh_edition)
            # if post.get('utm_campaign'):
            utm_campaign = post.get('utm_campaign') or request.website.sudo().sh_softhealer_website_default_campaign_id.id  # noqa
            utm_medium =  post.get('utm_medium') or request.website.sudo().sh_softhealer_website_default_medium_id.id
            utm_source = post.get('utm_source') or request.website.sudo().sh_softhealer_website_default_source_id.id
            country_id = post.get('country') or False
            country = False
            contact_no = post.get('contact_no',False)
            if country_id :
                country = request.env['res.country'].sudo().search([('code','=',country_id)],limit=1)
            
            if contact_no and country:
                contact_no = f"+{country.phone_code} {contact_no}"
            else:
                contact_no = contact_no if contact_no else False

            if new_partner:
                new_helpdesk_ticket = helpdesk_ticket_obj.create({
                    'partner_id':new_partner.id,
                    'sh_version_id':version.id if version else False,
                    'description':post.get('message'),
                    'product_ids':[(6,0,[product_id])],
                    'sh_edition_id':sh_edition if sh_edition else False,
                    'custom_website_form_url' : post.get('theme_softhealer_store_website_sale_ticket_url',False),
                    'custom_website_form_campaign_id' : utm_campaign or False,
                    'custom_website_form_medium_id' : utm_medium or False,
                    'custom_website_form_source_id' : utm_source or False,
                    'custom_website_form_company' : post.get('company_name',False),
                    'custom_website_form_contact_no' : contact_no,
                    'custom_website_form_country_id' : country.id if country else False
                })
                
                if new_helpdesk_ticket:

                    # Create a rec if Notify bool is tick
                    # So, when the product will create (blog is published)
                    # Then notify that user
                    if post.get('migration_notify_me'):
                        request.env['sh.migration.notify.me'].sudo().create({
                            'partner_id':new_partner.id,
                            'product_id':product_id,
                            'product_web_url':post.get('product_url'),
                        })

                    attachments_record_list = []
                    for attachments_base64 in post.get('attachment_base64_list'):
                        extension = guess_extension(guess_type(attachments_base64)[0])
                        file_name = new_helpdesk_ticket.name + str(extension)
                        attachments_record = request.env['ir.attachment'].sudo().create({
                            'name':file_name,
                            'datas':attachments_base64.split(',')[1],
                            'res_model':'helpdesk.ticket',
                            'public':True
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
                    
                    if post.get('btn_origin','') == 'sh_contact_us':
                        get_ticket_type = request.env['sh.helpdesk.ticket.type'].sudo().search([('name','=','Migration')],limit=1)

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
            
            if get_product and get_product.sh_blog_post_id:
                res.update(
                    {'product_variant_desc': get_product.sh_blog_post_id.content})
            else:
                res.update(
                    {'product_variant_desc': None})
                
            ###### Product Blog Display

            ###### Change LOG

            if get_product.product_variant_change_log_id:
                change_log_html = request.env['ir.ui.view']._render_template("theme_softhealer_store.sh_ecommerce_change_log_common_tmpl", {
                    'change_logs': get_product.product_variant_change_log_id,
                })
                res.update({'change_log_html': change_log_html})

            ###### Change LOG

            ###### Module Information

            product_list = []
            for dependency in get_product.depends:
                product_list = get_product.get_dependent_product_in_variants(
                    dependency.technical_name, product_list, get_product)
                
            module_info_html = request.env['ir.ui.view']._render_template("theme_softhealer_store.sh_ecommerce_module_information_common_tmpl", {
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
    
class ShThemeSofthealerStoreShop(WebsiteSale):

    @http.route(['/shop/cart/update_option'], type='http', auth="public", methods=['POST'], website=True, multilang=False)
    def cart_options_update_json(self, product_and_options, goto_shop=None, lang=None, **kwargs):
        """This route is called when submitting the optional product modal.
            The product without parent is the main product, the other are options.
            Options need to be linked to their parents with a unique ID.
            The main product is the first product in the list and the options
            need to be right after their parent.
            product_and_options {
                'product_id',
                'product_template_id',
                'quantity',
                'parent_unique_id',
                'unique_id',
                'product_custom_attribute_values',
                'no_variant_attribute_values'
            }
        """
        if lang:
            request.website = request.website.with_context(lang=lang)

        order = request.website.sale_get_order(force_create=True)
        if order.state != 'draft':
            request.session['sale_order_id'] = None
            order = request.website.sale_get_order(force_create=True)

        product_and_options = json.loads(product_and_options)
        if product_and_options:
            # The main product is the first, optional products are the rest
            main_product = product_and_options[0]

            value = order._cart_update(
                product_id=main_product['product_id'],
                add_qty=main_product['quantity'],
                product_custom_attribute_values=main_product['product_custom_attribute_values'],
                no_variant_attribute_values=main_product['no_variant_attribute_values'],
                **kwargs
            )
            
            if value.get("sh_blog_post_not_exists", False) == "sh_blog_post_not_exists":
                value.update({
                    'quantity':order.cart_quantity,
                })
                return str(value)

            if value['line_id']:
                # Link option with its parent iff line has been created.
                option_parent = {main_product['unique_id']: value['line_id']}
                for option in product_and_options[1:]:
                    parent_unique_id = option['parent_unique_id']
                    option_value = order._cart_update(
                        product_id=option['product_id'],
                        set_qty=option['quantity'],
                        linked_line_id=option_parent[parent_unique_id],
                        product_custom_attribute_values=option['product_custom_attribute_values'],
                        no_variant_attribute_values=option['no_variant_attribute_values'],
                        **kwargs
                    )
                    option_parent[option['unique_id']] = option_value['line_id']

        request.session['website_sale_cart_quantity'] = order.cart_quantity
        
        return str(order.cart_quantity)

    def _get_search_options(
            self, category=None, attrib_values=None, pricelist=None, min_price=0.0, max_price=0.0, conversion_rate=1, **post):
        """
            INHERITED BY SOFTHEALER
            Get tag values from URL/POST and add it into options in order to use it in
            1) _search_get_detail in product template
        """
        result = super(ShThemeSofthealerStoreShop, self)._get_search_options(
            category=category, attrib_values=attrib_values, pricelist=pricelist, min_price=min_price, max_price=max_price, conversion_rate=conversion_rate, **post
        )

        ### Price (Free or Paid)
        if post.get('price', False):
            options_prices = {
                'price': request.httprequest.args.get('price'),
            }
            result.update(options_prices)
        
        ### Filter (Most Downloaded)
        if post.get('order', False) and post.get('order', False) == "sh_product_counter desc":
            options_most_downloaded = {
                'most_downloaded': True,
            }
            result.update(options_most_downloaded)
        
        return result

    def _shop_get_query_url_kwargs(self, category, search, min_price, max_price, attrib=None, order=None, **post):
        """
            INHERITED BY SOFTHEALER
            Get tag values from URL/POST and add it into KEEP in order to keep
            all the parameter when user click on category, attribute or price filter
        """
        result = super(ShThemeSofthealerStoreShop, self)._shop_get_query_url_kwargs(
            category, search, min_price, max_price, attrib, order, **post)
        result.update({
            'price': request.httprequest.args.get('price'),
        })
        return result
    
    @http.route()
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        """
        INHERITED BY SOFTHEALER
        """
        res = super(ShThemeSofthealerStoreShop, self).shop(
            page, category, search, min_price, max_price, ppg, **post)
        attr_value_obj = request.env["product.attribute.value"].sudo()
        attr_name = ''
        if res.qcontext.get('attrib_set'):
            attr = list(res.qcontext.get('attrib_set'))[0]
            attr_name = attr_value_obj.browse(attr)
        
        custom_filter = request.httprequest.args.get('price')


        res.qcontext.update({
            'attr_name':attr_name.name if attr_name else 'All Versions',
            'custom_filter':custom_filter,
        })
        return res
    
    @http.route("/theme_softhealer_store/check_is_depends_product_deleting",type="json",auth="public",website=True)
    def check_is_depends_product_deleting(self,line_id,product_id):
        order = request.website.sale_get_order(force_create=True)
        line = order.order_line.filtered(lambda ln: ln.id == line_id and ln.product_id.id == product_id)
        product = line and line.product_id or False
        
        if product:
            dependency_required_lines = []
            for order_line in order.order_line.filtered(lambda ol: ol.product_id and ol.product_id.depends):
                if product.sh_technical_name in order_line.product_id.depends.mapped("technical_name"):
                    dependency_required_lines.append(order_line)
            if bool(dependency_required_lines):
                return {"show_waring": bool(dependency_required_lines),
                            "line_qty":line.product_uom_qty,
                            "message": request.env["ir.ui.view"]._render_template("theme_softhealer_store.dependency_required_lines", {"order_line": dependency_required_lines,"depends_product":product})
                        }
        
        return {"line_qty":line.product_uom_qty}    

    @http.route()
    def shop_payment_get_status(self, sale_order_id, **post):
        result = super().shop_payment_get_status(sale_order_id, **post)
        if sale_order_id:
            Order_sudo = request.env['sale.order'].sudo()
            order = Order_sudo.browse(sale_order_id).exists()
            if order and not order.is_sh_lognote_posted_for_delete_depends_products:
                tx = order.get_portal_last_transaction()
                order.is_sh_lognote_posted_for_delete_depends_products = True
                
                provider = tx and tx.provider_id or False
                if not result.get("recall") or bool(provider and provider.code=="custom" and result.get("recall")):
                    product_depends_list = order.order_line.mapped(lambda line: line.product_id.sh_technical_name)
                    deleted_depends_products_vals = {}
                    for line in order.order_line.filtered(lambda line: line.product_id.depends):
                        deleted_depends = line.product_id.depends.filtered_domain([("technical_name","not in",product_depends_list)])
                        if bool(deleted_depends):
                            domain=[("sh_technical_name","in",deleted_depends.mapped("technical_name")),("product_template_attribute_value_ids.product_attribute_value_id","=", line.product_id.product_template_attribute_value_ids.product_attribute_value_id.id)]
                            query_product = request.env["product.product"]._search(domain)
                            
                            query_string, query_param = query_product.select()
                            request.env.cr.execute(query_string,query_param)
                            deleted_products =request.env["product.product"].browse([r[0] for r in request.env.cr.fetchall()])
                            for deleted_product in deleted_products:
                                if deleted_product not in deleted_depends_products_vals:
                                    deleted_depends_products_vals[deleted_product] = [line.product_id]
                                elif bool(deleted_depends_products_vals.get(deleted_product,[])):
                                    deleted_depends_products_vals[deleted_product].append(line.product_id)

                    if bool(deleted_depends_products_vals):

                        order.message_post(body=_(F"""Below depends Products are Removed.<br />{"<br />".join([dp.display_name for dp in deleted_depends_products_vals.keys()])}"""),
                                    message_type='comment',
                                    subtype_xmlid='mail.mt_note',
                                    author_id=request.env.user.partner_id.id)
        return result