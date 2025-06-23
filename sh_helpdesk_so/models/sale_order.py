# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api


class helpdeskSO(models.Model):
    _inherit = 'sale.order'

    sh_sale_ticket_ids = fields.Many2many("sh.helpdesk.ticket", string="Tickets")
    sale_ticket_count = fields.Integer(
        'Ticket', compute='_compute_sale_ticket_count')
    sh_invoice_verified = fields.Selection([('yes','Yes'),('no','No')],string='Invoice Verified')
    sh_custom_module_conflict = fields.Selection([('yes','Yes'),('no','No')],string='Custom Apps/Themes Installed Verified')
    sh_need_to_setup_environment = fields.Selection([('yes','Yes'),('no','No')],string='Need to setup Environment')
    sh_latest_update = fields.Selection([('yes','Yes'),('no','No')],string='Feature Update Verified')
    sh_original_module_send = fields.Boolean('Original Module need to send ?')
    sh_edition_id = fields.Many2one('sh.edition',string='Edition')
    sh_odoo_hosted_id = fields.Many2one('sh.odoo.hosted.on',string='Hosted On')
    sh_deployment_required = fields.Selection([('yes','Yes'),('no','No')],string='Deployment Verified')
    ticket_url = fields.Char('Ticket URL')
    # @api.depends('partner_id', 'sale_order_template_id')
    # def _compute_note(self):
    #     return
    
    def write(self,vals):
        for rec in self:
            if vals.get('state') and vals.get('state') == 'sent':
                related_task_ids = rec.tasks_ids
                if related_task_ids:
                    for task in related_task_ids:
                        task.stage_id = self.env.user.company_id.done_project_stage_id.id
                if rec.sh_sale_ticket_ids:
                    for ticket in rec.sh_sale_ticket_ids:
                        task_ids = self.env['project.task'].sudo().search([('sh_ticket_ids','in',ticket.id)])
                        if task_ids:
                            for task in task_ids:
                                task.stage_id = self.env.user.company_id.done_project_stage_id.id
        return super(helpdeskSO,self).write(vals)

    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            if vals.get('opportunity_id'):
                opportunity_id = self.env['crm.lead'].sudo().search([('id','=',vals.get('opportunity_id'))],limit=1)
                if opportunity_id and opportunity_id.sh_ticket_ids:
                    vals.update({
                        'sh_sale_ticket_ids':[(6,0,opportunity_id.sh_ticket_ids.ids)]
                    })
            res = super(helpdeskSO,self).create(vals)
            if self.env.context.get('active_model') == 'sh.helpdesk.ticket' and self.env.context.get('active_id'):
                ticket_id = self.env[self.env.context.get('active_model')].sudo().browse(self.env.context.get('active_id'))
                if ticket_id:
                    res.estimated_hrs = ticket_id.estimation_hours
        return res

    def action_create_sale_ticket(self):
        context = {}
        if self.partner_id:
            context.update({
                'default_partner_id': self.partner_id.id,
                'default_partner_ids':[(6,0,self.partner_id.ids)]
            })

        if self:
            context.update({
                'default_sh_sale_order_ids': [(6, 0, self.ids)],
            })
        if self.order_line:
            products = []
            for line in self.order_line:
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

    def _compute_sale_ticket_count(self):
        for record in self:
            record.sale_ticket_count = 0
            tickets = self.env['sh.helpdesk.ticket'].search(
                [('sh_sale_order_ids', 'in', record.ids)], limit=None)
            record.sale_ticket_count = len(tickets.ids)

    def action_view_sale_tickets(self):
        self.ensure_one()
        tickets = self.env['sh.helpdesk.ticket'].sudo().search(
            [('sh_sale_order_ids', 'in', self.ids)])
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
