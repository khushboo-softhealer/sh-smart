# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, api
from datetime import date, datetime, time
from pytz import timezone

class DeductionDetails(models.Model):
    _name = 'contract.tds.deduction'
    _description = "Deduction Details"

    contract_id = fields.Many2one("hr.contract",string="Contract")
    line_ids = fields.One2many("contract.tds.deduction.line",'dedution_id',string="")


class DeductionDetailsLine(models.Model):
    _name = 'contract.tds.deduction.line'
    _description = "Deduction Details Line"

    dedution_id = fields.Many2one("contract.tds.deduction")
    name = fields.Char("Deduction")
    amount = fields.Float("Amount")

class TDSSlabOld(models.Model):
    _name = 'contract.tds.slab'
    _description = 'Contract Tax Slab'

    from_amount = fields.Float("From")
    to_amount = fields.Float("Upto")
    tax_rate = fields.Float("Tax Rate(%)")
    contract_id = fields.Many2one("hr.contract",string="Contract")
    payslip_id = fields.Many2one("hr.payslip",string="Payslip")
    actual_amount = fields.Float("Tax Amount",compute='_compute_taxable_amount')

    @api.depends('from_amount','to_amount','tax_rate','contract_id.net_pay_monthly','contract_id.other_income','contract_id.other_deductions',
                 'contract_id.perquisites','contract_id.standard_deduction')
    def _compute_taxable_amount(self):
        for rec in self:
            rec.actual_amount = 0.0
            if rec.contract_id:
                net_yearaly_income = rec.contract_id.net_yearaly_income
                if net_yearaly_income >= rec.from_amount and net_yearaly_income <= rec.to_amount:
                    rec.actual_amount = (net_yearaly_income - rec.from_amount) * (rec.tax_rate/100)
                if net_yearaly_income >= rec.from_amount and net_yearaly_income >= rec.to_amount:
                    rec.actual_amount = (rec.to_amount-rec.from_amount) * (rec.tax_rate/100)
                if net_yearaly_income <= rec.from_amount:
                    rec.actual_amount = 0.0
            if rec.payslip_id:
                net_yearaly_income = rec.payslip_id.net_yearaly_income
                if net_yearaly_income >= rec.from_amount and net_yearaly_income <= rec.to_amount:
                    rec.actual_amount = (net_yearaly_income - rec.from_amount) * (rec.tax_rate/100)
                if net_yearaly_income >= rec.from_amount and net_yearaly_income >= rec.to_amount:
                    rec.actual_amount = (rec.to_amount-rec.from_amount) * (rec.tax_rate/100)
                if net_yearaly_income <= rec.from_amount:
                    rec.actual_amount = 0.0


