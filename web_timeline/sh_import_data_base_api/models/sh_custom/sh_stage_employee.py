# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ShStageEmployee(models.Model):
    _inherit = 'sh.stage.employee'

    remote_sh_stage_employee_id = fields.Char("Remote Stage Employee ID",copy=False)
