# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import _, api, fields, models

class ShSaleQuotationCancel(models.TransientModel):
    _name = 'sh.sale.quotation.cancel'
    _description = "sh sale quotation cancel reason"

    cancel_reason = fields.Char(string="Cancel Reason",required=True)
    order_id  = fields.Many2one('sale.order',string="Sale Order")

    def sale_quotation_cancel_reason(self):
        if self.order_id:
            self.order_id.with_context(disable_cancel_warning=True).action_cancel()
            project = self.order_id.project_id
            if project.allocated_hours >= self.order_id.estimated_hrs and self.order_id.state == 'cancel':
                project_allocated_hrs = project.allocated_hours - self.order_id.estimated_hrs  
                project.sudo().write({'allocated_hours' : project_allocated_hrs})

            self.order_id.message_post(body=self.cancel_reason + '(Quotation Cancel Reason)')
