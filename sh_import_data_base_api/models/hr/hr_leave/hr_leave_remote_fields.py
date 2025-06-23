# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class HrLeave(models.Model):
    _inherit = 'hr.leave'
    remote_leave_id = fields.Char("Remote Time Off ID",copy=False)


class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'
    remote_leave_type_id = fields.Char("Remote Leave Type ID",copy=False)


class HrEmployeeCategory(models.Model):
    _inherit = 'hr.employee.category'
    remote_emp_tag_id = fields.Char("Remote Employee Tag ID",copy=False)


class HrLeaveAllocation(models.Model):
    _inherit = 'hr.leave.allocation'
    remote_allocation_id = fields.Char("Remote Allocation ID",copy=False)
