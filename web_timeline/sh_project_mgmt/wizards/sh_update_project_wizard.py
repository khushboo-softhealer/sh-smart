# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, api
from odoo.exceptions import ValidationError

class ShUpdateProjectWizard(models.TransientModel):
    _name = "sh.update.project.wizard"
    _description = "Update Project Wizard"

    project_id = fields.Many2one("project.project", string='Project')
    stage_id = fields.Many2one('project.project.stage',string='Stage')
    # stage_id = fields.Many2one('project.project.stage',string='Stage', domain="[('id','in',project_id.sh_project_stage_ids.ids)]")
    sh_project_stage_ids = fields.Many2many('project.project.stage',related='project_id.sh_project_stage_ids')
    end_date = fields.Date()
    
    name = fields.Char(string="Name")
    tag_ids = fields.Many2many("project.tags",string="Tags")
    default_task_user_ids = fields.Many2many('res.users',string="Default Task Users", domain=[('share','=',False)])
    support_start_date = fields.Date("Support Start Date")
    support_end_date = fields.Date("Support End Date")
    # sale_estimation_line = fields.Many2many('sh.sale.line.estimation.template.line',string="Sale Estimation Line")
    sale_line_estimation_line = fields.Many2many('sh.sale.line.estimation.template.line','rel_sale_line_estimation_wizard_line','wizard_id','template_line_id',string="Sale Estimation Line"
)

    def update_project(self):
        print(f"\n\n\n\t--------------> 26 self.env.context",self.env.context)
        vals = {}
        if self.stage_id:
            vals.update({'stage_id' : self.stage_id.id})
        
        if self.end_date:
            if self.project_id.date_start and self.end_date < self.project_id.date_start:
                raise ValidationError(f"Project End Date must be greater than Start Date ({self.project_id.date_start})")
            vals.update({'date' : self.end_date})
        if vals:
            self.project_id.sudo().write(vals)

    
