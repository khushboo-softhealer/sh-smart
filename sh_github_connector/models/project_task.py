# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api


class ShProjectTaskGithub(models.Model):
    _inherit = "project.task"

    sh_is_appstore = fields.Boolean(
        "Is Appstore Project", compute="_compute_project_bool")
    sh_is_training = fields.Boolean(
        "Is Training Project", compute="_compute_project_bool")
    sh_is_parent_task = fields.Boolean(
        "Is Parent Task", compute="_compute_project_bool")

    def _compute_project_bool(self):
        for rec in self:
            rec.sh_is_appstore = False
            rec.sh_is_training = False
            rec.sh_is_parent_task = False
            # if rec.project_id.name == "App Store":
            if rec.project_id.id == rec.company_id.appstore_project_id.id:
                rec.sh_is_appstore = True
            # if rec.project_id.name == "Training":
            if rec.project_id.id == rec.company_id.sh_training_project_id.id:
                rec.sh_is_training = True
            if rec.child_ids and rec.project_id.id == rec.company_id.preappstore_project_id.id:
                rec.sh_is_parent_task = True

    # @api.model_create_multi
    # def create(self, vals_list):
    #     recs = super(ShProjectTaskGithub, self).sudo().create(vals_list)
    #     for rec in recs:
    #         if rec.parent_id:
    #             if rec.parent_id.sh_technical_name:
    #                 rec.sh_technical_name = rec.parent_id.sh_technical_name
    #     return recs

