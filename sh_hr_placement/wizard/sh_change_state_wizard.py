# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models


class ShChangeStateWizard(models.TransientModel):
    _name = 'sh.change.state.wizard'
    _description = 'Change State of HR Applicant'

    stage_id = fields.Many2one(
        'hr.recruitment.stage', string="State", required=True)
    schedule_datetime = fields.Datetime(string="Schedule")

    def change_state_action(self):
        context = self.env.context or {}
        if context and context.get("active_ids", False):
            active_ids = context.get('active_ids')
            applicant = self.env["hr.applicant"].browse(active_ids)

            if applicant:
                applicant.sudo().write({
                    "stage_id": self.stage_id.id,
                    "sh_hr_placement_is_confirm": False,
                    "sh_hr_placement_schedule_datetime": False,
                })
