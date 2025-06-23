# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.tools.float_utils import float_round

class Leave(models.AbstractModel):
    _inherit = "hr.leave.allocation"

    date_start = fields.Date()
    date_end = fields.Date()

    @api.depends('number_of_hours_display', 'number_of_days_display')
    def _compute_duration_display(self):
        for allocation in self:
            allocation.duration_display = '%g %s' % (
                (float_round(allocation.number_of_days_display, precision_digits=2)),
                _('days'))