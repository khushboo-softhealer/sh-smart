# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    def open_update_timesheet_wizard(self):
        return {
            'name': 'Update Timesheets',
            'res_model': 'sh.update.timesheet.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('sh_update_timesheets.sh_update_timesheet_wizard_form_view').id,
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {'default_account_analytic_line_ids': [(6, 0, self.env.context.get('active_ids'))]}
        }
