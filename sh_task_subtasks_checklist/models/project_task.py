# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models, api


class SubTask(models.Model):
    _inherit = "project.task"

    sh_sub_task_lines = fields.One2many(
        "project.task", "parent_id", "Sub Task")
    stage_done = fields.Boolean("done", related="stage_id.sh_done")
    stage_cancel = fields.Boolean("cancel", related="stage_id.sh_cancel")
    stage_draft = fields.Boolean("draft", related="stage_id.sh_draft")

    def action_subtask(self):
        action = self.env.ref('project.project_task_action_sub_task').read()[0]
        ctx = self.env.context.copy()
        ctx.update({
            'default_parent_id': self.id,
            'default_project_id': self.env.context.get('project_id', self.project_id.id),
            'default_name': self.env.context.get('name', self.name) + ':',
            'default_partner_id': self.env.context.get('partner_id', self.partner_id.id),
            'search_default_project_id': self.env.context.get('project_id', self.project_id.id),
            'search_default_parent_only': 0,
            'default_date_deadline': self.date_deadline,
            'default_description': self.description,
            'default_user_ids': [(6, 0, self.user_ids.ids)],
            'default_tag_ids': [(6, 0, self.tag_ids.ids)],
        })
        action['context'] = ctx
        action['domain'] = [('id', 'child_of', self.id), ('id', '!=', self.id)]
        return action

    def write(self, vals):
        res1 = super(SubTask, self).write(vals)
        for res in self:
            for rec in res.sh_sub_task_lines:
                if res.stage_id.sh_cancel:
                    rec.stage_id = res.stage_id.id
        return res1

    def action_check(self):
        if self.stage_id.sh_done != True:
            done_id = self.env['project.task.type'].search(
                [('sh_done', '=', True)], limit=1)
            self.write({'stage_id': done_id.id})

    def action_cancel(self):
        if self.stage_id.sh_cancel != True:
            cancel_id = self.env['project.task.type'].search(
                [('sh_cancel', '=', True)], limit=1)
            self.write({'stage_id': cancel_id.id})

    def action_draft(self):
        if self.stage_id.sh_draft != True:
            draft_id = self.env['project.task.type'].search(
                [('sh_draft', '=', True)], limit=1)
            self.write({'stage_id': draft_id.id})

    @api.depends('sh_sub_task_lines')
    def _compute_custom_checklist(self):

        done_id = self.env['project.task.type'].search(
            [('sh_done', '=', True)], limit=1)
        total_cnt = self.search_count([('parent_id', '=', self.id)])
        compl_cnt = self.search_count(
            [('parent_id', '=', self.id), ('stage_id', '=', done_id.id)])

        if total_cnt > 0:
            self.custom_checklist = (100.0 * compl_cnt) / total_cnt
        else:
            self.custom_checklist = 0

    custom_checklist = fields.Float(
        "Checklist Completed", compute="_compute_custom_checklist", digits=(12, 0))
