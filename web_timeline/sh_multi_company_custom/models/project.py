# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class Project(models.Model):
    _inherit = "project.project"

    @api.model_create_multi
    def create(self, vals_list):
        # Prevent double project creation
        projects = super().create(vals_list)

        for project in projects:
            if project.analytic_account_id.plan_id:
                project.analytic_account_id.plan_id.sudo().write({'company_id':False})
            project.analytic_account_id.sudo().write({'company_id':False})
        return projects
    
class ProjectTask(models.Model):
    _inherit = "project.task"


    project_id = fields.Many2one('project.project', string='Project', recursive=True,
        compute='_compute_project_id', store=True, readonly=False, precompute=True,
        index=True, tracking=True, check_company=False, change_default=True,domain="[]")

