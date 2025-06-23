# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import _, api, fields, models
from datetime import datetime, timedelta, date
from odoo.tools import DotDict


class ShLeaveEncasement(models.Model):
    _name = "sh.leave.encasement"
    _description = "Sh Leave Encasement"
    _rec_name = 'employee'

    employee = fields.Many2one('hr.employee',string="Employee")
    contract_start = fields.Date('Start Date')  
    contract_end = fields.Date('End Date')  
    total_leave = fields.Float("Total Leave(Days)")
    remaining_leave = fields.Float("Remaining Leave(Days)")
    leave_encasement = fields.Float("Total Leave Encasement")
    current_contract_id = fields.Many2one("hr.contract",string="Current Contract")
    stage = fields.Selection([('unpaid','Unpaid'),
                              ('paid','Paid'),
                              ('cancel','Canceled'),])
   
    def cancel_encasement(self):
        self.stage = 'cancel'

    # def sh_leave_encasement_cron(self):
        
    #     employee = self.env['hr.employee'].sudo().search([('id','=',135)])
    #     hr_contract = self.env['hr.contract']
    #     print(f"\n\n\n\t--------------> 21 date.today()",date.today())
    #     print(f"\n\n\n\t--------------> 22 employee.contract_id.date_end - timedelta(days=1)",employee.contract_id.date_end - timedelta(days=1))
    #     if date.today() == (employee.contract_id.date_end - timedelta(days=1)) and employee.remaining_leaves:
            
    #         print(f"\n\n\n\t--------------> 20 employee.name",employee.name)
    #         print(f"\n\n\n\t--------------> 21 employee.remaining_leave",employee.remaining_leaves)
    #         print(f"\n\n\n\t--------------> 28 employee.leaves_count",employee.leaves_count)
    #         print(f"\n\n\n\t--------------> 30 hr_contract",hr_contract)
    #         day_rate = 93.137254902 * 8.5
    #         print(f"\n\n\n\t--------------> 32 hours_rate",day_rate)
    #         domain = [
    #                     ('employee', '=', employee.id),
    #                     ('contract_start', '=', employee.contract_id.date_start),
    #                     ('contract_end', '=', employee.contract_id.date_end),
    #                 ]
            
    #         leave_record = self.env['sh.leave.encasement'].sudo().search(domain)
    #         if not leave_record:
    #             leave_encasement = day_rate * employee.remaining_leaves
    #             vals = {'employee' : employee.id,
    #                     'contract_start' : employee.contract_id.date_start,
    #                     'contract_end' : employee.contract_id.date_end,
    #                     'total_leave': employee.contract_id.allocation_id.number_of_days_display,
    #                     'remaining_leave' : employee.remaining_leaves,
    #                     'leave_encasement' : leave_encasement
    #                     }
    #             self.env['sh.leave.encasement'].sudo().create(vals)
    #             print(f"\n\n\n\t--------------> 35 employee.remaining_leaves",employee.remaining_leaves)
    #             print(f"\n\n\n\t--------------> 33 leave_encasement",leave_encasement)
    #             print(f"\n\n\n\t--------------> 32 hour_rate",day_rate)

    def sh_leave_encasement_cron(self):
        """
        Cron job to process leave encasement for all employees whose contracts 
        are ending tomorrow and have remaining leaves.
        """
        # Get all employees with active contracts
        employees = self.env['hr.employee'].sudo().search([('contract_id', '=', 1027)])
        hr_contract = self.env['hr.contract']

        print(f"\n\n\n\t--------------> 62 employees",employees)
        # Process each employee
        for employee in employees:
            try:
                today = datetime.today()
                first_day = today.replace(day=1)
                last_day = today.replace(day=1) + timedelta(days=32)
                last_day = last_day.replace(day=1) - timedelta(days=1) # Hourly rate * daily hours
                print(f"\n\n\n\t--------------> 73 first_day",first_day.date())
                print(f"\n\n\n\t--------------> 74 last_day",last_day.date())
                month_date={'date_from' : first_day.date(), 
                            'date_to' : last_day.date()}
                working_data_dates = DotDict(month_date)
                print(f"\n\n\n\t--------------> 74 month_date",month_date)
                daily_rate = hr_contract.hour_rate_leave_encasement(employee,working_data_dates) * 8.5  # Hourly rate * daily hours

                print(f"\n\n\n\t--------------> 76 daily_rate",daily_rate)
                # daily_rate = hr_contract.hourly_rate(employee) * 8.5 
                print(f"\n\n\n\t--------------> 69 daily_rate",daily_rate) # Hourly rate * daily hours

                # # Check if today is one day before contract end date
                target_date = employee.contract_id.date_end - timedelta(days=1)
                if date.today() != target_date or not employee.remaining_leaves:
                    continue
                print(f"\n\n\n\t--------------> 98 target_date",target_date)
                # Search for existing leave encasement record
                domain = [
                    ('employee', '=', employee.id),
                    ('contract_start', '=', employee.contract_id.date_start),
                    ('contract_end', '=', employee.contract_id.date_end),
                    ('stage','!=','cancel')
                ]
                print(f"\n\n\n\t--------------> 106 domain",domain)
                leave_record = self.env['sh.leave.encasement'].sudo().search(domain)
                print(f"\n\n\n\t--------------> 108 leave_record",leave_record)
                # Create new record if it doesn't exist
                if not leave_record:
                    leave_encasement_amount = daily_rate * employee.remaining_leaves

                    vals = {
                        'employee': employee.id,
                        'contract_start': employee.contract_id.date_start,
                        'contract_end': employee.contract_id.date_end,
                        'total_leave': employee.contract_id.allocation_id.number_of_days_display,
                        'remaining_leave': employee.remaining_leaves,
                        'leave_encasement': leave_encasement_amount,
                        'current_contract_id' : employee.contract_id.id,
                        'stage':'unpaid',
                    }

                    self.env['sh.leave.encasement'].sudo().create(vals)

            except Exception as e:
                print(f"\n\n\n\t--------------> 110 e",e)
                continue
