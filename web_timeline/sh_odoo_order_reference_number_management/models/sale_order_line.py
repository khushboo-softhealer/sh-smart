# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.


from odoo import models, fields
import re
# from datetime import date

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    odoo_partner_id = fields.Many2one("res.partner", string='Odoo Customer', domain="[('name', '!=', 'unknown customer')]")
    sh_price_subtotal = fields.Float(string='Base Price Total', compute='_compute_sh_price_subtotal')
    sh_helpdesk_ticket_id = fields.Many2one('sh.helpdesk.ticket')
    
    def _compute_sh_price_subtotal(self):
        company_currency = self.env.company.currency_id
        for rec in self:
            rec.sh_price_subtotal = rec.currency_id._convert(rec.price_subtotal,company_currency, self.env.company,fields.Date.today())

    def action_remove_odoo_customer(self):
        for rec in self:
            if rec.odoo_partner_id:
                rec.odoo_partner_id = False
            if rec.origin and rec.origin not in ("",False,None):
                origin = rec.origin
                if 'Commission' in origin:
                    pattern = r"'(.*?)'"
                    result = re.search(pattern, origin).group(1)
                    if result:
                        ticket_id = self.env['sh.helpdesk.ticket'].search([('store_reference','not in',[" ",False,None]),('store_reference','=',result),('partner_id.name','!=','unknown customer')],limit=1)
                        if ticket_id:
                            rec.odoo_partner_id = ticket_id.partner_id.id
                else:
                    ticket_id = self.env['sh.helpdesk.ticket'].search([('store_reference','not in',[" ",False,None]),('store_reference','=',origin),('partner_id.name','!=','unknown customer')],limit=1)
                    if ticket_id:
                        rec.odoo_partner_id = ticket_id.partner_id.id
