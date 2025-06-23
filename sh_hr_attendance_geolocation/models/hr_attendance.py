# Part of Softhealer Technologies.
from odoo import models, fields, api, exceptions, _, SUPERUSER_ID
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class HrEmployee(models.Model):
    _inherit = "hr.attendance"

    def name_get(self):
        result = []
        for attendance in self:
            if not attendance.check_out:
                result.append((attendance.id, _("%(check_in)s") % {
                    'check_in': attendance.check_in + relativedelta(hours=5, minutes=30),
                }))
            else:
                result.append((attendance.id, _("%(check_in)s to %(check_out)s") % {
                    'check_in': attendance.check_in + relativedelta(hours=5, minutes=30),
                    'check_out': attendance.check_out + relativedelta(hours=5, minutes=30),
                }))
        return result
    # inherited hr.attendance model and added new fields
    message_in = fields.Char('Check in message')
    message_out = fields.Char('Check out message')
    in_latitude = fields.Char("Latitude ")
    in_longitude = fields.Char("Longitude ")
    out_latitude = fields.Char("Latitude")
    out_longitude = fields.Char("Longitude")
    check_in_url = fields.Char("Open Check-in location in Google Maps")
    check_out_url = fields.Char("Open Check-out location in Google Maps")
    total_time = fields.Float("Total Time Checked ")
    sh_break_start = fields.Datetime('Break Start')
    sh_break_start_date = fields.Date('Break Start Date')
    sh_break_end = fields.Datetime('Break End')
    sh_break_reason = fields.Char('Break Reason')
    sh_break_duration = fields.Float('Break Duration')
    sh_break_over = fields.Boolean('Break Over ?')
    other_data = fields.Char("Login data")

    def write(self, vals):
        for rec in self:
            total_time = 0.0
            if vals.get('check_out'):
                if type(vals.get('check_out')) == str:
                    checkout = datetime.strptime(
                        vals.get('check_out'), DEFAULT_SERVER_DATETIME_FORMAT)
                else:
                    checkout = vals.get('check_out')
                total_time = checkout - rec.check_in
                if total_time:
                    duration = float(total_time.days) * 24 + \
                        (float(total_time.seconds) / 3600)
                    vals.update({'total_time': round(duration, 2)})

            if vals.get('check_in'):
                if type(vals.get('check_in')) == str:
                    check_in = datetime.strptime(
                        vals.get('check_in'), DEFAULT_SERVER_DATETIME_FORMAT)
                else:
                    check_in = vals.get('check_in')
                if rec.check_out and check_in:
                    total_time = rec.check_out - check_in
                    if total_time:
                        duration = float(total_time.days) * \
                            24 + (float(total_time.seconds) / 3600)
                        vals.update({'total_time': round(duration, 2)})

        return super(HrEmployee, self).write(vals)
