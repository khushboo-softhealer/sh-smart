# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields


class SalaryStructure(models.Model):
    _name = 'sh.salary.structure'
    _description = 'salary structure details'

    name = fields.Char(string='Label')
    sequence = fields.Integer()
    amount = fields.Char()
    contract_id = fields.Many2one('hr.contract')
