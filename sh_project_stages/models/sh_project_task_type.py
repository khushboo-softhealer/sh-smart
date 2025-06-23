# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _


class sh_project_task_type(models.Model):
    _inherit = 'project.task.type'

    # default_add_new_project = fields.Boolean(string="Default Add New Project")
    # test = fields.Char(string="Test")

    def action_mass_stage_update(self):
        return {
            'name':
            'Mass Update',
            'res_model':
            'sh.stage.project.mass.update.wizard',
            'view_mode':
            'form',
            'context': {
                'default_project_task_ids':
                [(6, 0, self.env.context.get('active_ids'))]
            },
            'view_id':
            self.env.ref(
                'sh_project_stages.sh_stage_project_update_wizard_form_view').
            id,
            'target':
            'new',
            'type':
            'ir.actions.act_window'
        }
