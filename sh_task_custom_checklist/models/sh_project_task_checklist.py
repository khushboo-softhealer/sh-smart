# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models


class TaskCustomChecklist(models.Model):
    _name = "sh.project.task.checklist"
    _description = 'Project Task Checklist'

    name = fields.Char('Name')
    project_ids = fields.Many2many('project.project', string='Projects')
    sh_project_task_checklist_line = fields.One2many(
        'sh.project.task.checklist.line', 'sh_project_task_checklist_id', string='Required Checklist')
