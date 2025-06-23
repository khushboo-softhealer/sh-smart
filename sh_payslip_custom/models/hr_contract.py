# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp
from odoo import api, fields, models, tools, _


class Contract(models.Model):
    _inherit = 'hr.contract'

    leave_payment_done = fields.Boolean("Leave Payment Done ?")
