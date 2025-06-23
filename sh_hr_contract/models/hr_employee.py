# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    total_overtime = fields.Float(
        compute='_compute_total_overtime', compute_sudo=True,groups=False
        # groups="hr_attendance.group_hr_attendance_kiosk,hr_attendance.group_hr_attendance,hr.group_hr_user"
        )

    hr_manager = fields.Many2one('hr.employee')
    is_remote_employee = fields.Boolean("Allow Task Without Checkin ?")


    @api.onchange('coach_id')
    def _onchange_coach_id(self):
        if self.coach_id and self.coach_id.user_id:
            self.leave_manager_id = self.coach_id.user_id.id

class HrEmployee(models.Model):
    _inherit = 'hr.employee.public'

    hr_manager = fields.Many2one('hr.employee')
    is_remote_employee = fields.Boolean("Allow Task Without Checkin ?")
