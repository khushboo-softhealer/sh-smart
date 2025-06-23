# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models

class sh_project_task_type(models.Model):
    _inherit = 'project.task.type'

    default_add_new_project = fields.Boolean(string="Default Add New Project")
    test = fields.Char(string="Test")

    # for task time
    user_ids = fields.Many2many('res.users', string="Related Employees")
    stage_wize_employee_line = fields.One2many(
        'sh.stage.employee', 'task_type_id', string="Employees")
    stage_wize_default_employee_line = fields.One2many(
        'sh.stage.employee', 'sh_task_type_id', string="Default Employees")
    sh_is_appstore_task_state = fields.Boolean('Is Appstore Task State ?', compute='_compute_sh_is_appstore_task_state', store=True)

    def _compute_sh_is_appstore_task_state(self):
        for state in self:
            state.sh_is_appstore_task_state = False
            if state.env.user.company_id.appstore_project_id.id in state.project_ids.ids:
                state.sh_is_appstore_task_state = True
