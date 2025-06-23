# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import _, api, fields, models
from datetime import datetime
import pytz
class ShPublicHolidayLine(models.Model):
    _name = "sh.public.holiday.line"
    _description = "Sh Public Holiday Line"

    sh_public_holiday_id = fields.Many2one("sh.public.holiday", string="id")

    name = fields.Char(string="Reason")
    sh_start_date = fields.Datetime(string="Start Date", default=datetime.now())
    sh_end_date = fields.Datetime(string="End Date", default=datetime.now())

    @api.model
    def default_get(self, field):
        res = super().default_get(field)
        user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')

        if 'sh_start_date' in field:
            start_date = user_tz.localize(fields.Datetime.now().replace(hour=00, minute=00, second=00))
            res.update({'sh_start_date':start_date.astimezone(pytz.timezone('UTC')).replace(tzinfo=None)})
        if 'sh_end_date' in field:
            end_date = user_tz.localize(fields.Datetime.now().replace(hour=23, minute=59, second=59))
            res.update({'sh_end_date':end_date.astimezone(pytz.timezone('UTC')).replace(tzinfo=None)})
    
        return res
