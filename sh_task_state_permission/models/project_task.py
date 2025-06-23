# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import models, _
from odoo.exceptions import UserError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    def write(self, vals):
        res = super(ProjectTask, self).write(vals)
        if not vals.get('stage_id'):
            return res
        if not self.project_id:
            return res
        if not self.project_id.sh_restrict_stage_movement:
            return res
        if not self.env.user:
            raise UserError(_('Error: Unknown user !'))
        user = self.env.user
        if not user.employee_id:
            raise UserError(_("Error: User arn't an employee !"))
        employee = user.employee_id
        if not employee.department_id:
            raise UserError(
                _("Error: Please select the department for the employee !"))
        department = employee.department_id
        stage_id = self.env['project.task.type'].browse(vals['stage_id'])
        if stage_id.allow_department_ids:
            if department.id in stage_id.allow_department_ids.ids:
                return res
        allow_task_states = department.allow_task_state_ids
        if not allow_task_states:
            raise UserError(
                _(f"Error: You are not allowed to change the state to '{stage_id.name}' !"))
        if vals['stage_id'] in allow_task_states.ids:
            return res
        raise UserError(
            _(f"Error: You are not allowed to change the state to '{stage_id.name}' !"))
