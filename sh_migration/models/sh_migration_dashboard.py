# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
from datetime import datetime


class MigrationDashboard(models.Model):
    _name = 'sh.migrations.dashboard'
    _description = 'Migration Dashboard'

    name = fields.Char("")

    def get_migration_details(self):

        data = {}
        dashboard_stages=[]
        company_id=self.env['res.company'].sudo().browse(1)
        if company_id:
            dashboard_stages = company_id.sudo().sh_migration_dashboard_stage_id

        # total_product = self.env['product.template'].sudo(
        # ).search_count([('sh_technical_name', '!=', False)])

        total_product = self.env['project.task'].search_count([
            ('sh_migration_is_v17_task', '=', True),
            ('sh_migration_is_appstore_project_task', '=', True)
        ])

        # for days left count calculation
        today = datetime.now().date()
        final_day = self.env.company.sudo().sh_migration_last_date
        if final_day:
            delta = final_day - today
            days_left = delta.days
            data["Days' Left"] = days_left

        # for total module count
        data['Total'] = total_product

        # for pending count
        pending_exclude_stages = self.env.company.sudo(
        ).sh_migration_pendign_exclude_stage_id.ids
        pending_stage_count = self.env['project.task'].search_count([
            ('stage_id', 'not in', pending_exclude_stages),
            ('sh_migration_is_v17_task', '=', True),
            ('sh_migration_is_appstore_project_task', '=', True)
        ])
        data['Pending'] = pending_stage_count

        # for add stage and their counts calculations
        for stage in dashboard_stages:
            # stage_count = 0
            # stage_count = self.env['project.task'].search_count(
            #     [('stage_id', '=', stage.id), ('sh_migration_is_v17_task', '=', True)])
            data[stage.name] = self.env['project.task'].search_count([
                ('stage_id', '=', stage.id), 
                ('sh_migration_is_v17_task', '=', True),
                ('sh_migration_is_appstore_project_task', '=', True)
            ])

        # for pylint counts
        pylint_checked = 0
        pylint_less_eight = 0
        pylint_greater_eight = 0
        pylint_zero = 0

        pylint_checked = self.env['project.task'].search_count([
            ('pylint_score', '>', 0.00),
            ('sh_migration_is_v17_task', '=', True)
        ])
        pylint_less_eight = self.env['project.task'].search_count([
            ('pylint_score', '>', 0.00),
            ('pylint_score', '<', 8.00),
            ('sh_migration_is_v17_task', '=', True)
        ])
        pylint_greater_eight = self.env['project.task'].search_count([
            ('pylint_score', '>=', 8.00),
            ('sh_migration_is_v17_task', '=', True)
        ])
        pylint_zero = self.env['project.task'].search_count([
            ('pylint_score', '=', False),
            ('sh_migration_is_v17_task', '=', True)
        ])

        data['Pylint Checked'] = pylint_checked
        data['Pylint Greated 8'] = pylint_greater_eight
        data['Pylint Less 8'] = pylint_less_eight
        data['Pylint Zero'] = pylint_zero

        return data
