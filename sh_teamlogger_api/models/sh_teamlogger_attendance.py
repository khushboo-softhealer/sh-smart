# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api
from datetime import datetime
import requests
import logging
import pytz


_logger = logging.getLogger(__name__)

class TeamloggerAttendance(models.Model):
    _name = 'sh.teamlogger.attendance'
    _description = 'Teamlogger Daily Attendance'
    _rec_name = "employee_id"

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    date = fields.Date(string="Date", required=True)
    punch_in = fields.Datetime(string="Punch In")
    punch_out = fields.Datetime(string="Punch Out")
    total_hours = fields.Float(string="Total Hours")
    break_hours = fields.Float(string="Break Hours")
    span_hours = fields.Float(string="Span Hours")

    _sql_constraints = [
        ('unique_attendance_per_day', 'unique(employee_id, date)', 'Attendance already exists for this employee on this date.')
    ]
    
    @api.model
    def sync_teamlogger_data(self):
        api_key = self.env['ir.config_parameter'].sudo().get_param('teamlogger.api_key')
        if not api_key:
            _logger.error("Teamlogger API Key not set in ir.config_parameter.")
            return

        headers = {'Authorization': f'Bearer {api_key}'}
        today = datetime.now()
        year, month, day = today.year, today.month, today.day
        date_obj = datetime(year, month, day).date()

        # Punch in/out API
        punch_url = f"https://api2.teamlogger.com/api/company_punch_in_out_report?year={year}&month={month:02d}&day={day:02d}&timezoneOffsetMinutes=330&dayStartsAtHours=6&dayEndsAtHours=23"
        punch_res = requests.get(punch_url, headers=headers)
        punch_data = punch_res.json() if punch_res.ok else []

        # Summary report API
        start_time = int(datetime(year, month, day, 6, 0).timestamp() * 1000)
        end_time = int(datetime(year, month, day, 23, 0).timestamp() * 1000)
        summary_url = f"https://api2.teamlogger.com/api/employee_summary_report?startTime={start_time}&endTime={end_time}"
        summary_res = requests.get(summary_url, headers=headers)
        summary_data = summary_res.json() if summary_res.ok else []

        # Map summaries by code
        summary_map = {entry.get('code'): entry for entry in summary_data}

        for punch in punch_data:
            code = punch.get('employeeCode')
            employee = self.env['hr.employee'].search([('sh_rmm_employee_id', '=', code)], limit=1)
            if not employee:
                continue

            summary = summary_map.get(code, {})
            
            local_tz = pytz.timezone("Asia/Kolkata")  # GMT+5:30
            utc_tz = pytz.utc

            # Build full local datetime strings
            local_date_str = f"{year}-{month:02d}-{day:02d}"
            punch_in_str = punch.get('punchInLocalTime')  # e.g., "09:34"
            punch_out_str = punch.get('punchOutLocalTime')  # e.g., "21:32"

            print("\n\n\npunch_in_str",punch_in_str)
            print("\n\n\npunch_in_str",punch_out_str)

            # Convert to localized datetime (from string)
            punch_in_dt = None
            punch_out_dt = None
            if punch_in_str != "Absent":
                local_punch_in = datetime.strptime(f"{local_date_str} {punch_in_str}", "%Y-%m-%d %H:%M")
                punch_in_dt = local_tz.localize(local_punch_in).astimezone(utc_tz).replace(tzinfo=None)

            if punch_out_str != "Absent":
                local_punch_out = datetime.strptime(f"{local_date_str} {punch_out_str}", "%Y-%m-%d %H:%M")
                punch_out_dt = local_tz.localize(local_punch_out).astimezone(utc_tz).replace(tzinfo=None)
            vals = {
                'employee_id': employee.id,
                'date': date_obj,
                'punch_in': punch_in_dt,
                'punch_out': punch_out_dt,
                'total_hours': summary.get('totalHours', 0.0),
                'break_hours': summary.get('breakHours', 0.0),
                'span_hours': summary.get('spanHours', 0.0),
            }

            # Avoid duplicate entries per day
            existing = self.env['sh.teamlogger.attendance'].search([
                ('employee_id', '=', employee.id),
                ('date', '=', date_obj)
            ], limit=1)

            if existing:
                existing.write(vals)
            else:
                self.env['sh.teamlogger.attendance'].create(vals)