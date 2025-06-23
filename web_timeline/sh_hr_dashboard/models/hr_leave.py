# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import _, api, fields, models

class HrLeave(models.Model):
    
    _inherit = 'hr.leave'

    def request_unit_hours_get_value(self,key):
        hours = dict(self._fields['request_hour_from'].selection).get(key)
        return hours
