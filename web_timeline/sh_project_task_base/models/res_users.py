# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields

class User(models.Model):
    _inherit = 'res.users'

    task_id = fields.Many2one('project.task', copy=False)
    start_time = fields.Datetime("Start Time", copy=False)
    end_time = fields.Datetime("End Time", copy=False)

    support_task_id = fields.Many2one('project.task', copy=False)
    support_start_time = fields.Datetime("Support Start Time", copy=False)
    support_end_time = fields.Datetime("Support End Time", copy=False)
    support_hours = fields.Float("Total Support Hours")
