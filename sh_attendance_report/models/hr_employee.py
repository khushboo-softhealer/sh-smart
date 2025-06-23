# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models, api
from datetime import datetime


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    sh_work_hours_notify = fields.Boolean("Working Hours Email Notify ?")


class HrEmployee(models.Model):
    _inherit = 'hr.employee.public'

    sh_work_hours_notify = fields.Boolean("Working Hours Email Notify ?")


class HremployeeWorkhoursNotify(models.Model):
    _name = "sh.employee.workhours.notify"
    _description = 'Workhours Notify'

    emp_id = fields.Many2one("hr.employee", "Employee")
    worked_date = fields.Char("Date")
    worked_hours = fields.Float("Worked Hours")
    min_work_hours = fields.Float("Minimum Working Hours")
    email_id = fields.Many2one("sh.employee.workhours.email", "Email Id")
    mail_id = fields.Many2one('mail.mail', string='Mail')

    def action_view_mail(self):
        self.ensure_one()

        Mails = self.mapped('mail_id')
        action = self.env.ref('mail.action_view_mail_mail').read()[0]
        if len(Mails) > 1:
            action['domain'] = [('id', 'in', Mails.ids)]
        elif len(Mails) == 1:
            action['views'] = [
                (self.env.ref('mail.view_mail_form').id, 'form')]
            action['res_id'] = Mails.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action


class HrEmployeeWorkhoursEmail(models.Model):
    _name = "sh.employee.workhours.email"
    _description = 'Workhours Email'

    name = fields.Char("Employee Work Hours Email")
    notify_ids = fields.One2many(
        "sh.employee.workhours.notify", "email_id", "Notify Id")
    emp_email = fields.Char("Summary Email")
    emp_summ = fields.Boolean("Summary Template?")
    worked_date = fields.Char("Worked Date")
    emp_name = fields.Char("Employee Name")
    company_id = fields.Many2one('res.company', 'Company')
    mail_id = fields.Many2one('mail.mail', string='Mail')

    def action_view_mail(self):
        self.ensure_one()

        Mails = self.mapped('mail_id')
        action = self.env.ref('mail.action_view_mail_mail').read()[0]
        if len(Mails) > 1:
            action['domain'] = [('id', 'in', Mails.ids)]
        elif len(Mails) == 1:
            action['views'] = [
                (self.env.ref('mail.view_mail_form').id, 'form')]
            action['res_id'] = Mails.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    @api.model
    def notify_employee_workhours_fun(self):
        employee_object = self.env['hr.employee'].search([])
        if employee_object:
            for empl_rec in employee_object:
                month_date = fields.Date.today().weekday()
                cal_att_id = self.env['resource.calendar.attendance'].sudo().search(
                    [('calendar_id', '=', empl_rec.resource_calendar_id.id), ('dayofweek', '=', month_date)], limit=1)
                notify_user_email = self.env.user.company_id.sh_notify_user_email
                day = fields.Date.today()
                curr_start_date = datetime.strftime(
                    datetime.now(), "%Y/%m/%d 00:00:00")
                curr_end_date = datetime.strftime(
                    datetime.now(), "%Y/%m/%d 23:59:00")
                day_date = str(day)
                email_id = False
                if cal_att_id.sh_wroked_hours > 0.0 and cal_att_id:
                    vals = []
                    if empl_rec.sh_work_hours_notify:
                        attendance_obj = self.env['hr.attendance'].search(
                            [('employee_id', '=', empl_rec.id), ('check_in', '>', curr_start_date), ('check_in', '<', curr_end_date)])
                        if attendance_obj:
                            day_work_hours = 0
                            email_id = self.env['sh.employee.workhours.email'].sudo().create({
                                'name': 'Notification Email'+'-'+str(fields.Date.today())
                            })
                            for att_rec in attendance_obj:
                                day_work_hours += round(att_rec.att_duration)
                            if day_work_hours < cal_att_id.sh_wroked_hours:
                                emp_vals = {
                                    'emp_id': empl_rec.id,
                                    'worked_date': datetime.strftime(datetime.now(), "%Y/%m/%d"),
                                    'worked_hours': day_work_hours,
                                    'min_work_hours': cal_att_id.sh_wroked_hours,
                                    'email_id': email_id.id,
                                }
                                vals.append(emp_vals)
                                notify_object = self.env['sh.employee.workhours.notify'].create(
                                    emp_vals)
                                if notify_object and empl_rec.work_email:
                                    if email_id:
                                        email_id.emp_email = empl_rec.work_email
                                        email_id.emp_summ = False
                                        email_id.emp_name = empl_rec.name
                                        email_id.company_id = self.env.user.company_id.id
                                    template = self.env.ref(
                                        'sh_attendance_report.sh_template_employee_work_hours_notify_email')
                                    # if template:
                                    #     mail_res = template.sudo().send_mail(email_id.id, force_send=True)
                                    #     if mail_res:
                                    #         mail_id = self.env['mail.mail'].sudo().browse(
                                    #             mail_res)
                                    #         notify_object.mail_id = mail_id.id
                if notify_user_email:
                    notify = self.env['sh.employee.workhours.notify'].search([
                    ])
                    if vals:
                        notify_object = []

                        for rec in vals:
                            rec['emp_summ'] = True

                        if email_id:
                            email_id.emp_email = notify_user_email
                            email_id.emp_summ = True
                            email_id.worked_date = datetime.strftime(
                                datetime.now(), "%Y/%m/%d")
                            email_id.emp_name = "Summary"

                        if email_id:
                            template = self.env.ref(
                                'sh_attendance_report.sh_template_employee_work_hours_notify_email')

                            # if template:
                            #     mail_res = template.sudo().send_mail(email_id.id, force_send=True)
                            #     if mail_res:
                            #         mail_id = self.env['mail.mail'].sudo().browse(
                            #             mail_res)
                            #         if mail_id:
                            #             email_id.mail_id = mail_id.id
