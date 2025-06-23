# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import _, api, fields, models

class HrApplicant(models.Model):
    _inherit = 'hr.applicant'
    _description = "HR Applicant"

    sh_city = fields.Char('City')
    sh_state_id = fields.Many2one('res.country.state')
    sh_country_id = fields.Many2one('res.country')
    sh_current_salary_pm = fields.Char('Current Salary(PM)')
    sh_expected_salary_pm = fields.Char('Expected Salary(PM)')
    sh_notice_period = fields.Char('Notice Period')
    sh_open_to_relocate = fields.Selection([('yes','Yes'),('no','No')])
