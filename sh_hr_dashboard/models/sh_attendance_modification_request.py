# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, api
from datetime import date, datetime


class AttendanceModificationRequest(models.Model):
    _inherit = 'sh.attendance.modification.request'

    def write(self, vals):
        res = super(AttendanceModificationRequest, self).write(vals)

        if 'state' in vals and vals.get('state') == 'approved':
            check_in_date = self.attendance_id.check_in.date()
            attendances = self.env['hr.attendance'].search([('employee_id', '=', self.employee_id.id), (
                'employee_id', 'not in', self.env.user.company_id.sh_employee_ids.ids)]).filtered(lambda x: x.check_in.date() == check_in_date)
            attendance_hrs = 0
            for rec in attendances:
                if rec.check_in and rec.check_out:
                    total_time = rec.check_out - rec.check_in
                    if total_time:
                        duration = float(total_time.days) * \
                            24 + (float(total_time.seconds) / 3600)
                        attendance_hrs += duration

            timesheet_hrs = sum(self.env['account.analytic.line'].search(
                [('employee_id', '=', self.employee_id.id)]).filtered(lambda x: x.date == check_in_date).mapped('unit_amount'))
            if (attendance_hrs - timesheet_hrs) > 1:
                self.env['sh.warning.message'].create({
                    'name': 'Your Timesheet Hours not matched with Attendance',
                    'description': 'Your Timesheet Hours not matched with Attendance',
                    'user_id': self.employee_id.user_id.id,
                    'res_model': 'sh.attendance.modification.request',
                    'res_id': self.id,
                    'sh_create_date': date.today()
                })

        return res
