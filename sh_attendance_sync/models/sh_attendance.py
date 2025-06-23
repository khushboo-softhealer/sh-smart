# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields
import requests
import json
from datetime import datetime, timedelta
import logging
_logger = logging.getLogger(__name__)


class ShAttendance(models.Model):
    _inherit = 'hr.attendance'

    sh_remark = fields.Char('Remarks')
    sh_duration = fields.Char('Duration ', compute='_get_duration')

    def _get_duration(self):
        if self:
            for rec in self:
                rec.sh_duration = ''
                if rec.check_in and rec.check_out:
                    duration = str(rec.check_out - rec.check_in)
                    split_value = duration.strip()[:-3]
                    final_value = split_value.split(':')
                    rec.sh_duration = final_value[0] + \
                        ' Hours ' + final_value[1] + ' Minutes'