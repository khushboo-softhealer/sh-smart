# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, _

class Employee(models.AbstractModel):
    _inherit = "hr.employee"

    # def _compute_remaining_leaves(self):
    #     # Overwrite standard method
    #     for employee in self:
    #         data_days = {}
    #         employee.leaves_count = 0.0
    #         paid_leave_type = self.env['hr.leave.type'].sudo().search(
    #             [('allocation_type', '=', 'fixed_allocation')], limit=1)
    #         if paid_leave_type:
    #             employee_id = employee.id

    #             if employee_id:
    #                 data_days = paid_leave_type.get_days(employee_id)

    #             result = data_days.get(paid_leave_type.id, {})
    #             employee.leaves_count = result.get('remaining_leaves', 0)

class EmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    # def _compute_remaining_leaves(self):
    #     # Overwrite standard method
    #     for employee in self:
    #         data_days = {}
    #         employee.leaves_count = 0.0
    #         paid_leave_type = self.env['hr.leave.type'].sudo().search(
    #             [('allocation_type', '=', 'fixed_allocation')], limit=1)
    #         if paid_leave_type:
    #             employee_id = employee.id

    #             if employee_id:
    #                 data_days = paid_leave_type.get_days(employee_id)

    #             result = data_days.get(paid_leave_type.id, {})
    #             employee.leaves_count = result.get('remaining_leaves', 0)
