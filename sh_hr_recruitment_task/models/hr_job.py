# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields


class HrJob(models.Model):
    _inherit = "hr.job"

    min_salary = fields.Float("Minimun Salary")
    max_salary = fields.Float("Maximum Salary")