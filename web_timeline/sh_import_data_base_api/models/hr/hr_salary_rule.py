# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class HrSalaryRules(models.Model):
    _inherit = 'hr.salary.rule'

    remote_hr_salary_rule_id = fields.Char("Remote Salary Rule Id",copy=False)


class HrSalaryRulesCat(models.Model):
    _inherit = 'hr.salary.rule.category'

    remote_hr_salary_rule_category_id = fields.Char("Remote Salary Rule Category Id",copy=False)


class HrRulesInput(models.Model):
    _inherit = 'hr.rule.input'

    remote_hr_rule_input_id = fields.Char("Remote Rule Input Id",copy=False)


class HrContributionRegister(models.Model):
    _inherit = 'hr.contribution.register'

    remote_hr_contribution_register_id = fields.Char("Remote Contribution Register Id",copy=False)

class HrCotractGoals(models.Model):
    _inherit = 'hr.contract.goals'

    remote_hr_contract_goals_id = fields.Char("Remote Contract Goals Id",copy=False)

class HrCotractImprovement(models.Model):
    _inherit = 'hr.contract.improvement'

    remote_hr_contract_improvement_id = fields.Char("Remote Contract Improvement Id",copy=False)


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    remote_hr_expense_id = fields.Char("Remote Employee Expense ID",copy=False)

