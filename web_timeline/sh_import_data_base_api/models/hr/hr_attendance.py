# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    remote_hr_attendance_id = fields.Char("Remote Attendance Id",copy=False)


class HrAttendanceModificationRequest(models.Model):
    _inherit = 'sh.attendance.modification.request'

    remote_sh_attendance_modification_request_id = fields.Char("Remote Attendance Modification Request Id",copy=False)
