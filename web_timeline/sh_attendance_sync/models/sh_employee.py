# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields

class Leave(models.Model):
    _inherit = 'hr.leave'

    created_leave = fields.Boolean('created')
    automatic = fields.Boolean('Automatic')
