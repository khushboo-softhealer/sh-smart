# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models


class ShChangeDatetimeWizard(models.TransientModel):
    _name = 'sh.change.datetime.wizard'
    _description = 'Change Datetime of HR Applicant'

    schedule_datetime = fields.Datetime(string="Schedule")

    def change_datetime_action(self):
        context = self.env.context or {}
        if context and context.get("active_ids", False):
            active_ids = context.get('active_ids')
            applicant = self.env["hr.applicant"].browse(active_ids)

            if applicant:
                applicant.sudo().write({
                    "sh_hr_placement_schedule_datetime": self.schedule_datetime,
                })
