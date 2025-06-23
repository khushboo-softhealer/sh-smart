# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models


class ShEmployeeManagerUpdateMassTagWizard(models.TransientModel):
    _name = "sh.employee.manager.update.mass.tag.wizard"
    _description = "Mass Tag Update Wizard"

    all_hr_employee_ids = fields.Many2many('hr.employee')
    update_job_position_bool = fields.Boolean(string="Update Job Position")
    update_job_position_id = fields.Many2one('hr.job', string="Jobs")
    update_hr_manager_bool = fields.Boolean(string="HR Manager")
    update_hr_manager = fields.Many2one('hr.employee', string="Manager")
    update_emp_manager_bool = fields.Boolean(string="Update Manager")
    update_emp_manager = fields.Many2one('hr.employee', string=" Manager")
    update_coach_bool = fields.Boolean(string="Update Coach")
    update_coach_id = fields.Many2one('hr.employee', string='Coach')

    def update_mass_employee_details(self):
        if self.update_job_position_bool:
            self.all_hr_employee_ids.write(
                {'job_id': self.update_job_position_id.id})

        if self.update_hr_manager_bool:
            self.all_hr_employee_ids.write(
                {'hr_manager': self.update_hr_manager.id})

        if self.update_emp_manager_bool:
            self.all_hr_employee_ids.write(
                {'parent_id': self.update_emp_manager.id})

        if self.update_coach_bool:
            self.all_hr_employee_ids.write(
                {'coach_id': self.update_coach_id.id})
