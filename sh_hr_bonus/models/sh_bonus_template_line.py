# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models


class BonusTemplateLine(models.Model):
    _name = 'sh.bonus.template.line'
    _description = "Bonus Template Line"

    from_month = fields.Integer(string="From (Month)")
    to_month = fields.Integer(string="To (Month)")
    bonus = fields.Float(string="Bonus(%)")
    bonus_template_id = fields.Many2one('sh.bonus.template')
