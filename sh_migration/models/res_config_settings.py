# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields


class ShMigrationSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_migration_bug_testing_state_id = fields.Many2one(
        string='Bug Testing State', related='company_id.sh_migration_bug_testing_state_id', readonly=False)
    sh_migration_bug_complete_state_ids = fields.Many2many(
        string='Bug Complete States', related='company_id.sh_migration_bug_complete_state_ids', readonly=False)
    sh_migration_v17_version_id = fields.Many2one(
        string='Version Ref.', related='company_id.sh_migration_v17_version_id', readonly=False)
    sh_migration_dashboard_stage_id = fields.Many2many(
        'project.task.type', string='Dashboard Stages', related='company_id.sh_migration_dashboard_stage_id', readonly=False)
    sh_migration_pendign_exclude_stage_id = fields.Many2many('project.task.type', 'sh_migration_pendign_exclude_stage',
                                                             string='Pending Exclude Stages', related='company_id.sh_migration_pendign_exclude_stage_id', readonly=False)
    sh_migration_last_date = fields.Date(
        string='Migration Last Date', related='company_id.sh_migration_last_date', readonly=False)

    sh_is_migration_enabled = fields.Boolean(
        "Is Migration Module Request Ignore",
        related='company_id.sh_is_migration_enabled',
        readonly=False)
