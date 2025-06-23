# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from datetime import datetime
from odoo import models, fields

class TimesheetWizard(models.TransientModel):
    _name = 'sh.update.timesheet'
    _description = "Helps to Update Timesheet"

    name = fields.Char("Description")
    sh_update_date = fields.Date("Date",default=datetime.now().date())
    sh_employee_id = fields.Many2one("hr.employee","Employee")
    unit_amount = fields.Float("Hours")

    def update_data(self):  
        parent_id = self.env.context.get("active_id")
        parent_model = self.env.context.get("active_model")
        parent_record = self.env[parent_model].browse(parent_id)
        employee = self.env['hr.employee'].sudo().search([('user_id','=',self.env.user.id)])
        if employee:
            timesheet_vals = {
                'name' : self.name,
                'date' : self.sh_update_date,
                'unit_amount' : self.unit_amount,
                'unit_amount_invoice' : self.unit_amount,
                'task_id' : parent_record.id,
                'employee_id' : employee.id,
                'account_id' : parent_record.project_id.analytic_account_id.id,
                'company_id' : parent_record.project_id.analytic_account_id.company_id.id,            
            }                
            self.env['account.analytic.line'].sudo().create(timesheet_vals) 