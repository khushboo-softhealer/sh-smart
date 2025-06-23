# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models, api, _
from odoo.exceptions import UserError

class ActionMenus(models.Model):
    _inherit = 'sh.attendance.modification.request'

    def action_draft_action(self):

        parent_id = self.env.context.get("active_ids")
        parent_model = self.env.context.get("active_model")
        parent_record = self.env[parent_model].browse(parent_id)

        for rec in parent_record:
            rec.action_draft()

    def action_confirm_action(self):

        parent_id = self.env.context.get("active_ids")
        parent_model = self.env.context.get("active_model")
        parent_record = self.env[parent_model].browse(parent_id)

        for rec in parent_record:
            rec.confirm()

    def action_approve_action(self):
        if self.user_has_groups('hr_attendance.group_hr_attendance_manager'):
            parent_id = self.env.context.get("active_ids")
            parent_model = self.env.context.get("active_model")
            parent_record = self.env[parent_model].browse(parent_id)

            for rec in parent_record:
                rec.approve()
        else:
            raise UserError("You are not Allowed to Approve The Modification Request")

    def action_cancle_action(self):
        parent_id = self.env.context.get("active_ids")
        parent_model = self.env.context.get("active_model")
        parent_record = self.env[parent_model].browse(parent_id)

        for rec in parent_record:
            rec.cancel()
