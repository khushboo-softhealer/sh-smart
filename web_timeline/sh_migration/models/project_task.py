# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api
from odoo.exceptions import UserError


class ShMigrationProjectTask(models.Model):
    _inherit = 'project.task'

    # COMPUTE FIELDS
    sh_migration_is_appstore_project_task = fields.Boolean(
        'Is Appstore Project Task')
    sh_migration_is_v17_task = fields.Boolean('Is v17 Task')
    sh_migration_pending_bugs = fields.Integer(
        'Pending Bugs', compute='_compute_pending_bugs')
    sh_migration_bug_line = fields.One2many('sh.module.bug', 'task_id', string='Bug Line')
    sh_migration_cr_line = fields.One2many('sh.task.upcoming.feature', 'task_id', string='CR Line')

    # ----------------------------------------------
    #  COMPUTE METHODS
    # ----------------------------------------------

    # @api.depends('version_ids', 'company_id.sh_migration_v17_version_id')
    @api.depends('version_ids')
    def _compute_is_v17_task(self):
        for task in self:
            task._get_responsible_user()
            task.sh_migration_is_v17_task = False
            if not (task.version_ids and task.company_id.sh_migration_v17_version_id):
                continue
            if len(task.version_ids) != 1:
                continue
            if task.company_id.sh_migration_v17_version_id.id == task.version_ids[0].id:
                task.sh_migration_is_v17_task = True

    # @api.depends('project_id', 'company_id.appstore_project_id')
    @api.depends('project_id')
    def _compute_is_appstore_project(self):
        for task in self:
            task.sh_migration_is_appstore_project_task = False
            if task.company_id.appstore_project_id and task.project_id:
                if task.company_id.appstore_project_id.id == task.project_id.id:
                    task.sh_migration_is_appstore_project_task = True

    def _compute_pending_bugs(self):
        for task in self:
            task.sh_migration_pending_bugs = self.env['sh.module.bug'].sudo().search_count([
                ('task_id', '=', task.id),
                ('state_id', 'not in',
                 self.company_id.sh_migration_bug_complete_state_ids.ids),
            ])

    def _compute_v17_and_appstore(self):
        for task in self:
            task._compute_is_appstore_project()
            task._compute_is_v17_task()

    # ----------------------------------------------
    #  ORM METHODS
    # ----------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        tasks = super(ShMigrationProjectTask, self).create(vals_list)
        for task in tasks:
            if task.version_ids:
                task._compute_is_v17_task()
            if task.project_id:
                task._compute_is_appstore_project()
        return tasks

    def write(self, vals):
        status = super(ShMigrationProjectTask, self).write(vals)
        if 'version_ids' in vals:
            self._compute_is_v17_task()
        if 'project_id' in vals:
            self._compute_is_appstore_project()
        return status

    # ----------------------------------------------
    #  SMART BUTTONS
    # ----------------------------------------------

    def smart_btn_open_bugs(self):
        view = {
            'name': 'Bugs',
            'type': 'ir.actions.act_window',
            'res_model': 'sh.module.bug',
            'domain': [('task_id', '=', self.id)],
            'context': {
                'default_task_id': self.id,
                'search_default_group_by_state_id': 1,
                'create': False
            },
            'target': 'current',
        }
        if self.sh_migration_pending_bugs == 0:
            view.update({
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': self.env.ref('sh_migration.sh_module_bug_view_form').id
            })
            return view
        view.update({
            'view_type': 'form',
            'view_mode': 'tree,form',
        })
        return view

    # ----------------------------------------------
    #  OTHER BUTTONS
    # ----------------------------------------------

    def btn_show_task(self):
        return {
            'name': 'Task',
            'type': 'ir.actions.act_window',
            'res_model': 'project.task',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('project.view_task_form2').id,
            'res_id': self.id,
            'target': 'current',
        }
