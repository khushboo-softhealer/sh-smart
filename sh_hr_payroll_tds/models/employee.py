# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
from datetime import date, datetime, time
from pytz import timezone

class Company(models.Model):
    _inherit = 'res.company'

    is_applicable_for_tds = fields.Boolean("Is applicable for TDS ?")

class FuturePayslipIncome(models.Model):
    _name = 'future.payslip.monthly.income'
    _description = "Future Payslip Income"

    employee_id = fields.Many2one('hr.employee',string="")
    month = fields.Integer("Future Month")
    amount = fields.Float("Amount")

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = 'Employee'

    is_applicable_for_tds = fields.Boolean("Is applicable for TDS ?",related='company_id.is_applicable_for_tds')
    employee_contract_type = fields.Selection([('contractual','Contractual'),
                                      ('salaries','Salaried')], string=" Contract Type")
    tds_scheme_type = fields.Selection([('old','Old Regime'),
                                      ('new','New Regime')],default='old', string="TDS Scheme")
    
    having_uan_number = fields.Boolean("Having UAN Number ?")
    uan_number = fields.Char("UAN Number")

    future_payslip_monthly_income_calculation_ids = fields.One2many("future.payslip.monthly.income",
                                                                    'employee_id',string="")
    

    
    
    def get_basic_salary_salaried(self, wage,contract, payslip):
        basic_amount = 0.0

        employee_id = self.id
        contract_id = contract.id
        contract_wage = wage
        payslip_id = payslip.id
        batch_id = payslip.payslip_run_id.id

        batch_start_date = payslip.payslip_run_id.date_start
        batch_end_date = payslip.payslip_run_id.date_end

        payslip_start_date = payslip.date_from
        payslip_end_date = payslip.date_to


        #find work 100
        
        batch_work100_days = self.sh_get_work100_number_of_days(batch_start_date, batch_end_date,contract)
        batch_number_of_days = batch_work100_days[0]
        batch_number_of_hours = batch_work100_days[1]


        payslip_work100_days = self.sh_get_work100_number_of_days(payslip_start_date, payslip_end_date,contract)
        payslip_number_of_days = payslip_work100_days[0]
        payslip_number_of_hours = payslip_work100_days[1]


        # compute gloabl holidays
        batch_leave_days = self.sh_get_leave_details_of_employees(batch_start_date,batch_end_date,contract)
        batch_gloabl_number_of_days = batch_leave_days[0]
        batch_global_number_of_hours = batch_leave_days[1]
        batch_unpaid_number_of_days = batch_leave_days[2]
        batch_unpaid_number_of_hours = batch_leave_days[3]


        payslip_leave_days = self.sh_get_leave_details_of_employees(payslip_start_date,payslip_end_date,contract)
        payslip_gloabl_number_of_days = payslip_leave_days[0]
        payslip_global_number_of_hours = payslip_leave_days[1]
        payslip_unpaid_number_of_days = payslip_leave_days[2]
        payslip_unpaid_number_of_hours = payslip_leave_days[3]
        

        batch_total_working_days = batch_number_of_days + batch_unpaid_number_of_days
        payslip_total_working_days = payslip_number_of_days + payslip_unpaid_number_of_days
        
        basic_amount = (contract_wage/batch_total_working_days) * (payslip_total_working_days)

        return basic_amount