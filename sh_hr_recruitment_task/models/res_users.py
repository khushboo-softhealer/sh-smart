# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models
from odoo.http import request

class ResUsers(models.Model):
    _inherit = 'res.users'

    sh_job_applicant_notification_on_off = fields.Boolean(
        'Job Applicant Notification ?')
    display_hr_notification_boolean = fields.Boolean("Display sale order ",compute="_compute_display_hr_notification_boolean",compute_sudo=True)

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + ['sh_job_applicant_notification_on_off','display_hr_notification_boolean']

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + ['sh_job_applicant_notification_on_off','display_hr_notification_boolean']

    def _compute_display_hr_notification_boolean(self):
        if self:
            for rec in self:
                rec.display_hr_notification_boolean=False
                if rec.has_group('hr.group_hr_manager'):
                    rec.display_hr_notification_boolean=True


class Http(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        info = super().session_info()
        user = request.env.user
        info["sh_job_applicant_notification_on_off"] = user.sh_job_applicant_notification_on_off
        info["display_hr_notification_boolean"]=user.display_hr_notification_boolean
        return info
