# -*- coding: utf-8 -*-
# Part of Softhealer Technology

from odoo import fields, models, _
 
class TimesheetSmartButton(models.Model):
    _inherit = 'project.task'

    timesheet_count = fields.Float("Timesheet",compute="action_open_related_timesheet")

    def action_open_related_timesheet(self):
        for rec in self:
            lst = []
            rec.timesheet_count = 0
            related_timesheet_ids = self.env['account.analytic.line'].search([('task_id', '=', rec.id)]).ids
            for record in related_timesheet_ids:
                lst.append(record)
            temp_list=[]
            if rec.child_ids:
                for first_child in rec.child_ids:
                    temp_list.append(first_child)
                for child in temp_list:
                    if child.child_ids:
                        for record in child.child_ids:
                            temp_list.append(record)
                for child_record in temp_list:
                    related_timesheet_child_ids = self.env['account.analytic.line'].search([('task_id', '=', child_record.id)]).ids
                    for final in related_timesheet_child_ids:
                        lst.append(final)

            rec.timesheet_count=rec.total_hours_spent
        return {
            'type': 'ir.actions.act_window',
            'name': _('Timesheet'),
            'res_model': 'account.analytic.line',
            'view_type': 'list',
            'view_mode': 'list',
            'views': [[False, 'list'], [False, 'form']],
            'domain': [('id', 'in', lst)],
        }
