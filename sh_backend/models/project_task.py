# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, api

class Task(models.Model):
    _inherit='project.task'

    # @api.multi
    @api.model
    def link_task_to_variant(self):
        active_task_ids = self.env['project.task'].sudo().browse(self.env.context.get('active_ids'))
        for task in active_task_ids:
            if task.sh_product_id:              
                task.sh_product_id.sudo().write({"related_sub_task":task.id,'sh_sub_task_created':True})
