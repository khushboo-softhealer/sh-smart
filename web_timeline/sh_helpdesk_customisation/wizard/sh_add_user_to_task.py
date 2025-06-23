# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields

class AddUserToTask(models.TransientModel):
    _name = 'sh.add.user.to.task'
    _description = 'Add users to tasks'

    sh_action = fields.Selection([('add','Add'),('remove','Remove')],string='Add/Remove',default='add')
    sh_user_ids = fields.Many2many('res.users',string='Users',domain=[('share','=',False)],required=True)

    def action_users(self):
        ticket_id = self.env['sh.helpdesk.ticket'].search([('id','=',self.env.context.get('active_id'))])
        if ticket_id:
            if ticket_id.sh_version_id and ticket_id.product_ids:
                sub_task_ids = self.env['project.task'].search([
                    ('version_ids', 'in', [ticket_id.sh_version_id.id]),
                    ('sh_product_id', 'in', ticket_id.product_ids.ids),
                    ('parent_id', '!=', False)
                ])
                if sub_task_ids:
                    if self.sh_action == 'add':
                        for task in sub_task_ids:
                            task.user_ids = [(4, user.id) for user in self.sh_user_ids]
                    elif self.sh_action == 'remove':
                        for task in sub_task_ids:
                            task.user_ids = [(3, user.id) for user in self.sh_user_ids]




