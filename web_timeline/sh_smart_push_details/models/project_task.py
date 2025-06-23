# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import models, fields, api

class ProjectTask(models.Model):
    _inherit = 'project.task'

        
    sh_push_to_main_date = fields.Date('Push to main')
    sh_push_modules_ids = fields.Many2many(string='Modules Tech Name ',comodel_name='sh.push.module')
    sh_is_testing = fields.Boolean(related='stage_id.sh_is_testing')
    is_required_in_testing_stage = fields.Boolean(compute="_compute_is_required_in_testing_stage")
    
    @api.depends('stage_id')
    def _compute_is_required_in_testing_stage(self):
        for rec in self:
            rec.is_required_in_testing_stage = False
            if rec.sh_is_testing and rec.project_id.id != rec.env.user.company_id.appstore_project_id.id:
                rec.is_required_in_testing_stage = True
    
    