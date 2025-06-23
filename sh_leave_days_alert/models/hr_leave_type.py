# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models


class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    leave_before_day_alert = fields.Boolean("Leave before day alert")
    leave_before_days = fields.Integer("Leave before days")
