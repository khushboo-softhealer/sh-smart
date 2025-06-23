# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields

class HelpdeskTicket(models.Model):
    _inherit = 'sh.helpdesk.ticket'

    def create_task(self):
        ctx = {
                'default_name': self.name,
                'default_user_id': self.user_id.id,
                'default_sh_ticket_ids': [(4, self.id)],
                'default_partner_id': self.partner_id.id,
                'default_date_deadline': fields.Date.today(),
                'default_responsible_ids':[(6,0,self.sh_user_ids.ids)],
                'default_description': self.description,
                'default_project_id' : self.env.user.company_id.project_id_created_from_so.id
            }
        if self.sh_sale_order_ids:
            ctx.update({
                'default_sale_order_id':self.sh_sale_order_ids[0].id,
            })
        if self.sh_invoice_ids:
            ctx.update({
                'default_account_move_id':self.sh_invoice_ids[0].id,
            })
        if len(self.product_ids.mapped('product_tmpl_id')) == 1:
            ctx.update({
                'product_template_id':self.product_ids.mapped('product_tmpl_id').id,
                })
        return{
            'name': 'Tasks',
            'res_model': 'project.task',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': ctx
        }

    def view_task(self):
        task_ids = self.env['project.task'].sudo().search(
            [('sh_ticket_ids', 'in', [self.id])])
        return{
            'name': 'Tasks',
            'res_model': 'project.task',
            'view_mode': 'kanban,tree,form',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', task_ids.ids)],
            'target': 'current',
        }
