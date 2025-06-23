# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models


class BonusTemplate(models.Model):
    _name = 'sh.bonus.template'
    _description = "Bonus Template"

    name = fields.Char(required=True)
    bonus_template_line = fields.One2many(
        'sh.bonus.template.line', 'bonus_template_id', copy=True)
    description = fields.Html()
