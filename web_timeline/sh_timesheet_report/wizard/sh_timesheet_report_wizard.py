# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

import math
import io
import xlwt
from xlwt import easyxf
import base64
from babel.dates import format_datetime, format_date
from datetime import datetime, timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.addons.resource.models.resource import float_to_time
# from odoo.addons.hr_timesheet.models.hr_timesheet import float_to_time
import logging
_logger = logging.getLogger(__name__)


class TimesheetReportWizard(models.TransientModel):
    _name = 'sh.timesheet.report.wizard'
    _description = 'Timesheet Report Wizard'

    group_by_task = fields.Boolean(string="Group By Task ?")
    account_analytic_line_ids = fields.Many2many('account.analytic.line')
    is_lock = fields.Boolean('Is Lock',groups="project.group_project_manager")
    invoice_id = fields.Many2one('account.move',groups="project.group_project_manager")
    sh_is_task_desc_needed = fields.Boolean('Task Description Needed')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if not self.env.user.has_group('project.group_project_manager'):
            raise UserError(
                "Only project manager has access to print timesheet")
        return res

    # def print_timesheet_report(self):
    #     if self.group_by_task:
    #         return self.env.ref('sh_timesheet_report.check_total_invoice_amount_action').report_action(self.account_analytic_line_ids)
    #     return self.env.ref('sh_timesheet_report.sh_timesheet_report_action').report_action(self.account_analytic_line_ids)

    def print_timesheet_report(self):
        
        # Lock Timesheet and add Invoice 
        for line in self.account_analytic_line_ids:
                if self.is_lock:
                    line.write({
                        'timesheet_lock':self.is_lock})
                if self.invoice_id:
                    line.write({
                         'timesheet_invoice_id':self.invoice_id})

        if self.group_by_task and self.sh_is_task_desc_needed:
            prevent_zero = [0.0,00,0,'0:0','0.0','00:00','00.00']
            account_analytic_line_ids = self.account_analytic_line_ids.filtered(lambda x:x.unit_amount_invoice not in prevent_zero and not x.task_id.not_billable)
            return self.env.ref('sh_timesheet_report.sh_report_timesheet_group_task_action').report_action(account_analytic_line_ids)
        else:
            datas = self._get_data_for_report()
            return self.env.ref('sh_timesheet_report.sh_timesheet_report_action').report_action(self, datas)

    def print_timesheet_xls_report(self):
        workbook = xlwt.Workbook(encoding='utf-8')
        heading_style = easyxf('font:height 180;font:bold True;align:horiz center;borders: top thin, bottom thin, left thin, right thin; ')
        data_style = easyxf('font:height 180;align:horiz center;borders: top thin, bottom thin, left thin,right thin;')
        title_style = easyxf('font:height 220;font:bold True;align:vert centre,horiz center;')
        worksheet = workbook.add_sheet('Timesheet Entries')
        report_name='Timesheet Entries'
        desc_style = easyxf('font:height 180;borders: top thin, bottom thin, left thin,right thin;')
        desc_len = 20000
        obj = self.env['project.task']
        
        # lock timesheet
        for line in self.account_analytic_line_ids:
            if self.is_lock:
                line.write({
                        'timesheet_lock':self.is_lock})
            if self.invoice_id:
                line.write({
                         'timesheet_invoice_id':self.invoice_id})
            
        def float_to_time(float_hours):
                # Extract hours
                hours = int(float_hours)
                # Extract minutes
                minutes = round((float_hours - hours) * 60)
                return f"{hours:02}:{minutes:02}"

        if self.group_by_task and self.sh_is_task_desc_needed:
            mapped_tasks = self.account_analytic_line_ids.mapped('task_id')
            main_title_style = easyxf('font:height 240;font:bold True;align:vert centre,horiz center;')

            worksheet.write_merge(0,1, 0,4, "Timesheet Entries",main_title_style)
            worksheet.col(0).width = 6000
            worksheet.col(1).width = 6000
            worksheet.col(2).width = desc_len
            worksheet.col(3).width = 5000

            count_line=3
            total_time  = 0.0
            total_timesheets_time = []
            for each_task in mapped_tasks:
                each_docs = self.account_analytic_line_ids.filtered(lambda x : x.task_id.id == each_task.id)
                timesheet_blank_rec_set = self.env['account.analytic.line'].sudo().browse()
                datas = timesheet_blank_rec_set.prepare_each_master_dictonary(each_docs)
                # Skip the 00:00 timesheets
                if not datas.get('total_unit_amount'):
                    continue

                merged_records_list = datas.get('master_dictonary_for_timesheet').get('merged_records_list')

                check_total_invoice_amount = timesheet_blank_rec_set.check_total_invoice_amount(merged_records_list)

                if not check_total_invoice_amount:
                    continue

                # ----------------------
                # if check_total_invoice_amount:
                if each_task:
                    cell_val = each_task.name
                    if each_task.project_id:
                        cell_val = f"{each_task.project_id.name} / {each_task.name}"
                    worksheet.write_merge(count_line,count_line, 0, 3, cell_val, title_style)
                count_line += 2

                # ----------------------
                # if check_total_invoice_amount:
                worksheet.write(count_line,0, "Date",heading_style)
                worksheet.write(count_line,1, "Responsible",heading_style)
                worksheet.write(count_line,2, "Description",heading_style)
                worksheet.write(count_line,3, "Time",heading_style)
                count_line += 1
                total_task_time = 0
                total_timesheet_task_time = []
                # task_total_hrs = 0
                # task_total_mint = 0
                for each_dictonary in merged_records_list:
                    # Skip the 00:00 timesheets
                    if not each_dictonary.get('unit_amount_invoice') or str(each_dictonary['unit_amount_invoice']) == '00:00':
                        continue
                    worksheet.write(count_line, 0,format_date(each_dictonary.get('date')), data_style)
                    worksheet.write(count_line, 1,each_dictonary.get('employee_id'), data_style)
                    # Description
                    description = '\n ->'.join(each_dictonary.get('name').split('#@%',))
                    worksheet.write(count_line, 2,'->' + description, desc_style)
                    worksheet.write(count_line, 3, str(each_dictonary['unit_amount_invoice']), data_style)
                    # total_task_time += each_dictonary.get('unit_amount_invoice')
                    # total_time +=  each_dictonary.get('unit_amount_invoice')
                    count_line += 1
                    total_timesheet_task_time.append(each_dictonary.get('unit_amount_invoice'))
                    total_timesheets_time.append(each_dictonary.get('unit_amount_invoice'))
                # total_task_time = obj.sh_float_to_time_val(total_task_time)
                total_task_time = self.calculate_total_time(total_timesheet_task_time)

                if datas.get('total_unit_amount'):

                    worksheet.write(count_line,2, 'Total',heading_style)
                    worksheet.write(count_line,3,str(total_task_time),heading_style) #str(float_to_time(total_time))
                count_line += 2

            total_time = self.calculate_total_time(total_timesheets_time)


            worksheet.write(count_line,2, 'Total', heading_style)
            worksheet.write(count_line,3,str(total_time),heading_style)

        else:
            worksheet.write_merge(0,1, 0,4, "Timesheet Entries",title_style)
            worksheet.write(3,0, "Project - Task",heading_style)
            worksheet.write(3,1, "Status",heading_style)
            worksheet.write(3, 2, "Time", heading_style)

            worksheet.col(0).width = desc_len
            worksheet.col(1).width = 6000
            worksheet.col(2).width = 6000
            worksheet.col(3).width = 8000
            worksheet.col(4).width = 5000

            datas = self._get_data_for_report()
            count_line=4
            total_time = 0.0
            total_hrs = 0
            total_mint = 0
            
            if datas.get('master_dictonary_for_timesheet') and datas['master_dictonary_for_timesheet'].get('merged_records_list'):
                all_timesheets = []
                for each_dictonary in datas['master_dictonary_for_timesheet']['merged_records_list']:
                    
                    # worksheet.write(count_line, 0,format_date(each_dictonary.get('date')), data_style) #format_date(date)
                    # worksheet.write(count_line, 1,each_dictonary.get('employee_id'), data_style)

                    # # Description
                    # description = '\n ->'.join(each_dictonary.get('name').split('#@%',))
                    # worksheet.write(count_line, 2,'->' + description, desc_style)


                    # Project/Task
                    project_task_cell_val = each_dictonary.get('project')
                    if project_task_cell_val:
                        project_task_cell_val += ' - '
                    if each_dictonary.get('parent'):
                        project_task_cell_val += f"{each_dictonary['parent']} / "
                    if each_dictonary.get('task'):
                        project_task_cell_val += each_dictonary['task']

                    worksheet.write(count_line, 0, project_task_cell_val, desc_style)
                    worksheet.write(count_line, 1, each_dictonary.get('task_status'), desc_style)

                    worksheet.write(count_line, 2,str(each_dictonary.get('unit_amount_invoice')), data_style) #str(float_to_time(unit_amount_invoice))
                    unit_amount = each_dictonary.get('unit_amount_invoice')
                    all_timesheets.append(unit_amount)
                    count_line += 1

                # Example float value representing hours
                # 2 hours and 30 minutes
                # Convert float to time format
                total_time = self.calculate_total_time(all_timesheets)
                

                worksheet.write(count_line,1, 'Total',heading_style)
                worksheet.write(count_line,2,str(total_time),heading_style) #str(float_to_time(total_time))
                count_line += 1


        fp = io.BytesIO()
        workbook.save(fp)
        data = base64.b64encode(fp.getvalue())
        fp.close()
        IrAttachment = self.env['ir.attachment']
        attachment_vals = {
            "name": report_name + '.xls',
            "res_model": "ir.ui.view",
            "type": "binary",
            "datas": data,
            "public": True,
        }
        attachment = IrAttachment.create(attachment_vals)
        if not attachment:
            raise UserError('There is no attachments...')

        url = "/web/content/" + str(attachment.id) + "?download=true"
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }


    def _get_data_for_report(self):
            print(f"\n\n\n\t--------------> 249 ",)
            # -------------------------------------------------------------------------
            # PREPARE MASTER
            # -------------------------------------------------------------------------

            timesheet_ids = self.account_analytic_line_ids

            # Create an empty dictionary to hold the merged records
            merged_records = {}

            for timesheet in timesheet_ids:
                # Extract the relevant fields from the timesheet record
                date = timesheet.date
                employee_id = timesheet.employee_id.name
                name = timesheet.name
                project = timesheet.project_id.name
                task = timesheet.task_id.name if timesheet.task_id else ''
                task_status = timesheet.task_id.stage_id.name if timesheet.task_id else ''
                parent = timesheet.task_id.parent_id.name if timesheet.task_id.parent_id else ''
                unit_amount = timesheet.unit_amount
                unit_amount_invoice = timesheet.task_id.estimated_hrs if timesheet.task_id else 0

                # Check if a record with the same date and employee_id already exists in the merged_records dictionary
                key = (timesheet.date, timesheet.employee_id.id,
                       timesheet.project_id.id, timesheet.task_id.id)
                if key in merged_records:
                    # If it does, merge the fields into the existing record
                    merged_records[key]['name'] += '#@%' + name
                    merged_records[key]['unit_amount'] += unit_amount
                    # merged_records[key]['unit_amount_invoice'] += unit_amount_invoice
                    merged_records[key]['sh_test_unit_amount_invoice'] += unit_amount_invoice

                else:
                    # If it doesn't, create a new record in the dictionary
                    merged_records[key] = {
                        'date': date,
                        'employee_id': employee_id,
                        'name': name,
                        'task_status': task_status,
                        'project': project,
                        'parent':parent,
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
                # if not record.get('unit_amount_invoice'):
                #     continue
                try:
                    # record['unit_amount'] = float_to_time(123.5)
                    total_unit_amount += record['unit_amount_invoice']
                    record['unit_amount_invoice'] = task_obj.sh_float_to_time_val(record['unit_amount_invoice'])


                    # if unit_amount_invoice < 23.99:
                    #     record['unit_amount_invoice'] = float_to_time(record['unit_amount_invoice'])
                except Exception:
                    raise UserError('Error while convert float to time data, record details - %s'%(record))

            # -------------------------------------------------------------------------
            # PREPARE MASTER
            # -------------------------------------------------------------------------

            master_dictonary_for_timesheet = {
                'merged_records_list': merged_records_list}

            # Remove record which contain 00:00 Invoice Hours
            if merged_records_list:
                prevent_zero = [0.0,00,0,'0:0','0.0','00:00','00.00']

                # Remove dictionaries with 'unit_amount_invoice' equal to 0
                # filtered_data = [item for item in merged_records_list if item.get('unit_amount_invoice', 1) != 0.0 ]
                # filtered_data = [item for item in merged_records_list if item.get('unit_amount_invoice', 1) not in prevent_zero]
            # master_dictonary_for_timesheet = {
            #     'merged_records_list': filtered_data}

            total_unit_amount = '{0:02.0f}:{1:02.0f}'.format(
                *divmod(total_unit_amount * 60, 60)) if total_unit_amount else 0.0

            datas = {'master_dictonary_for_timesheet': master_dictonary_for_timesheet,
                     'total_unit_amount': total_unit_amount}
            return datas
    
    def calculate_total_time(self,timesheets):
        total_hrs = 0
        total_min = 0
        for timesheet in timesheets:
            int_hr = timesheet.split(':')[0]
            int_min = timesheet.split(':')[1]

            total_hrs += int(int_hr)
            total_min += int(int_min)

        total_hours = 0
        remain_hour = math.floor(total_min / 60)
        total_hours = total_hrs + remain_hour
        total_minutes = (total_min % 60)

        return f"{total_hours:02}:{total_minutes:02}"
