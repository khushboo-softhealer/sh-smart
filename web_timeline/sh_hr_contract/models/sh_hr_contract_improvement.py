# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields


class ContractImprovement(models.Model):
    _name = 'hr.contract.improvement'
    _description = "Contract Improvement"

    name = fields.Char("Description")
    contract_id = fields.Many2one('hr.contract')
    sequence = fields.Integer()
    goal_sheet_id = fields.Many2one("sh.goal.sheet")
