# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ShCompanyFacilities(models.Model):
    _inherit = 'sh.company.facilities'

    remote_sh_company_facilities_id = fields.Char(
        "Remote Company Facilities ID",copy=False)


class ResourceResource(models.Model):
    _inherit = 'resource.resource'

    remote_resource_resource_id = fields.Char("Remote Resource Resource ID",copy=False)


class ShEmpTechnicalSkill(models.Model):
    _inherit = 'sh.emp.technical.skill'

    remote_sh_emp_technical_skill_id = fields.Char(
        "Remote Emp Technical Skill ID",copy=False)


class ShTechnicalSkill(models.Model):
    _inherit = 'sh.technical.skill'

    remote_sh_technical_skill_id = fields.Char(
        "Remote Technical Skill ID",copy=False)


class ShEmployeeReligion(models.Model):
    _inherit = 'sh.employee.religion'
    remote_sh_employee_religion_id = fields.Char("Remote Employee Religion ID",copy=False)
