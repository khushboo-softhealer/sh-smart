# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    sh_billed_total_amount = fields.Monetary(
        string="Billed Amount", readonly=True, compute="_compute_bill_total_amount")
    sh_billed_due_amount = fields.Monetary(
        string="Due Amount", readonly=True, compute="_compute_bill_total_amount")
    sh_billed_paid_amount = fields.Monetary(
        string="Paid Amount", readonly=True, compute="_compute_bill_total_amount")
    sh_billed_paid_amount_in_percent = fields.Float(
        string="Amount Paid(%)", readonly=True, compute="_compute_bill_total_amount")

    sh_total_bill = fields.Monetary()
    sh_due_bill = fields.Monetary()
    sh_paid_bill = fields.Monetary()
    sh_paid_bill_percent = fields.Monetary()

    @api.depends('invoice_ids')
    def _compute_bill_total_amount(self):
        if self:
            for rec in self:
                if rec.invoice_ids:
                    sum_of_bill_amount = 0.0
                    sum_of_due_amount = 0.0
                    for invoice_id in rec.invoice_ids.filtered(lambda inv: inv.state not in ['cancel', 'draft']):
                        sum_of_bill_amount = sum_of_bill_amount + invoice_id.amount_total
                        sum_of_due_amount = sum_of_due_amount + invoice_id.amount_residual

                    rec.sh_billed_total_amount = sum_of_bill_amount
                    rec.sh_billed_due_amount = sum_of_due_amount
                    rec.sh_billed_paid_amount = rec.sh_billed_total_amount - rec.sh_billed_due_amount


                    # rec.sh_total_bill = sum_of_bill_amount
                    rec.sh_total_bill = rec.sh_billed_total_amount
                    # rec.sh_due_bill = sum_of_due_amount
                    rec.sh_due_bill = rec.sh_billed_due_amount
                    # rec.sh_paid_bill = rec.sh_billed_total_amount - rec.sh_billed_due_amount
                    rec.sh_paid_bill = rec.sh_billed_paid_amount

                    if rec.amount_total != 0:
                        sh_percent = (rec.sh_billed_paid_amount *
                                      100) / rec.amount_total
                        rec.sh_billed_paid_amount_in_percent = round(
                            sh_percent, 2)
                        rec.sh_paid_bill_percent = rec.sh_billed_paid_amount_in_percent

                    else:
                        rec.sh_billed_paid_amount_in_percent = 0.0
                        rec.sh_paid_bill_percent = 0.0
                else:
                    rec.sh_billed_total_amount = 0.0
                    rec.sh_billed_due_amount = 0.0
                    rec.sh_billed_paid_amount = 0.0
                    rec.sh_billed_paid_amount_in_percent = 0.0


                    rec.sh_total_bill =  rec.sh_billed_total_amount
                    rec.sh_due_bill = rec.sh_billed_due_amount
                    rec.sh_paid_bill = rec.sh_billed_paid_amount
                    rec.sh_paid_bill_percent = rec.sh_billed_paid_amount_in_percent
