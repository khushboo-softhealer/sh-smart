# -*- coding: UTF-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api, _
import pytz
from datetime import timedelta
import pytz
from datetime import datetime



class AttendanceModofocationRequest(models.Model):
    _inherit = ['mail.thread',
                'mail.activity.mixin']
    _name = 'sh.attendance.modification.request'
    _description = "Attendance Modification Request"
    _rec_name = "user_id"

    def _default_employee(self):
        return self.env.context.get('default_employee_id') or self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    user_id = fields.Many2one('res.users', related='employee_id.user_id',store=True, readonly=True)
    name = fields.Char(tracking=True)
    employee_id = fields.Many2one(
        'hr.employee', readonly=True, default=_default_employee, tracking=True)
    date = fields.Date(default=fields.Date.today(),
                       required=True, tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('waiting_for_approve', 'Waiting For Approve'), ('approved', 'Approved'), (
        'cancel', 'Cancel'),  ('reject', 'Reject')], default='draft', tracking=True)
    type = fields.Selection(selection=[(
        'checkin', 'Check In'), ('checkout', 'Check Out'), ('both', 'Both')], required=True, default="checkin", tracking=True)
    attendance_id = fields.Many2one(
        'hr.attendance', required=True, tracking=True)
    reason = fields.Text(required=True,
                         tracking=True)
    updated_value = fields.Datetime(
        string='Updated Value Checkin', tracking=True)
    rejection_reason = fields.Char(tracking=True)
    updated_value_checkout = fields.Datetime(tracking=True)
    checkin_alert = fields.Boolean('Checkin Alert', default=False)
    checkout_alert = fields.Boolean('Checkout Alert', default=False)

    sh_timesheet_count = fields.Float(compute="compute_timesheet_count")
    sh_leave_count = fields.Integer(compute="compute_leave_count")
    sh_attendance_count = fields.Float(
        compute="compute_attendance_count_for_modif")

    less_timesheet_alert = fields.Boolean(
        compute="compute_late_timesheet_alert")

    @api.onchange('attendance_id', 'type')
    def _onchange_attendance(self):
        if self.attendance_id:
            self.updated_value = self.attendance_id.check_in
            self.updated_value_checkout = self.attendance_id.check_out

    @api.model_create_multi
    def create(self, vals_list):
        res = super(AttendanceModofocationRequest, self).create(vals_list)
        for vals in vals_list:
            sequence1 = self.env['ir.sequence'].sudo(
            ).next_by_code('sh.attendance.modification.request')
            res.name = sequence1
        return res

    def confirm(self):
        template = self.env.ref(
            'sh_attendance_modification_request.sh_attendance_modification_request_email_tmpl', raise_if_not_found=False)
        
        # value = self.updated_value_checkout
       
        # updated_value = value-timedelta(hours=6, minutes=30, seconds=0)
        # updated_value = str(updated_value)

        for i in self:
            user_tz = pytz.timezone(
                self.env.context.get("tz") or self.env.user.tz or "UTC")
            if i.attendance_id.check_in:
                date_today = pytz.utc.localize(
                    i.attendance_id.check_in).astimezone(user_tz)
                date_today = str(date_today)

        email_to = self.employee_id.sudo().parent_id.work_email
        email_from = self.employee_id.work_email
        # if template:
        #     email_values = {
        #         'email_to': email_to, 'email_from': email_from}
        #     template.send_mail(self.id,
        #                        email_values=email_values, force_send=True, email_layout_xmlid='mail.mail_notification_light')

        # self.env['bus.bus']._sendone(self.employee_id.sudo().parent_id.user_id.partner_id, 'simple_notification', {
        #     'title': _("Notification"),
        #     'message': _('Modification Request %(partner_names)s submitted by  %(employee)s', partner_names=self.name, employee=self.employee_id.name)
        # })

        self.state = "waiting_for_approve"

        listt = []
        users = self.env['res.users'].search([])
        for user in users:
            if user.has_group('hr.group_hr_manager'):
                listt.append(user)

        base_url = self.env['ir.config_parameter'].sudo(
        ).get_param('web.base.url')
        self.env['user.push.notification'].hr_push_notification(listt,'Modification Request Created','New attendance modification request created by %s:'% (self.employee_id.name),base_url+"/mail/view?model=sh.attendance.modification.request&res_id="+str(self.id),
                                                           'sh.attendance.modification.request',self.id,'hr',self.env.ref('sh_push_notification_tile.sh_attendance_modification'))




    def compute_leave_count(self):
        for rec in self:
            rec.sh_leave_count = 0
            check_in_date = self.attendance_id.check_in.date()
            rec.sh_leave_count = len(self.env['hr.leave'].search([('employee_id', '=', self.employee_id.id)]).filtered(
                lambda x: x.request_date_from and x.request_date_from == check_in_date))

    def compute_timesheet_count(self):
        for rec in self:
            rec.sh_timesheet_count = 0
            check_in_date = self.attendance_id.check_in.date()
            timesheets = self.env['account.analytic.line'].search(
                [('employee_id', '=', self.employee_id.id)]).filtered(lambda x: x.date == check_in_date)
            rec.sh_timesheet_count = sum(timesheets.mapped('unit_amount'))

    def action_view_timesheet(self):
        check_in_date = self.attendance_id.check_in.date()
        timesheets = self.env['account.analytic.line'].search(
            [('employee_id', '=', self.employee_id.id)]).filtered(lambda x: x.date == check_in_date)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Timesheets',
            'view_mode': 'tree,form',
            'res_model': 'account.analytic.line',
            'domain': [('id', 'in', timesheets.ids)],
        }

    def approve(self):
        if self.type == 'checkout':
            self.attendance_id.check_out = self.updated_value_checkout
        elif self.type == 'checkin':
            self.attendance_id.check_in = self.updated_value
        else:
            self.attendance_id.check_out = self.updated_value_checkout
            self.attendance_id.check_in = self.updated_value

        template = self.env.ref(
            'sh_attendance_modification_request.sh_attendance_modification_request_email_approve_tmpl', raise_if_not_found=False)
        email_to = self.employee_id.work_email
        email_from = self.employee_id.parent_id.work_email

        if template:
            email_values = {
                'email_to': email_to, 'email_from': email_from}
            # template.send_mail(self.id,
            #                    email_values=email_values, force_send=True, email_layout_xmlid='mail.mail_notification_light')

        # self.env['bus.bus']._sendone(self.employee_id.user_id.partner_id, 'simple_notification', {
        #     'title': _("Notification"),
        #     'message': _('%(partner_names)s  has been approved by  %(employee)s', partner_names=self.name, employee=self.employee_id.parent_id.name)
        # })

        self.state = "approved"
        base_url = self.env['ir.config_parameter'].sudo(
        ).get_param('web.base.url')
        self.env['user.push.notification'].hr_push_notification([self.employee_id.user_id], 'Modification Request Approved', 'Your attendance modification request %s is approved :' % (self.name), base_url+"/mail/view?model=sh.attendance.modification.request&res_id="+str(self.id),
                                                           'sh.attendance.modification.request', self.id, 'hr',self.env.ref('sh_push_notification_tile.sh_attendance_modification'))

    def cancel(self):
        self.state = 'cancel'

    def action_draft(self):
        self.state = 'draft'

    def compute_late_timesheet_alert(self):
        for rec in self:
            rec.less_timesheet_alert = False

            check_in_date = self.attendance_id.check_in.date()
            timesheets = self.env['account.analytic.line'].search(
                [('employee_id', '=', self.employee_id.id)]).filtered(lambda x: x.date == check_in_date)
            timesheet_hrs = sum(timesheets.mapped('unit_amount'))

            check_in_date_day = check_in_date.weekday()

            domain = [('calendar_id', '=', rec.employee_id.resource_calendar_id.id),
                      ('dayofweek', '=', check_in_date_day),
                      ('day_period', 'in', ['morning', 'afternoon']),
                      ('date_from', '<=', check_in_date),
                      ('date_to', '>=', check_in_date),
                      ]

            calendar_att_id = self.env['resource.calendar.attendance'].sudo().search(
                domain)
            if calendar_att_id:

                worked_hrs = sum(calendar_att_id.mapped('sh_wroked_hours'))

                leave = self.env['hr.leave'].search([('employee_id', '=', rec.employee_id.id),
                                                     ('request_date_from', '<=', check_in_date), ('request_date_to', '>=', check_in_date)])

                leave_sum = sum(leave.mapped('number_of_days_display'))
                if worked_hrs - timesheet_hrs - leave_sum > 0.5:
                    rec.less_timesheet_alert = True

    def compute_attendance_count_for_modif(self):
        for rec in self:
            rec.sh_attendance_count = 0.0
            curr_start_date = datetime.strftime(rec.attendance_id.check_in, "%Y/%m/%d 00:00:00")
            curr_end_date = datetime.strftime(rec.attendance_id.check_in, "%Y/%m/%d 23:59:59")
            attendances = self.env['hr.attendance'].search([('employee_id', '=', rec.attendance_id.employee_id.id), ('check_in', '>=', curr_start_date), ('check_in', '<=', curr_end_date)])
            rec.sh_attendance_count = sum(attendances.mapped('total_time'))

    def action_view_leaves(self):
        check_in_date = self.attendance_id.check_in.date()
        leaves = self.env['hr.leave'].search([('employee_id', '=', self.employee_id.id)]).filtered(
            lambda x: x.request_date_from and x.request_date_from == check_in_date)

        return {
            'type': 'ir.actions.act_window',
            'name': 'LEaves',
            'view_mode': 'tree,form',
            'res_model': 'hr.leave',
            'domain': [('id', 'in', leaves.ids)],
        }

    def action_view_attendance(self):
        curr_start_date = datetime.strftime(
            self.attendance_id.check_in, "%Y/%m/%d 00:00:00")
        curr_end_date = datetime.strftime(
            self.attendance_id.check_in, "%Y/%m/%d 23:59:59")
        attendances = self.env['hr.attendance'].search([('employee_id', '=', self.attendance_id.employee_id.id), (
            'check_in', '>=', curr_start_date), ('check_in', '<=', curr_end_date)])
        return {
            'type': 'ir.actions.act_window',
            'name': 'Attendances',
            'view_mode': 'tree,form',
            'res_model': 'hr.attendance',
            'domain': [('id', 'in', attendances.ids)],
        }
