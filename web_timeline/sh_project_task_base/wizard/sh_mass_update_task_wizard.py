# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models


class UpdatemassTag(models.TransientModel):
    _name = "sh.mass.update.task.wizard"
    _description = "Task Mass Update Wizard"

    task_ids = fields.Many2many('project.task', string='Tasks')
    assignees_update_method = fields.Selection([
        ("add", "Add"),
        ("remove", "Remove"),
        ("replace", "Replace"),
    ], string='Assignees Update Method')
    user_ids = fields.Many2many(
        'res.users', string="Assidnees", domain=[('share', '=', False)])
    tag_update_method = fields.Selection([
        ("add", "Add"),
        ("replace", "Replace"),
    ], string='Tag Update Method')
    project_tags_ids = fields.Many2many('project.tags', string="Tags")
    deadline = fields.Date('Deadline')
    stage_id = fields.Many2one("project.task.type", string="Stage")
    tl_id = fields.Many2one('res.users', string='TL Id', domain=[('share', '=', False)])
    dev_id = fields.Many2one('res.users', string='Developer', domain=[('share', '=', False)])
    support_dev_id = fields.Many2one('res.users', string='Support Developer', domain=[('share', '=', False)])
    tester_id = fields.Many2one('res.users', string='Tester', domain=[('share', '=', False)])
    designer_id = fields.Many2one('res.users', string='Designer', domain=[('share', '=', False)])
    index_by_id = fields.Many2one('res.users', string='Index By', domain=[('share', '=', False)])
    market_by_id = fields.Many2one('res.users', string='Market By', domain=[('share', '=', False)])

    def btn_mass_update_task(self):
        if not self.task_ids:
            return
        task_vals = {}

        if self.assignees_update_method and self.user_ids:
            responsible_user_list = []
            if self.assignees_update_method == 'add':
                for user in self.user_ids:
                    responsible_user_list.append((4, user.id))
            elif self.assignees_update_method == 'remove':
                for user in self.user_ids:
                    responsible_user_list.append((3, user.id))
            elif self.assignees_update_method == 'replace':
                responsible_user_list = [(6, 0, self.user_ids.ids)]
            if responsible_user_list:
                task_vals['user_ids'] = responsible_user_list

        if self.tag_update_method and self.project_tags_ids:
            tag_list = []
            if self.tag_update_method == 'add':
                for tag in self.project_tags_ids:
                    tag_list.append((4, tag.id))
            elif self.tag_update_method == 'replace':
                tag_list = [(6, 0, self.project_tags_ids.ids)]
            if tag_list:
                task_vals['tag_ids'] = tag_list

        if self.deadline:
            task_vals['date_deadline'] = self.deadline
        if self.stage_id:
            task_vals['stage_id'] = self.stage_id.id
        if self.tl_id:
            task_vals['sh_project_task_base_responsible_tl_id'] = self.tl_id.id
        if self.dev_id:
            task_vals['sh_project_task_base_dev_id'] = self.dev_id.id
        if self.support_dev_id:
            task_vals['sh_project_task_base_support_dev_id'] = self.support_dev_id.id
        if self.tester_id:
            task_vals['sh_project_task_base_tester_id'] = self.tester_id.id
        if self.designer_id:
            task_vals['sh_project_task_base_designer_id'] = self.designer_id.id
        if self.index_by_id:
            task_vals['sh_project_task_base_index_by_id'] = self.index_by_id.id
        if self.market_by_id:
            task_vals['sh_project_task_base_marketed_by_id'] = self.market_by_id.id

        if task_vals:
            for task in self.task_ids:
                task.sudo().write(task_vals)
