# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError



class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    resource_calendar_id = fields.Many2one('resource.calendar', domain="[]")
    coach_id = fields.Many2one(
        'hr.employee', 'Coach', compute='_compute_coach', store=True, readonly=False,
        help='Select the "Employee" who is the coach of this employee.\n'
             'The "Coach" has no specific rights or responsibilities by default.', domain="[]")
    parent_id = fields.Many2one('hr.employee', 'Manager', compute="_compute_parent_id", store=True, readonly=False, domain="[]")
    job_id = fields.Many2one('hr.job', 'Job Position', domain="[]")
    department_id = fields.Many2one('hr.department', 'Department', domain="[]")
    address_id = fields.Many2one('res.partner', 'Work Address', compute="_compute_address_id", store=True, readonly=False, domain="[]")
    

class Contract(models.Model):
    _inherit = 'hr.contract'

    resource_calendar_id = fields.Many2one(
        'resource.calendar', 'Working Schedule', compute='_compute_employee_contract', store=True, readonly=False,
        default=lambda self: self.env.company.resource_calendar_id.id, copy=False, index=True,
        domain="[]")
   