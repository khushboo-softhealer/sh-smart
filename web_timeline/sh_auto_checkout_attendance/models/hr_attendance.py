# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, _
from datetime import datetime, timedelta, date


class Attendance(models.Model):
    _inherit = 'hr.attendance'

    def employee_autocheckout(self):
        print(f"\n\n\n\t--------------> 12 called",)
        # today = fields.Date.today()
        today = datetime.now()+ timedelta(hours=5, minutes=30) - timedelta(days=1)
        today_date = today.date()
        today = today_date

        today_day = today.weekday()
        attendance_records = self.search([('check_out', '=', False)])
        now = datetime.now() + timedelta(hours=5, minutes=30)
        current_time = now.strftime("%H.%M")
        employees = self.env['hr.employee'].search([])

        print(f"\n\n\n\t--------------> 24 attendance_records",attendance_records)
        for employee in employees:
            employee_wise_todays_attendances = self.env['hr.attendance'].search(
                [('employee_id', '=', employee.id)]).filtered(lambda x: x.check_in.date() == today)

            domain = [('calendar_id', '=', employee.resource_calendar_id.id),
                      ('dayofweek', '=', today_day),
                      ('day_period', 'in', ['morning', 'afternoon']),
                      ('date_from', '<=', today),
                      ('date_to', '>=', today),
                      ]

            calendar_att_id = self.env['resource.calendar.attendance'].sudo().search(
                domain)
            if calendar_att_id:

                attendance_hrs = 0
                worked_hrs = 0

                for rec in employee_wise_todays_attendances:
                    if rec.check_in and rec.check_out:
                        total_time = rec.check_out - rec.check_in
                        if total_time:
                            duration = float(total_time.days) * \
                                24 + (float(total_time.seconds) / 3600)
                            attendance_hrs += duration

                worked_hrs = sum(calendar_att_id.mapped('sh_wroked_hours'))
                if worked_hrs - attendance_hrs > 0.5:
                    leave = self.env['hr.leave'].search([('employee_id', '=', employee.id),
                                                         ('request_date_from', '<=', today), ('request_date_to', '>=', today)])

                    if not leave:

                        if employee.id not in self.env.user.company_id.sh_employee_ids.ids:
                            self.env['sh.warning.message'].create({
                                'name': 'You have not created leave for date : '+str(today),
                                'description': 'You have not created leave for date : '+str(today)+'.Please check Attendance of that date !',
                                'user_id': employee.user_id.id,
                                'sh_create_date': date.today(),
                            })

        for attendance_record in attendance_records:
            print(f"\n\n\n\t--------------> 65 attendance_record.employee_id.name",attendance_record.employee_id.name)
            domain = [('calendar_id', '=', attendance_record.employee_id.resource_calendar_id.id),
                      ('dayofweek', '=', today_day),
                      ('day_period', '=', 'morning'),
                      ('date_from', '=', today),
                      ('date_to', '=', today),
                      ('high_priority', '=', True)
                      ]
            cal_att_id = self.env['resource.calendar.attendance'].sudo().search(
                domain, limit=1)
            if not cal_att_id:
                domain = [('calendar_id', '=', attendance_record.employee_id.resource_calendar_id.id),
                          ('dayofweek', '=', today_day),
                          ('day_period', '=', 'afternoon'),
                          ('date_from', '<=', today),
                          ('date_to', '>=', today),
                          ('high_priority', '=', False)
                          ]
                cal_att_id = self.env['resource.calendar.attendance'].sudo().search(
                    domain, limit=1)

            if not cal_att_id:
                domain = [('calendar_id', '=', attendance_record.employee_id.resource_calendar_id.id),
                          ('dayofweek', '=', today_day),
                          ('day_period', '=', 'morning'),
                          ('date_from', '<=', today),
                          ('date_to', '>=', today),
                          ('high_priority', '=', False)
                          ]
                cal_att_id = self.env['resource.calendar.attendance'].sudo().search(
                    domain, limit=1)
            print(f"\n\n\n\t--------------> 98 cal_att_id.read()",cal_att_id.read())
            print(f"\n\n\n\t--------------> 99 attendance_record.read()",attendance_record.read())
            if (cal_att_id.date_from and cal_att_id.date_to):
                print(f"\n\n\n\t--------------> 100 first if",)
                today = today - timedelta(days=1)
                if (cal_att_id.date_from <= today and cal_att_id.date_to >= today and (float(current_time)) > cal_att_id.hour_to or (float(current_time)) < cal_att_id.hour_from):
                # if True:
                    new_time = attendance_record.check_in + \
                        timedelta(hours=5, minutes=30)
                    print(f"\n\n\n\t--------------> 104 second if",)
                    attendance_record.write({
                        'check_out': new_time - timedelta(hours=5, minutes=30)
                    })



                    modification_req = self.env['sh.attendance.modification.request'].create({
                        'employee_id': attendance_record.employee_id.id,
                        'type': 'checkout',
                        'attendance_id': attendance_record.id,
                        'updated_value_checkout': attendance_record.check_out,
                        'reason': 'Please modify Your Updated value and Confirm this request'
                    })

                    if employee.id not in self.env.user.company_id.sh_employee_ids.ids:
                        self.env['sh.warning.message'].create({
                            'name': 'Please check modification request',
                            'description': 'Please check modification request',
                            'user_id': attendance_record.employee_id.user_id.id,
                            'res_model': 'sh.attendance.modification.request',
                            'res_id': modification_req.id,
                            'sh_create_date': date.today()
                        })

                    print(f"\n\n\n\t--------------> 125 employee",employee)
                    running_tasks = attendance_record.employee_id.user_id.task_running_ids
                    base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

                    if running_tasks:
                        print(f"\n\n\n\t--------------> 134 attendance_ercord.employee_id.user_id.task_running_ids",running_tasks)
                        for task in running_tasks:
                            timesheet = self.env['account.analytic.line'].sudo().browse(task.account_analytic_id.id)
                            if timesheet and timesheet.id != attendance_record.employee_id.user_id.active_running_task_id.id:
                                print(f"\n\n\n\t--------------> 138 task.read()",task.read())
                                timesheet.write({'end_date':datetime.now(),
                                                'unit_amount':task.difference_time_float})
                                notify = self.env['user.push.notification'].push_notification(attendance_record.employee_id.user_id, 'Please update timesheet hours.',
                                                                               'Please update timesheet hours.',
                                                                               base_url+"/mail/view?model=project.task&res_id=" +
                                                                               str(
                                                                                   timesheet.task_id.id),
                                                                               'project.task', timesheet.task_id.id, 'project')
                                print(f"\n\n\n\t--------------> 149 notify",notify)
                        # Clear paused timesheets (task_running_ids)
                        attendance_record.employee_id.user_id.task_running_ids = [(5, 0, 0)]
                        print(f"\n\n\n\t--------------> 140 attendance_record.employee_id.user_id.task_running_ids",attendance_record.employee_id.user_id.task_running_ids)
                        pass



                    timesheet_line = self.env['account.analytic.line'].sudo().search(
                        [('task_id', '=', attendance_record.employee_id.user_id.task_id.id), ('employee_id.user_id',
                                                                                              '=', attendance_record.employee_id.user_id.id), ('end_date', '=', False)],
                        limit=1)
                    if timesheet_line and attendance_record.employee_id and attendance_record.employee_id.user_id and attendance_record.employee_id.user_id.task_id:
                        self.env['mail.activity'].sudo().create({
                            'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                            'user_id': attendance_record.employee_id.user_id.id,
                            'res_id': attendance_record.employee_id.user_id.task_id.id,
                            'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'project.task')], limit=1).id,
                            'summary': 'Please update timesheet hours.',
                        })

                        listt = []
                        listt.append(attendance_record.employee_id.user_id)
                        base_url = self.env['ir.config_parameter'].sudo(
                        ).get_param('web.base.url')
                        self.env['user.push.notification'].push_notification(listt, 'Please update timesheet hours.',
                                                                           'Please update timesheet hours.',
                                                                           base_url+"/mail/view?model=project.task&res_id=" +
                                                                           str(
                                                                               attendance_record.employee_id.user_id.task_id.id),
                                                                           'project.task', attendance_record.employee_id.user_id.task_id.id, 'project')

                        timesheet_line.write({'end_date': datetime.now()})
                    self.sudo()._cr.commit()
                    attendance_record.employee_id.user_id.write(
                        {'task_id': False, 'start_time': None})

                    # notifications = []
                    # if attendance_record.employee_id:
                    #     notifications.append([
                    #         (self._cr.dbname, 'res.partner',
                    #          attendance_record.employee_id.user_id.partner_id.id),
                    #         {'type': 'simple_notification', 'title': _('Notification'),  'message': "Please Check Modification Request " + modification_req.name,
                    #             'sticky': True, 'warning': False}
                    #     ])idid
                    # self.env['bus.bus'].sendmany(notifications)
                    listt = []
                    listt.append(attendance_record.employee_id.user_id)
                    base_url = self.env['ir.config_parameter'].sudo(
                    ).get_param('web.base.url')
                    self.env['user.push.notification'].push_notification(listt, 'Please Check Modification Request',
                                                                       'Please Check Modification Request',
                                                                       base_url+"/mail/view?model=sh.attendance.modification.request&res_id=" +
                                                                       str(modification_req),
                                                                       'sh.attendance.modification.request', modification_req, 'hr')
            if not (cal_att_id.date_from and cal_att_id.date_to):
                if ((float(current_time)) > cal_att_id.hour_to or (float(current_time)) < cal_att_id.hour_from):
                    new_time = now.replace(hour=int(cal_att_id.hour_to), minute=int(
                        (cal_att_id.hour_to - int(cal_att_id.hour_to))*60))
                    attendance_record.write({
                        'check_out': (new_time - timedelta(hours=5, minutes=30)).replace(microsecond=0)

                    })

                    modification_req = self.env['sh.attendance.modification.request'].create({
                        'employee_id': attendance_record.employee_id.id,
                        'type': 'checkout',
                        'attendance_id': attendance_record.id,
                        'updated_value_checkout': attendance_record.check_out,
                        'reason': 'Please modify Your Updated value and Confirm this request'
                    })

                    if employee.id not in self.env.user.company_id.sh_employee_ids.ids:
                        self.env['sh.warning.message'].create({
                            'name': 'Please check modification request',
                            'description': 'Please check modification request',
                            'user_id': attendance_record.employee_id.user_id.id,
                            'res_model': 'sh.attendance.modification.request',
                            'res_id': modification_req.id,
                            'sh_create_date': date.today()
                        })


                    if running_tasks:
                        print(f"\n\n\n\t--------------> 134 attendance_ercord.employee_id.user_id.task_running_ids",running_tasks)
                        for task in running_tasks:
                            timesheet = self.env['account.analytic.line'].sudo().browse(task.account_analytic_id.id)
                            if timesheet and timesheet.id != attendance_record.employee_id.user_id.active_running_task_id.id:

                                print(f"\n\n\n\t--------------> 138 task.read()",task.read())
                                timesheet.write({'end_date':datetime.now(),
                                                'unit_amount':task.difference_time_float})
                                notify = self.env['user.push.notification'].push_notification(attendance_record.employee_id.user_id, 'Please update timesheet hours.',
                                                                               'Please update timesheet hours.',
                                                                               base_url+"/mail/view?model=project.task&res_id=" +
                                                                               str(
                                                                                   timesheet.task_id.id),
                                                                               'project.task', timesheet.task_id.id, 'project')
                                print(f"\n\n\n\t--------------> 149 notify",notify)
                        # Clear paused timesheets (task_running_ids)
                        attendance_record.employee_id.user_id.task_running_ids = [(5, 0, 0)]
                        print(f"\n\n\n\t--------------> 140 attendance_record.employee_id.user_id.task_running_ids",attendance_record.employee_id.user_id.task_running_ids)

                    timesheet_line = self.env['account.analytic.line'].sudo().search(
                        [('task_id', '=', attendance_record.employee_id.user_id.task_id.id), ('employee_id.user_id',
                                                                                              '=', attendance_record.employee_id.user_id.id), ('end_date', '=', False)],
                        limit=1)
                    if timesheet_line and attendance_record.employee_id and attendance_record.employee_id.user_id and attendance_record.employee_id.user_id.task_id:
                        activity = self.env['mail.activity'].sudo().create({
                            'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                            'user_id': attendance_record.employee_id.user_id.id,
                            'res_id': attendance_record.employee_id.user_id.task_id.id,
                            'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'project.task')], limit=1).id,
                            'summary': 'Please update timesheet hours.',
                        })
                        listt = []
                        listt.append(attendance_record.employee_id.user_id)
                        base_url = self.env['ir.config_parameter'].sudo(
                        ).get_param('web.base.url')
                        self.env['user.push.notification'].push_notification(listt, 'Please update timesheet hours.',
                                                                           'Please update timesheet hours.',
                                                                           base_url+"/mail/view?model=project.task&res_id=" +
                                                                           str(
                                                                               attendance_record.employee_id.user_id.task_id.id),
                                                                           'project.task', attendance_record.employee_id.user_id.task_id.id, 'project')

                        timesheet_line.write({'end_date': datetime.now()})
                    self.sudo()._cr.commit()
                    attendance_record.employee_id.user_id.write(
                        {'task_id': False, 'start_time': None})

                    # notifications = []
                    # if attendance_record.employee_id:
                    #     notifications.append([
                    #         (self._cr.dbname, 'res.partner',
                    #          attendance_record.employee_id.user_id.partner_id.id),
                    #         {'type': 'simple_notification', 'title': _('Notification'),  'message': "Please Check Modification Request " + modification_req.name,
                    #             'sticky': True, 'warning': False}
                    #     ])
                    # self.env['bus.bus'].sendmany(notifications)
                    listt = []
                    listt.append(attendance_record.employee_id.user_id)
                    self.env['user.push.notification'].push_notification(listt, 'Please Check Modification Request',
                                                                       'Please Check Modification Request',
                                                                       base_url+"/mail/view?model=sh.attendance.modification.request&res_id=" +
                                                                       str(modification_req),
                                                                       'sh.attendance.modification.request', modification_req, 'hr')
