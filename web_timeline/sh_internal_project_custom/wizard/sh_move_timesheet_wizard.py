# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, api,_
from datetime import date
from odoo.exceptions import UserError

class ShMoveTimesheetWizard(models.TransientModel):

    _name = "sh.move.timesheet.wizard"
    _description = "Move Timesheet Wizard"

    project_id = fields.Many2one("project.project", string="Project")
    appstore_project_id = fields.Many2one("project.project")
    task_id = fields.Many2one("project.task", string="App Store Task")

    def action_move_timesheet_to_appstore(self):
        task_ids = self.env['project.task'].sudo().search([('project_id','=',self.project_id.id)])
        project_timesheets_ids = []
        for task in task_ids:
            task_timesheet_ids = self.env['account.analytic.line'].sudo().search([('project_id','=',self.project_id.id), ('task_id','=',task.id),'|',('unit_amount','>',0),('unit_amount_invoice','>',0)])
            if task_timesheet_ids:
                project_timesheets_ids += task_timesheet_ids.ids
        
        project_timesheets = False
        if project_timesheets_ids:
            project_timesheets = self.env['account.analytic.line'].sudo().browse(project_timesheets_ids)
        
        if project_timesheets:
            emp_ids = project_timesheets.mapped('employee_id')
            for emp in emp_ids:
                emp_timesheets = project_timesheets.filtered(lambda x:x.employee_id.id == emp.id)
                if emp_timesheets:
                    if sum(emp_timesheets.mapped('unit_amount')) > 0 or sum(emp_timesheets.mapped('unit_amount_invoice')):
                        vals = {
                            'project_id' : self.appstore_project_id.id,
                            'task_id' : self.task_id.id,
                            'employee_id' : emp.id,
                            'name' : '/',
                            'date' : date.today(),
                            'unit_amount' : sum(emp_timesheets.mapped('unit_amount')),
                            'unit_amount_invoice' : sum(emp_timesheets.mapped('unit_amount_invoice')),
                        }
                        new_timesheet = self.env['account.analytic.line'].sudo().create(vals)
                        if new_timesheet:
                            emp_timesheets.with_context(bypass_done_task=True).write({ 'unit_amount':0, 'unit_amount_invoice':0 })
        else:
            raise UserError(_('There are no any timesheet available with Spend Hours or Invoice Hours greater than 0.'))
