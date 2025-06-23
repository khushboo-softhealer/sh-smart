# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, api, _


class ShProjectTask(models.Model):
    _inherit = 'project.task'

    batch_id = fields.Many2many(
        comodel_name='sh.training.batch', string='Batch')
    course_id = fields.Many2one(
        comodel_name='sh.training.course', string='Course')
    sh_training_rating = fields.Selection(string='Rating ', selection=[
        ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ], default='0')
    sh_training_comment = fields.Text(string='Comment')

    trainee = fields.Boolean(string='Trainee',
                             compute="_compute_trainee",
                             default=False)

    @api.depends('company_id')
    def _compute_trainee(self):
        if self.project_id.id == self.company_id.sh_training_project_id.id:
            self.trainee = True
        else:
            self.trainee = False

    @api.model
    def action_view_training_task(self):
        project_id = self.env.user.company_id.sh_training_project_id.id
        action = {
            'name': _('Tasks'),
            'view_mode': 'kanban,tree,form,calendar,pivot,graph,activity',
            'search_view_id': [self.env.ref('project.view_task_search_form').id],
            'res_model': 'project.task',
            'type': 'ir.actions.act_window',
            'domain': [('course_id', '!=', False), ('project_id', '=', project_id)],
            'help': """
                <p class="o_view_nocontent_smiling_face">
                Create a new task
            </p>
            <p> Odoo's project management allows you to manage the pipeline of your tasks
                efficiently. <br /> You can track progress, discuss on tasks, attach documents, etc. </p>
                """
        }
        return action
