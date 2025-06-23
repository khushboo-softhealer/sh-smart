# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models, api
from datetime import datetime, timedelta


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    bool_field = fields.Boolean(default=True)
    alert_leave = fields.Char()
    leave_days = fields.Integer()
    warning = fields.Char()

    is_desc_hide = fields.Boolean(compute="compute_is_desc_hide")

    def compute_is_desc_hide(self):
        for rec in self:
            rec.is_desc_hide = True
            if rec.env.user.id == rec.employee_id.user_id.id or self.env.user.has_group('hr.group_hr_manager'):
                rec.is_desc_hide = False

    @api.onchange('holiday_status_id', 'date_from', 'employee_id')
    def date_from_onchange(self):
        self.bool_field = True
        if self.holiday_status_id and self.date_from and self.employee_id:
            hol_status_obj = self.env['hr.leave.type'].search(
                [('id', '=', self.holiday_status_id.id)], limit=1)
            if hol_status_obj:
                if hol_status_obj.leave_before_day_alert and hol_status_obj.leave_before_days:
                    if not (self.user_has_groups('hr.group_hr_manager') and
                            (self.employee_id.user_id and
                             self.env.user.id != self.employee_id.user_id.id)):
                        leave_from = datetime.strptime(str(
                            self.date_from), "%Y-%m-%d %H:%M:%S") - timedelta(
                                days=hol_status_obj.leave_before_days)
                        self.leave_days = hol_status_obj.leave_before_days
                        leave_start_date = datetime.strptime(str(
                            self.date_from), "%Y-%m-%d %H:%M:%S")
                        if (datetime.now().date() > leave_from.date()):
                            self.warning = str(
                                'Please! Always apply preplanned leave before  ' +
                                str(self.leave_days) + ' days')
                            self.bool_field = False
                        elif (datetime.now() > leave_start_date):
                            self.warning = str(
                                'Please! Always apply preplanned leave before  ' +
                                str(self.leave_days) + ' days')
                            self.bool_field = False
                        else:
                            self.bool_field = True
                else:
                    self.bool_field = True
            else:
                self.bool_field = True
        else:
            self.bool_field = True
