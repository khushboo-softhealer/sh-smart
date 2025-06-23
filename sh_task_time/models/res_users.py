# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_
from odoo.http import request

class User(models.Model):
    _inherit = 'res.users'
    
    task_id = fields.Many2one('project.task', copy=False)
    start_time = fields.Datetime("Start Time", copy=False)
    end_time = fields.Datetime("End Time", copy=False)
    
    support_task_id = fields.Many2one('project.task', copy=False)
    support_start_time = fields.Datetime("Support Start Time", copy=False)
    support_end_time = fields.Datetime("Support End Time", copy=False)
    support_hours = fields.Float("Total Support Hours")

    # new_changes
    account_analytic_id=fields.Many2one('account.analytic.line','Timesheet Id')
    active_running_task_id=fields.Many2one('sh.pause.task.entry','Active Running Task Info')
    task_running_ids=fields.One2many('sh.pause.task.entry','user_id',string='Total Running Tasks')


    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + ['task_id','support_task_id']

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + ['task_id','support_task_id']



class Http(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        info = super().session_info()
        user = request.env.user
        info["task_id"] = user.task_id.id
        info["support_task_id"] = user.support_task_id.id
        return info
