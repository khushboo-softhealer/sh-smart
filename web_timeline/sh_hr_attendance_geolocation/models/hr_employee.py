# Part of Softhealer Technologies.
from odoo import models, fields,  exceptions, _, api, SUPERUSER_ID
from datetime import timedelta, datetime
from datetime import date
import calendar
import math
from odoo.exceptions import UserError


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    total_overtime = fields.Float(
        compute='_compute_total_overtime', compute_sudo=True,groups=False
        # groups="hr_attendance.group_hr_attendance_kiosk,hr_attendance.group_hr_attendance,hr.group_hr_user"
        )
    attendance_activity = fields.Many2one('mail.activity',string="Activity")
    late_message_id=fields.Many2one('mail.message',string="Late Message")
    sh_allow_late_check_in = fields.Boolean(string='Allow Late Check-in',default=False)
    
    sh_attendance_state = fields.Selection(string="Attendance Status ", compute='sh_compute_attendance_state', selection=[
                                           ('checked_out', "Checked out"), ('checked_in', "Checked in")])
    # inherited hr.employee model to override methods

    @api.depends('last_attendance_id.check_in', 'last_attendance_id.check_out', 'last_attendance_id.sh_break_start')
    def sh_compute_attendance_state(self):

        for employee in self:
            att = employee.last_attendance_id.sudo()
            employee.sh_attendance_state = att and not att.check_out and 'checked_in' or 'checked_out'

            if employee.last_attendance_id.sh_break_start:
                employee.sh_attendance_state = 'checked_out'
    
    def sh_allow_late_employee_action(self):
        for rec in self:
            if rec.sh_allow_late_check_in:
                rec.sudo().sh_allow_late_check_in=False
                message_id=self.env['mail.message'].sudo().create({
                    'subject': 'Late Check in..',
                    'date': fields.Datetime.now(),
                    'author_id': self.env.user.partner_id.id,
                    'record_name': rec.name,
                    'model': 'hr.employee',
                    'res_id': rec.id,
                    'message_type': 'comment',
                    'subtype_id': self.env.ref('mail.mt_note').id,
                    'body': 'Meeting Subject : You are late more then 5 times per month.',
                    
                })
                if message_id:
                    rec.sudo().late_message_id=message_id.id

            
    @api.model
    def sh_get_break_duration(self):
        related_employee = self.env['hr.employee'].sudo().search(
            [('user_id', '=', self.env.uid)], limit=1)
        if related_employee:
            break_attendance = self.env['hr.attendance'].sudo().search([('employee_id', '=', related_employee.id), (
                'sh_break_start', '!=', False), ('sh_break_end', '=', False), ('check_out', '=', False)], limit=1, order='id desc')
            if break_attendance:
                return True
            else:
                return False

    def sh_onchange_break(self, vals):

        users = self.env['res.users'].search([])
        hr_listt = []

        for user in users:
            if user.has_group('hr.group_hr_manager'):
                hr_listt.append(user)
        base_url = self.env['ir.config_parameter'].sudo(
        ).get_param('web.base.url')

        last_attendance_id = self.env['hr.attendance'].sudo().search(
            [('employee_id', '=', self.id), ('check_in', '!=', False), ('check_out', '=', False)], limit=1)
        if last_attendance_id:
            if vals[1] == True:
                today = fields.Date.today()
                today_day = today.weekday()
                cal_att_id = self.env['resource.calendar.attendance'].sudo().search([('date_from', '=', today), ('date_to', '=', today), (
                    'calendar_id', '=', self.resource_calendar_id.id), ('dayofweek', '=', today_day), ('high_priority', '=', True)])
                if not cal_att_id:
                    cal_att_id = self.env['resource.calendar.attendance'].sudo().search([('date_from', '<=', today), ('date_to', '>=', today), (
                        'calendar_id', '=', self.resource_calendar_id.id), ('dayofweek', '=', today_day), ('high_priority', '=', False)])

                if not cal_att_id:
                    cal_att_id = self.env['resource.calendar.attendance'].sudo().search([('date_from', '=', False), (
                        'date_to', '=', False), ('calendar_id', '=', self.resource_calendar_id.id), ('dayofweek', '=', today_day)])

                if cal_att_id:
                    calendar_id = cal_att_id[0]
                    if calendar_id and calendar_id.sh_break > 0:

                        if self.user_id.task_id:
                            # return {'warning': _('Please Stop Your task timer first  !')}
                            raise UserError ("Take a moment to pause your timer as you go on your break !")


                        last_attendance_id.sudo().write({
                            'sh_break_start': fields.Datetime.now(),
                            'sh_break_start_date': fields.Datetime.now().date(),
                            'sh_break_end': False,

                        })

                        return {'warning': _('Break Start'), 'timer_start': True, 'duration': 0}
                    else:
                        return {'warning_break': _('You can not Take Break.'), 'timer_start': True, 'duration': 0}
            else:
                last_attendance_id = self.env['hr.attendance'].sudo().search(
                    [('employee_id', '=', self.id), ('sh_break_end', '=', False), ('sh_break_start', '!=', False)], limit=1)

                if last_attendance_id:
                    today = fields.Date.today()
                    today_day = today.weekday()
                    cal_att_id = self.env['resource.calendar.attendance'].sudo().search([('date_from', '=', today), ('date_to', '=', today), (
                        'calendar_id', '=', self.resource_calendar_id.id), ('dayofweek', '=', today_day), ('high_priority', '=', True)])
                    if not cal_att_id:
                        cal_att_id = self.env['resource.calendar.attendance'].sudo().search([('date_from', '<=', today), ('date_to', '>=', today), (
                            'calendar_id', '=', self.resource_calendar_id.id), ('dayofweek', '=', today_day), ('high_priority', '=', False)])

                    if not cal_att_id:
                        cal_att_id = self.env['resource.calendar.attendance'].sudo().search([('date_from', '=', False), (
                            'date_to', '=', False), ('calendar_id', '=', self.resource_calendar_id.id), ('dayofweek', '=', today_day)])

                    if cal_att_id:
                        calendar_id = cal_att_id[0]
                        if calendar_id and calendar_id.sh_break > 0:
                            break_start = last_attendance_id.sh_break_start + \
                                timedelta(hours=5, minutes=30, seconds=0)
                            now = fields.Datetime.now() + timedelta(hours=5, minutes=30, seconds=0)
                            break_duration = now - break_start
                            break_duration_in_hours = break_duration.seconds / 3600
                            if break_duration_in_hours > calendar_id.sh_break and vals[0] == '':
                                if vals[0] == '':
                                    return {'warning_end': _('Please Enter Reason for your break hours are extended !')}
                            else:
                                if vals[0] != '':
                                    break_extended_in_minutes = (
                                        break_duration_in_hours - calendar_id.sh_break)*60

                                    action = self.env.ref(
                                        'hr_attendance.hr_attendance_action')
                                    self.env['user.push.notification'].hr_push_notification(hr_listt, "Break Hour Extend %s minutes" % (int(break_extended_in_minutes)), "%s's :  %s." % (
                                        self.name, vals[0]), base_url+'/web?&#min=1&limit=80&view_type=list&model=hr.attendance&action=%s' % (action.id), 'hr.attendance', action.id, 'hr',self.env.ref('sh_push_notification_tile.sh_break_extend'))
                                employee_id = self.env['hr.employee'].sudo().search(
                                    [('user_id', '=', self.env.uid)], limit=1)
                                if employee_id:

                                    if vals[0] != '':
                                        last_attendance_id.sudo().write({
                                            'sh_break_end': fields.Datetime.now(),
                                            'check_out': last_attendance_id.sh_break_start,
                                            'sh_break_over': True,
                                            'sh_break_reason': vals[0]
                                        })
                                    else:
                                        last_attendance_id.sudo().write({
                                            'sh_break_end': fields.Datetime.now(),
                                            'check_out': last_attendance_id.sh_break_start,
                                            'sh_break_over': True
                                        })
                                    new_attendance = self.env['hr.attendance'].sudo().create({
                                        'employee_id': employee_id.id,
                                        'check_in': fields.Datetime.now(),
                                    })
                                    return {'warning': _('Break End'), 'timer_start': False}

       # inherited hr.employee model to override methods

    def sh_attendance_manual(self, vals, next_action, entered_pin=None):
        users = self.env['res.users'].search([])
        hr_listt = []
        for user in users:
            if user.has_group('hr.group_hr_manager'):
                hr_listt.append(user)
        base_url = self.env['ir.config_parameter'].sudo(
        ).get_param('web.base.url')

        self.ensure_one()
        today = fields.Date.today()
        today_day = today.weekday()
        cal_att_id = self.env['resource.calendar.attendance'].sudo().search([('date_from', '=', today), ('date_to', '=', today), (
            'calendar_id', '=', self.resource_calendar_id.id), ('dayofweek', '=', today_day), ('high_priority', '=', True)])
        if not cal_att_id:
            cal_att_id = self.env['resource.calendar.attendance'].sudo().search([('date_from', '<=', today), ('date_to', '>=', today), (
                'calendar_id', '=', self.resource_calendar_id.id), ('dayofweek', '=', today_day), ('high_priority', '=', False)])

        if not cal_att_id:
            cal_att_id = self.env['resource.calendar.attendance'].sudo().search([('date_from', '=', False), (
                'date_to', '=', False), ('calendar_id', '=', self.resource_calendar_id.id), ('dayofweek', '=', today_day)])

        if cal_att_id:
            if self.attendance_state == 'checked_out':
                date_start = str(today) + " 00:00:00"
                date_start_end = str(today) + " 23:59:59"
                attendance_id = self.env['hr.attendance'].sudo().search(
                    [('employee_id', '=', self.id), ('check_in', '>=', date_start), ('check_out', '<=', date_start_end)])
                if not attendance_id:
                    calendar_id = cal_att_id[0]
                    if calendar_id and self.resource_calendar_id.sh_late_early_restriction > 0:
                        now = fields.Datetime.now() + timedelta(hours=5, minutes=30, seconds=0)
                        current_time = now.strftime("%H:%M")
                        current_time_split = [int(n)
                                              for n in current_time.split(":")]
                        current_time_float = current_time_split[0] + \
                            current_time_split[1] / 60.0
                        allow_time = calendar_id.hour_from + \
                            self.resource_calendar_id.sh_late_early_restriction
                        # check if leave applied
                        leave_applied = self.env['hr.leave'].sudo().search([('request_date_from', '=', fields.Date.today()), ('employee_id', '=', self.id), (
                            'request_unit_hours', '=', True), ('custom_hour_from', '=', calendar_id.hour_from), ('state', 'in', ['validate', 'validate1'])], limit=1)

                        half_leave_applied = self.env['hr.leave'].sudo().search([('request_date_from', '=', fields.Date.today()),
                                                                                 ('employee_id', '=', self.id), (
                                                                                     'request_unit_half', '=', True),
                                                                                 ('request_date_from_period', '=', 'am'), ('state', 'in', ['validate', 'validate1'])], limit=1)

                        if allow_time < current_time_float and not leave_applied and not half_leave_applied:
                            # check total late coming of month
                            start_day_of_prev_month = date.today().replace(day=1)
                            no_of_days_in_month = calendar.monthrange(
                                date.today().year, date.today().month)[1]
                            last_day_of_prev_month = date.today().replace(day=no_of_days_in_month)

                            start_datetime_of_prev_month = datetime.strftime(
                                start_day_of_prev_month, "%Y-%m-%d 00:00:00")
                            last_datetime_of_prev_month = datetime.strftime(
                                last_day_of_prev_month, "%Y-%m-%d 23:59:59")

                            last_attendances = self.env['hr.attendance'].sudo().search([('employee_id', '=', self.id), ('check_in', '>=', start_datetime_of_prev_month), ('check_out', '<=', last_datetime_of_prev_month),
                                                                                        ('message_in', '!=', '')])
                            if len(last_attendances) >= 5:
                                if not self.sudo().late_message_id and not self.sudo().sh_allow_late_check_in:
                                    self.sudo().sh_allow_late_check_in=True
                                    return {'warning': _('You are late more then 5 times per month ! Please contact your manager !')}
                                if not self.sudo().late_message_id and  self.sudo().sh_allow_late_check_in:    
                                    return {'warning': _('You are late more then 5 times per month ! Please contact your manager !')}
                                if vals[0] == '':
                                    return {'warning': _('Please Enter Reason for Late coming !')}
                                # if not self.attendance_activity or self.attendance_activity.date_deadline != date.today():
                                #     activity = self.env['mail.activity'].sudo().create({
                                #         'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                                #         'user_id': self.sudo().parent_id.user_id.id or self.sudo().hr_manager.user_id.id,
                                #         'res_id': self.id,
                                #         'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'hr.employee')], limit=1).id,
                                #         'summary': 'Meeting Subject : You are late more then 5 times per month',
                                #     })
                                #     self.env.cr.execute(
                                #         """ update hr_employee set attendance_activity=%s where id=%s """ % (activity.id, self.id))
                                #     return {'warning': _('You are late more then 5 times per month ! Please contact your manager !')}

                                # if self.attendance_activity and self.attendance_activity.state != 'done':
                                #     return {'warning': _('You are late more then 5 times per month ! Please contact your manager !')}
                            
                            
                            elif len(last_attendances) >= 4 and vals[0] == '':
                                return {'warning': _('You have reached the limit of late coming ! Please Enter Reason for Late coming !')}
                            elif vals[0] == '':
                                return {'warning': _('Please Enter Reason for Late coming !')}
                            else:

                                late_check_in_msg_for_hr = ''
                                late_time_in_hrs = current_time_float - allow_time
                                fractional_part, int_part = math.modf(
                                    late_time_in_hrs)
                                if int_part != 0:
                                    late_check_in_msg_for_hr += str(
                                        int_part) + ' hour '

                                if fractional_part != 0:
                                    late_check_in_msg_for_hr += str(
                                        round(fractional_part * 60, 2)) + ' minute'

                                action = self.env.ref(
                                    'hr_attendance.hr_attendance_action')
                                self.env['user.push.notification'].hr_push_notification(hr_listt, "Late Check in %s late" % (late_check_in_msg_for_hr), "%s's Check in is late due to  %s." % (
                                    self.name, vals[0]), base_url+'/web?&#min=1&limit=80&view_type=list&model=hr.attendance&action=%s' % (action.id), 'hr.attendance', action.id, 'hr',self.env.ref('sh_push_notification_tile.sh_late_coming'))

            elif self.attendance_state == 'checked_in':
                if len(cal_att_id) > 1:
                    calendar_id = cal_att_id[1]
                else:
                    calendar_id = cal_att_id[0]
                if self.user_id.task_id:
                    return {'warning': _('Please Stop Your task timer first !')}

                if calendar_id and self.resource_calendar_id.sh_late_early_restriction > 0:
                    now = fields.Datetime.now() + timedelta(hours=5, minutes=30, seconds=0)
                    current_time = now.strftime("%H:%M")
                    current_time_split = [int(n)
                                          for n in current_time.split(":")]
                    current_time_float = current_time_split[0] + \
                        current_time_split[1] / 60.0
                    allow_time = calendar_id.hour_to - \
                        self.resource_calendar_id.sh_late_early_restriction
                    # if allow_time > current_time_float:
                        # check if leave applied
                        # leave_applied = self.env['hr.leave'].sudo().search([('request_date_from', '<=', fields.Date.today()),
                        #                                                 ('request_date_to', '>=', fields.Date.today()), ('employee_id', '=', self.id), ('state', 'in', ['validate', 'validate1'])], limit=1)


                        # if vals[0] == '' and vals[3] == True and not leave_applied:
                        #     return {'warning': _('Please Enter Reason for Early Going !')}

                        # if vals[0] and vals[3] == True:

                        #     early_check_out_msg_for_hr = ''
                        #     early_going_in_hrs = allow_time - current_time_float
                        #     fractional_part, int_part = math.modf(
                        #         early_going_in_hrs)
                        #     if int_part != 0:
                        #         early_check_out_msg_for_hr += str(
                        #             int_part) + ' hour '

                        #     if fractional_part != 0:
                        #         early_check_out_msg_for_hr += str(
                        #             round(fractional_part * 60, 2)) + ' minute'

                        #     action = self.env.ref(
                        #         'hr_attendance.hr_attendance_action')
                        #     self.env['user.push.notification'].hr_push_notification(hr_listt, "Early Check Out %s" % (early_check_out_msg_for_hr), "%s's Check Out is early due to  %s." % (
                        #         self.name, vals[0]), base_url+'/web?&#min=1&limit=80&view_type=list&model=hr.attendance&action=%s' % (action.id), 'hr.attendance', action.id, 'hr',self.env.ref('sh_push_notification_tile.sh_early_going'))

                date_start = str(today) + " 00:00:00"
                date_start_end = str(today) + " 23:59:59"
                listt_cal_hour = []
                for cal_att in cal_att_id:
                    listt_cal_hour.append(cal_att.hour_to - cal_att.hour_from)

                listt = []
                attendance_ids = self.env['hr.attendance'].sudo().search(
                    [('employee_id', '=', self.id), ('check_in', '>=', date_start)])
                if attendance_ids:
                    for attendance_id in attendance_ids:
                        listt.append(attendance_id.total_time)

                    current_attendance_ids = self.env['hr.attendance'].sudo().search(
                        [('employee_id', '=', self.id), ('check_in', '>=', date_start), ('check_out', '=', False)])
                    if current_attendance_ids:
                        for current_attendance_id in current_attendance_ids:
                            attendance_time = fields.Datetime.now() - current_attendance_id.check_in
                            duration = float(
                                attendance_time.days) * 24 + (float(attendance_time.seconds) / 3600)
                            listt.append(duration)

                    allowe_late_early = attendance_ids[0].employee_id.resource_calendar_id.sh_late_early_restriction
                    timesheet_lines = self.env['account.analytic.line'].sudo().search(
                        [('employee_id', '=', self.id), ('date', '=', today), ('task_id.is_temp_task', '=', False)])

                    total_timesheet = sum(
                        timesheet_lines.mapped('unit_amount'))
                    leave_taken = self.env['hr.leave'].sudo().search([('employee_id', '=', self.id),
                                                                      ('request_date_from', '<=', date_start), (
                                                                          'request_date_to', '>=', date_start_end),
                                                                      ('state', 'not in', ['cancel', 'refuse', 'draft'])], limit=1)

                    leave_hours = leave_taken.number_of_hours_display
                    if leave_taken.number_of_hours_display > sum(listt_cal_hour):
                        leave_hours = sum(listt_cal_hour)

                    # Timesheet validation based on working time setting
                    if self.resource_calendar_id.timesheet_validation_after > 0.0:
                        current_time = now.strftime("%H:%M")
                        current_time_split = [int(n)
                                            for n in current_time.split(":")]
                        current_time_float = current_time_split[0] + \
                            current_time_split[1] / 60.0
                        
                        if self.resource_calendar_id.timesheet_validation_after  < current_time_float:
                            if total_timesheet < (sum(listt_cal_hour) - leave_hours - 0.25):
                                return {'warning': _('Your today\'s timesheet is incomplete, and no leave records have been found. Kindly reach out to your team leader for assistance.')}


                    if vals[3] == True and total_timesheet < (sum(listt_cal_hour) - leave_hours - 0.25):
                        return {'warning': _('Your today\'s timesheet is incomplete, and no leave records have been found. Kindly reach out to your team leader for assistance.')}

                     # check if leave applied
                    leave_applied = self.env['hr.leave'].sudo().search([('request_date_from', '<=', fields.Date.today()),
                                                                        ('request_date_to', '>=', fields.Date.today()), ('employee_id', '=', self.id), ('state', 'in', ['validate', 'validate1'])], limit=1)

                    if leave_applied:
                        allowe_late_early += leave_applied.number_of_hours_display

                    if ((sum(listt) + allowe_late_early) < sum(listt_cal_hour)):
                        if vals[0] == '' and vals[3] == True:
                            return {'warning': _('Your work hours not completed. Please Enter Reason !')}

                        if vals[0] and vals[3] == True:
                            action = self.env.ref(
                                'hr_attendance.hr_attendance_action')
                            self.env['user.push.notification'].hr_push_notification(hr_listt, 'Less Work Hours', "%s's work hours is not completed due to %s." % (
                                self.name, vals[0]), base_url+'/web?&#min=1&limit=80&view_type=list&model=hr.attendance&action=%s' % (action.id), 'hr.attendance', action.id, 'hr',self.env.ref('sh_push_notification_tile.sh_less_work_hours'))

        if not (entered_pin is None) or self.env['res.users'].browse(SUPERUSER_ID).has_group('hr_attendance.group_hr_attendance_use_pin') and (self.user_id and self.user_id.id != self._uid or not self.user_id):
            if entered_pin != self.pin:
                return {'warning': _('Wrong PIN')}
        self.sudo().late_message_id=False
        return self.sh_attendance_action(next_action, vals)

    def sh_attendance_action(self, next_action, vals):
        """ Changes the attendance of the employee.
            Returns an action to the check in/out message,
            next_action defines which menu the check in/out message should return to. ("My Attendances" or "Kiosk Mode")
        """
        self.ensure_one()
        self = self.sudo()
        employee = self.sudo()
        message = vals
        action_message = self.env.ref(
            'hr_attendance.hr_attendance_action_greeting_message').read()[0]
        action_message['previous_attendance_change_date'] = employee.last_attendance_id and (
            employee.last_attendance_id.check_out or employee.last_attendance_id.check_in) or False
        action_message['employee_name'] = employee.name
        action_message['barcode'] = employee.barcode
        action_message['next_action'] = next_action
        # action_message['hours_today'] = employee.hours_today

        if employee.user_id:
            modified_attendance = employee.with_user(
                employee.user_id).sh_attendance_action_change(message)
        else:
            modified_attendance = employee.sh_attendance_action_change(message)
        action_message['attendance'] = modified_attendance.read()[0]
        return {'action': action_message}

    def sh_attendance_action_change(self, message):
        """ Check In/Check Out action
            Check In: create a new attendance record
            Check Out: modify check_out field of appropriate attendance record
        """
        check_in_out_message = message[0]
        vals = {}
        latitude = message[1]
        longitude = message[2]
        url = "http://maps.google.com/maps?"

        url = "http://maps.google.com/maps?q=" + \
            str(latitude) + ',' + str(longitude)

        if url:
            vals = {'check_in_url': url}

        if len(self) > 1:
            raise exceptions.UserError(
                _('Cannot perform check in or check out on multiple employees.'))
        action_date = fields.Datetime.now()

        if self.attendance_state != 'checked_in':
            vals.update({
                'employee_id': self.id,
                'check_in': action_date,
                'message_in': check_in_out_message,
            })
            if latitude and longitude:
                vals.update({
                    'in_latitude': latitude,
                    'in_longitude': longitude,
                })
            return self.env['hr.attendance'].sudo().create(vals)

        else:
            attendance = self.env['hr.attendance'].sudo().search(
                [('employee_id', '=', self.id), ('check_out', '=', False)], limit=1)
            attendance.message_out = check_in_out_message
            if latitude and longitude:
                attendance.check_out_url = url
                attendance.out_latitude = latitude
                attendance.out_longitude = longitude
            if attendance:
                attendance.check_out = action_date
            else:
                raise exceptions.UserError(_('Cannot perform check out on %(empl_name)s, could not find corresponding check in. '
                                             'Your attendances have probably been modified manually by human resources.') % {'empl_name': self.name, })
            return attendance


class HrEmployee(models.Model):
    _inherit = "hr.employee.public"

    attendance_activity = fields.Many2one('mail.activity')
    sh_attendance_state = fields.Selection(string="Attendance Status ", compute='sh_compute_attendance_state', selection=[
                                           ('checked_out', "Checked out"), ('checked_in', "Checked in")])

    total_overtime = fields.Float(related='employee_id.total_overtime', readonly=True,groups=False
                                  # groups="hr_attendance.group_hr_attendance_kiosk,hr_attendance.group_hr_attendance")
                                  )
