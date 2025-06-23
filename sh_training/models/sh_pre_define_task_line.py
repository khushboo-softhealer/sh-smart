# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields


class PredefineTasks(models.Model):
    _name = 'pre.define.task.line'
    _description = 'Pre Define Task Details'
    _order = "sequence, name, id"

    tick = fields.Boolean()
    name = fields.Char(string='Name', required=True)

    description = fields.Html(string='Description')
    sequence = fields.Integer(string='Sequence', default=1)

    sh_course_id = fields.Many2one(
        'sh.training.course', string='Training Record')

    def btn_tick_untick(self):
        if self.tick == True:
            self.tick = False
        else:
            self.tick = True
