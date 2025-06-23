# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def _letter_count(self):
        oe_letter = self.env['sh.letter']
        for pa in self:
            domain = [('employee_id', '=', pa.id)]
            letter_ids = oe_letter.search(domain)
            letters = oe_letter.browse(letter_ids)
            letter_count = 0
            for _ in letters:
                letter_count += 1
            pa.letter_count = letter_count

        return True

    letter_count = fields.Integer(compute=_letter_count, string="Letter")
