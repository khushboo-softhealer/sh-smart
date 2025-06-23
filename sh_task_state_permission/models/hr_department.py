# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models


class ShDepartment(models.Model):
    _inherit = 'hr.department'

    allow_task_state_ids = fields.Many2many(
        'project.task.type', string='Allowing Task States')

    def write(self, vals):
        if not vals.get('allow_task_state_ids'):
            return super(ShDepartment, self).write(vals)
        old_allow_task_state_ids = self.allow_task_state_ids
        old_task_types = self.env['project.task.type'].search([
            ('id', 'in', old_allow_task_state_ids.ids)
        ])
        res = super(ShDepartment, self).write(vals)
        new_allow_task_state_ids = self.allow_task_state_ids
        for task_type in new_allow_task_state_ids:
            if self.id not in task_type.allow_department_ids.ids:
                # Add the department in the stage
                task_type.write({
                    'allow_department_ids': [(4, self.id)]
                })
        for old_task_type in old_task_types:
            if old_task_type.id not in new_allow_task_state_ids.ids:
                if self.id in old_task_type.allow_department_ids.ids:
                    # Remove the department from the stage
                    old_task_type.write({
                        'allow_department_ids': [(3, self.id)]
                    })
        return res