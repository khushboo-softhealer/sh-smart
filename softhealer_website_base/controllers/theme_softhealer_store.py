# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.


from odoo import http, _ 
from odoo.http import request
from odoo.http import Response
from werkzeug.exceptions import Forbidden, NotFound
import zipfile
import logging
import io

_logger = logging.getLogger(__name__)

class mobiheal_website_controller(http.Controller):

    def create_module_download_log(self,sale_order=False,products=False,msg=False,msg_type='',current_partner_id=False):
        product_obj = request.env['product.product'].sudo() 
        download_log_obj = request.env['sh.module.download.log'].sudo() 
        if products: 
            product_int_list = [int(x) for x in products.split(',')]
            products = product_obj.browse(product_int_list)
            # domain = [
            #         ('sale_order_id','=',sale_order.id),
            #         ('partner_id','=',current_partner_id.id)
            #     ]
            for product in products:

                ## Search existing record
                # search_domain = domain + [('product_id','=',product.id)]
                
                ## if error create new one, if success update count
                # if msg_type == 'error':
                #     search_domain = search_domain + [('type','!=','error')]
                # else:
                #     search_domain = search_domain + [('type','=','info')]

                # get_search = download_log_obj.search(search_domain)
                
                ## Update existing record
                # if get_search:
                #     get_search.write({
                #         'download_count':get_search.download_count + 1,
                #     })
                # else:
                ## Create existing record
                vals = ({
                    'sale_order_id':sale_order.id if sale_order else False,
                    'product_id':product.id if product else False,
                    'type':msg_type if msg_type else False,
                    'download_count':1,
                    'download_comment':msg if msg else '',
                    'partner_id':current_partner_id.id if current_partner_id else False,
                })
                if vals:
                    download_log_obj.create(vals)
        return

    def _download_modules(self, id_list_str, sale_order=False,current_partner_id=False):
        connector_obj = request.env["sh.github.connector"].sudo().search(
            [("state", "=", "success")], limit=1)
        if not connector_obj:
            msg = _('Not Getting The Github Connector')
            self.create_module_download_log(sale_order=sale_order,msg=msg,msg_type='error',products=id_list_str,current_partner_id=current_partner_id)
            return f'<h1>Something went wrong. Kindly contact our support team by email at support@softhealer.com.</h1>'
        download_zip_name = 'sh_modules'
        new_zip_content_stream = io.BytesIO()
        notifications = [] 
        for id in id_list_str.split(","):
            module = request.env["sh.module"].sudo().search([
                ('sh_product_id', '=', int(id))
            ], limit=1)
            if not module:
                msg = _('Failed To Find The Module')
                self.create_module_download_log(sale_order=sale_order,msg=msg,msg_type='error',products=id_list_str,current_partner_id=current_partner_id)
                return f'<h1>Something went wrong. Kindly contact our support team by email at support@softhealer.com.</h1>'
            if ',' not in id_list_str:
                download_zip_name = module.name
            sha = module.sha
            if not sha:
                sha = self.get_latest_commit(connector_obj, module)
                if not sha:
                    msg = _('Failed To Get Latest Version / Commit(Sha) For The Module from Github')
                    self.create_module_download_log(sale_order=sale_order,msg=msg,msg_type='error',products=id_list_str,current_partner_id=current_partner_id)
                    return f'<h1>Something went wrong. Kindly contact our support team by email at support@softhealer.com.</h1>'
            response = connector_obj.get_req(f"{module.sh_module_url.split('contents')[0]}zipball/{sha}", '+json')
            if response.status_code != 200:
                msg = _('Failed To Get The Module from Github.')
                self.create_module_download_log(sale_order=sale_order,msg=msg,msg_type='error',products=id_list_str,current_partner_id=current_partner_id)
                return f'<h1>Something went wrong. Kindly contact our support team by email at support@softhealer.com.</h1>'
            is_error = False
            # Conver Binary Data to File
            with zipfile.ZipFile(io.BytesIO(response.content), 'r') as zip_file:
                # Extract names
                zip_entries = zip_file.namelist()
                old_folder_name = None
                # Process to set proper Module Name
                for entry in zip_entries:
                    if entry.endswith('/'):
                        old_folder_name = entry.split('/')[0]
                        break
                if old_folder_name is not None:
                    with zipfile.ZipFile(new_zip_content_stream, 'a') as new_zip_file:
                        for entry in zip_entries:
                            # Replace the old folder name with the new folder name
                            # in the entry's filename and Update new_zip_file
                            new_entry_filename = entry.replace(old_folder_name, module.name, 1)
                            entry_content = zip_file.read(entry)
                            new_zip_file.writestr(new_entry_filename, entry_content)
                else:
                    is_error = True
            if is_error:
                msg = _('Something Went Wrong! Creating Zip File!')
                self.create_module_download_log(sale_order=sale_order,msg=msg,msg_type='error',products=id_list_str,current_partner_id=current_partner_id)
                return '<h1>Something went wrong. Kindly contact our support team by email at support@softhealer.com.</h1>'
        file_content_bytes = new_zip_content_stream.getvalue()

        ### Success
        self.create_module_download_log(sale_order=sale_order,msg='',msg_type='info',products=id_list_str,current_partner_id=current_partner_id)
        
        return http.request.make_response(file_content_bytes, headers=[
            ('Content-Disposition', http.content_disposition(f'{download_zip_name}.zip')),
            ('Content-Type', 'application/zip'),
            ('Content-Length', len(file_content_bytes))
        ])

    @http.route(['/theme_softhealer_store/sh_get_app_data'], type='http',methods=['GET'], auth="user", website=True, sitemap=False)
    def sh_get_app_data(self, **post):
        """
        Get App details
        """
        common_war_msg = 'Something went wrong. Kindly contact our support team by email at support@softhealer.com.'
        sale_order_obj = request.env['sale.order'].sudo()
        product_id = post.get('product_id')
        
        sale_order_id = post.get('sale_order_id')
        current_partner_id = request.env.user.partner_id 
        access_token = post.get('access_token')
        sale_order_id = sale_order_obj.browse(int(sale_order_id))
        products = ''
        product_int_list = []
        line_product_lst = False
        
        
        if sale_order_id:
            sale_order = sale_order_obj.browse(int(sale_order_id))
            if sale_order:
                line_product_lst = sale_order.order_line.product_id.filtered(lambda pro: pro.sh_technical_name).ids
        
        if product_id: 
            if product_id.find(',') >= 0:
                products = 'multiple'
                product_int_list = [int(x) for x in product_id.split(',')]
            else:
                products = 'single'
        
        try :
            if not access_token or request.env.user._is_public() \
                or not current_partner_id or sale_order.partner_id.id != current_partner_id.id:
                msg = _("Apologies, you are not an authorized user to access this record.")
                self.create_module_download_log(sale_order,msg_type='error',msg=msg,products=product_id,current_partner_id=current_partner_id)
                raise Forbidden(_(common_war_msg))
                # raise Forbidden(_("Apologies, you are not an authorized user to access this record."))
            
            if products and products == 'multiple' and line_product_lst != product_int_list:
                msg=_("Apologies, the requested app was not found in the record.")
                self.create_module_download_log(sale_order,msg_type='error',msg=msg,products=product_id,current_partner_id=current_partner_id)
                raise NotFound(_(common_war_msg))
                # raise NotFound(_("Apologies, the requested app was not found in the record."))
                
            if products and products == 'single' and not int(product_id) in line_product_lst:
                msg = _("Apologies, you are not an authorized user to access this record.")
                self.create_module_download_log(sale_order,msg_type='error',msg=msg,products=product_id,current_partner_id=current_partner_id)
                raise NotFound(_(common_war_msg))
                # raise NotFound(_("Apologies, the requested app was not found in the record."))
            
            if sale_order and access_token == sale_order.access_token and sale_order.is_sh_confirm_sale:
                id_list_str = str(product_id)
                if id_list_str:
                    return self._download_modules(id_list_str,sale_order,current_partner_id)
                else:
                    msg = _("Apologies, the requested app was not found in the record.")
                    self.create_module_download_log(sale_order,msg_type='error',msg=msg,products=product_id,current_partner_id=current_partner_id)
                    raise NotFound(_(common_war_msg))
                    # raise NotFound(_("Apologies, the requested app was not found in the record."))
            else:
                msg = _("Apologies, you are not an authorized user to access this record.")
                self.create_module_download_log(sale_order,msg_type='error',msg=msg,products=product_id,current_partner_id=current_partner_id)
                raise Forbidden(_(common_war_msg))
                # raise Forbidden(_("Apologies, you are not an authorized user to access this record."))

        except Exception as e:
            # _logger.error('A error encountered : %s ' % e)
            pass
            return Response(str(e), status=500)