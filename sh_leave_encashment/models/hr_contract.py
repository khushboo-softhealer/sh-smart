# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
from datetime import datetime, time


class HRContract(models.Model):
    _inherit = 'hr.contract'

    def get_leave_encashment_data(self, employee, payslip):
        leave_encasement = 0
        try:
            if employee and payslip:
            
                hr_employee = self.sudo().env['hr.employee']
                hr_employee.get_leave_deduction_salary()
                month = f"%-{payslip.date_to.strftime('%m')}-%"
                # search record with the corrected pattern of month
                leave_record = self.env['sh.leave.encasement'].sudo().search([('employee', '=', employee.id),('current_contract_id', '=',payslip.contract_id.id ),('stage','not in',['paid','cancel'])], limit=1)
                print(f"\n\n\n\t--------------> 19 leave_record",leave_record)
                if leave_record:
                    leave_encasement = leave_record.leave_encasement
                print(f"\n\n\n\t--------------> 22 leave_encasement",leave_encasement)
        except Exception as e:        
            print(f"\n\n\n\t--------------> 23 e",e)
        return leave_encasement
    
    
    def hour_rate_leave_encasement(self,employee,working_data_dates):
        print(f"\n\n\n\t--------------> 14 self.read()",self.read())
        print(f"\n\n\n\t--------------> 15 working_data_dates",working_data_dates)
        per_hour_rate = 0
        if employee and employee.contract_id:
            related_contract = employee.contract_id
            if related_contract:
                # compute worked days
                if working_data_dates:
                    first_day = working_data_dates.date_from
                    last_day = working_data_dates.date_to
                    per_day_avg_hours = related_contract.resource_calendar_id.hours_per_day or 8.5
                    print(f"\n\n\n\t--------------> 39 {'holiday_status_id.requires_allocation','=','No',' ------- date_from','<=',first_day,' ------- date_to','>=',last_day}",)
                    unpaid_leaves = self.env['hr.leave'].sudo().search([('employee_ids','in',employee.id),('holiday_status_id.requires_allocation','=','no'),('date_from','>=',first_day),('date_to','<=',last_day),('state','in',['validate','validate1'])])
                    total_unpaid_leaves = sum(unpaid_leaves.mapped('number_of_hours_display'))
                    print(f"\n\n\n\t--------------> 41 unpaid_leaves",unpaid_leaves.mapped('number_of_hours_display'))
                    if total_unpaid_leaves > per_day_avg_hours:
                        total_unpaid_leaves = total_unpaid_leaves / per_day_avg_hours

                    
                    print(f"\n\n\n\t--------------> 41 unpaid_leave",unpaid_leaves)

                    day_from = datetime.combine(fields.Date.from_string(first_day), time.min)
                    day_to = datetime.combine(fields.Date.from_string(last_day), time.max)
                    work_data = related_contract.employee_id._get_work_days_data_batch(day_from, day_to, calendar=related_contract.resource_calendar_id)
                    print(f"\n\n\n\t--------------> 31 work_Data",work_data)


                    total_working_hours_of_month = work_data[related_contract.employee_id.id]['hours'] or 204
                    print(f"\n\n\n\t--------------> 58 total_working_hours_of_month",total_working_hours_of_month)


                    total_working_hours_of_month += total_unpaid_leaves
                    print(f"\n\n\n\t--------------> 60 total_working_hours_of_month",total_working_hours_of_month)


                    total_working_days_of_month = total_working_hours_of_month / per_day_avg_hours
                    print(f"\n\n\n\t--------------> 62 total_working_days_of_month",total_working_days_of_month)
                    print(f"\n\n\n\t--------------> 63 total_working_hours_of_month",total_working_hours_of_month)


                    # total_working_days_of_month = work_data[related_contract.employee_id.id]['days'] or 24
                    # print(f"\n\n\n\t--------------> 65 total_working_days_of_month",total_working_days_of_month)
                    # total_working_days_of_month += total_unpaid_leaves


                    print(f"\n\n\n\t--------------> 67 total_unpaid_leaves",total_unpaid_leaves)
                    print(f"\n\n\n\t--------------> 68 total_working_days_of_month",total_working_days_of_month)

                    wage =  related_contract.wage
                    per_hour_rate = wage / (total_working_days_of_month * per_day_avg_hours)
                    day = per_hour_rate * 8.5
        return per_hour_rate
        