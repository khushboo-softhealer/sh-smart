# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields

class StageEmployee(models.Model):
    _name = 'sh.stage.employee'
    _description = "Stage Employee"

    sequence = fields.Integer(required=True)
    user_id = fields.Many2one('res.users', string="Employee")
    task_type_id = fields.Many2one('project.task.type')
    sh_task_type_id = fields.Many2one('project.task.type')
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.company)