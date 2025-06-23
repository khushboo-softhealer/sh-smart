# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _


class sh_project_task(models.Model):
    _inherit = 'project.task'

    @api.onchange('project_id')
    def _onchange_project(self):
        if self.project_id and not self.sh_ticket_ids:
            self.user_ids =[(6, 0,[self.env.user.id])]
