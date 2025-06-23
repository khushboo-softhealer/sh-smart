# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ShLeaveRequest(models.Model):
    _inherit = "hr.leave"

    sh_leave_req_attachment = fields.Binary("Attachment")
    is_required_attach = fields.Boolean("leave attach", default=False)
    is_sick_leave = fields.Boolean("Sick Leave ?")

    @api.model_create_multi
    def create(self, vals):
        res = super(ShLeaveRequest, self).create(vals)
        if res.number_of_days_display == 0.0 and 'check_validaty' not in self.env.context:
            raise ValidationError("Duration is 0.0 Please check leave again !")
        return res

    @api.onchange("number_of_days_display", "is_sick_leave")
    def _onchange_(self):
        if self.holiday_status_id:
            self.is_required_attach = False
            if self.number_of_days_display >= self.holiday_status_id.no_of_days and self.is_sick_leave:
                self.is_required_attach = True
