# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, api
from datetime import date, datetime, time
from pytz import timezone


class EmployeePayslip(models.Model):
    _inherit = 'hr.payslip'

    wage = fields.Float("Wage")

    is_applicable_for_tds = fields.Boolean("Is applicable for TDS ?",related='contract_id.is_applicable_for_tds')
    employee_contract_type = fields.Selection(string=" Contract Type ",related="contract_id.employee_contract_type")
    tds_scheme_type = fields.Selection([('old','Old Regime'),
                                      ('new','New Regime')],default='old', string="TDS Scheme")
    
    basic_salary = fields.Float("Basic Salary")
    dearness_allowance = fields.Float("Dearness Allowance")
    special_allowance = fields.Float("Special Allowance")
    travelling_allowance = fields.Float("Travelling Allowance")
    house_rent_allowance = fields.Float("House Rent Allowance")
    convenyance_allowance = fields.Float("Convenyance Allowance")
    other_allowance = fields.Float("Other Allowance")

    net_pay_monthly = fields.Float("Net Pay (Monthly)")
    net_pay_yearly = fields.Float("Net Pay (Yearly)")
    other_income = fields.Float("Other Income")
    perquisites=fields.Float("Perquisites")
    standard_deduction = fields.Float("Standard Deduction",default=50000)
    other_deductions = fields.Float("Deductions")
    net_yearaly_income = fields.Float("Net Yearly Income")

    slab_template_id = fields.Many2one("tax.slab.template",string="Please choose Tax Slab")
    contract_tds_slab_ids = fields.One2many('contract.tds.slab','payslip_id',string="TDS Slab")
    total_tax_before_cess = fields.Float("TAX BEFORE EDUCATION CESS", compute="_compute_tax_before_edu_cess")

    rebate_taxable_limit = fields.Float("Taxable income")
    rebate_tax_relief_limit = fields.Float("Tax Relief")
    education_cess = fields.Float("Education Cess(%)")

    net_tax_payable_yearly = fields.Float("NET TAX PAYABLE")
    net_tax_payable_monthly = fields.Float("NET TAX PAYABLE EVERY MONTH")

    def compute_sheet(self):
        for payslip in self:
            if payslip.contract_id:
                payslip.tds_scheme_type = payslip.contract_id.tds_scheme_type
                payslip.wage = payslip.contract_id.wage
                payslip.basic_salary = payslip.contract_id.basic_salary
                payslip.dearness_allowance = payslip.contract_id.dearness_allowance
                payslip.special_allowance = payslip.contract_id.special_allowance
                payslip.travelling_allowance = payslip.contract_id.travelling_allowance
                payslip.house_rent_allowance = payslip.contract_id.house_rent_allowance
                payslip.convenyance_allowance = payslip.contract_id.convenyance_allowance
                payslip.other_allowance = payslip.contract_id.other_allowance
                
                payslip.other_income = payslip.contract_id.other_income
                payslip.perquisites = payslip.contract_id.perquisites
                payslip.standard_deduction = payslip.contract_id.standard_deduction
                payslip.other_deductions = payslip.contract_id.other_deductions
                payslip.slab_template_id = payslip.contract_id.slab_template_id.id
                payslip._onchange_slab_template_id()
                payslip.compute_monthly_income()
                payslip.compute_net_yearly_income()
                payslip._compute_net_tax_payable()
            
            super(EmployeePayslip,self).compute_sheet()
        return True


    def _onchange_slab_template_id(self):
    
        if self.slab_template_id:
            self.contract_tds_slab_ids = False
        if self.slab_template_id.template_line_ids:
            line_list = []
            for line in self.slab_template_id.template_line_ids:
                line_vals = {
                    'from_amount':line.from_amount,
                    'to_amount':line.to_amount,
                    'tax_rate':line.tax_rate
                }
                line_list.append((0, 0, line_vals))
            self.contract_tds_slab_ids = line_list
        self.rebate_taxable_limit = self.slab_template_id.rebate_taxable_limit
        self.rebate_tax_relief_limit = self.slab_template_id.rebate_tax_relief_limit
        self.education_cess = self.slab_template_id.education_cess

    def _compute_net_tax_payable(self):
        for rec in self:
            if rec.net_yearaly_income <= rec.rebate_taxable_limit:
                rec.net_tax_payable_yearly = 0.0
                rec.net_tax_payable_monthly = 0.0
            
            elif rec.net_yearaly_income > rec.rebate_taxable_limit:
                # taxable_amount = rec.total_tax_before_cess - rec.rebate_tax_relief_limit
                taxable_amount = rec.total_tax_before_cess
                rec.net_tax_payable_yearly =taxable_amount +  (taxable_amount * (rec.education_cess/100))
                
                
                current_month = rec.date_from.month
                current_year = rec.date_from.year
                if current_month == '4':
                    # if april then consider 12 month
                    rec.net_tax_payable_monthly = rec.net_tax_payable_yearly /12

                elif current_month < 4:
                    previous_year = current_year-1
                    april_date = date(previous_year, 4, 1)
                    all_old_payslips = self.env['hr.payslip'].sudo().search([('employee_id','=',rec.employee_id.id),
                                                      ('state','=','done'),
                                                      ('date_from','>=',april_date)])
                    old_payslip_with_tds = 0
                    total_month =(4-current_month)
                    old_paid_tax = 0
                    if all_old_payslips:
                        old_payslip_with_tds = all_old_payslips.filtered(lambda x:x.net_tax_payable_monthly >0.0)
                        if old_payslip_with_tds:
                            # total_month += len(old_payslip_with_tds)
                            old_paid_tax +=  sum(old_payslip_with_tds.mapped('net_tax_payable_monthly'))
                    
                    
                    rec.net_tax_payable_monthly = (rec.net_tax_payable_yearly-old_paid_tax) / total_month
                   
                elif current_month > 4:
                    current_year_april_date = date(current_year, 4, 1)
                    all_old_payslips = self.env['hr.payslip'].sudo().search([('employee_id','=',rec.employee_id.id),
                                                      ('state','=','done'),
                                                      ('date_from','>=',current_year_april_date)])
                    
                    total_month =(12-(current_month-1))+3
                    old_payslip_with_tds = 0
                    old_paid_tax = 0
                    if all_old_payslips:
                        old_payslip_with_tds = all_old_payslips.filtered(lambda x:x.net_tax_payable_monthly >0.0)
                        if old_payslip_with_tds:
                            # total_month += len(old_payslip_with_tds)
                            old_paid_tax +=  sum(old_payslip_with_tds.mapped('net_tax_payable_monthly'))
                    
                    rec.net_tax_payable_monthly = (rec.net_tax_payable_yearly-old_paid_tax) / total_month
                
                


    @api.depends('contract_tds_slab_ids.actual_amount')
    def _compute_tax_before_edu_cess(self):
        for rec in self:
            rec.total_tax_before_cess = 0.0
            for line in rec.contract_tds_slab_ids:
                rec.total_tax_before_cess += line.actual_amount


    def compute_monthly_income(self):
        for rec in self:
            rec.net_pay_monthly = rec.contract_id.wage
            # deduct pt
            if rec.contract_id.wage >12000:
                rec.net_pay_monthly -= 200
            if rec.employee_id.having_uan_number or (rec.basic_salary+rec.dearness_allowance) < 15000:
                if (rec.basic_salary+rec.dearness_allowance)*0.12 <1800:
                    rec.net_pay_monthly -= (rec.basic_salary+rec.dearness_allowance)*0.12
                else:
                    rec.net_pay_monthly -= 1800
            # deduct leave
            unpaid_leave_line = rec.worked_days_line_ids.filtered(lambda x:x.code == 'Unpaid')
            if unpaid_leave_line:
                if unpaid_leave_line.number_of_days > 0.0:
                    result=rec.employee_id.get_leave_deduction_salary(rec.contract_id,rec)
                    rec.net_pay_monthly += result

            


    def compute_net_yearly_income(self):
        for rec in self:
            
            # to find yearly income in payslip we need to find nearby March
            # yearly income is sum of old payslip till last april +
            # Curent payslip monthly income +
            # (contract monthly income * remaining month till next march)

            current_month_tds = rec.net_pay_monthly

            current_month = rec.date_from.month
            current_year = rec.date_from.year

            rec.net_pay_yearly = current_month_tds

            if current_month == '4':
                # if april then no need to find previous payslips
                rec.net_pay_yearly += (rec.contract_id.net_pay_monthly * 11)


            elif current_month < 4:
                #Need to find payslip from last year april month
                print()
                previous_year = current_year-1
                april_date = date(previous_year, 4, 1)

                #find all payslip tds amount sum
                all_old_payslips = self.env['hr.payslip'].sudo().search([('employee_id','=',rec.employee_id.id),
                                                      ('state','=','done'),
                                                      ('date_from','>=',april_date)])

                if all_old_payslips:
                    for payslip in all_old_payslips:
                        rec.net_pay_yearly += payslip.net_pay_monthly

                        # #in case of increment add difference amount
                        # if payslip.contract_id != rec.contract_id:
                            


                #compute remaining future payslip till march end
                rec.net_pay_yearly += rec.contract_id.net_pay_monthly * (4-(current_month+1))


            elif current_month > 4:
                # Need to find payslip from current year april Month

                current_year_april_date = date(current_year, 4, 1)
                #find all payslip tds amount sum
                all_old_payslips = self.env['hr.payslip'].sudo().search([('employee_id','=',rec.employee_id.id),
                                                      ('state','=','done'),
                                                      ('date_from','>=',current_year_april_date)])

                if all_old_payslips:
                    for payslip in all_old_payslips:
                        rec.net_pay_yearly += payslip.net_pay_monthly
                    
                #compute remaining future payslip till march end
                rec.net_pay_yearly += rec.contract_id.net_pay_monthly * ((12-current_month)+3)

            rec.net_yearaly_income = 0.0
            if rec.tds_scheme_type == 'old':
                rec.net_yearaly_income = rec.net_pay_yearly + rec.other_income - rec.other_deductions
            elif rec.tds_scheme_type == 'new':
                rec.net_yearaly_income = rec.net_pay_yearly + rec.other_income

