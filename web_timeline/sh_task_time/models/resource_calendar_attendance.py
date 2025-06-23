# Part of Softhealer Technologies.

from odoo import models, fields, api, _
from datetime import date, datetime,timedelta

class ResourceCalendarAttendance(models.Model):
    _inherit = 'resource.calendar.attendance'

    high_priority = fields.Boolean("High Priority")
    

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
        dt_of_first_saturday=0
      
        # dt_of_first_saturday = date(year, month, first_saturday)
        
        if first_saturday == 0:
            dt_of_first_saturday = date(year, month, 7)
        else:
            dt_of_first_saturday = date(year, month, first_saturday)
        # dt_of_first_saturday = date(year, month, first_saturday)
        if first_saturday == 0:
            third_saturday = 21
        else:
            third_saturday = 21 - first_weekday
        dt_of_third_saturday = date(year, month, third_saturday)
        resource_calendars = self.env['resource.calendar'].search([('except_from_half_day','=',False)])
        for resource_calendar in resource_calendars:

            calendar_attendance_1 = resource_calendar.global_leave_ids.filtered(lambda x: x.date_from.date() + timedelta(days=1) == dt_of_first_saturday and x.date_to.date() == dt_of_first_saturday)

            calendar_attendance_2 = resource_calendar.global_leave_ids.filtered(lambda x:x.date_from.date() + timedelta(days=1) == dt_of_third_saturday and x.date_to.date() == dt_of_third_saturday)

            if not calendar_attendance_1:

                self.env['resource.calendar.leaves'].create({
                    'name': str(dt_of_first_saturday.strftime("%B")) + ' 1st Saturday',
                    'date_from': datetime(dt_of_first_saturday.year, dt_of_first_saturday.month, dt_of_first_saturday.day,0,0,0),
                    'date_to': datetime(dt_of_first_saturday.year, dt_of_first_saturday.month, dt_of_first_saturday.day,23,59,59),
                    'calendar_id': resource_calendar.id,
                    'is_saturday_leave':True,
                })
            if not calendar_attendance_2:

                self.env['resource.calendar.leaves'].create({
                    'name': str(dt_of_third_saturday.strftime("%B")) + ' 3rd Saturday',
                    'date_from': datetime(dt_of_third_saturday.year, dt_of_third_saturday.month, dt_of_third_saturday.day,0,0,0),
                    'date_to': datetime(dt_of_third_saturday.year, dt_of_third_saturday.month, dt_of_third_saturday.day,23,59,59),
                    'calendar_id': resource_calendar.id,
                    'is_saturday_leave':True
                })
