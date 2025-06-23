# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, api, _


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.model
    def action_view_training_timesheet(self):
        project_id = self.env.user.company_id.sh_training_project_id.id
        action = {
            'name': _('Timesheet'),
            'view_mode': 'tree,form,kanban',
            'search_view_id': [self.env.ref('hr_timesheet.hr_timesheet_line_search').id],
            'res_model': 'account.analytic.line',
            'type': 'ir.actions.act_window',
            'domain': [('project_id', '=', project_id)],
            'context': {
                'search_default_month': True,
                'search_default_groupby_employee': True,
                'search_default_groupby_task': True,
            }
        }
        return action
