# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models, api, _


class AttendanceModofocationRequestReason(models.TransientModel):
    _name = 'sh.attendance.modification.request.reason'
    _description = "Attendance Modification Request Reason"

    myreason = fields.Char("Reason", required=True)

    def add_reason(self):
        active_id = self.env.context.get("active_id")
        active_record = self.env['sh.attendance.modification.request'].browse(
            active_id)
        vals = {
            'rejection_reason': self.myreason
        }

        template = self.env.ref(
            'sh_attendance_modification_request.sh_attendance_modification_request_email_reject_tmpl', raise_if_not_found=False)

        email_to = active_record.employee_id.work_email
        email_from = active_record.employee_id.parent_id.work_email

        if template:
            email_values = {
                'email_to': email_to, 'email_from': email_from}
            # template.send_mail(active_record.id,
            #                    email_values=email_values, force_send=True, email_layout_xmlid='mail.mail_notification_light')

        # self.env['bus.bus']._sendone(active_record.employee_id.user_id.partner_id, 'simple_notification', {
        #     'title': _("Notification"),
        #     'message': _('%(partner_names)s has been rejected by  %(employee)s', partner_names=active_record.name, employee=active_record.employee_id.parent_id.name)
        # })

        active_record.write(vals)
        active_record.state = "reject"


        base_url = self.env['ir.config_parameter'].sudo(
        ).get_param('web.base.url')
        self.env['user.push.notification'].hr_push_notification(active_record.employee_id.user_id, 'Modification Request Rejected', 'Your attendance modification request %s is rejected :' % (active_record.name), base_url+"/mail/view?model=sh.attendance.modification.request&res_id="+str(active_record.id),
                                                           'sh.attendance.modification.request', active_record.id, 'hr',self.env.ref('sh_push_notification_tile.sh_attendance_modification'))
