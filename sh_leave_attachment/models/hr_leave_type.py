# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class ShLeaveType(models.Model):
    _inherit = "hr.leave.type"

    no_of_days = fields.Integer(string="No of Days(Sick Leave)")
