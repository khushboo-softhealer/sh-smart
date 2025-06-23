# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'

    def sh_action_update_global_leaves(self):
        return {
            'name': 'Update Global Leave',
            'res_model': 'sh.global.leave.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('sh_leave_custom.sh_global_leave_wizard_form_view').id,
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {'default_calendar_ids': [(6, 0, self.env.context.get('active_ids'))]}
        }
