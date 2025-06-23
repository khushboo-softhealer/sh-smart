# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

import logging
from collections import namedtuple
from datetime import datetime, timedelta
from pytz import timezone, UTC
from odoo import api, fields, models
from odoo.addons.resource.models.resource import float_to_time, HOURS_PER_DAY
from odoo.tools import float_compare
from odoo.tools.translate import _
from odoo.exceptions import ValidationError
import math

_logger = logging.getLogger(__name__)
DummyAttendance = namedtuple(
    'DummyAttendance', 'hour_from, hour_to, dayofweek, day_period')
NOTI_CODE = 'CODE_SH_SALE_PRICELIST_SIMPLE_NOTIFICATION_'


class CreateLeaveWizard(models.TransientModel):
    _name = 'sh.create.leave'
    _description = 'Create Leave'

    employee_ids = fields.Many2many(
        'hr.employee', 'rel_employee_create_leave', string='Exclude Employees')
    include_employee_ids = fields.Many2many(
        'hr.employee', 'rel_include_employee_create_leave', string='Include Employees')
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)

    def default_get(self, fields):
        rec = super(CreateLeaveWizard, self).default_get(fields)

        rec.update({
            'employee_ids': [(6, 0, self.env.user.company_id.sh_employee_ids.ids)],
        })

        return rec
    
    def _create_full_day_leave(self,employee,start,end, leave_type_id):
        d_from = fields.Datetime.from_string(start)
        d_to = fields.Datetime.from_string(end)
        leave_date_from = fields.Datetime.from_string(
            d_from)
        leave_date_to = fields.Datetime.from_string(
            d_to)
        domain = [
            ('calendar_id', '=', employee.resource_calendar_id.id or self.env.user.company_id.resource_calendar_id.id)]
        attendances = self.env['resource.calendar.attendance'].read_group(
            domain, ['ids:array_agg(id)', 'hour_from:min(hour_from)', 'hour_to:max(hour_to)', 'dayofweek', 'day_period'], ['dayofweek', 'day_period'], lazy=False)

        # Must be sorted by dayofweek ASC and day_period DESC
        attendances = sorted([DummyAttendance(group['hour_from'], group['hour_to'], group['dayofweek'], group['day_period'])
                                for group in attendances], key=lambda att: (att.dayofweek, att.day_period != 'morning'))

        default_value = DummyAttendance(
            0, 0, 0, 'morning')

        # find first attendance coming after first_day
        attendance_from = next((att for att in attendances if int(
            att.dayofweek) >= start.weekday()), attendances[0] if attendances else default_value)
        # find last attendance coming before last_day
        attendance_to = next((att for att in reversed(attendances) if int(
            att.dayofweek) <= end.weekday()), attendances[-1] if attendances else default_value)
        hour_from = float_to_time(
            attendance_from.hour_from)
        hour_to = float_to_time(attendance_to.hour_to)
        leave_vals = {
            'name': 'Automatic leave based on employee attendance.',
            'holiday_type': 'employee',
            'date_from': timezone(employee.tz).localize(datetime.combine(start, hour_from)).astimezone(UTC).replace(tzinfo=None),
            'date_to': timezone(employee.tz).localize(datetime.combine(end, hour_to)).astimezone(UTC).replace(tzinfo=None),
            'request_date_from': start,
            'request_date_to': end,
            'employee_id': employee.id,
            'automatic': True,
            'holiday_status_id': leave_type_id.id
        }

        leave_id = False
        domain = [
            ('date_from', '<=', timezone(employee.tz).localize(
                datetime.combine(end, hour_to)).astimezone(UTC).replace(tzinfo=None)),
            ('date_to', '>=', timezone(employee.tz).localize(datetime.combine(
                start, hour_from)).astimezone(UTC).replace(tzinfo=None)),
            ('employee_id', '=', employee.id),
            ('state', 'not in', ['cancel','refuse']),
        ]
        nholidays = self.env['hr.leave'].search_count(
            domain)
        already_taken_leave = self.env['hr.leave'].search(
            domain)
        if nholidays:
            pass
            
        else:
            if employee.date_of_joining and employee.date_of_joining < start:

                leave_id = self.env['hr.leave'].sudo().with_context(
                    check_validaty=False).create(leave_vals)

                if employee.id not in self.env.user.company_id.sh_employee_ids.ids:
                    self.env['sh.warning.message'].create({
                        'name': 'Please Check System Generated leave for date : '+str(start),
                        'description': 'Please Check System Generated leave for date : : '+str(start),
                        'user_id': employee.user_id.id,
                        'sh_create_date': start,
                        'res_model': 'hr.leave',
                        'res_id': leave_id.id,
                    })

                if leave_id:
                    activity = self.env['mail.activity'].create({
                        'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                        'user_id': leave_id.employee_id.user_id.id,
                        'res_id': leave_id.id,
                        'res_model_id': self.env['ir.model'].search([('model', '=', 'hr.leave')], limit=1).id,
                        'summary': 'Please check your leave and confirm it.',
                    })
                    if leave_id.number_of_hours_display >= 2:

                        base_url = self.env['ir.config_parameter'].sudo(
                        ).get_param('web.base.url')

                        self.env['user.push.notification'].push_notification([leave_id.employee_id.user_id], 'Please check your leave and confirm it.', 'Please update leave details.', base_url+"/mail/view?model=hr.leave&res_id="+str(leave_id.id),
                                                                            'hr.leave', leave_id.id, 'hr')
                    leave_id._compute_number_of_hours_display()
                    leave_id._compute_number_of_days_display()
                    leave_id.created_leave = True

    def _create_half_or_custom_hour_leave(self,employee,start,end, leave_type_id, schedule_hours, total_worked_hours, last_schedule_id):
        if schedule_hours > 0.0 and total_worked_hours > 0.0 and total_worked_hours < schedule_hours:
                                    
            duration = schedule_hours - total_worked_hours
            
            start_value = last_schedule_id.hour_to - \
                float("{:.2f}".format(duration))
            start_hours, start_minutes = divmod(
                abs(start_value) * 60, 60)
            start_minutes = round(start_minutes)
            if start_minutes == 60:
                start_minutes = 0
                start_hours += 1
            if start_value < 0:
                leave_start_converted = str(
                    '-%02d:%02d' % (start_hours, start_minutes))
            leave_start_converted = str(
                '%02d:%02d' % (start_hours, start_minutes))
            end_value = last_schedule_id.hour_to
            end_hours, end_minutes = divmod(
                abs(end_value) * 60, 60)
            end_minutes = round(end_minutes)
            if end_minutes == 60:
                end_minutes = 0
                end_hours += 1
            if end_value < 0:
                leave_end_converted = str(
                    '-%02d:%02d' % (end_hours, end_minutes))
            leave_end_converted = str(
                '%02d:%02d' % (end_hours, end_minutes))
            leave_start_from_str = leave_start_converted.split(
                ':')
            leave_start_from_str_joint = leave_start_from_str[0] + \
                ':'+leave_start_from_str[1]+':00'
            leave_start_to_str = leave_end_converted.split(
                ':')
            leave_start_to_str_joint = leave_start_to_str[0] + \
                ':'+leave_start_to_str[1]+':00'
            leave_start = str(
                start) + " "+leave_start_from_str_joint
            leave_start_date = datetime.strptime(
                leave_start, '%Y-%m-%d %H:%M:%S') - timedelta(hours=5, minutes=30)
            leave_end = str(start) + \
                " "+leave_start_to_str_joint
            leave_end_date = datetime.strptime(
                leave_end, '%Y-%m-%d %H:%M:%S') - timedelta(hours=5, minutes=30)
            if (total_worked_hours / schedule_hours) >= 0.5 and (total_worked_hours / schedule_hours) < 0.6:

                leave_vals = {
                    'name': 'Automatic Partial leave based on employee attendance.',
                    'holiday_type': 'employee',
                    'date_from': leave_start_date,
                    'date_to': leave_end_date,
                    'request_date_from': start,
                    'request_date_to': end,
                    'employee_id': employee.id,
                    'request_unit_hours': False,
                    'holiday_status_id': leave_type_id.id,
                    'request_unit_half': True,
                    'automatic': True,
                }
            else:
                leave_vals = {
                    'name': 'Automatic Partial leave based on employee attendance.',
                    'automatic': True,
                    'holiday_type': 'employee',
                    'date_from': leave_start_date,
                    'date_to': leave_end_date,
                    'request_date_from': start,
                    'request_date_to': start,
                    'employee_id': employee.id,
                    'request_unit_hours': True,
                    'holiday_status_id': leave_type_id.id,
                    'request_unit_half': False,
                    'request_hour_from': str(math.ceil(last_schedule_id.hour_from)),
                    'request_hour_to': str(math.ceil(last_schedule_id.hour_from) + math.ceil(duration)) ,
                }
            leave_taken = self.env['hr.leave'].sudo().search([('employee_id', '=', employee.id), (
                'request_date_from', '<=', start), ('request_date_to', '>=', end), ('state', 'not in', ['cancel','refuse'])], limit=1)
            leave_id = False

            if not leave_taken and employee.date_of_joining and employee.date_of_joining < start:
                if duration > 0.35:

                    leave_id = self.env['hr.leave'].sudo().with_context(
                        check_validaty=False).create(leave_vals)
                    if employee.id not in self.env.user.company_id.sh_employee_ids.ids:
                        self.env['sh.warning.message'].create({
                            'name': 'Please Check System Generated leave for date : '+str(start),
                            'description': 'Please Check System Generated leave for date : : '+str(start),
                            'user_id': employee.user_id.id,
                            'sh_create_date': start,
                            'res_model': 'hr.leave',
                            'res_id': leave_id.id
                        })

            if leave_id:

                activity = self.env['mail.activity'].create({
                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                    'user_id': leave_id.employee_id.user_id.id,
                    'res_id': leave_id.id,
                    'res_model_id': self.env['ir.model'].search([('model', '=', 'hr.leave')], limit=1).id,
                    'summary': 'Please check your leave and confirm it.',
                })
                if duration >= 1.5:
                    base_url = self.env['ir.config_parameter'].sudo(
                    ).get_param('web.base.url')
                    self.env['user.push.notification'].push_notification([leave_id.employee_id.user_id], 'Please check your leave and confirm it.', 'Please update leave details.', base_url+"/mail/view?model=hr.leave&res_id="+str(leave_id.id),
                                                                        'hr.leave', leave_id.id, 'hr')



    def action_create_leave(self):

        employees = False
        if self.employee_ids and self.include_employee_ids:
            employees = self.env['hr.employee'].sudo().search(
                [('id', 'not in', self.employee_ids.ids), ('id', 'in', self.include_employee_ids.ids)])
        elif self.employee_ids and not self.include_employee_ids:
            employees = self.env['hr.employee'].sudo().search(
                [('id', 'not in', self.employee_ids.ids)])
        elif not self.employee_ids and self.include_employee_ids:
            employees = self.env['hr.employee'].sudo().search(
                [('id', 'in', self.include_employee_ids.ids)])
        elif not self.employee_ids and not self.include_employee_ids:
            employees = self.env['hr.employee'].sudo().search([])

        draft_leaves = self.env['hr.leave'].sudo().search([('employee_id', 'in', employees.ids), (
            'date_from', '>=', self.start_date), ('date_to', '<=', self.end_date), ('state', 'in', ['confirm', 'validate1'])])
        if draft_leaves:
            raise ValidationError("Need to Approve Leaves First !")

        modification_request = self.env['sh.attendance.modification.request'].sudo().search(
            [('employee_id','in',employees.ids),('date', '>=', self.start_date), ('date', '<=', self.end_date), ('state', 'in', ['waiting_for_approve'])])
        if modification_request:
            raise ValidationError(
                "Need to Approve Modification Requests First !")

        if employees:
            start_date = self.start_date
            end_date = self.end_date
            delta = end_date - start_date
            for i in range(delta.days + 1):
                start = start_date + timedelta(days=i)
                end = start_date + timedelta(days=i)

                day_start = start.weekday()
                date_start = str(start) + " 00:00:00"
                date_start_end = str(start) + " 23:59:59"
                st_date = datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S")
                en_date = datetime.strptime(
                    date_start_end, '%Y-%m-%d %H:%M:%S')
                s_date = st_date - timedelta(hours=5, minutes=30)
                e_date = en_date - timedelta(hours=5, minutes=30)
                for employee in employees:
                    leave_type_id = False
                    if self.env.user.company_id.sh_leave_type_id:
                        leave_type_id = self.env.user.company_id.sh_leave_type_id
                        leave_days = leave_type_id.get_days(
                            employee.id)[leave_type_id.id]
                        if float_compare(leave_days['remaining_leaves'], 0, precision_digits=2) == -1 or \
                                float_compare(leave_days['virtual_remaining_leaves'], 0, precision_digits=2) == -1:
                            if self.env.user.company_id.sh_unpaid_leave_type_id:
                                leave_type_id = self.env.user.company_id.sh_unpaid_leave_type_id
                            else:
                                leave_type_id = self.env.ref(
                                    'hr_holidays.holiday_status_sl')
                    else:
                        if self.env.user.company_id.sh_unpaid_leave_type_id:
                            leave_type_id = self.env.user.company_id.sh_unpaid_leave_type_id
                        else:
                            leave_type_id = self.env.ref(
                                'hr_holidays.holiday_status_sl')

                    resource_calendr_id = self.env['resource.calendar.leaves'].sudo().search([('holiday_id', '=', False), (
                        'calendar_id', '=', employee.resource_calendar_id.id), ('date_from', '>=', s_date), ('date_to', '<=', e_date)], limit=1)
                    if not resource_calendr_id:
                        domain = [('calendar_id', '=', employee.resource_calendar_id.id),
                                  ('dayofweek', '=', day_start),
                                  ('date_from', '=', start),
                                  ('date_to', '=', start),
                                  ('high_priority', '=', True)
                                  ]
                        cal_att_ids = self.env['resource.calendar.attendance'].sudo().search(
                            domain)
                        if not cal_att_ids:
                            domain = [('calendar_id', '=', employee.resource_calendar_id.id),
                                      ('dayofweek', '=', day_start),
                                      ('date_from', '<=', start),
                                      ('date_to', '>=', end),
                                      ('high_priority', '=', False)
                                      ]
                            cal_att_ids = self.env['resource.calendar.attendance'].sudo().search(
                                domain)

                        schedule_hours = 0.0
                        last_schedule_id = False
                        if cal_att_ids:
                            # last_schedule_id = cal_att_ids[-1]
                            last_schedule_id = cal_att_ids[0]
                            for cal_att_id in cal_att_ids:
                                schedule_hours += cal_att_id.hour_to - cal_att_id.hour_from

                            #=====Start========== Auto generate leave based on timehseet=============
                            # print("\n\n date_start_end",employee,date_start,date_start_end)
                            timesheet_ids = self.env['account.analytic.line'].sudo().search(
                                [('employee_id', '=', employee.id), ('date', '=', start)])

                            total_timesheet_hours = 0
                            if timesheet_ids:
                                total_timesheet_hours = sum(timesheet_ids.mapped('unit_amount'))
                            
                            #check leave already generated
                            
                            # employee_leave_exist = self.env['hr.leave'].sudo().search([
                            # ('employee_id', '=', employee.id),
                            # ('date_from', '>=', s_date), 
                            # ('date_to', '<=', e_date)])

                            # print("\n\nemployee_leave_exist",employee_leave_exist)

                            if schedule_hours >0.0:
                                if total_timesheet_hours <= 1:
                                    self._create_full_day_leave(employee,start,end, leave_type_id)
                                else:
                                    self._create_half_or_custom_hour_leave(employee,start,end, leave_type_id, schedule_hours, total_worked_hours, last_schedule_id)
                                    
                                
                                    # full day leave
                                    # leave_vals = {
                                    #     'automatic':True,
                                    #     'name': 'Automatic leave based on employee Timesheet.',
                                    #     'holiday_type': 'employee',
                                    #     'request_date_from': start_date,
                                    #     'request_date_to': start_date,
                                    #     'employee_id': employee.id,
                                    #     'holiday_status_id': leave_type_id.id
                                    # }

                                    # leave_id = self.env['hr.leave'].sudo().with_context(
                                    #         check_validaty=False).create(leave_vals)

                                    # if leave_id:
                                    #     activity = self.env['mail.activity'].create({
                                    #         'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                                    #         'user_id': leave_id.employee_id.user_id.id,
                                    #         'res_id': leave_id.id,
                                    #         'res_model_id': self.env['ir.model'].search([('model', '=', 'hr.leave')], limit=1).id,
                                    #         'summary': 'Please check your leave and confirm it.',
                                    #     })

                                    #     base_url = self.env['ir.config_parameter'].sudo(
                                    #     ).get_param('web.base.url')

                                    #     self.env['user.push.notification'].push_notification([leave_id.employee_id.user_id], 'Please check your leave and confirm it.', 'Please update leave details.', base_url+"/mail/view?model=hr.leave&res_id="+str(leave_id.id),
                                    #                                                         'hr.leave', leave_id.id, 'hr')
                                        
                            #     print("\n\n----total_timesheet_hours",leave_vals,schedule_hours,total_timesheet_hours)
                                
                            #=====End========== Auto generate leave based on timehseet=============
 
                            attendance_ids = self.env['hr.attendance'].sudo().search(
                                [('employee_id', '=', employee.id), ('check_in', '>=', date_start), ('check_out', '<=', date_start_end)])
                            total_worked_hours = 0.0

                            if attendance_ids:
                                for attendance in attendance_ids:
                                    if attendance.check_in and attendance.check_out:
                                        duration = attendance.check_out - attendance.check_in
                                        diff = duration.total_seconds()/3600
                                        total_worked_hours += diff
                                    
                                if total_worked_hours <= 1:
                                    self._create_full_day_leave(employee,start,end, leave_type_id)
                                else:
                                    self._create_half_or_custom_hour_leave(employee,start,end, leave_type_id, schedule_hours, total_worked_hours, last_schedule_id)
                                
                            else:
                                self._create_full_day_leave(employee,start,end, leave_type_id)
                                
