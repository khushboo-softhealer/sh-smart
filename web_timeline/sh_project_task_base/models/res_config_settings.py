# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models


class res_config_settings(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_website_prod_price_label_label = fields.Char(related='website_id.sh_website_prod_price_label_label', 
                                                  string = "Product Prices Label",
                                                  help = "This label will visible after product price. eg - $10(Ex-VAT)", 
                                                  readonly=False)


    category_style = fields.Selection(related="website_id.category_style",string="Category Style",readonly=False)
    category_header_style = fields.Selection(default='style1',related="website_id.category_header_style",string="Category Header Style",readonly=False)

    sub_category_style = fields.Selection(related="website_id.sub_category_style",string="Subcategory Style",readonly=False)


    # For Project Stages
    close_project_stage_ids = fields.Many2many('project.project.stage', string="Close Project Stage", readonly=False, related='company_id.close_project_stage_ids')
    auto_close_project_stage_id = fields.Many2one('project.project.stage', string="Auto Close Project Stage", readonly=False, related='company_id.auto_close_project_stage_id')    
    project_stage_template_id = fields.Many2one(related="company_id.project_stage_template_id",string="Template ",readonly=False)
    
    # For Task Stages
    to_be_project_stage_id = fields.Many2one('project.task.type', string="To Be Project Task Stage", readonly=False, related='company_id.to_be_project_stage_id')
    done_project_stage_id = fields.Many2one('project.task.type', string="Done Task Stage", readonly=False, related='company_id.done_project_stage_id')
    developement_project_stage_id = fields.Many2one('project.task.type', string="Developement Task Stage", readonly=False, related='company_id.developement_project_stage_id')
    timesheet_restricted_task_stage_ids = fields.Many2many('project.task.type', string="Timesheet Restricted Task Stages", readonly=False, related='company_id.timesheet_restricted_task_stage_ids')

    # ========================================
    # ============ TAKS TIME FIELDS ==========
    # ========================================

    appstore_project_id = fields.Many2one(
        'project.project',
        related="company_id.appstore_project_id",
        string="Appstore Project",
        readonly=False)
    feature_project_stage_id = fields.Many2one('project.task.type', string="Feature Project Stage", readonly=False, related='company_id.feature_project_stage_id')
    preappstore_project_id = fields.Many2one(
        'project.project',
        related="company_id.preappstore_project_id",
        string="PreAppstore Project",
        readonly=False)

    sh_under_review_task_stage_id = fields.Many2one('project.task.type', related='company_id.sh_under_review_task_stage_id', string='Under Reiview Task Stage', readonly=False,)

    sh_done_task_stage_id = fields.Many2one('project.task.type', string='Done Task Stage', readonly=False, related='company_id.sh_done_task_stage_id')

    # == sh_autoinvoice_task_flow========

    project_id_created_from_so = fields.Many2one(
        related="company_id.project_id_created_from_so",
        string="Project Created From SO",
        readonly=False)

    sh_tech_name_and_version_req_stage_ids = fields.Many2many(
        string='Technical Name & Version Required At Stages',
        related="company_id.sh_tech_name_and_version_req_stage_ids",
        readonly=False,
        domain=[('sh_is_appstore_task_state', '=', True)]
    )

    sh_pending_ss_id = fields.Many2one(
        string='Pending Screenshot Auto Tick When Stage',
        related="company_id.sh_pending_ss_id",
        readonly=False,
        domain=[('sh_is_appstore_task_state', '=', True)]
    )

    def update_old_task(self):
        tasks = self.env['project.task'].sudo().search([('estimated_hrs','>',0.0),'|',('estimated_internal_hrs','=',False),('estimated_internal_hrs','=',0.0)])
        if tasks:
            for task in tasks:
                task.sudo().write({'estimated_internal_hrs':task.estimated_hrs})

    