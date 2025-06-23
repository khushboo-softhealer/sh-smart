# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields


class ShMigrationResCompany(models.Model):
    _inherit = 'res.company'

    sh_migration_bug_testing_state_id = fields.Many2one(
        'sh.bug.state', string='Bug Testing State')
    sh_migration_bug_complete_state_ids = fields.Many2many(
        'sh.bug.state', string='Bug Complete States')
    sh_migration_v17_version_id = fields.Many2one(
        'sh.version', string='Version Ref.')
    sh_migration_dashboard_stage_id = fields.Many2many(
        'project.task.type', string='Dashboard Stages')
    sh_migration_pendign_exclude_stage_id = fields.Many2many(
        'project.task.type', 'sh_migration_pendign_exclude_stage', string='Pending Exclude Stages')

    sh_migration_last_date = fields.Date(string='Migration Last Date')
    sh_is_migration_enabled = fields.Boolean("Is Migration Module Request Ignore")

    def write(self, vals):
        res = super(ShMigrationResCompany, self).write(vals)
        if 'sh_migration_v17_version_id' in vals:
            self.env['project.task'].sudo().search([
                ('project_id', '=', self.appstore_project_id.id)
            ])._compute_is_v17_task()
        return res
