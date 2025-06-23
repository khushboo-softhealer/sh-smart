# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields
from odoo.http import request

class Users(models.Model):
    _inherit = 'res.users'

    sh_display_timesheet = fields.Boolean('Display Timesheet at portal')
    sh_display_allocated_hours = fields.Boolean('Display Allocated Hours')
    sh_display_progress = fields.Boolean('Display Progress')
    sh_display_task_menu = fields.Boolean('Display Tasks Menu at portal')
    sh_display_milestone = fields.Boolean('Display Milestore in task')
    sh_display_assignees = fields.Boolean('Display Assignees in task')

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + ['sh_display_assignees','sh_display_milestone','sh_display_task_menu','sh_display_timesheet','sh_display_allocated_hours','sh_display_progress']

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + ['sh_display_assignees','sh_display_milestone','sh_display_task_menu','sh_display_timesheet','sh_display_allocated_hours','sh_display_progress']

class Http(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        info = super().session_info()
        user = request.env.user
        info["sh_display_timesheet"] = user.sh_display_timesheet
        info["sh_display_allocated_hours"] = user.sh_display_allocated_hours
        info["sh_display_progress"] = user.sh_display_progress
        info['sh_display_task_menu'] = user.sh_display_task_menu
        info["sh_display_assignees"] = user.sh_display_assignees
        info['sh_display_milestone'] = user.sh_display_milestone
        return info