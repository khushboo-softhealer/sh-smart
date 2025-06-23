# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sh_invoice_task_count = fields.Integer('Tasks ',compute='_compute_sh_invoice_task_count')
    responsible_user_id = fields.Many2one("res.users", string="Technical Head", readonly=False,store=True)
    sh_responsible_user_ids = fields.Many2many(
        "res.users", string="Responsible USers")
    sh_task_id = fields.Many2one("project.task", string="Task")
    
    def _compute_sh_invoice_task_count(self):
        for rec in self:
            rec.sh_invoice_task_count = 0
            tasks = self.env['project.task'].sudo().search(['|','|',('id','=',self.sh_task_id.id),('sh_ticket_ids','in',rec.sh_sale_ticket_ids.ids),('account_move_id.invoice_origin','=',rec.name)])
            if tasks:
                rec.sh_invoice_task_count = len(tasks.ids)


    def action_view_sale_invoice_task(self):
        self.ensure_one()
        tasks = self.env['project.task'].sudo().search(['|', '|', ('id', '=', self.sh_task_id.id), (
            'sh_ticket_ids', 'in', self.sh_sale_ticket_ids.ids), ('account_move_id.invoice_origin', '=', self.name)])
        return{
            'name': 'Tasks',
            'res_model': 'project.task',
            'view_mode': 'kanban,tree,form',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', tasks.ids)],
            'target': 'current',
        }
