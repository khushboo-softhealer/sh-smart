# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, api
from datetime import datetime


class ShBugStateLog(models.Model):
    _name = 'sh.bug.state.log'
    _description = 'Module Bug'
    _rec_name = 'sh_bug_module_id'

    # Inverse Field
    sh_bug_module_id = fields.Many2one('sh.module.bug', string='Bug')
    state_id = fields.Many2one('sh.bug.state', string='State')
    date_in = fields.Datetime(string='Date In')
    date_in_by = fields.Many2one('res.users', string='Date In By')
    date_out = fields.Datetime(string='Date Out')
    date_out_by = fields.Many2one('res.users', string='Date Out By')
    day_diff = fields.Integer(string='Day Diff')
    time_diff = fields.Float(string='Time Diff')
    total_time_diff = fields.Float(string='Total Time Diff')
