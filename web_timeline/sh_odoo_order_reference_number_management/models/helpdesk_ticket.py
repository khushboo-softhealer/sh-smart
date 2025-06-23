# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from datetime import timedelta
from odoo import models, fields, api,_
import logging
_logger = logging.getLogger(__name__)

class HelpdeskTicketOrderInformation(models.Model):
    _inherit = 'sh.helpdesk.ticket'
    
    country = fields.Char('Country')
    
    sale_order_lines = fields.Many2many('sale.order.line',string="Product Lines")
    
    # compute="_compute_sale_order_lines"
    sh_valid_store_reference_bool = fields.Boolean('Valid Reference', default=False)
    

    
    def update_store_reference(self):
        for record in self:
            if record.store_reference and record.store_reference not in (" ",False,None):
                order_line = self.env['sale.order.line'].search([('origin','ilike',record.store_reference)])
                if order_line:
                    record.sh_valid_store_reference_bool = True
                    if record.partner_id.name != 'unknown customer':
                        if order_line:
                            for order in order_line:
                                if not order.odoo_partner_id:
                                    order.write({'odoo_partner_id':record.partner_id.id})
            else:
                record.sh_valid_store_reference_bool = False
                self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
                    'title': _("Warning"),
                    'message': _('Your Reference Number %s is invalid',record.store_reference),
                })

    def action_get_so_lines(self):
        self.ensure_one()
        ticket_order_line = []
        if self.partner_id.name == 'unknown customer':
            sale_order_line = False
            if self.store_reference and self.store_reference not in (""," ",False, None):
                sale_order_line_ids = """
                    SELECT ARRAY_AGG(id) FROM sale_order_line 
                    WHERE 
                    origin ILIKE %s
                """
                self.env.cr.execute(sale_order_line_ids,[f'%{self.store_reference}%'])
                # Fetch the results
                sale_order_line_ids_record = self.env.cr.fetchall()[0][0]
                sale_order_line = self.env['sale.order.line'].browse(sale_order_line_ids_record[0])
                
                if sale_order_line_ids_record and sale_order_line_ids_record != None:
                    ticket_order_line = ticket_order_line + sale_order_line_ids_record
                else:
                    ticket_order_line = []
                    
                if ticket_order_line:
                    if sale_order_line:
                        country = sale_order_line[0].country
                    self.country = country
                    self.sale_order_lines = [(6,0, ticket_order_line)]
                else:
                    self.sale_order_lines = False
            else:
                self.sale_order_lines = False
        elif self.partner_id.name != 'unknown customer':
            sale_order_line = False
            # Get partner parent and child ids 
            all_partner_list = [self.partner_id.id]
            if self.partner_id.parent_id.id:
                all_partner_list = all_partner_list +  [self.partner_id.parent_id.id]
                
            if self.partner_id.child_ids.ids:
                all_partner_list += self.partner_id.child_ids.ids
                
            if self.partner_id.parent_id.child_ids.ids:
                all_partner_list += self.partner_id.parent_id.child_ids.ids
                
            # Get sale order with same partner and done state
            sale_order_ids = """
                    SELECT ARRAY_AGG(id) FROM sale_order 
                    WHERE 
                        partner_id IN %s
                        AND state IN ('sale', 'done')
                """
            self.env.cr.execute(sale_order_ids,(tuple(all_partner_list),))
            
            # Fetch the results
            sale_order_ids_record = self.env.cr.fetchall()[0][0]
            
            if sale_order_ids_record and sale_order_ids_record!=None:
                # if sale order ids get sale order line
                sale_order_line_ids = """
                        SELECT ARRAY_AGG(id) FROM sale_order_line 
                        WHERE 
                            odoo_partner_id IN %s
                            OR order_id IN %s
                            OR origin ILIKE %s
                    """
                self.env.cr.execute(sale_order_line_ids,(tuple(all_partner_list),tuple(sale_order_ids_record),f'%{self.store_reference}%'))
                # Fetch the results
                sale_order_line_ids_record = self.env.cr.fetchall()[0][0]
            else:
                # get sale order line
                sale_order_line_ids = """
                        SELECT ARRAY_AGG(id) FROM sale_order_line 
                        WHERE 
                            odoo_partner_id IN %s
                            OR origin ILIKE %s
                    """
                self.env.cr.execute(sale_order_line_ids,(tuple(all_partner_list),f'%{self.store_reference}%'))
                # Fetch the results
                sale_order_line_ids_record = self.env.cr.fetchall()[0][0]
                
    
            if sale_order_line_ids_record and sale_order_line_ids_record!=None:
                sale_order_line = self.env['sale.order.line'].browse(sale_order_line_ids_record[0])
                ticket_order_line = ticket_order_line + sale_order_line_ids_record
            else:
                ticket_order_line = []
                
            if ticket_order_line:
                if sale_order_line:
                    country = sale_order_line.country
                self.sale_order_lines = [(6,0,ticket_order_line)]
                self.country = country
            else:
                self.sale_order_lines = [(6,0,ticket_order_line)]
                self.country = False
    
    def action_mass_reference_number(self):
        active_helpdesk_ticket_ids = self.env['sh.helpdesk.ticket'].sudo().browse(self.env.context.get('active_ids'))
        if active_helpdesk_ticket_ids:
            for ticket in active_helpdesk_ticket_ids:
                order_line = self.env['sale.order.line'].search([('origin','ilike',ticket.store_reference)])
        
           
                sale_order = self.env['sale.order'].search([('name','=',ticket.store_reference),('state','in',['sale','done'])])
       
                
                if order_line:
                    # This Condition execute when store reference number in sol origins.
                    ticket.sh_valid_store_reference_bool = True
                    if ticket.partner_id.name != 'unknown customer':
                        # this condition ectecute when customer is not unknown. 
                       
                        sale_order = self.env['sale.order'].search([('partner_id','=',ticket.partner_id.id),('state','in',['sale','done'])])
                        ticket_order_line = []
                        if order_line:
                            for order in order_line:
                                order.update({'odoo_partner_id':ticket.partner_id.id})
                                if order.odoo_partner_id:
                                    ticket_order_line.append(order.id)
                        if sale_order and sale_order.order_line:
                            for order in sale_order.order_line:
                                ticket_order_line.append(order.id)
                            
                        if ticket_order_line:
                            if order_line:
                                country = order_line[0].country
                            elif sale_order:
                                country = sale_order.order_line[0].country
                            ticket.update({
                                    'sale_order_lines' : [(6,0, ticket_order_line)],
                                    'country':country,
                                    }) 
                    elif ticket.partner_id.name == 'unknown customer':
                        
                        # this condition ectecute when customer is unknown 
                        
                        ticket_order_line = []
                        if order_line:
                            for order in order_line:
                                ticket_order_line.append(order.id)
                        
                        if ticket_order_line:
                            if order_line:
                                country = order_line[0].country
                            elif sale_order:
                                country = sale_order.order_line[0].country
                            ticket.update({
                                    'sale_order_lines' : [(6,0, ticket_order_line)],
                                    'country':country,
                                    }) 
                            
                elif sale_order:
                    # This Condition execute when store reference number in so name.
                    ticket.sh_valid_store_reference_bool = True
                    if ticket.partner_id.name != 'unknown customer':
                        
                        sale_order = self.env['sale.order'].search([('name','=',ticket.store_reference),('state','in',['sale','done'])])
                        ticket_order_line = []
                        if sale_order and sale_order.order_line:
                            for order in sale_order.order_line:
                                ticket_order_line.append(order.id)
                        if ticket_order_line:
                            if sale_order and sale_order.country_code:
                                country = sale_order.country_code
                            elif sale_order.order_line:
                                country = sale_order.order_line[0].country
                            ticket.update({
                                    'sale_order_lines' : [(6,0, ticket_order_line)],
                                    'country':country,
                                    }) 
                    elif ticket.partner_id.name == 'unknown customer':
                        
                        sale_order = self.env['sale.order'].search([('name','=',ticket.store_reference),('state','in',['sale','done'])])
                        ticket_order_line = []
                        if sale_order and sale_order.order_line:
                            for order in sale_order.order_line:
                                ticket_order_line.append(order.id)
                        
                        if ticket_order_line:
                            if sale_order and sale_order.country_code:
                                country = sale_order.country_code
                            elif sale_order.order_line:
                                country = sale_order.order_line[0].country
                            ticket.update({
                                    'sale_order_lines' : [(6,0, ticket_order_line)],
                                    'country':country,
                                    }) 
                else:
                    ticket.sh_valid_store_reference_bool = False
                    self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
                    'title': _("Warning"),
                    'message': _('In Your Ticket %s Reference Number %s is Invalid ',ticket.name, ticket.store_reference),
                })
                
             
                
        
   
    def _compute_sh_common_compute_form(self):
        res = super(HelpdeskTicketOrderInformation,self)._compute_sh_common_compute_form()
        for record in self:
            record.sh_common_compute_form = True
            # if record.store_reference:
                
            order_line = self.env['sale.order.line'].sudo().search(
                [('origin', 'ilike', record.store_reference)], limit=1)
            sale_order = self.env['sale.order'].search([('name','=',record.store_reference),('state','in',['sale','done'])])
            if order_line:
                record.sh_order_date = order_line.so_order_date
                support_end_date = order_line.so_order_date + \
                    timedelta(days=60)
                sh_order_date = support_end_date - fields.Datetime.now()
                record.sh_days_left = int(sh_order_date.days)
                
            elif sale_order:
                record.sh_order_date = sale_order.date_order
                support_end_date = sale_order.date_order + \
                    timedelta(days=60)
                sh_order_date = support_end_date - fields.Datetime.now()
                record.sh_days_left = int(sh_order_date.days)
                
            if record.sale_order_lines:
                sh_total_order_qty = 0.0
                sh_total_order_price_unit = 0.0
                for line in record.sale_order_lines:
                    sh_total_order_qty += line.product_uom_qty
                    sh_total_order_price_unit += line.sh_price_subtotal
                record.sh_total_order_qty = sh_total_order_qty
                record.sh_total_order_price_unit = sh_total_order_price_unit
        return res
    
    