# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models


class HRContract(models.Model):
    _inherit = 'hr.contract'

    def get_bonus_data(self, employee, payslip):
        bonus_amount = 0
        bonus_allocation = self.env['sh.bonus.allocation'].search(
            [('application_date', '>=', payslip.date_from), ('application_date', '<=', payslip.date_to)])

        if bonus_allocation:
            bonus_employee = bonus_allocation[0].bonus_employee_allocation_line.filtered(
                lambda x: x.employee_id.id == employee.id)
            bonus_amount = bonus_employee.bonus_amount

        return bonus_amount
