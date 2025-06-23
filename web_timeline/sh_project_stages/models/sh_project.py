# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _

class UpdatemassStage(models.TransientModel):

    _name = "sh.stage.project.mass.update.wizard"
    _description = "Mass Update Wizard"

    project_task_ids = fields.Many2many('project.task.type', string="Stages")
    update_project_bool = fields.Boolean(string="Update Project")
    update_project_ids = fields.Many2many('project.project', string='Project')
    update_method_project = fields.Selection([
        ("add", "Add"),
        ("replace", "Replace"),
    ],
        default="add")

    def update_record(self):
        if self.update_method_project == 'add':
            for i in self.update_project_ids:
                self.project_task_ids.write({'project_ids': [(4, i.id)]})

        if self.update_method_project == 'replace':
            self.project_task_ids.write(
                {'project_ids': [(6, 0, self.update_project_ids.ids)]})

class sh_project_project(models.Model):
    _name = 'project.project'
    _inherit = ['project.project','mail.thread','mail.activity.mixin']

    @api.model
    def default_get(self, fields):
        res = super(sh_project_project, self).default_get(fields)
        if self.env.user.company_id.project_stage_template_id:
            res['sh_stage_template_id'] = self.env.user.company_id.project_stage_template_id.id

        return res

    @api.onchange('sh_stage_template_id')
    def _onchange_stage(self):
        self.sh_stage_ids = [(6, 0, self.sh_stage_template_id.stage_ids.ids)]

    @api.model_create_multi
    def create(self, values):
        res = super(sh_project_project, self).create(values)
        domain = [('default_add_new_project', '=', True)]
        stages = self.env['project.task.type'].search(domain)
        res.sh_stage_ids = stages.ids
        return res

    def action_mass_stage_update(self):
        return {
            'name':
            'Mass Update',
            'res_model':
            'sh.project.stage.mass.update.wizard',
            'view_mode':
            'form',
            'context': {
                'default_project_project_ids':
                [(6, 0, self.env.context.get('active_ids'))]
            },
            'view_id':
            self.env.ref(
                'sh_project_stages.sh_project_stage_update_wizard_form_view').
            id,
            'target':
            'new',
            'type':
            'ir.actions.act_window'
        }
