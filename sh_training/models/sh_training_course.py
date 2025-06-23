# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields


class ShTraining(models.Model):
    _name = 'sh.training.course'
    _description = 'Softhealer Training Details'

    name = fields.Char(string='Name', required=True)
    responsible_user_ids = fields.Many2many('res.users',
                                            string='Responsible Users',
                                            domain=[('share', '=', False)])
    pre_define_task_ids = fields.One2many(
        'pre.define.task.line', 'sh_course_id', string='Predefine Task')
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.company)
    def open_create_task_wizard(self):
        return {
            'name': 'Generate Task',
            'res_model': 'sh.generate.task.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('sh_training.view_sh_generate_task_wizard_form_view').id,
            'target': 'new',
            'type': 'ir.actions.act_window'
        }

    def action_check(self):
        if self.pre_define_task_ids:
            for line in self.pre_define_task_ids:
                line.tick = True

    def action_uncheck(self):
        if self.pre_define_task_ids:
            for line in self.pre_define_task_ids:
                line.tick = False
