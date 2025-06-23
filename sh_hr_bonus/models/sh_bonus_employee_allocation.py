# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import api, fields, models
from datetime import date
from dateutil.relativedelta import relativedelta
import calendar


class BonusEmployeeAllocation(models.Model):
    _name = 'sh.bonus.employee.allocation'
    _description = "Bonus Employee Allocation"

    employee_id = fields.Many2one('hr.employee', string="Employee")
    joining_date = fields.Date(related="employee_id.date_of_joining", store=True)
    contract_1_wage = fields.Float()
    contract_2_wage = fields.Float()
    average_wage = fields.Float()
    total_month = fields.Float(compute="compute_total_month", store=True)
    allocated_bonus_per = fields.Float(
        string="Allocated Bonus Per(%)", compute="compute_allocated_bonus_per", store=True)
    bonus_amount = fields.Float(compute="compute_bonus_amount", store=True)
    bonus_allocation_id = fields.Many2one('sh.bonus.allocation')
    actual_bonus_amount = fields.Float("Actual Bonus Amount")

    @api.depends('joining_date')
    def compute_total_month(self):
        today = date.today()
        for rec in self:
            if rec.joining_date:
                rdelta = relativedelta(today, rec.joining_date)
                current_month_days = calendar.mdays[today.month]
                rdelta_days = rdelta.days
                total_month = round(
                    (rdelta.years * 12) + (rdelta.months) + (rdelta_days/current_month_days))
                rec.total_month = total_month

    @api.depends('total_month')
    def compute_allocated_bonus_per(self):
        for rec in self:
            if rec.total_month != 0:
                related_allocation = rec.bonus_allocation_id.bonus_template_id.bonus_template_line.filtered(
                    lambda x: x.from_month < rec.total_month and x.to_month > rec.total_month)

                if not related_allocation:
                    related_allocation = rec.bonus_allocation_id.bonus_template_id.bonus_template_line.filtered(
                        lambda x: x.from_month == rec.total_month)

                if not related_allocation:
                    related_allocation = rec.bonus_allocation_id.bonus_template_id.bonus_template_line.filtered(
                        lambda x: x.to_month == rec.total_month)

                if related_allocation:
                    rec.allocated_bonus_per = related_allocation[0].bonus

    @api.depends('average_wage', 'allocated_bonus_per')
    def compute_bonus_amount(self):
        for rec in self:
            if rec.average_wage != 0 and rec.allocated_bonus_per != 0:
                rec.bonus_amount = (rec.average_wage *
                                    rec.allocated_bonus_per)/100
