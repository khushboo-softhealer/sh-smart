# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from datetime import date, datetime, time
from pytz import timezone


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = 'Employee'

    def sh_get_work100_number_of_days(self,start_date,end_date,contract):
        day_from = datetime.combine(fields.Date.from_string(start_date), time.min)
        day_to = datetime.combine(fields.Date.from_string(end_date), time.max)
        work_data = contract.employee_id._get_work_days_data_batch(day_from, day_to, calendar=contract.resource_calendar_id)
        number_of_days = work_data[contract.employee_id.id]['days']
        number_of_hours = work_data[contract.employee_id.id]['hours']

        return (number_of_days,number_of_hours)

    
    def sh_get_leave_details_of_employees(self,start_date,end_date,contract):
        calendar = contract.resource_calendar_id
        tz = timezone(calendar.tz)
        day_from = datetime.combine(fields.Date.from_string(start_date), time.min)
        day_to = datetime.combine(fields.Date.from_string(end_date), time.max)
        
        day_leave_intervals = contract.employee_id.list_leaves(day_from,day_to,calendar=contract.resource_calendar_id)
        global_number_of_hours = 0.0
        gloabl_number_of_days = 0.0
        unpaid_number_of_hours = 0.0
        unpaid_number_of_days = 0.0
        for day, hours, leave in day_leave_intervals:
            
            holiday = leave[:1].holiday_id

            if holiday.holiday_status_id.name == 'Unpaid':
                unpaid_number_of_hours += hours
            if not holiday.holiday_status_id.name:
                global_number_of_hours += hours

            work_hours = calendar.get_work_hours_count(
                tz.localize(datetime.combine(day, time.min)),
                tz.localize(datetime.combine(day, time.max)),
                compute_leaves=False,
            )
            if work_hours:
                if holiday.holiday_status_id.name == 'Unpaid':
                    unpaid_number_of_days += hours / work_hours
                if not holiday.holiday_status_id.name:
                    gloabl_number_of_days += hours / work_hours

        return (gloabl_number_of_days,global_number_of_hours,unpaid_number_of_days,unpaid_number_of_hours)

    def get_basic_salary(self, contract, payslip):
        basic_amount = 0.0

        employee_id = self.id
        contract_id = contract.id
        contract_wage = contract.wage
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
        

        print("batch_number_of_days",batch_number_of_days,batch_number_of_hours)
        print("batch_gloabl_number_of_days",batch_gloabl_number_of_days,batch_global_number_of_hours)
        print("batch_unpaid_number_of_days",batch_unpaid_number_of_days,batch_unpaid_number_of_hours)

        batch_total_working_days = batch_number_of_days + batch_unpaid_number_of_days
        payslip_total_working_days = payslip_number_of_days + payslip_unpaid_number_of_days
        print("payslip_number_of_days",payslip_number_of_days,payslip_unpaid_number_of_days)
        print("\n\n",contract_wage,batch_total_working_days,payslip_total_working_days)
        basic_amount = (contract_wage/batch_total_working_days) * (payslip_total_working_days)

        return basic_amount
    

    def get_leave_deduction_salary(self, contract, payslip):
        leave_deduction_amount = 0.0
        
        employee_id = self.id
        contract_id = contract.id
        contract_wage = contract.wage
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
        

        print("batch_number_of_days",batch_number_of_days,batch_number_of_hours)
        print("batch_gloabl_number_of_days",batch_gloabl_number_of_days,batch_global_number_of_hours)
        print("batch_unpaid_number_of_days",batch_unpaid_number_of_days,batch_unpaid_number_of_hours)

        batch_total_working_days = batch_number_of_days + batch_unpaid_number_of_days
        payslip_total_working_days = payslip_number_of_days + payslip_unpaid_number_of_days
        
        print("\n\n",contract_wage,batch_total_working_days,payslip_unpaid_number_of_days)
        leave_deduction_amount = (contract_wage/batch_total_working_days) * (payslip_unpaid_number_of_days)

        return leave_deduction_amount * (-1)
    


    slip_ids = fields.One2many(
        'hr.payslip', 'employee_id', string='Payslips', readonly=True)
    payslip_count = fields.Integer(compute='_compute_payslip_count',
                                   string='Payslip Count', groups="sh_hr_payroll.group_hr_payroll_user")

    def _compute_payslip_count(self):
        for employee in self:
            employee.payslip_count = len(employee.slip_ids)


class HrEmployee(models.Model):
    _inherit = 'hr.employee.public'
    _description = 'Employee'

    slip_ids = fields.One2many(
        'hr.payslip', 'employee_id', string='Payslips', readonly=True)
    payslip_count = fields.Integer(compute='_compute_payslip_count',
                                   string='Payslip Count', groups="sh_hr_payroll.group_hr_payroll_user")
