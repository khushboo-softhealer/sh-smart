# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class HrContract(models.Model):
    _inherit = 'hr.contract'

    remote_hr_contract_id = fields.Char("Remote Contract Id",copy=False)

class HrContractType(models.Model):
    _inherit = 'hr.contract.type'

    remote_hr_contract_type_id = fields.Char("Remote Contract Type Id",copy=False)

class HrDepartment(models.Model):
    _inherit = 'hr.department'

    remote_hr_department_id = fields.Char("Remote department ID",copy=False)

class HrJob(models.Model):
    _inherit = 'hr.job'

    remote_hr_job_id = fields.Char("Remote Job ID",copy=False)

