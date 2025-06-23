# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, api, fields

class ProjectProject(models.Model):
    _inherit = 'project.project'

    sh_send_email = fields.Boolean('Send Email',tracking=True)

    def action_assign_employee(self):

        return {
            'view_mode': 'form',
            'res_model': 'sh.assign.employee',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {'current_id': self.id}
        }
