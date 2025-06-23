# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields


class ContractGoals(models.Model):
    _name = 'hr.contract.goals'
    _description = "Contract goals"

    name = fields.Char("Description")
    contract_id = fields.Many2one('hr.contract')
    sequence = fields.Integer()
    goal_sheet_id = fields.Many2one("sh.goal.sheet")

