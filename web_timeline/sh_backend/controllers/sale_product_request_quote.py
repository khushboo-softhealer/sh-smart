# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import http
from odoo.http import request
from datetime import datetime

class SaleProductRequestQuote(http.Controller):

    @http.route(['/sale/product_request_quote'], type='json', auth="public",methods=['POST'], website=True)
    def product_request_quote(self, **post ):
        
        if post.get('product_id',False):            
            product_search = request.env['product.product'].sudo().search([('id','=',post.get('product_id') )],limit=1)
            
            if product_search:                
                vals={'date_order':datetime.now()}
                    
                if request.uid :
                    user_search = request.env['res.users'].sudo().search([('id','=', request.uid )],limit=1)
                    
                    if user_search:
                        vals.update({'partner_id': user_search.partner_id.id})

                        if post.get('message',False):           
                            vals.update({'request_quote_message' : post.get('message') })
                                        
                        so_obj = request.env['sale.order'].sudo().create(vals)
                
                        if so_obj:                                                        
                            vals_line = {'order_id':so_obj.id ,'product_id':product_search.id,'price_unit':0.0}                                     
                            
                            if post.get('quantity',False):
                                vals_line.update({'product_uom_qty':post.get('quantity') })
                            
                            so_line_obj = request.env['sale.order.line'].sudo().create(vals_line)
 
                            if so_line_obj: 
                                return 1
        return 0                       
