# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_
# from odoo.addons.resource.models.resource import float_to_time
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError
import math
from datetime import datetime, timedelta



class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    timesheet_lock = fields.Boolean(string='Lock Timesheet',default=False)
    timesheet_billed = fields.Boolean(string="Billed Timesheet",default=False)

    def auto_lock_timesheet(self):

        tod = datetime.now()
        date_before_3 = tod.date() - timedelta(days=3)
    
        # timesheet_before_3 = self.sudo().search([('date', '=', date_before_3),('timesheet_lock','=',False),('project_id.sh_auto_lock_timesheet','=',True)])
        # if timesheet_before_3:
        #     timesheet_before_3.sudo().write({
        #         'timesheet_lock': True})

        query = """
        UPDATE account_analytic_line
        SET timesheet_lock = TRUE
        WHERE date = %s
        AND timesheet_lock = FALSE
        AND project_id IN (
            SELECT pp.id
            FROM project_project pp 
            JOIN account_analytic_line aal ON aal.id = pp.analytic_account_id
            WHERE pp.sh_auto_lock_timesheet = TRUE
        )
    """
        self.env.cr.execute(query, (date_before_3,))



    def open_wizard(self):
        return {
            'name': 'Timesheet Entries',
            'res_model': 'sh.timesheet.report.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('sh_timesheet_report.sh_timesheet_report_wizard_view_form').id,
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {'default_account_analytic_line_ids': [(6, 0, self.env.context.get('active_ids'))]}
        }

    def check_total_invoice_amount(self,merged_records_list):
        # total_sum = sum(1 for entry in merged_records_list if entry['unit_amount_invoice'].hour > 0 or entry['unit_amount_invoice'].minute > 0)
        total_sum = sum(1 for entry in merged_records_list if entry['unit_amount_invoice'] or entry['unit_amount_invoice'])
        return total_sum > 0

    def prepare_each_master_dictonary(self, docs):
        # -------------------------------------------------------------------------
        # PREPARE MASTER
        # -------------------------------------------------------------------------

        timesheet_ids = docs

        # Create an empty dictionary to hold the merged records
        merged_records = {}

        for timesheet in timesheet_ids:
            # Extract the relevant fields from the timesheet record
            date = timesheet.date
            employee_id = timesheet.employee_id.name
            name = timesheet.name
            project = timesheet.project_id.name
            task = timesheet.task_id.name if timesheet.task_id else ''
            unit_amount = timesheet.unit_amount
            unit_amount_invoice = timesheet.unit_amount_invoice

            # Check if a record with the same date and employee_id already exists in the merged_records dictionary
            key = (timesheet.date, timesheet.employee_id.id,
                   timesheet.project_id.id, timesheet.task_id.id)

            if key in merged_records:
                # If it does, merge the fields into the existing record
                merged_records[key]['name'] += '#@%' + name
                merged_records[key]['unit_amount'] += unit_amount
                merged_records[key]['unit_amount_invoice'] += unit_amount_invoice
                merged_records[key]['sh_test_unit_amount_invoice'] += unit_amount_invoice
            else:
                # If it doesn't, create a new record in the dictionary
                merged_records[key] = {
                    'date': date,
                    'employee_id': employee_id,
                    'name': name,
                    'project': project,
                    'task': task,
                    'unit_amount': unit_amount,
                    'unit_amount_invoice': unit_amount_invoice,
                    'sh_test_unit_amount_invoice':unit_amount_invoice,
                    
                }
        # Convert the dictionary into a list of records
        merged_records_list = list(merged_records.values())
        task_obj = self.env['project.task']
        total_unit_amount = 0.0
        for record in merged_records_list:
            try:
                # record['unit_amount'] = float_to_time(record['unit_amount'])
                record['unit_amount'] = task_obj.sh_float_to_time_val(record['unit_amount'])
                total_unit_amount = total_unit_amount + record['unit_amount_invoice']
                # if _unit_amount < 23.99:
                #     record['unit_amount_invoice'] = float_to_time(_unit_amount)
                record['unit_amount_invoice'] = task_obj.sh_float_to_time_val(record['unit_amount_invoice'])
            except Exception:
                raise UserError('Error while convert float to time data, record details - %s'%(record))

        master_dictonary_for_timesheet = {
            'merged_records_list': merged_records_list}

        total_unit_amount = '{0:02.0f}:{1:02.0f}'.format(
            *divmod(total_unit_amount * 60, 60)) if total_unit_amount else 0.0

        datas = {'master_dictonary_for_timesheet': master_dictonary_for_timesheet,
                 'total_unit_amount': total_unit_amount}

        return datas
        # -------------------------------------------------------------------------
        # PREPARE MASTER
        # -------------------------------------------------------------------------
    def lock_timesheet(self):
        for line in self:
            line.write({
                'timesheet_lock': True})
            
    def unlock_timesheet(self):
        for line in self:
            line.write({
                'timesheet_lock': False})
            
    def billed_timesheet(self):
        for line in self:
            line.write({
                'timesheet_billed': True})

    
    def write(self, values):
        for rec in self:
            # if rec.timesheet_lock == True and not self.user_has_groups('project.group_project_manager') :
            if rec.timesheet_lock == True and not values.get('timesheet_lock') == False and not self.env.context.get('by_pass_timesheet_lock_validation') and not self.env.context.get('bypass_done_task'):
                raise UserError(_("You can't Modified Locked Timesheet "))

        return super().write(values)

    def calculate_timesheet_time(self,total_hrs,total_min):
                total_hours = 0
                remain_hour = math.floor(total_min / 60)
                total_hours = total_hrs + remain_hour
                total_minutes = (total_min % 60)

                return f"{total_hours:02}:{total_minutes:02}"
