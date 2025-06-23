# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

import math
from odoo import models, fields, api, _
from odoo.addons.resource.models.resource import float_to_time
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError

class Project(models.Model):
    _inherit = 'project.project'

    sh_auto_lock_timesheet = fields.Boolean("Auto Lock Timsheet",default=True,tracking=True)

class TimesheetPrint(models.Model):
    _inherit = 'project.task'

    timesheet_from_date = fields.Date("From Date")
    timesheet_to_date = fields.Date("To Date")
    changed_effective_hours = fields.Float(
        "Effective CC Hours", compute="_compute_from_to_date")
    invoice_hours = fields.Float("Invoice Quantity", compute="_compute_invoice_hours")
    
    @api.depends('timesheet_ids.unit_amount_invoice')
    def _compute_invoice_hours(self):
        for rec in self:
            rec.invoice_hours = 0.0
            if rec.timesheet_ids:
                rec.invoice_hours = sum(rec.timesheet_ids.mapped('unit_amount_invoice'))
    
    def autofill_timesheet(self):
        date_list = []
        for lines in self.timesheet_ids:
            date_list.append(lines.date)
        if date_list:
            self.timesheet_from_date = min(date_list)
            self.timesheet_to_date = max(date_list)

    @api.depends('timesheet_from_date', 'timesheet_to_date')
    def _compute_from_to_date(self):
        for task in self:
            task.changed_effective_hours = 0.0
            if task.timesheet_from_date and task.timesheet_to_date:
                timesheet = []
                for line_date in task.timesheet_ids:
                    if line_date.date >= task.timesheet_from_date and line_date.date <= task.timesheet_to_date:
                        timesheet.append(line_date)
                eff_time = 0.0
                for data in timesheet:
                    eff_time += data.unit_amount
                task.changed_effective_hours = eff_time


    # def sh_timesheet_print(self):
    #     if self.timesheet_from_date and self.timesheet_to_date:
    #         return self.env.ref('sh_timesheet_report.action_report_timesheet').report_action(self)
    #     raise UserError(
    #         _("Please provide the 'From Date' and 'To Date' field in order to print the Timesheet...!"))

    def sh_timesheet_print(self):

        # -------------------------------------------------------------------------
        # PREPARE MASTER
        # -------------------------------------------------------------------------

        timesheet_ids = self.timesheet_ids

        if self.timesheet_from_date and self.timesheet_to_date:
            timesheet_ids = timesheet_ids.filtered(
                lambda m: m.date >= self.timesheet_from_date and m.date <= self.timesheet_to_date)

        # Create an empty dictionary to hold the merged records
        merged_records = {}
        # Loop through each timesheet record
        for timesheet in timesheet_ids:
            # Extract the relevant fields from the timesheet record
            date = timesheet.date
            employee_id = timesheet.employee_id.name
            name = timesheet.name
            unit_amount = timesheet.unit_amount
            unit_amount_invoice = timesheet.unit_amount_invoice

            # Check if a record with the same date and employee_id already exists in the merged_records dictionary
            key = (date, employee_id)
            if key in merged_records:
                # If it does, merge the fields into the existing record
                merged_records[key]['name'] += ' - ' + name
                merged_records[key]['unit_amount'] += unit_amount
                merged_records[key]['unit_amount_invoice'] += unit_amount_invoice
                merged_records[key]['sh_test_unit_amount_invoice'] += unit_amount_invoice

            else:
                # If it doesn't, create a new record in the dictionary
                merged_records[key] = {
                    'date': date,
                    'employee_id': employee_id,
                    'name': name,
                    'unit_amount': unit_amount,
                    'unit_amount_invoice': unit_amount_invoice,
                    'sh_test_unit_amount_invoice':unit_amount_invoice
                }

        # Convert the dictionary into a list of records
        merged_records_list = list(merged_records.values())

        for record in merged_records_list:
            try:
                # record['unit_amount'] = float_to_time(record['unit_amount'])
                record['unit_amount'] = self.sh_float_to_time_val(record['unit_amount'])
                # record['unit_amount_invoice'] = float_to_time(record['unit_amount_invoice'])
                record['unit_amount_invoice'] = self.sh_float_to_time_val(record['unit_amount_invoice'])
            except Exception:
                raise UserError('Error while convert float to time data, record details - %s'%(record))

        # ----------------------------------------------------- BEFORE MERGE DATA VISUALS -------------------------------------------------------------------------
        #  DATE            EMPLOYEE         DESCRIPTION                  QUANTITY     INVOICE_QUANTITY
        #  10-22-2022      Mayur            [FIX]-xyz not working        00:58        00:58
        #  10-31-2022      Mayur            [UPDATE]-xyz update          00:43        00:43
        #  10-21-2022      Mayur            [ADD]-xyz add                01:00        01:00
        #  10-21-2022      Mayur            [ADD]-xyz add                01:46        01:46
        # ----------------------------------------------------- BEFORE MERGE DATA VISUALS -------------------------------------------------------------------------

        # ----------------------------------------------------- AFTER MERGE DATA VISUALS -------------------------------------------------------------------------
        #  DATE            EMPLOYEE         DESCRIPTION                         QUANTITY     INVOICE_QUANTITY
        #  10-22-2022      Mayur            [FIX]-xyz not working               00:58        00:58
        #  10-31-2022      Mayur            [UPDATE]-xyz update                 00:43        00:43
        #  10-21-2022      Mayur            [ADD]-xyz add \n [ADD]-xyz add      02:46        02:46              (MERGED LINE)
        # ----------------------------------------------------- BEFORE MERGE DATA VISUALS -------------------------------------------------------------------------

        # -------------------------------------------------------------------------
        # PREPARE MASTER
        # -------------------------------------------------------------------------

        master_dictonary_for_timesheet = {'merged_records_list': merged_records_list}
        datas = {
            'name': self.name,
            'timesheet_from_date': self.timesheet_from_date,
            'timesheet_to_date': self.timesheet_to_date,
            'master_dictonary_for_timesheet': master_dictonary_for_timesheet,
            # 'changed_effective_hours': float_to_time(self.changed_effective_hours),
            'changed_effective_hours': self.sh_float_to_time_val(self.changed_effective_hours),
        }
        return self.env.ref('sh_timesheet_report.action_report_timesheet').report_action(self, datas)

    def sh_float_to_time_val(self, hours):
        # Calculate hours and minutes
        total_minutes = math.ceil(hours * 60)
        hours_int = total_minutes // 60
        minutes_int = total_minutes % 60
        # Create a time string
        return f"{hours_int:02d}:{minutes_int:02d}"
