# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ShGenerateTaskWizard(models.TransientModel):
    _name = 'sh.generate.task.wizard'
    _description = 'Generate Task Wizard Details'

    trainee_ids = fields.Many2many('res.users',
                                   string="Trainee",
                                   domain=[('share', '=', False)])
    training_batch_ids = fields.Many2many(
        'sh.training.batch', string="Training Batch")
    predefined_task_ids = fields.Many2many(
        comodel_name='pre.define.task.line', string='Predefined Task')

    course_id = fields.Many2one(
        comodel_name='sh.training.course', string='Course')

    @api.onchange('training_batch_ids')
    def onchange_training_batch(self):
        if self.training_batch_ids.mapped('sh_trainee_ids').ids:
            self.trainee_ids = [
                (6, 0, self.training_batch_ids.mapped('sh_trainee_ids').ids)]
        else:
            self.trainee_ids = False

    def create_task_action(self):
        if not self.env.user.company_id.sh_training_project_id:
            raise UserError(
                "Please select training project in project -> configuration -> setting")

        if not self.trainee_ids:
            raise UserError(
                "Please select trainee for which this task will be generate (Please check course batch)")

        if not self.predefined_task_ids:
            raise UserError(
                "Please select task")

        course = self.env.context.get('active_id', False)

        if not course:
            raise UserError(
                "Wizard method executed without active_id in context")

        course = self.env['sh.training.course'].browse(
            self.env.context.get('active_id'))
        project_name = self.env.user.company_id.sh_training_project_id
        list_responsible_user_list = course.responsible_user_ids.ids if course.responsible_user_ids else []

        user_ids = list_responsible_user_list + self.trainee_ids.ids + self.env.user.ids
        for predefined in self.predefined_task_ids:
            self.env["project.task"].create({
                "name":  predefined.name,
                "user_ids": [(6, 0, user_ids)],
                "project_id": project_name.id,
                "description": predefined.description,
                "course_id": course.id,
                "estimated_hrs" : 1,
                "batch_id": [(6, 0, self.training_batch_ids.ids)],
            })
        
        return {
            'name': 'Tasks',
            'type': 'ir.actions.act_window',
            'res_model': 'project.task',
            'view_mode': 'tree,form',
            'target': 'current',
        }

    @api.model
    def default_get(self, fields):
        res = super(ShGenerateTaskWizard, self).default_get(fields)

        course = self.env.context.get('active_id', False)

        if not course:
            raise UserError(
                "Wizard method executed without active_id in context")

        course = self.env['sh.training.course'].browse(
            self.env.context.get('active_id'))

        ticked = self.env['pre.define.task.line'].search(
            [('tick', '=', True), ('sh_course_id', "=", course.id)])

        res.update({
            'course_id': course.id if course else False,
        })

        if ticked:
            res.update({
                'predefined_task_ids': [(6, 0, ticked.ids)],
                'course_id': course.id,
            })
        return res
