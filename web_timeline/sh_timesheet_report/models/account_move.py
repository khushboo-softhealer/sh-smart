# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import _, api, fields, models

class AccountMove(models.Model):
    _inherit = "account.move"
    _description = "Account Move"

    total_invoiced_timesheet_count = fields.Integer(string=" View",compute="total_invoiced_timesheet_count_views")
    
    def total_invoiced_timesheet_count_views(self):
        for record in self:
            total_timesheet = self.env['account.analytic.line'].sudo().search([('timesheet_invoice_id','=',self.id)])
            record.total_invoiced_timesheet_count = len(total_timesheet)

            if total_timesheet:
                return {
                'type': 'ir.actions.act_window',
                'name': _('Timesheet'),
                'res_model': 'account.analytic.line',
                'view_type': 'list',
                'view_mode': 'list',
                'views': [[False, 'list'], [False, 'form']],
                'domain': [('id', 'in', total_timesheet.ids)],
            }
    