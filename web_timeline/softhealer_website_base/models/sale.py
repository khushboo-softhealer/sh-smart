# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, SUPERUSER_ID, fields

class SaleOrder(models.Model):
    _inherit = "sale.order"

    sh_download_log_count = fields.Integer(readonly=True,compute='_compute_download_count_count')

    def _compute_download_count_count(self):
        for record in self:
            record.sh_download_log_count = 0
            sale_orders = self.env['sh.module.download.log'].search(
                [('sale_order_id', '=', record.id)], limit=None)
            if sale_orders:
                record.sh_download_log_count = len(sale_orders.ids)

    def action_view_sh_download_logs_views(self):
        self.ensure_one()
        # sale_orders = self.env['sh.module.download.log'].search(
        #         [('sale_order_id', '=', self.id)], limit=None)
        return{
            'name': 'Download Logs',
            'res_model': 'sh.module.download.log',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'domain': [('sale_order_id', '=', self.id)],
            'target': 'current',
        }

    def write(self, values):
        result = super(SaleOrder, self).write(values)
        
        inter_state = self.env["account.fiscal.position"].search([
            ('state_type','=','inter_state'),('country_id.code','=','IN')
            ], limit=1)
        
        intra_state = self.env["account.fiscal.position"].search([
            ('state_type','=','intra_state'),('country_id.code','=','IN')
            ], limit=1)

        if (self and self.partner_id
            and self.partner_id.country_id 
            and self.pricelist_id.currency_id.name == 'INR' 
            and self.partner_id.country_id.code == 'IN'
            and self.partner_id.state_id
            and self.partner_id.state_id.code != 'GJ'):
            
            if not self.fiscal_position_id.id == inter_state.id or not self.fiscal_position_id:
                self.partner_id.with_user(SUPERUSER_ID).write({
                    "property_account_position_id": inter_state.id,
                })
                self.with_user(SUPERUSER_ID).write({
                    "fiscal_position_id": inter_state.id,
                })
        if (self and self.partner_id
            and self.partner_id.country_id
            and self.partner_id.country_id.code == 'IN'
            and self.pricelist_id.currency_id.name == 'INR' 
            and self.partner_id.state_id
            and self.partner_id.state_id.code == 'GJ'):

            if not self.fiscal_position_id.id == intra_state.id or not self.fiscal_position_id:
                
                self.partner_id.with_user(SUPERUSER_ID).write({
                    "property_account_position_id": intra_state.id,
                })
                self.with_user(SUPERUSER_ID).write({
                    "fiscal_position_id": intra_state.id,
                })
        return result