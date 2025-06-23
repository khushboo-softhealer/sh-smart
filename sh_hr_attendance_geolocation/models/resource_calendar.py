# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api
from datetime import datetime, timedelta, date
import calendar


class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'

    sh_late_early_restriction = fields.Float(
        'Late/Early Restriction (Hour:Min)')
    except_from_half_day = fields.Boolean("Exlude from Saturday Leave")
    timesheet_hrs = fields.Float(string="Timesheet Hrs")
    timesheet_validation_after = fields.Float("Timesheet Validation After Checkout")

    def multi_action_add_remove_working_hours(self):
        return {
            'name': 'Add / Remove Working Hours',
            'type': 'ir.actions.act_window',
            'res_model': 'resource.calendar.entry.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('sh_hr_attendance_geolocation.sh_calender_entry_wizard_view').id,
            'target': 'new',
            'context': {
                'default_resource_calendar_ids': [(6, 0, self.env.context.get('active_ids'))],
            }
        }

class ResourceCalendarAttendance(models.Model):
    _inherit = 'resource.calendar.attendance'

    high_priority = fields.Boolean("High Priority")
    sh_break = fields.Float(string="Break")
    sh_wroked_hours = fields.Float(string="Worked Hours")

    @api.onchange('hour_from', 'hour_to')
    def onchange_worked_hours(self):
        if self:
            for rec in self:
                rec.sh_wroked_hours = (rec.hour_to - rec.hour_from)

    def copy_line(self):
        self.create({
            'name': self.name,
            'dayofweek': self.dayofweek,
            'hour_from': self.hour_from,
            'hour_to': self.hour_to,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'day_period': self.day_period,
            'calendar_id': self.calendar_id.id,
            'sh_break': self.sh_break,
            'sh_wroked_hours': self.sh_wroked_hours
        })

    def auto_fill_calendar(self):
        year = date.today().year
        month = date.today().month
        dt = date(year, month, 1)
        first_weekday = dt.isoweekday()
        first_saturday = 7 - first_weekday

        dt_of_first_saturday = date(year, month, first_saturday)

        if first_saturday == 0:
            dt_of_first_saturday = date(year, month, 7)
            if first_saturday == 0:
                third_saturday = 21
        else:
            third_saturday = 21 - first_weekday
        dt_of_third_saturday = date(year, month, third_saturday)
        resource_calendars = self.env['resource.calendar'].search(
            [('except_from_half_day', '=', False)])
        for resource_calendar in resource_calendars:

            calendar_attendance_1 = resource_calendar.global_leave_ids.filtered(lambda x: x.date_from.date(
            ) + timedelta(days=1) == dt_of_first_saturday and x.date_to.date() == dt_of_first_saturday)

            calendar_attendance_2 = resource_calendar.global_leave_ids.filtered(lambda x: x.date_from.date(
            ) + timedelta(days=1) == dt_of_third_saturday and x.date_to.date() == dt_of_third_saturday)

            if not calendar_attendance_1:

                self.env['resource.calendar.leaves'].create({
                    'name': str(dt_of_first_saturday.strftime("%B")) + ' 1st Saturday',
                    'date_from': datetime(dt_of_first_saturday.year, dt_of_first_saturday.month, dt_of_first_saturday.day, 0, 0, 0) - timedelta(hours=5, minutes=30),
                    'date_to': datetime(dt_of_first_saturday.year, dt_of_first_saturday.month, dt_of_first_saturday.day, 23, 59, 59) - timedelta(hours=5, minutes=30),
                    'calendar_id': resource_calendar.id,
                    'is_saturday_leave': True,


                })
            if not calendar_attendance_2:

                self.env['resource.calendar.leaves'].create({
                    'name': str(dt_of_third_saturday.strftime("%B")) + ' 3rd Saturday',
                    'date_from': datetime(dt_of_third_saturday.year, dt_of_third_saturday.month, dt_of_third_saturday.day, 0, 0, 0) - timedelta(hours=5, minutes=30),
                    'date_to': datetime(dt_of_third_saturday.year, dt_of_third_saturday.month, dt_of_third_saturday.day, 23, 59, 59) - timedelta(hours=5, minutes=30),
                    'calendar_id': resource_calendar.id,
                    'is_saturday_leave': True

                })
