# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
from datetime import datetime, time
import calendar
from odoo.addons.resource.models.resource import float_to_time
from datetime import date

class HRContract(models.Model):
    _inherit = 'hr.contract'

    def hour_rate(self,employee,working_data_dates,contract_search_date):
        per_hour_rate = 0
        if employee and employee.contract_id:
            related_contract = self.sudo().search([('employee_id','=',employee.id),
                                                                      ('date_start','<=',contract_search_date),
                                                                      ('date_end','>=',contract_search_date),
                                                                      ('state','!=','cancel')],limit=1)
            # related_contract = employee.contract_id
            if related_contract:
                # compute worked days
                if working_data_dates:
                    first_day = working_data_dates.date_from
                    last_day = working_data_dates.date_to
                    day_from = datetime.combine(fields.Date.from_string(first_day), time.min)
                    day_to = datetime.combine(fields.Date.from_string(last_day), time.max)
                    work_data = related_contract.employee_id._get_work_days_data_batch(day_from, day_to, calendar=related_contract.resource_calendar_id)
                    total_working_days_of_month = work_data[related_contract.employee_id.id]['days'] or 24
                    perday_avg_hours = related_contract.resource_calendar_id.hours_per_day or 8.5
                    wage =  related_contract.wage
                    per_hour_rate = wage / (total_working_days_of_month * perday_avg_hours)
                    day = per_hour_rate * 8.5
        return per_hour_rate
    
    def get_over_time_data(self, employee, payslip):
        overtime = 0
        try: 
            if employee :
                ot_employees = self.env['sh.employee.ot'].search([('sh_employee_id','=',employee.id),('sh_ot_date', '>=', payslip.date_from), ('sh_ot_date', '<=', payslip.date_to),('state','=','done')])
                float_time = 0
                ot_date = False
                for ot in ot_employees:
                    float_time += ot.sh_total_timesheet
                    ot_date = ot.sh_ot_date

                hours_rate = self.hour_rate(employee,payslip,ot_date)
                f_time = float_to_time(float_time)
                hours,minutes = f_time.hour,f_time.minute
                total_minutes = (hours*60) + minutes
                overtime = (hours_rate/60)*total_minutes
            return overtime
        except Exception as e:
            return overtime 
