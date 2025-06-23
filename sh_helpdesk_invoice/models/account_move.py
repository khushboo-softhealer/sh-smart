# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api


class helpdeskMove(models.Model):
    _inherit = 'account.move'

    sh_ticket_ids = fields.Many2many("sh.helpdesk.ticket", string="Tickets")
    ticket_count = fields.Integer(
        'Ticket', compute='_compute_ticket_count')

    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            if vals.get('invoice_origin'):
                sale_id = self.env['sale.order'].sudo().search([('name','=',vals.get('invoice_origin'))],limit=1)
                if sale_id and sale_id.sh_sale_ticket_ids:
                    vals.update({
                        'sh_ticket_ids':[(6,0,sale_id.sh_sale_ticket_ids.ids)]
                    })
                if sale_id and sale_id.sh_responsible_user_ids:
                    vals.update({
                        'responsible_user_ids':[(6,0,sale_id.sh_responsible_user_ids.ids)]
                    })
                if sale_id and sale_id.responsible_user_id:
                    vals.update({
                        'responsible_user_id': sale_id.responsible_user_id.id
                    })

        return super(helpdeskMove, self).create(vals_list)

    def action_create_ticket(self):
        context = {}
        if self.partner_id:
            context.update({
                'default_partner_id': self.partner_id.id,
                'default_partner_ids':[(6,0,self.partner_id.ids)]
            })
        if self:
            context.update({
                'default_sh_invoice_ids': [(6, 0, self.ids)],
            })
        if self.invoice_line_ids:
            products = []
            for line in self.invoice_line_ids:
                if line.product_id.id not in products:
                    products.append(line.product_id.id)
            context.update({
                'default_product_ids': [(6, 0, products)]
            })
        return{
            'name': 'Helpdesk Ticket',
            'type': 'ir.actions.act_window',
            'res_model': 'sh.helpdesk.ticket',
            'view_mode': 'form',
            'context': context,
            'target': 'current'
        }

    def _compute_ticket_count(self):
        for record in self:
            record.ticket_count = 0
            tickets = self.env['sh.helpdesk.ticket'].search(
                [('sh_invoice_ids', 'in', record.ids)], limit=None)
            record.ticket_count = len(tickets.ids)

    def ticket_counts(self):
        self.ensure_one()
        tickets = self.env['sh.helpdesk.ticket'].sudo().search([('sh_invoice_ids', 'in', self.ids)])

        # REDIRECT TO FORM VIEW 
        if len(tickets) == 1:
            return {
            'name': 'Helpdesk Tickets',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'sh.helpdesk.ticket',
            'res_id': tickets.id,
        }

        # REDIRECT TO kanban VIEW 
        if len(tickets) > 1:
            view_id = self.env.ref('sh_helpdesk.helpdesk_ticket_tree_view').id
            return {
                'type': 'ir.actions.act_window',
                'name': "Helpdesk Tickets",
                'res_model': 'sh.helpdesk.ticket',
                'view_mode': 'tree',
                'views': [[view_id, 'list']],
                'domain': [('id', 'in', tickets.ids)],
            }
