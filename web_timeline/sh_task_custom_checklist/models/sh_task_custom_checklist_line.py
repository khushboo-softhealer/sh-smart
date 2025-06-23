# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models, api
from datetime import datetime


class TaskCustomChecklistLine(models.Model):
    _name = "task.custom.checklist.line"
    _description = 'Task Custom Checklist Line'
    # _rec_name = 'sh_name'

    sh_name = fields.Char('Name')
    # name = fields.Many2one(
    #     'task.custom.checklist', string='Checklist')
    name = fields.Char('Checklist')
    task_custom_checklist_id = fields.Many2one(
        'task.custom.checklist', string='Checklist ')
    description = fields.Char('Description')
    updated_date = fields.Date(
        "Date", readonly=True, default=datetime.now().date())
    state = fields.Selection([
        ('new', 'New'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='new', readonly=True, index=True, string='State ')
    state_id = fields.Many2one(
        'sh.checklist.state', string='State', default=lambda x: x.get_new_state_id())
    state_updated_by = fields.Many2one('res.users', string='State Updated By')
    active = fields.Boolean('Active', default=True)

    def get_new_state_id(self):
        check_list_state = self.env['sh.checklist.state'].search([
            ('is_default_state', '=', True)
        ], limit=1)
        if check_list_state:
            return check_list_state.id
        return False

    task_id = fields.Many2one("project.task", string='Task')
    comments = fields.Char('Comments')
    pt_checklist_line_id = fields.Many2one(
        'sh.project.task.checklist.line', string='Project Task Checklist Line Ref')
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note"),
    ], default=False, string='Display Type')

    # def btn_check(self):
    #     self.write({
    #         'state': 'completed',
    #         'state_id':
    #     })

    # def btn_close(self):
    #     self.write({
    #         'state': 'cancelled'
    #     })

    @api.onchange('task_custom_checklist_id')
    def onchange_custom_chacklist_name(self):
        if self.task_custom_checklist_id:
            self.description = self.task_custom_checklist_id.description
            if not self.name:
                self.name = self.task_custom_checklist_id.name

    def write(self, vals):
        status = super(TaskCustomChecklistLine, self).write(vals)
        if 'state_id' in vals:
           self.state_updated_by = self.env.user.id
        return status