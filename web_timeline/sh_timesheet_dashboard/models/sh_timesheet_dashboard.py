# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models, api


class ShcrmDashboard(models.Model):
    _name = 'sh.timesheet.dashboard'
    _description = 'SH Timesheet Dashboard'

    name = fields.Char('Name')
