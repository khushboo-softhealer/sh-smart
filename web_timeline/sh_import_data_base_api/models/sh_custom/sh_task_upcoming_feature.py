# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ShTaskUpcomingFeature(models.Model):
    _inherit = 'sh.task.upcoming.feature'

    remote_sh_task_upcoming_feature_id = fields.Char("Remote Task Upcoming Feature ID",copy=False)
