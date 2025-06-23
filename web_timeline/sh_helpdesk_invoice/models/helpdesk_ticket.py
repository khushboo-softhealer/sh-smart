# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields

class HelpdeskTicketInvoice(models.Model):
    _inherit = 'sh.helpdesk.ticket'

    invoice_count = fields.Integer(
        'Invoice', compute='_compute_invoice_count_helpdesk')

    def action_create_invoice(self):
        context = {
            'default_type': 'out_invoice',
            'form_view_ref': 'account.view_move_form',
        }
        if self.partner_id:
            context.update({
                'default_partner_id': self.partner_id.id,
            })
        if self.user_id:
            context.update({
                'default_user_id': self.user_id.id,
            })
        if self:
            context.update({
                'default_sh_ticket_ids': [(6, 0, self.ids)],
            })
        if self.product_ids:
            line_list = []
            for product in self.product_ids:
                journal_id = self.env["account.journal"].search(
                    [("type", "=", "sale"), ('name', '=', 'Customer Invoices'), ('company_id', '=', self.env.user.company_id.id)], limit=None)
                account_id = False
                if journal_id.default_account_id:
                    account_id = journal_id.default_account_id
                line_vals = {
                    'product_id': product.id,
                    'name': product.name_get()[0][1],
                    'quantity': 1.0,
                    'price_unit': product.list_price,
                    'product_uom_id': product.uom_id.id,
                    'currency_id':self.env.company.currency_id.id,
                    'account_id': False,
                }
                if account_id:
                    line_vals.update({
                    'account_id': account_id.id,
                    'currency_id':account_id.currency_id.id,
                    })

                if product.taxes_id:
                    line_vals.update({
                        'tax_ids': [(6, 0, product.taxes_id.ids)]
                    })
                line_list.append((0, 0, line_vals))
            context.update({
                'default_invoice_line_ids': line_list,
            })
        return{
            'name': 'Customer Invoice',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'context': context,
            'target': 'current'
        }

    def _compute_invoice_count_helpdesk(self):
        for record in self:
            record.invoice_count = 0
            tickets = self.env['account.move'].search(
                [('id', 'in', record.sh_invoice_ids.ids)], limit=None)
            record.invoice_count = len(tickets.ids)

    def invoice_counts(self):
        self.ensure_one()
        
        orders = self.env['account.move'].sudo().search(
            [('id', 'in', self.sh_invoice_ids.ids)])

        # REDIRECT TO FORM VIEW 
        if len(orders) == 1:
            return {
            'name': 'Account Invoice',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': orders.id,
        }

        # REDIRECT TO TREE VIEW 
        if len(orders) > 1:
            view_id = self.env.ref('account.view_out_invoice_tree').id
            return {
                'type': 'ir.actions.act_window',
                'name': "Account Invoice",
                'res_model': 'account.move',
                'view_mode': 'tree',
                'views': [[view_id, 'list']],
                'domain': [('id', 'in', orders.ids)],
            }
