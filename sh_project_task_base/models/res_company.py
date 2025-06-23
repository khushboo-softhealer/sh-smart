# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, api, _


class ResCompany(models.Model):
    _inherit = 'res.company'
    
    # For Project Stages
    close_project_stage_ids = fields.Many2many('project.project.stage', string="Close Project Stages")
    auto_close_project_stage_id = fields.Many2one('project.project.stage', string="Auto Close Project Stage")
    project_stage_template_id = fields.Many2one('sh.project.stage.template')
    
    # For Task Stages
    to_be_project_stage_id = fields.Many2one('project.task.type', string="To Be Task Stage")
    done_project_stage_id = fields.Many2one('project.task.type', string="Done Task Stage")
    developement_project_stage_id = fields.Many2one('project.task.type', string="Development Task Stage")
    timesheet_restricted_task_stage_ids = fields.Many2many(
        'project.task.type', 
        'sh_task_stage_company_rel', 
        'task_stage_id',
        'company_id',
        string="Timesheet Restricted Task Stages")
    
    feature_project_stage_id = fields.Many2one('project.task.type', string="Feature Project Stage")
    sh_under_review_task_stage_id = fields.Many2one('project.task.type', string='Under Reiview Task Stage')
    sh_tech_name_and_version_req_stage_ids = fields.Many2many(
        'project.task.type',
        'task_stage_company_rel',
        'task_stage_id',
        'company_id',
        string='Technical Name & Version Required At Stages',
        domain=[('sh_is_appstore_task_state', '=', True)]
    )
        
    sh_done_task_stage_id = fields.Many2one('project.task.type', string='Done Task Stage')

    appstore_project_id = fields.Many2one('project.project',string="Appstore Project")

    preappstore_project_id = fields.Many2one('project.project',string="PreAppstore Project")

    
    # == sh_autoinvoice_task_flow========
    project_id_created_from_so = fields.Many2one(
        'project.project', string="Project Created From SO")


    sh_pending_ss_id = fields.Many2one(
        'project.task.type',
        string='Pending Screenshot Auto Tick When Stage',
        domain=[('sh_is_appstore_task_state', '=', True)]
    )