class EmployeeContract(models.Model):
    _inherit = 'hr.contract'

    is_applicable_for_tds = fields.Boolean("Is applicable for TDS ?")
    employee_contract_type = fields.Selection([('contractual','Contractual'),
                                      ('salaries','Salaried')], string="Contract Type ")
    tds_scheme_type = fields.Selection([('old','Old Regime'),
                                      ('new','New Regime')],default='old', string="TDS Scheme")
    
    tds_percentage = fields.Float("TDS(%)",default="2")
    
    basic_salary_perc = fields.Float("Basic Salary(%)",default="35")
    dearness_allowance_perc = fields.Float("Dearness Allowance(%)",default="13")
    special_allowance_perc = fields.Float("Special Allowance(%)",default="10")
    travelling_allowance_perc = fields.Float("Travelling Allowance(%)",default="10")
    house_rent_allowance_perc = fields.Float("House Rent Allowance(%)",default="12")
    convenyance_allowance_perc = fields.Float("Convenyance Allowance(%)",default="10")
    other_allowance_perc = fields.Float("Other Allowance(%)",default="10")

    basic_salary = fields.Float("Basic Salary")
    dearness_allowance = fields.Float("Dearness Allowance")
    special_allowance = fields.Float("Special Allowance")
    travelling_allowance = fields.Float("Travelling Allowance")
    house_rent_allowance = fields.Float("House Rent Allowance")
    convenyance_allowance = fields.Float("Convenyance Allowance")
    other_allowance = fields.Float("Other Allowance")

    net_pay_monthly = fields.Float("Net Pay (Monthly)",compute='compute_monthly_income')
    net_pay_yearly = fields.Float("Net Pay (Yearly)",compute='compute_net_yearly_income')
    other_income = fields.Float("Other Income")
    perquisites=fields.Float("Perquisites")
    standard_deduction = fields.Float("Standard Deduction",default=50000)
    other_deductions = fields.Float("Deductions")
    net_yearaly_income = fields.Float("Net Yearly Income",compute='compute_net_yearly_income')

    slab_template_id = fields.Many2one("tax.slab.template",string="Please choose Tax Slab")
    contract_tds_slab_ids = fields.One2many('contract.tds.slab','contract_id',string="TDS Slab")
    total_tax_before_cess = fields.Float("TAX BEFORE EDUCATION CESS", compute="_compute_tax_before_edu_cess")

    rebate_taxable_limit = fields.Float("Taxable income")
    rebate_tax_relief_limit = fields.Float("Tax Relief")
    education_cess = fields.Float("Education Cess(%)")

    net_tax_payable_yearly = fields.Float("NET TAX PAYABLE",compute="_compute_net_tax_payable")
    net_tax_payable_monthly = fields.Float("NET TAX PAYABLE EVERY MONTH",compute="_compute_net_tax_payable")

    def check_deduction_details(self):
        res_id = self.env['contract.tds.deduction'].sudo().search([('contract_id','=',self.id)])
        if res_id:
            return {
                'name': 'Deduction Details',
                'type': 'ir.actions.act_window',
                'res_model': 'contract.tds.deduction',
                'view_type': 'form',
                'view_mode': 'form',
                'domain': [('contract_id', '=', self.id)],
                'context': {'default_contract_id': self.id},
                'target': 'new',
                'res_id':res_id.id
            }
        else:
            return {
                'name': 'Deduction Details',
                'type': 'ir.actions.act_window',
                'res_model': 'contract.tds.deduction',
                'view_type': 'form',
                'view_mode': 'form',
                'domain': [('contract_id', '=', self.id)],
                'context': {'default_contract_id': self.id},
                'target': 'new',
            }


    @api.depends('employee_id')
    def _compute_employee_contract(self):
        for contract in self.filtered('employee_id'):
            contract.job_id = contract.employee_id.job_id
            contract.department_id = contract.employee_id.department_id
            contract.resource_calendar_id = contract.employee_id.resource_calendar_id
            contract.company_id = contract.employee_id.company_id
            contract.is_applicable_for_tds = contract.employee_id.is_applicable_for_tds
            contract.employee_contract_type = contract.employee_id.employee_contract_type
            contract.tds_scheme_type = contract.employee_id.tds_scheme_type



    @api.onchange('slab_template_id')
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

    @api.depends('rebate_taxable_limit','rebate_tax_relief_limit','education_cess','total_tax_before_cess')
    def _compute_net_tax_payable(self):
        for rec in self:
            if rec.net_yearaly_income <= rec.rebate_taxable_limit:
                rec.net_tax_payable_yearly = 0.0
                rec.net_tax_payable_monthly = 0.0
            
            elif rec.net_yearaly_income > rec.rebate_taxable_limit:
                # taxable_amount = rec.total_tax_before_cess - rec.rebate_tax_relief_limit
                taxable_amount = rec.total_tax_before_cess
                rec.net_tax_payable_yearly =taxable_amount +  (taxable_amount * (rec.education_cess/100))
                rec.net_tax_payable_monthly = rec.net_tax_payable_yearly /12


    @api.depends('contract_tds_slab_ids.actual_amount')
    def _compute_tax_before_edu_cess(self):
        for rec in self:
            rec.total_tax_before_cess = 0.0
            for line in rec.contract_tds_slab_ids:
                rec.total_tax_before_cess += line.actual_amount


    @api.depends('wage','basic_salary','dearness_allowance')
    def compute_monthly_income(self):
        for rec in self:
            rec.net_pay_monthly = rec.wage
            # deduct pt
            if rec.wage >12000:
                rec.net_pay_monthly -= 200
            if rec.employee_id.having_uan_number or (rec.basic_salary+rec.dearness_allowance) < 15000:
                if (rec.basic_salary+rec.dearness_allowance)*0.12 <1800:
                    rec.net_pay_monthly -= (rec.basic_salary+rec.dearness_allowance)*0.12
                else:
                    rec.net_pay_monthly -= 1800
            


    @api.depends('net_yearaly_income','net_pay_monthly','other_income','other_deductions','standard_deduction','perquisites')
    def compute_net_yearly_income(self):
        for rec in self:
            rec.net_pay_yearly = 12 * rec.net_pay_monthly
            rec.net_yearaly_income = 0.0
            if rec.tds_scheme_type == 'old':
                rec.net_yearaly_income = rec.net_pay_yearly + rec.other_income +rec.perquisites - rec.other_deductions -rec.standard_deduction
            elif rec.tds_scheme_type == 'new':
                rec.net_yearaly_income = rec.net_pay_yearly + rec.other_income +rec.perquisites - rec.standard_deduction


    @api.onchange('employee_contract_type','wage','tds_scheme_type','is_applicable_for_tds','employee_id','company_id',
                  'basic_salary_perc','dearness_allowance_perc','special_allowance_perc',
                  'travelling_allowance_perc','house_rent_allowance_perc','convenyance_allowance_perc',
                  'other_allowance_perc')
    def _onchange_contract_type(self):
        if self.is_applicable_for_tds and self.wage >0:
            self.basic_salary = self.wage * (self.basic_salary_perc /100)
            self.dearness_allowance = self.wage * (self.dearness_allowance_perc /100)
            self.special_allowance = self.wage * (self.special_allowance_perc /100)
            self.travelling_allowance = self.wage * (self.travelling_allowance_perc /100)
            self.house_rent_allowance = self.wage * (self.house_rent_allowance_perc /100)
            self.convenyance_allowance = self.wage * (self.convenyance_allowance_perc /100)
            self.other_allowance = self.wage * (self.other_allowance_perc /100)

        # Auto select salary structure based on selection
        if not self.is_applicable_for_tds and self.env.ref('sh_hr_payroll_tds.structure_base_employee'):

            self.struct_id = self.env.ref('sh_hr_payroll_tds.structure_base_employee').id

        if self.is_applicable_for_tds:
            if self.employee_contract_type == 'salaries':
                if self.tds_scheme_type == 'old' and self.env.ref('sh_hr_payroll_tds.structure_salaries_employee_old_scheme'):
                    self.struct_id = self.env.ref('sh_hr_payroll_tds.structure_salaries_employee_old_scheme').id
                elif self.tds_scheme_type == 'new' and self.env.ref('sh_hr_payroll_tds.structure_salaries_employee_new_scheme'):
                    self.struct_id = self.env.ref('sh_hr_payroll_tds.structure_salaries_employee_new_scheme').id
            elif self.employee_contract_type == 'contractual' and self.env.ref('sh_hr_payroll_tds.structure_contractual_employee'):
                    self.struct_id = self.env.ref('sh_hr_payroll_tds.structure_contractual_employee').id

