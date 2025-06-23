# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models, api


class TaskCustomChecklist(models.Model):
    _name = "sh.project.task.checklist.line"
    _description = 'Project Task Checklist'
    # _rec_name = 'sh_project_task_checklist_id'

    name = fields.Char('Name', compute='_compute_name')
    # Inverse Field
    sh_project_task_checklist_id = fields.Many2one(
        'sh.project.task.checklist', string='Project Task Checklist Ref')
    from_wich_state_id = fields.Many2one(
        'project.task.type', string='From Which State')
    at_which_state_ids = fields.Many2many(
        'project.task.type', string='At Which State')
    checklist_template_ids = fields.Many2many(
        'sh.task.checklist.template', string='Checklist Templates')
    checklist_ids = fields.Many2many(
        'task.custom.checklist', string='Checklists')

    @api.depends('checklist_template_ids')
    def _compute_name(self):
        for rec in self:
            rec.name = 'Templates'
            if rec.checklist_template_ids:
                tmpl_name_list = []
                for tmpl in rec.checklist_template_ids:
                    tmpl_name_list.append(tmpl.name)
                if tmpl_name_list:
                    rec.name = ' | '.join(tmpl_name_list)

    @api.onchange('checklist_template_ids')
    def _onchange_checklist_template_ids(self):
        self.ensure_one()
        if self.checklist_template_ids:
            checklist_list = []
            for checklist_template in self.checklist_template_ids:
                if checklist_template.checklist_ids:
                    for checklist in checklist_template.checklist_ids:
                        # if checklist.id not in self.checklist_ids.ids:
                        #     checklist_list.append((4, checklist.id))
                        checklist_list.append(checklist.id)
            if checklist_list:
                # self.checklist_ids = checklist_list
                self.checklist_ids = [(6, 0, checklist_list)]
        else:
            self.checklist_ids = False
