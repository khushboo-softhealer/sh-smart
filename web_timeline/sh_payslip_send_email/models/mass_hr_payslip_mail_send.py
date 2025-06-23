# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models, api


class MassHrPayslipEmailSend(models.Model):
    _name = 'mass.hr.payslip.mail.send'
    _description = 'Send Payslip in Mail'

    def send_payslip_email_confirm(self):

        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []

        for record in self.env['hr.payslip'].browse(active_ids):
            mail_id = ''
            mails = []
            if record.employee_id:
                if record.employee_id.company_id and record.employee_id.company_id.send_payslip:
                    if record.employee_id.send_payslip:
                        if record.employee_id.company_id.sh_send_mail_on == 'personal':
                            mail_id = record.employee_id.personal_email
                        elif record.employee_id.company_id.sh_send_mail_on == 'work':
                            mail_id = record.employee_id.work_email
                        elif record.employee_id.company_id.sh_send_mail_on == 'both':
                            if record.employee_id.personal_email:
                                mails.append(
                                    str(record.employee_id.personal_email))
                            if record.employee_id.work_email:
                                mails.append(
                                    str(record.employee_id.work_email))

                            mail_id = ','.join(mails)

                        if mail_id:

                            template = self.env.ref(
                                'sh_payslip_send_email.template_hr_employee_payslip_send_email')

                            if template.id:
                                template.send_mail(record.id,
                                                   force_send=True,
                                                   email_values={'email_to': mail_id})

        return {'type': 'ir.actions.act_window_close'}
