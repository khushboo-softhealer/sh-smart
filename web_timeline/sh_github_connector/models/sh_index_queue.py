# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
from datetime import datetime


class ShIndexQueue(models.Model):
    _name = "sh.index.queue"
    _description = "Index Queue"
    _rec_name = "sh_module_id"

    sh_module_id = fields.Many2one('sh.module', string='Module')
    sh_branch_id = fields.Many2one(
        related='sh_module_id.sh_branch_id', string='Branch')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('error', 'Error'),
        ('in_progress', 'In Progress')
    ], string='State', default='draft')
    sh_datetime = fields.Datetime(string='Datetime', default=datetime.now())
    sh_message = fields.Char('Message')
    sh_repo = fields.Many2one(
        'sh.git.repo', string='Repo', related='sh_branch_id.repo_id')
    is_small_index = fields.Boolean('Is Small Index', default=False)

    def update_queue(self, state, message):
        self.sudo().write({
            'state': state,
            'sh_message': message
        })

    def process_in_progress_blog(self):
        is_status_done, message = self.sh_module_id.get_blog_media()
        if is_status_done:
            if is_status_done == 2:
                self.update_queue('done', message)
            else:
                self.update_queue('in_progress', message)
        else:
            self.update_queue('error', message)

    def process_other_blog(self):
        is_status_done, message = self.sh_module_id.process_blog()
        if is_status_done:
            self.update_queue('in_progress', message)
        else:
            self.update_queue('error', message)

    # UNACTIVE
    def _cron_sync_small_index_from_queue(self):
        return False
        # queue_objs = self.sudo().search(
        #     [('state', '=', 'draft'), ('is_small_index', '=', True)], limit=2)
        # for queue_obj in queue_objs:
        #     is_status_done, message = queue_obj.sh_module_id.process_full_blog()
        #     if is_status_done:
        #         self.update_queue('done', message)
        #     else:
        #         self.update_queue('error', message)

    def _sync_index_from_queue_cron(self):
        return False
        # queue_obj_list = self.sudo().search(
        #     [('state', '=', 'in_progress')], limit=2)
        # if queue_obj_list:
        #     for queue_obj in queue_obj_list:
        #         queue_obj.process_in_progress_blog()
        # else:
        #     queue_obj_list = self.sudo().search(
        #         [('state', '=', 'draft'), ('is_small_index', '=', True)], limit=2)
        #     if queue_obj_list:
        #         for queue_obj in queue_obj_list:
        #             is_status_done, message = queue_obj.sh_module_id.process_full_blog()
        #             if is_status_done:
        #                 self.update_queue('done', message)
        #             else:
        #                 self.update_queue('error', message)
        #     else:
        #         queue_obj_list = self.sudo().search(
        #             [('state', '=', 'draft'), ('is_small_index', '=', False)], limit=1)
        #         if queue_obj_list:
        #             for queue_obj in queue_obj_list:
        #                 queue_obj.process_other_blog()

    # UNACTIVE
    def _cron_sync_in_progress_index(self):
        return False
        # queue_obj_list = self.sudo().search(
        #     [('state', '=', 'in_progress')], limit=1)
        # for queue_obj in queue_obj_list:
        #     queue_obj.process_in_progress_blog()

    # -------------------------------
    #  Multi Action (Sync Half Index)
    # -------------------------------
    def sync_index_from_queue(self):
        queue_obj_list = self.sudo().browse(self.env.context.get('active_ids'))
        # self._loop_through_queue_obj(queue_obj_list)
        for queue_obj in queue_obj_list:
            if queue_obj.state == 'in_progress':
                queue_obj.process_in_progress_blog()
            else:
                queue_obj.process_other_blog()

    # -------------------------------
    #  Multi Action (Sync Full Index)
    # -------------------------------
    def sync_full_index(self):
        queue_obj_list = self.sudo().browse(self.env.context.get('active_ids'))
        for queue_obj in queue_obj_list:
            is_status_done, message = queue_obj.sh_module_id.process_full_blog()
            if is_status_done:
                self.update_queue('done', message)
            else:
                self.update_queue('error', message)
