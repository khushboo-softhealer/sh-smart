# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    project_task_id = fields.Many2many('project.task',string='Project Task Id',copy=False)
    version_ids = fields.Many2many("sh.version", string="Version")
    responsible_user_ids = fields.Many2many('res.users',
                                            string="Responsible Users")
    responsible_user_id = fields.Many2one("res.users",string="Assign To")                                            
    sh_task_count = fields.Integer(compute='_compute_tasks_sh')

    def _compute_tasks_sh(self):
        for rec in self:
            rec.sh_task_count = 0
            tasks = self.env['project.task'].sudo().search([("account_move_id", "=", rec.id)])
            if tasks:
                rec.sh_task_count = len(tasks.ids)

    def get_tasks(self):

        if self.sh_task_count  == 1:
            return {
                "type": "ir.actions.act_window",
                "name": "Tasks",
                "view_mode": "form",
                "res_model": "project.task",
                "res_id" : self.env['project.task'].search([("account_move_id", "=", self.id)]).id
            }
        
        else:
            return {
                "type": "ir.actions.act_window",
                "name": "Tasks",
                "view_mode": "tree,form",
                "res_model": "project.task",
                "domain": [("account_move_id", "=", self.id)],
            }
