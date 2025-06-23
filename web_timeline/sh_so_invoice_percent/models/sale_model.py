# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    invoiced_total_amount = fields.Monetary(
        string="Invoiced Amount", readonly=True, compute="_compute_invoice_total_amount",compute_sudo=True)
    invoiced_due_amount = fields.Monetary(
        string="Due Amount", readonly=True, compute="_compute_invoice_total_amount",compute_sudo=True)
    invoiced_paid_amount = fields.Monetary(
        string="Paid Amount", readonly=True, compute="_compute_invoice_total_amount",compute_sudo=True)
    sh_invoiced_paid_amount_in_percent = fields.Float(
        string="Amount Paid(%)", readonly=True, compute="_compute_invoice_total_amount", store=True,compute_sudo=True)
    
    inv_total_amount = fields.Monetary(string="Invoiced Amount ")
    inv_due_amount = fields.Monetary(string="Due Amount ")
    inv_paid_amount = fields.Monetary(string="Paid Amount ")
    
    def action_view_invoice(self):
        if self.invoice_ids:
            if len(self.invoice_ids.ids) == 1:
                return {
                    'name': 'Invoice',
                    'type': 'ir.actions.act_window',
                    'res_model': 'account.move',
                    'res_id':self.invoice_ids.id,
                    'view_mode': 'form',
                }
            else:
                return {
                    'name': 'Invoice',
                    'type': 'ir.actions.act_window',
                    'res_model': 'account.move',
                    'view_mode': 'tree,kanban,form,graph',
                    'domain':[('id','in',self.invoice_ids.ids)]
                }


    @api.depends('invoice_ids')
    def _compute_invoice_total_amount(self):
        if self:
            for rec in self:
                if rec.invoice_ids:
                    sum_of_invoice_amount = 0.0
                    sum_of_due_amount = 0.0
                    sum_of_paid_amount = 0.0
                    
                    for invoice_id in rec.invoice_ids.filtered(lambda inv: inv.state not in ['cancel', 'draft']):
                        sum_of_invoice_amount = sum_of_invoice_amount + invoice_id.amount_total
                        sum_of_due_amount = sum_of_due_amount + invoice_id.amount_residual_signed
                        if invoice_id.payment_state == 'paid':
                            sum_of_paid_amount += invoice_id.amount_total
                        elif invoice_id.payment_state == 'partial':
                            sum_of_paid_amount += (invoice_id.amount_total - invoice_id.amount_residual)

                    
                    rec.inv_total_amount = rec.invoiced_total_amount = sum_of_invoice_amount
                    rec.inv_paid_amount = rec.invoiced_paid_amount = sum_of_paid_amount
                    rec.inv_due_amount = rec.invoiced_due_amount = rec.amount_total - sum_of_paid_amount
                                        
                    if rec.amount_total != 0:
                        sh_precent = (rec.invoiced_paid_amount *
                                      100) / rec.amount_total
                        rec.sh_invoiced_paid_amount_in_percent = round(
                            sh_precent, 2)
                    else:
                        rec.sh_invoiced_paid_amount_in_percent = 0.0
                else:
                    rec.inv_total_amount = rec.invoiced_total_amount = 0.0
                    rec.inv_due_amount = rec.invoiced_due_amount = rec.amount_total
                    rec.inv_paid_amount = rec.invoiced_paid_amount = 0.0
                    rec.sh_invoiced_paid_amount_in_percent = 0.0
