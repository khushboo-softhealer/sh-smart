# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, api



class HRPublic(models.Model):
    _inherit = 'hr.employee.public'

    # date_of_joining = fields.Date("Date of Joining")


class HR(models.Model):
    _inherit = 'hr.employee'

    date_of_joining = fields.Date("Date of Joining")


