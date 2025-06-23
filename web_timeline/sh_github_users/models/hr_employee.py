# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class GitEmployee(models.Model):
    _inherit = 'hr.employee'

    gituser_name = fields.Char("Github Username")


class GitEmployee(models.Model):
    _inherit = 'hr.employee.public'

    gituser_name = fields.Char("Github Username")
