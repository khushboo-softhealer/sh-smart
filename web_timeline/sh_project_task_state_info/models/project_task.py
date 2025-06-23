# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

import datetime
from odoo import fields, models, _, api


class ProjectTaskInherit(models.Model):
    _inherit = "project.task"

    stage_history_line = fields.One2many(
        "sh.project.task.info", 'stage_task_id', string="Stage History Line", readonly="True")

    @api.model_create_multi
    def create(self, vals_list):
        recs = super(ProjectTaskInherit, self).create(vals_list)
        for rec in recs:
            # When new task created, stage line added
            # if vals.get('stage_id'):
            if rec.stage_id:
                if not rec.stage_history_line:
                    # for new record====================
                    stage_history = {
                        'stage_task_id': rec.id,
                        'stage_name': rec.stage_id.name,
                        'date_in': datetime.datetime.now(),
                        'date_in_by': self.env.user.id,
                    }
                    rec.stage_history_line = [(0, 0, stage_history)]
        return recs

    def write(self, vals):
        res = super(ProjectTaskInherit, self).write(vals)
        if vals.get('stage_id'):
            # for update record=====================
            last_create_id = self.stage_history_line.ids
            if last_create_id:
                previous_id = self.env['sh.project.task.info'].browse(
                    last_create_id[-1])
                sub_time = datetime.datetime.now() - previous_id.date_in

                # for days difference
                day_diff = sub_time.days

                # for hours difference
                test = str(sub_time.seconds//3600) + ':' + \
                    str(((sub_time.seconds//60) % 60))
                vals = test.split(':')
                time, hours = divmod(float(vals[0]), 24)
                time, minutes = divmod(float(vals[1]), 60)
                minutes = minutes / 60.0
                time_to_fl = hours + minutes

                # for total time count
                if day_diff > 0:
                    test = str(sub_time.seconds//3600) + ':' + \
                        str(((sub_time.seconds//60) % 60))
                    vals = test.split(':')
                    time, hours = divmod(float(vals[0]), 24)
                    time, minutes = divmod(float(vals[1]), 60)
                    minutes = minutes / 60.0
                    hours += day_diff*24
                    total_time_to_fl = hours + minutes
                else:
                    total_time_to_fl = time_to_fl

                stage_history = {
                    'date_out':  datetime.datetime.now(),
                    'date_out_by': self.env.user,
                    'day_diff': day_diff,
                    'time_diff': time_to_fl,
                    'total_time_diff': total_time_to_fl,
                }
                self.stage_history_line = [
                    (1, last_create_id[-1], stage_history)]

            # for new record====================
            stage_history = {
                'stage_task_id': self.id,
                'stage_name': self.stage_id.name,
                'date_in': datetime.datetime.now(),
                'date_in_by': self.env.user.id,
            }
            self.stage_history_line = [(0, 0, stage_history)]
        return res

    def action_update_old_tasks_stage_history(self):
        '''Update Existing task's stage history'''
        for task in self.env['project.task'].browse(self.env.context.get('active_ids')).filtered(lambda task: not task.stage_history_line):
            stage_history = {
                'stage_task_id': task.id,
                'stage_name': task.stage_id.name,
                'date_in': task.date_last_stage_update,
                'date_in_by': task.write_uid.id,
            }
            task.stage_history_line = [(0, 0, stage_history)]
