# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import api, fields, models,_
from odoo.exceptions import UserError
from datetime import datetime, timedelta
import calendar
from dateutil.relativedelta import relativedelta
import pytz

class Employee(models.Model):
    _inherit = 'hr.employee'

    @api.onchange('job_id')
    def _onchange_job_employee(self):
        if self.job_id and self.user_id and self.job_id.sh_user_access_template:
            self.user_id.template_ids = [(6,0,[self.job_id.sh_user_access_template.id])]


class HrJob(models.Model):
    _inherit = "hr.job"

    sh_user_access_template = fields.Many2one("sh.template",string="User Access Template")

class Contract(models.Model):
    _inherit = 'hr.contract'
    _order = 'date_start, id desc'
    
    previous_contract_wage = fields.Float(string='Previous Contract Wedge',compute='_compute_previous_contract_wedge')
    increment_offer_amount = fields.Float(string="Increment Offer Amount",compute='_compute_previous_contract_wedge')
    increment_offer_percentage = fields.Float(string="Increment Offer (%) ",compute='_compute_previous_contract_wedge')
   
    hr_contract_ids = fields.Many2many('hr.contract', 'hr_contract_hr_contact_rel','hr_contract_id', 'new_hr_contract_id',string="Previous Contract")
    
    paid_leaves = fields.Float('Paid Leaves')
    unpaid_leaves = fields.Float('Unpaid Leaves')
    total_leaves_taken = fields.Float('Total Leave Taken')
    preplanned_leaves = fields.Float('Preplanned Leaves')
    unplanned_leaves = fields.Float('Unplanned Leaves')
    fullday_leaves = fields.Float('Full Day Leaves')
    halfday_leaves = fields.Float('Half Day Leaves')
    partial_leaves = fields.Float('Partial Leaves')
    allocated_paid_leaves = fields.Float('Allocated Paid Leaves')
    total_auto_generated_leaves = fields.Float('Total Auto Generated Leaves')
    
    # Attendance
    total_working_days_from_company = fields.Float('Total Working Days From Company')
    present_from_employee_excluding_leaves = fields.Float('Present From Employee Excluding Leaves')
    missed_attendance = fields.Float('Missed Attendance')
    check_in_late = fields.Float('Check In Late')
    check_out_early = fields.Float('Check Out Early')
    break_hour_extend = fields.Float('Break Hour Extend')
    total_attendance_modification_request = fields.Float('Total Attendance Modification Request')

    #Timesheet
    billable_internal_project_timesheet = fields.Float('Internal Project Timesheet')
    billable_external_project_timesheet = fields.Float('External Project Timesheet')
    billable_total_timesheet = fields.Float(' Total Timesheet')
    billable_avg_timesheet_per_day = fields.Float('Average Timesheet Per Day')
    unbillable_internal_project_timesheet = fields.Float(' Internal Project Timesheet')
    unbillable_external_project_timesheet = fields.Float(' External Project Timesheet')
    unbillable_total_timesheet = fields.Float('Total Timesheet ')
    unbillable_avg_timesheet_per_day = fields.Float('Average Timesheet Per Day')
    avg_timesheet_required_per_day = fields.Float('Average Timesheet Required Per Day', default=8)
   
    #cost calculation
    hourly_cost = fields.Float("Hourly Rate", default=15.0)
    billable_project_cost = fields.Float("Billable Project Cost",compute="_compute_profit")
    total_emp_pay = fields.Float("Total Pay",compute="_compute_profit")
    project_profit = fields.Float("External Project Profit",compute="_compute_profit")

    @api.depends('wage','hourly_cost','billable_external_project_timesheet')
    def _compute_profit(self):
        for rec in self:
            rec.total_emp_pay = 0.0
            rec.billable_project_cost = rec.hourly_cost * rec.billable_external_project_timesheet
            rec.project_profit = 0.0
            if rec.wage and rec.hourly_cost and rec.billable_external_project_timesheet and rec.contract_period and rec.contract_type:
                if rec.contract_type == 'year':
                    rec.total_emp_pay = rec.contract_period * rec.wage * 12
                if rec.contract_type == 'month':
                    rec.total_emp_pay = rec.contract_period * rec.wage
            rec.project_profit = rec.billable_project_cost - rec.total_emp_pay

    # def _compute_leave_count(self):
    #     """ Override this method for count only approved leaves.
    #     """
    #     in_contract_list = []
    #     domain = [("employee_id.id", "=", self.employee_id.id),('state','=','validate')]
    #     hr_leaves = self.env['hr.leave'].sudo().search(domain)
    #     for leave in hr_leaves:
    #         if self.date_end and self.date_start and leave.request_date_from and leave.request_date_to:
    #             if self.date_start <= leave.request_date_from and self.date_end >= leave.request_date_to:
    #                 in_contract_list.append(leave.id)
    #     self.leaves_count = len(in_contract_list)

    
    @api.depends('wage')
    def _compute_previous_contract_wedge(self):
        for rec in self:
            rec.previous_contract_wage = 0.0
            rec.increment_offer_percentage = 0.0
            rec.increment_offer_amount = 0.0
            last_contract = self.env['hr.contract'].search([
                ('employee_id', '=', rec.employee_id.id),
                ('date_start', '<', rec.date_start),('state','!=','cancel')], order='date_start desc', limit=1)
            if last_contract:
                rec.previous_contract_wage = last_contract.wage
            else:
                rec.previous_contract_wage = 0.0

            rec.increment_offer_amount = rec.wage - rec.previous_contract_wage
            if rec.previous_contract_wage > 0:
                rec.increment_offer_percentage = (100 * rec.increment_offer_amount) / rec.previous_contract_wage
 

    # @api.onchange('wage')
    # def onchange_wage(self):
    #     """Calculate Increment amount and percentage when change wage 
    #     """
    #     self.increment_offer_amount = self.wage - self.previous_contract_wage
    #     if self.previous_contract_wage > 0:
    #         self.increment_offer_percentage = (100 * self.increment_offer_amount) / self.previous_contract_wage
 

    
    def action_view_emp_timesheets(self):
        """view timesheets during contract start date and end date
        """
        check_in_date = self.date_start
        check_out_date = self.date_end
        timesheets = self.env['account.analytic.line'].sudo().search(
            [('employee_id', '=', self.employee_id.id)])
        if timesheets:
            timesheets = timesheets.filtered(
                lambda x: x.date >= check_in_date and x.date <= check_out_date)
            res = {
                'type': 'ir.actions.act_window',
                'name': 'Timesheets',
                'view_mode': 'tree,form',
                'view_type': 'tree,form',
                'res_model': 'account.analytic.line',
                'domain': [('id', 'in', timesheets.ids)],
            }
        return res
        
    def action_view_emp_attendance(self):
        """view attendance during contract start date and end date
        """
        curr_start_date = datetime.strftime(
            self.date_start, "%Y/%m/%d 00:00:00")
        curr_end_date = datetime.strftime(self.date_end, "%Y/%m/%d 23:59:59")
        attendances = self.env['hr.attendance'].search([('employee_id', '=', self.employee_id.id), (
            'check_in', '>=', curr_start_date), ('check_in', '<=', curr_end_date)])
        return {
            'type': 'ir.actions.act_window',
            'name': 'Attendances',
            'view_mode': 'tree,form',
            'res_model': 'hr.attendance',
            'domain': [('id', 'in', attendances.ids)],
        }
        
    def action_view_emp_attendance_modification_req(self):
        """view attendance modification request during contract start date and end date
        """
        check_in_date = self.date_start
        check_out_date = self.date_end
        attendance_modification = self.env['sh.attendance.modification.request'].search([('employee_id', '=', self.employee_id.id), ('date', '>=', check_in_date), ('date', '<=', check_out_date) ])
        return {
            'type': 'ir.actions.act_window',
            'name': 'Attendance Modification Request',
            'view_mode': 'tree,form',
            'res_model': 'sh.attendance.modification.request',
            'domain': [('id', 'in', attendance_modification.ids)],
        }
    
    def action_view_emp_notifications(self):
        """view notifications during contract start date and end date
        """
        start_date = self.date_start
        end_date = self.date_end
        push_notifications = self.env['user.push.notification'].search([('user_id', '=', self.employee_id.user_id.id), ('datetime', '>=', start_date), ('datetime', '<=', end_date) ])
        return {
            'type': 'ir.actions.act_window',
            'name': 'Notifications',
            'view_mode': 'tree',
            'res_model': 'user.push.notification',
            'domain': [('id', 'in', push_notifications.ids)],
        }
    
    def update_contract_details(self,start_date,end_date):
        self._compute_previous_contract_wedge()
        # search previous three contract
        query = """
            SELECT id
            FROM hr_contract
            WHERE employee_id = %s AND date_start <= %s AND state!='cancel'
            ORDER BY date_start
        """
        self.env.cr.execute(query, (self.employee_id.id, self.date_start))
        result = self.env.cr.fetchall()
        print(">>>>>>>>>>>>>>>.",result)
        if result:
            id = self.id
            contract_ids_to_set = tuple(result)
            query = """
                DELETE FROM hr_contract_hr_contact_rel
                WHERE hr_contract_id = %s
            """
            self.env.cr.execute(query, (id,))
            
            query = """
                INSERT INTO hr_contract_hr_contact_rel (hr_contract_id, new_hr_contract_id)
                VALUES (%s, %s)
            """
            print("\n\ncontract_ids_to_set",contract_ids_to_set)
            for prev_contract_id in contract_ids_to_set:
                update_record = self.env.cr.execute(query, (id, prev_contract_id))
            return update_record
        # else:
        #     raise UserError(_("No previous contract found!"))



    def update_contract(self):
        check_in_date = self.date_start
        check_out_date = self.date_end


        #convert date to UTC format
        # user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
        datetimeformat = "%Y-%m-%d %H:%M:%S"
        date1 = datetime.strptime(str(check_in_date) + " 00:00:00", datetimeformat)
        date2 = datetime.strptime(str(check_out_date) + " 23:59:59", datetimeformat)

        check_in_date = date1 - timedelta(hours=5, minutes=30)
        check_out_date = date2 - timedelta(hours=5, minutes=30)

        self.update_contract_details(check_in_date,check_out_date)
        total_leaves_taken = self.update_leave_details(check_in_date,check_out_date)
        present_days_of_employee = self.update_attandance_details(check_in_date,check_out_date,total_leaves_taken)
        self.update_timesheet_details(check_in_date,check_out_date, present_days_of_employee)
        
        
    def update_leave_details(self,start_date,end_date):
        # get paid leave ids
        paid_leave_ids_query = """
                SELECT id
                FROM hr_leave_type
                WHERE requires_allocation = 'yes'
            """
        self.env.cr.execute(paid_leave_ids_query)
        paid_leave_ids_result = self.env.cr.fetchall()
                
        # Get paid leave duration 
        paid_leave_query = """
            SELECT *
            FROM hr_leave
            WHERE employee_id = %s
                AND holiday_status_id IN %s
                AND request_date_from >= %s
                AND request_date_to <= %s
                AND state = 'validate'
        """
        self.env.cr.execute(paid_leave_query, (self.employee_id.id, tuple(paid_leave_ids_result), start_date, end_date))
        
        paid_leave_result = self.env.cr.fetchall()
            
        paid_leave_record = self.env['hr.leave'].browse([record[0] for record in paid_leave_result])
        
        total_paid_leave = 0
        for rec in paid_leave_record:
            total_paid_leave += rec.number_of_days_display
           
        # Get unpaid leave duration 
        unpaid_leave_query = """
            SELECT *
            FROM hr_leave
            WHERE employee_id = %s
                AND holiday_status_id NOT IN %s
                AND request_date_from >= %s
                AND request_date_to <= %s
                AND state = 'validate'
        """

        self.env.cr.execute(unpaid_leave_query, (self.employee_id.id, tuple(paid_leave_ids_result), start_date, end_date))
        unpaid_leave_result = self.env.cr.fetchall()
        unpaid_leave_record = self.env['hr.leave'].browse([record[0] for record in unpaid_leave_result])
        
        total_unpaid_leave = 0
        for rec in unpaid_leave_record:
            total_unpaid_leave += rec.number_of_days_display

        update_query = """
            UPDATE hr_contract
            SET paid_leaves = %s, unpaid_leaves = %s, total_leaves_taken = %s
            WHERE id = %s
        """
        self.env.cr.execute(update_query, (total_paid_leave, total_unpaid_leave, total_paid_leave + total_unpaid_leave, self.id))
        
       # Half day leave 
        halfday_leaves_query = """
            SELECT *
            FROM hr_leave
            WHERE 
                employee_id = %s
                AND request_unit_half = True
                AND request_date_from >= %s
                AND request_date_to <= %s
                AND state = 'validate'
        """
        self.env.cr.execute(halfday_leaves_query, (self.employee_id.id, start_date, end_date))
        halfday_leaves = self.env.cr.fetchall()
        halfday_leaves_record = self.env['hr.leave'].browse([record[0] for record in halfday_leaves])
        # halfday_leaves_total = sum(leave.number_of_days_display for leave in halfday_leaves_record)
       
       # Preplanned day leave 
        preplanned_leaves_query = """
        SELECT *
        FROM hr_leave
        WHERE 
            employee_id = %s
            AND bool_field = True
            AND request_date_from >= %s
            AND request_date_to <= %s
            AND state = 'validate'
        """
        self.env.cr.execute(preplanned_leaves_query, (self.employee_id.id,start_date, end_date))
        preplanned_leaves = self.env.cr.fetchall()
        preplanned_leaves_record = self.env['hr.leave'].browse([record[0] for record in preplanned_leaves])
        preplanned_leaves_total = sum(leave.number_of_days_display for leave in preplanned_leaves_record)
        
        # Unplanned day leave 
        unplanned_leaves_query = """
        SELECT *
        FROM hr_leave
        WHERE 
            employee_id = %s
            AND bool_field = False
            AND request_date_from >= %s
            AND request_date_to <= %s
            AND state = 'validate'
        """
        self.env.cr.execute(unplanned_leaves_query, (self.employee_id.id,start_date, end_date))
        unplanned_leaves = self.env.cr.fetchall()
        unplanned_leaves_record = self.env['hr.leave'].browse([record[0] for record in unplanned_leaves])
        
        unplanned_leaves_total = sum(leave.number_of_days_display for leave in unplanned_leaves_record)
        
        # Allocate Paid Leave 
        allocate_paid_leaves_query = """
            SELECT *
            FROM hr_leave_allocation
            WHERE 
                employee_id = %s
                AND date_end <= %s
                AND state='validate'
        """

        self.env.cr.execute(allocate_paid_leaves_query, (self.employee_id.id,end_date))
        allocate_leaves = self.env.cr.fetchall()
        allocate_leaves_record = self.env['hr.leave.allocation'].browse(record[0] for record in allocate_leaves)
        allocated_leave_total =  sum(leave.number_of_days_display for leave in allocate_leaves_record)
        
        # automatic generate leave
        automatic_leaves_query = """
            SELECT *
            FROM hr_leave
            WHERE 
                automatic = True
                AND employee_id = %s
                AND request_date_from >= %s
                AND request_date_to <= %s
        """
        
        self.env.cr.execute(automatic_leaves_query, (self.employee_id.id,start_date, end_date))
        automatic_leaves = self.env.cr.fetchall()
        automatic_leaves_record = self.env['hr.leave'].browse(record[0] for record in automatic_leaves)
        automatic_leave_total =  sum(leave.number_of_days_display for leave in automatic_leaves_record)
        
        
        # Full day leaves
        fullday_leaves_query = """
            SELECT *
            FROM hr_leave
            WHERE 
                employee_id = %s
                AND request_unit_half = False
                AND request_unit_hours = False
                AND request_date_from >= %s
                AND request_date_to <= %s
                AND state = 'validate'
        """

        self.env.cr.execute(fullday_leaves_query, (self.employee_id.id,start_date, end_date))
        fullday_leaves = self.env.cr.fetchall()
        fullday_leaves_record = self.env['hr.leave'].browse(record[0] for record in fullday_leaves)
        fullday_leaves_total =  sum(leave.number_of_days_display for leave in fullday_leaves_record)
        
        # Partial leaves
        fullday_leaves_query = """
            SELECT *
            FROM hr_leave
            WHERE 
                employee_id = %s
                AND request_unit_hours = True
                AND request_date_from >= %s
                AND request_date_to <= %s
                AND state = 'validate'
        """

        self.env.cr.execute(fullday_leaves_query, (self.employee_id.id,start_date, end_date))
        partial_leaves = self.env.cr.fetchall()
        partial_leaves_record = self.env['hr.leave'].browse(record[0] for record in partial_leaves)
        # partial_leaves_total =  sum(leave.number_of_days_display for leave in partial_leaves_record)
        
        
        # Update leaves details in contract Performance page
        leaves_details_update = """
            UPDATE hr_contract
            SET halfday_leaves = %s,
            preplanned_leaves = %s,
            unplanned_leaves = %s,
            allocated_paid_leaves = %s,
            total_auto_generated_leaves = %s,
            fullday_leaves = %s,
            partial_leaves = %s
            WHERE id = %s
        """
        self.env.cr.execute(leaves_details_update, (len(halfday_leaves_record),preplanned_leaves_total,unplanned_leaves_total, allocated_leave_total, automatic_leave_total, fullday_leaves_total,len(partial_leaves_record), self.id))
        return (total_paid_leave+total_unpaid_leave)
        
    def update_attandance_details(self,start_date,end_date,total_leaves_taken):
        
        # Check In Late 
        check_in_late_query = """
            SELECT *
            FROM hr_attendance
            WHERE 
                employee_id = %s
                AND LENGTH(message_in) > 1
                AND check_in >= %s
                AND check_out <= %s
            """
        self.env.cr.execute(check_in_late_query, (self.employee_id.id,start_date,end_date))
        check_in_late_ids = self.env.cr.fetchall()
        check_in_late_record = self.env['hr.attendance'].browse(record[0] for record in check_in_late_ids)
        
        # Check Out Early 
        check_out_early_query = """
            SELECT *
            FROM hr_attendance
            WHERE 
                employee_id = %s
                 AND LENGTH(message_out) > 1
                AND check_in >= %s
                AND check_out <= %s
            """
        self.env.cr.execute(check_out_early_query, (self.employee_id.id,start_date,end_date))
        check_out_early_ids = self.env.cr.fetchall()
        check_out_early_record = self.env['hr.attendance'].browse(record[0] for record in check_out_early_ids)
        
        # Break Hour Extend
        break_hour_extend_query = """
            SELECT *
            FROM hr_attendance
            WHERE 
                employee_id = %s
                AND LENGTH(sh_break_reason) > 1
                AND check_in >= %s
                AND check_out <= %s
            """
        self.env.cr.execute(break_hour_extend_query, (self.employee_id.id,start_date,end_date))
        break_hour_extend_ids = self.env.cr.fetchall()
        break_hour_extend_record = self.env['hr.attendance'].browse(record[0] for record in break_hour_extend_ids)
        
        
        # Attandance ModificationRequest
        attandance_modification_request_query = """
            SELECT *
            FROM sh_attendance_modification_request
            WHERE 
                employee_id = %s
                AND date >= %s
                AND date <= %s
            """
        self.env.cr.execute(attandance_modification_request_query, (self.employee_id.id,start_date,end_date))
        attandance_modification_request_ids = self.env.cr.fetchall()
        attandance_modification_request_record = self.env['sh.attendance.modification.request'].browse(record[0] for record in attandance_modification_request_ids)
        
       
        
        # This code for get Total Working Days From Company
        # get today date
        current_day_of_month = fields.Date.today()
        
        if end_date.date() >= current_day_of_month:
            # count sunday
            sundays_count = sum(1 for single_date in range((current_day_of_month - start_date.date()).days + 1)
                            if (start_date.date() + timedelta(days=single_date)).weekday() == 6)
                        
            calendar_leaves_query = """
                SELECT *
                FROM resource_calendar_leaves
                WHERE 
                    date_from >= %s
                    AND date_to <= %s
                    AND calendar_id = %s 
                    AND holiday_id IS NULL
                """
            self.env.cr.execute(calendar_leaves_query, (start_date,end_date,self.resource_calendar_id.id))
            calendar_leaves_ids = self.env.cr.fetchall()
            calendar_leaves_record = self.env['resource.calendar.leaves'].browse(record[0] for record in calendar_leaves_ids)
            
            # get total days
            totalday = current_day_of_month - start_date.date()
            current_day = totalday.days + 1
            Total_company_work_day = current_day - (sundays_count + len(calendar_leaves_record))
            
        elif end_date.date() < current_day_of_month:
            sundays_count = sum(1 for single_date in range((end_date.date() - start_date.date()).days + 1)
                            if (start_date.date() + timedelta(days=single_date)).weekday() == 6)
            
            calendar_leaves_query = """
                SELECT *
                FROM resource_calendar_leaves
                WHERE 
                    date_from >= %s
                    AND date_to <= %s
                    AND calendar_id = %s 
                    AND holiday_id IS NULL
                """
            self.env.cr.execute(calendar_leaves_query, (start_date,end_date,self.resource_calendar_id.id))
            calendar_leaves_ids = self.env.cr.fetchall()
            calendar_leaves_record = self.env['resource.calendar.leaves'].browse(record[0] for record in calendar_leaves_ids)
            
            # get total days
            totalday = end_date - start_date 
            current_day = totalday.days + 1
            
            Total_company_work_day = current_day - (sundays_count + len(calendar_leaves_record))
            
        
        # This code for get Present From Employee Excluding Leaves
        employee_calendar_leaves_query = """
                SELECT *
                FROM resource_calendar_leaves
                WHERE 
                    date_from >= %s
                    AND date_to <= %s
                    AND holiday_id IS NOT NULL
                """
        self.env.cr.execute(employee_calendar_leaves_query, (start_date,end_date))
        employee_calendar_leaves_ids = self.env.cr.fetchall()
        employee_calendar_leaves_record = self.env['resource.calendar.leaves'].browse(record[0] for record in employee_calendar_leaves_ids)
        
        present_days_of_employee = Total_company_work_day - total_leaves_taken
        #len(employee_calendar_leaves_record)

        
        
        emp_missed_attendance = Total_company_work_day - present_days_of_employee
        # Update Attandance details in contract Performance page
        attandance_details_update = """
            UPDATE hr_contract
            SET check_in_late = %s,
            check_out_early = %s,
            break_hour_extend = %s,
            total_attendance_modification_request = %s,
            total_working_days_from_company = %s,
            present_from_employee_excluding_leaves = %s,
            missed_attendance = %s
            WHERE id = %s
        """
        self.env.cr.execute(attandance_details_update, (len(check_in_late_record),len(check_out_early_record),len(break_hour_extend_record),len(attandance_modification_request_record),Total_company_work_day,present_days_of_employee,emp_missed_attendance, self.id))
        return present_days_of_employee
      
    def update_timesheet_details(self,start_date,end_date,present_days_of_employee):        
        # INTERNAL PROJECT
        billable_internal_project_timesheet_total = 0
        billable_external_project_timesheet_total = 0
        billable_total_timesheet = 0
        billable_avg_timesheet_per_day = 0
        unbillable_internal_project_timesheet_total = 0
        unbillable_external_project_timesheet_total = 0
        unbillable_total_timesheet = 0
        unbillable_avg_timesheet_per_day = 0

        get_internal_project_query = """
            SELECT *
            FROM project_project
            WHERE 
            project_type_selection = 'internal'
            """
        self.env.cr.execute(get_internal_project_query)
        get_internal_project_ids = self.env.cr.fetchall()
        project_record = self.env['project.project'].browse(record[0] for record in get_internal_project_ids)
        internal_project_ids = project_record.ids 
        internal_project_timesheet_record = False 
        if internal_project_ids:    
            # INTERNAL PROJECT TIMESHEET
            get_internal_project_timesheet_query = """
                SELECT *
                FROM account_analytic_line
                WHERE 
                    employee_id = %s
                    AND project_id IN %s
                    AND date >= %s
                    AND date <= %s
                """
            self.env.cr.execute(get_internal_project_timesheet_query,(self.employee_id.id,tuple(internal_project_ids),start_date,end_date))
            internal_project_timesheet_result = self.env.cr.fetchall()
            internal_project_timesheet_record = self.env['account.analytic.line'].browse([record[0] for record in internal_project_timesheet_result])
        if internal_project_timesheet_record:
            # BILLABLE INTERNAL PROJECT TIMESHEET
            billable_internal_project_timesheet_total =  sum(timesheet.unit_amount_invoice for timesheet in internal_project_timesheet_record)
            
            # UNBILLABLE INTERNAL PROJECT TIMESHEET
            unbillable_internal_project_timesheet_total =  sum(timesheet.unit_amount for timesheet in internal_project_timesheet_record)
        
        # EXTERNAL PROJECT
        get_external_project_query = """
            SELECT *
            FROM project_project
            WHERE 
            project_type_selection = 'external'
            """
        self.env.cr.execute(get_external_project_query)
        get_external_project_ids = self.env.cr.fetchall()
        external_project_record = self.env['project.project'].browse(record[0] for record in get_external_project_ids)
        external_project_ids = external_project_record.ids
        external_project_timesheet_record = False
        if external_project_ids:
            # External PROJECT TIMESHEET
            get_external_project_timesheet_query = """
                SELECT *
                FROM account_analytic_line
                WHERE 
                    employee_id = %s
                    AND project_id IN %s
                    AND date >= %s
                    AND date <= %s
                """
            self.env.cr.execute(get_external_project_timesheet_query,(self.employee_id.id,tuple(external_project_ids),start_date,end_date))
            external_project_timesheet_result = self.env.cr.fetchall()
            external_project_timesheet_record = self.env['account.analytic.line'].browse([record[0] for record in external_project_timesheet_result])
            
        # BILLABLE EXTERNAL PROJECT TIMESHEET
        if external_project_timesheet_record:
            billable_external_project_timesheet_total =  sum(timesheet.unit_amount_invoice for timesheet in external_project_timesheet_record)
            
        # BILLABLE TOTAL TIMESHEET
        billable_total_timesheet = billable_internal_project_timesheet_total + billable_external_project_timesheet_total
        
        # BILLABLE AVERAGE TIMESHEET PER DAY
        billable_avg_timesheet_per_day = billable_total_timesheet / present_days_of_employee
        
        # UNBILLABLE EXTERNAL PROJECT TIMESHEET
        if external_project_timesheet_record:
            unbillable_external_project_timesheet_total =  sum(timesheet.unit_amount for timesheet in external_project_timesheet_record)
        
        # UNBILLABLE TOTAL TIMESHEET
        unbillable_total_timesheet = unbillable_internal_project_timesheet_total + unbillable_external_project_timesheet_total
        
        # UNBILLABLE AVERAGE TIMESHEET PER DAY
        unbillable_avg_timesheet_per_day = unbillable_total_timesheet / present_days_of_employee
            
        # TIMESHEET DETAILS UPDATE
        avg_timesheet_req_per_day = self.resource_calendar_id.timesheet_hrs
        timesheet_details_update = """
            UPDATE hr_contract
            SET 
            billable_internal_project_timesheet = %s,
            billable_external_project_timesheet = %s,
            billable_total_timesheet = %s,
            billable_avg_timesheet_per_day = %s,
            unbillable_internal_project_timesheet = %s,
            unbillable_external_project_timesheet = %s,
            unbillable_total_timesheet = %s,
            unbillable_avg_timesheet_per_day = %s,
            avg_timesheet_required_per_day = %s
            WHERE id = %s
        """
        self.env.cr.execute(timesheet_details_update, (billable_internal_project_timesheet_total,billable_external_project_timesheet_total,billable_total_timesheet,billable_avg_timesheet_per_day,unbillable_internal_project_timesheet_total,unbillable_external_project_timesheet_total,unbillable_total_timesheet,unbillable_avg_timesheet_per_day,avg_timesheet_req_per_day, self.id))

        
        