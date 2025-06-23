# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api

class Task(models.Model):
    _inherit = 'project.task'

    ticket_count = fields.Integer('Tickets', compute='_compute_ticket_count')

    def _compute_ticket_count(self):
        if self:
            for rec in self:
                rec.ticket_count = 0
                ticket_ids = self.env['sh.helpdesk.ticket'].sudo().search(
                    [('task_ids', 'in', [rec.id])])
                if ticket_ids:
                    rec.ticket_count = len(ticket_ids.ids)

    def action_view_ticket(self):
        self.ensure_one()
        tickets = self.env['sh.helpdesk.ticket'].sudo().search(
            [('task_ids', 'in', self.ids)])
        action = self.env.ref(
            "sh_helpdesk.helpdesk_ticket_action").read()[0]
        if len(tickets) > 1:
            action['domain'] = [('id', 'in', tickets.ids)]
        elif len(tickets) == 1:
            form_view = [
                (self.env.ref('sh_helpdesk.helpdesk_ticket_form_view').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + \
                    [(state, view)
                     for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = tickets.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    @api.model_create_multi
    def create(self, vals_list):
        res = super(Task, self).create(vals_list)
        for vals in vals_list:
            if res.account_move_id:
                invoice_id = self.env['account.move'].sudo().search([('id','=',res.account_move_id.id)])
                if invoice_id and invoice_id.sh_ticket_ids:
                    res.sh_ticket_ids = [(6,0,invoice_id.sh_ticket_ids.ids)]
            if res.sh_ticket_ids:
                for ticket in res.sh_ticket_ids:
                    if res.partner_id:
                        ticket.partner_ids = [(6,0,res.partner_id.ids)]
                    ticket.sudo().write({
                        'task_ids': [(4, res.id)]
                    })
                    if ticket.attachment_ids:
                        for attachment in ticket.attachment_ids:
                            self.env['ir.attachment'].sudo().create({
                                'name': attachment.name,
                                'type': attachment.type,
                                'datas': attachment.datas,
                                'mimetype': attachment.mimetype,
                                'res_model': 'project.task',
                                'res_id': res.id,
                                'public': True,
                            })
        return res
