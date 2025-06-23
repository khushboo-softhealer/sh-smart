# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import _, api, fields, models
from odoo.exceptions import UserError

class ShProjectWizard(models.Model):
    _name = "sh.project.create.wizard"
    _description = "Project Create Wizard"

    name = fields.Char("Name",required=True)
    description = fields.Html(help="Description to provide more information and context about this project")
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    partner_id = fields.Many2one('res.partner',string="Customer", domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    tags = fields.Many2many('project.tags',string="Tags")
    parent_project_id = fields.Many2one('project.project',string="Parent Project")
    default_task_user_ids = fields.Many2many("res.users",relation="rel_res_users_project_wizard_task_user", column1='project_id', column2='user_id',domain=[('share', '=', False)])
    responsible_user_ids = fields.Many2many("res.users",relation="rel_res_users_project_wizard_responsible_user", column1='project_id', column2='user_id',domain=[('share', '=', False)])
    project_type = fields.Selection([('internal','Internal'),('external','External')], string="Project Type",required=True)
    send_email = fields.Boolean(string="Send Email")
    user_id = fields.Many2one('res.users',string="Project Manager",default=lambda self: self.env.user,readonly=True)
    technical_head = fields.Many2one('res.users',string="Technical Head")
    start_date = fields.Date(string="Start Date",required=True)
    end_date = fields.Date(string="Expiration Date",required=True)
    allocated_hours = fields.Float(string="Allocated Hours",required=True)
    odoo_version = fields.Many2one('sh.version',string="Version")
    edition_id = fields.Many2one('sh.edition',string="Edition")
    pricing_mode = fields.Selection([('fp','FP - Fixed Price'),('tm','T&M - Time and Material')])
    sh_fp_based_on = fields.Selection([
        ('no_milestone', 'No Milestone - One shot'),
        ('milestone', 'Implementation Project'),
    ], string='FP Based On')
    sh_tm_based_on = fields.Selection([
            ('success_pack', 'Success Packs Based'),
            ('billable', 'Billable Hours Based'),
        ], string='T&M Based On',
        help='Success Packs Based (Renewable required based on usage) - SO\nBillable Hours Based (Monthly billable invoice created) - MANUALLY'
    )
    sh_send_timesheet = fields.Selection([('yes','Yes'),('no','No')],string="Send Timesheet")

    create_task_to_app_store = fields.Boolean(string="Create Task To PreApp Store")
    stage_template_id = fields.Many2one('sh.project.stage.template',string="Stage Template")
    stage_ids = fields.Many2many('project.task.type',string="Stages") 
    project_stage_template_id = fields.Many2one('sh.project.project.stage.template',string="project Stage Template")
    project_estimation_line = fields.One2many('sh.project.wizard.estimation.line','project_wizard_id')
    
    @api.constrains('project_estimation_line')
    def _check_project_estimation_line(self):
        for rec in self:
            if not rec.project_estimation_line:
                raise UserError("Estimation Template Lines required.")
            
    
    
    @api.model
    def default_get(self, fields):
        res = super(ShProjectWizard, self).default_get(fields)
        if self.env.user.company_id.project_stage_template_id:
            res['stage_template_id'] = self.env.user.company_id.project_stage_template_id.id
        return res
    
    @api.onchange('stage_template_id')
    def _onchange_stage(self):
        self.stage_ids = [(6, 0, self.stage_template_id.stage_ids.ids)]

    def create_project(self):
        dict_vals = {}
        values = []
        if self :

            if self.project_estimation_line:
                vals = {}

                for line in self.project_estimation_line:
                    vals = {'department_id':line.department_id.id,
                            'estimated_hours':line.estimated_hours,
                            'accountable_user_ids':line.accountable_users_ids.ids,
                            'responsible_user_ids':line.responsible_user_ids.ids,
                            'other_details':line.other_details}
                    values.append((0,0,vals))

            dict_vals = {'name':self.name,
                    'description':self.description,
                    'partner_id':self.partner_id.id,
                    'tag_ids':self.tags.ids,
                    'sh_parent_id':self.parent_project_id.id,
                    'default_task_users_ids':self.default_task_user_ids.ids,
                    'responsible_user_ids':self.responsible_user_ids.ids,
                    'project_type_selection':self.project_type,
                    'sh_send_email':self.send_email,
                    'company_id':self.company_id.id,
                    'user_id':self.project_manager.id,
                    'sh_technical_head':self.responsible_user_id.id,
                    'sh_designing_head':self.sh_designing_head.id,
                    'date_start':self.start_date,
                    'date':self.end_date,
                    'allocated_hours':self.allocated_hours,
                    'odoo_version':self.odoo_version.id,
                    'sh_edition_id':self.edition_id.id,
                    'sh_pricing_mode':self.pricing_mode,
                    'sh_fp_based_on':self.sh_fp_based_on,
                    'sh_tm_based_on':self.sh_tm_based_on,
                    'sh_send_timesheet':self.sh_send_timesheet,
                    'sh_move_task_to_preapp_store':self.create_task_to_app_store,
                    'sh_stage_template_id':self.stage_template_id.id,
                    'sh_stage_ids':self.stage_ids.ids,
                    'sh_project_stage_tmpl_id':self.project_stage_template_id.id,
                    'sale_line_estimation_template_line':values,
                    }
            
            if dict_vals:
                self.env['project.project'].sudo().create(dict_vals)



class ShProjectWizardEstimationLine(models.Model):
    _name = 'sh.project.wizard.estimation.line'
    _description = "Sh Project Wizard Estimation Line"

    department_id = fields.Many2one('hr.department',string="Department")
    estimated_hours = fields.Float(string="Estimation Hours")
    accountable_users_ids = fields.Many2many('res.users',string="Accountable(S)",relation="rel_res_users_accountable_table", column1='project_wizard_id', column2='users_id') 
    responsible_user_ids = fields.Many2many('res.users',string="Responsible(S)",relation="rel_res_users_responsible_table", column1='project_wizard_id', column2='users_id') 
    other_details = fields.Text(string="Other Details")

    project_wizard_id = fields.Many2one('sh.project.create.wizard')
