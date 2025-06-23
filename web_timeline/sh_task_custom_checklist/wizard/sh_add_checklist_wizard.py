# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields


class ShAddChecklistWizard(models.TransientModel):
    _name = 'sh.add.checklist.wizard'
    _description = 'Add Checklist Wizard'

    pt_checklist_ids = fields.Many2many(
        'sh.project.task.checklist', string='Task Checklist Templates')
    task_ids = fields.Many2many('project.task', string='Tasks')

    def btn_add_checklists(self):
        message = self.task_ids._add_checklists_in_task(self.pt_checklist_ids)
        if not message:
            message = 'Failed to add or the task already have the checklists.'
        return self.env['project.task']._show_message(message)
