# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ShProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    allow_department_ids = fields.Many2many(
        'hr.department', string='Allowing Departments')

    def write(self, vals):
        if not vals.get('allow_department_ids'):
            return super(ShProjectTaskType, self).write(vals)
        old_allow_department_ids = self.allow_department_ids
        old_departments = self.env['hr.department'].search([
            ('id', 'in', old_allow_department_ids.ids)
        ])
        res = super(ShProjectTaskType, self).write(vals)
        new_departments = self.allow_department_ids
        for department in new_departments:
            if self.id not in department.allow_task_state_ids.ids:
                # Add the state in the department
                department.write({
                    'allow_task_state_ids': [(4, self.id)]
                })
        for old_department in old_departments:
            if old_department.id not in new_departments.ids:
                if self.id in old_department.allow_task_state_ids.ids:
                    # Remove the department from the stage
                    old_department.write({
                        'allow_task_state_ids': [(3, self.id)]
                    })
        return res