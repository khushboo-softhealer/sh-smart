# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ShUpdateTimesheetEntries(models.TransientModel):
    _name = 'sh.update.timesheet.wizard'
    _description = 'Update Timesheets'

    sh_timesheet_update_minutes=fields.Integer('Update In Minutes')
    account_analytic_line_ids = fields.Many2many('account.analytic.line',string='Timesheet Ids')
    sh_update_type = fields.Selection(
        [("increase", "Increase"),
        ("decrease", "Decrease")],
        default="increase",string='Update Type'
    )

    def action_update_timesheets(self):
        selected_lines = self.env['account.analytic.line'].browse(self._context.get('active_ids', []))
        for line in selected_lines:
            if line.unit_amount and line.unit_amount_invoice:
                if self.sh_update_type=='increase':
                    line.write({
                        'unit_amount': line.unit_amount + self.sh_timesheet_update_minutes / 60.0 ,
                        'unit_amount_invoice': line.unit_amount_invoice + self.sh_timesheet_update_minutes / 60.0
                    })
                else:
                    line.write({
                        'unit_amount': line.unit_amount - self.sh_timesheet_update_minutes / 60.0 ,
                        'unit_amount_invoice': line.unit_amount_invoice - self.sh_timesheet_update_minutes / 60.0
                    })
        return {'type': 'ir.actions.act_window_close'}