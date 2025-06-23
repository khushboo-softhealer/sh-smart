# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models


class TaskCustomChecklist(models.Model):
    _name = "task.custom.checklist"
    _description = 'Task Custom Checklist'

    name = fields.Char(required=True)
    description = fields.Char()
    accepted_state_ids = fields.Many2many(
        'sh.checklist.state', string='Accepted in State',
        help='When change the task state, Checklist must be in those mentioned states to move forward.')

    def multi_action_update_state(self):
        return {
            'name': 'Mass Update Accepted State',
            'res_model': 'sh.update.state.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('sh_task_custom_checklist.sh_update_state_wizard_form').id,
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_chechlist_ids': [(6, 0, self.env.context.get('active_ids'))]
            }
        }
