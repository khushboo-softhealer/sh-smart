# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ResCalendar(models.Model):
    _inherit = 'resource.calendar'

    remote_resource_calendar_id = fields.Char("Remote Resource Calendard ID",copy=False)
    
class ResCalendarAttendance(models.Model):
    _inherit = 'resource.calendar.attendance'

    remote_resource_calendar_attendance_id = fields.Char("Remote Resource Calendard Attendance ID",copy=False)
    
class ResCalendarLeave(models.Model):
    _inherit = 'resource.calendar.leaves'

    remote_resource_calendar_leaves_id = fields.Char("Remote Resource Calendard Leave ID",copy=False)
        
    
    
    