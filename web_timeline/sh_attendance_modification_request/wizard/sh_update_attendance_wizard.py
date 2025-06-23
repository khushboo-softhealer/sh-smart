# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models, api, _
from datetime import timedelta
import pytz
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class Attendancewizard(models.TransientModel):
    _name = 'sh.hr.attendance.update.wizard'
    _description = "Attendance wizard"

    type = fields.Selection(selection=[(
        'checkin', 'Check In'), ('checkout', 'Check Out'), ('both', 'Both')],
        default="checkin")
    updated_checkin = fields.Datetime()
    updated_checkout = fields.Datetime()
    reason = fields.Text(required=True)
    checkin_alert = fields.Boolean('Checkin Alert', default=False)
    checkout_alert = fields.Boolean('Checkout Alert', default=False)

    @api.model
    def default_get(self, fields):
        res = super(Attendancewizard, self).default_get(fields)
        hr_attendance_id = self.env.context.get('active_id')
        hr_attendance = self.env['hr.attendance'].browse(hr_attendance_id)
        if 'updated_checkin' in fields:
            res.update({'updated_checkin': hr_attendance.check_in})
        if 'updated_checkout' in fields:
            res.update({'updated_checkout': hr_attendance.check_out})
        return res

    @api.onchange('updated_checkin', 'updated_checkout')
    def _onchange_attendance(self):
        self.checkin_alert = False
        self.checkout_alert = False

        active_id = self.env.context.get('active_id')
        attendance_id = self.env['hr.attendance'].browse(active_id)
        Checkin_hours_schedule = False
        Checkout_hours_schedule = False
        if attendance_id.check_in:

            in_day = attendance_id.check_in.weekday()
            Checkin_hours_schedule = self.env['resource.calendar.attendance'].sudo().search(
                [('calendar_id', '=', attendance_id.employee_id.resource_calendar_id.id), ('dayofweek', '=', in_day)], limit=1)
        if attendance_id.check_out:
            out_day = attendance_id.check_out.weekday()

            Checkout_hours_schedule = self.env['resource.calendar.attendance'].sudo().search(
                [('calendar_id', '=', attendance_id.employee_id.resource_calendar_id.id), ('dayofweek', '=', out_day)], limit=1)

        if Checkin_hours_schedule:
            in_time = ''
            value = Checkin_hours_schedule.hour_from
            hours, minutes = divmod(abs(value) * 60, 60)
            minutes = round(minutes)
            if minutes == 60:
                minutes = 0
                hours += 1
            if value < 0:
                in_time = '-%02d:%02d:00' % (hours, minutes)
            in_time = '%02d:%02d:00' % (hours, minutes)
            in_time_object = datetime.strptime(in_time, '%H:%M:%S')
            Check_in_date = self.updated_checkin + \
                relativedelta(hours=5, minutes=30)
            if Check_in_date and in_time_object:
                if attendance_id and self.type in ['checkin', 'both'] and Check_in_date.time() < (in_time_object + timedelta(hours=-1)).time():
                    self.checkin_alert = True

        if Checkout_hours_schedule:
            out_time = ''
            value1 = Checkout_hours_schedule.hour_to
            hours, minutes = divmod(abs(value1) * 60, 60)
            minutes = round(minutes)
            if minutes == 60:
                minutes = 0
                hours += 1
            if value1 < 0:
                out_time = '-%02d:%02d:00' % (hours, minutes)
            out_time = '%02d:%02d:00' % (hours, minutes)
            out_time_object = datetime.strptime(out_time, '%H:%M:%S')

            Check_out_date = self.updated_checkout + \
                relativedelta(hours=5, minutes=30)

            if Check_out_date and out_time_object:
                if attendance_id and self.type in ['checkout', 'both'] and Check_out_date.time() > (out_time_object + timedelta(hours=2)).time():
                    self.checkout_alert = True

    def save_attendance(self):
        # self.checkin_alert = False
        active_id = self.env.context.get('active_id')
        attendance_id = self.env['hr.attendance'].browse(active_id)

        attendance = {
            'type': self.type,
            'reason': self.reason,
            'attendance_id': attendance_id.id,
            'updated_value': self.updated_checkin,
            'updated_value_checkout': self.updated_checkout,
            'employee_id': attendance_id.employee_id.id,
            'checkin_alert': self.checkin_alert,
            'checkout_alert': self.checkout_alert
        }
        request = self.env['sh.attendance.modification.request'].create(
            attendance)

        listt = []
        users = self.env['res.users'].search([])
        for user in users:
            if user.has_group('hr.group_hr_manager'):
                listt.append(user.id)

        request.confirm()
