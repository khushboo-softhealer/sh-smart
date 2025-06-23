# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

import base64
import logging

from odoo import models

_logger = logging.getLogger(__name__)


class CalendarAttendee(models.Model):
    _inherit = 'calendar.attendee'

    def _send_mail_to_attendees(self, mail_template, force_send=False):
        """Send mail for event invitation to event attendees.
            :param mail_template: a mail.template record
            :param force_send: if set to True, the mail(s) will be sent immediately (instead of the next queue processing)
        """
        if isinstance(mail_template, str):
            raise ValueError(
                'Template should be a template record, not an XML ID anymore.')
        if self.env['ir.config_parameter'].sudo().get_param('calendar.block_mail') or self._context.get("no_mail_to_attendees"):
            return False
        if not mail_template:
            _logger.warning(
                "No template passed to %s notification process. Skipped.", self)
            return False

        # get ics file for all meetings
        ics_files = self.mapped('event_id')._get_ics_file()

        # send email with attachments

        # mails_to_send = self.env['mail.mail']

        for attendee in self:
            if attendee.email:
                master_email = attendee.email
            else:
                master_email = attendee.partner_id.email
            if master_email:
                domain = [('email', '=', master_email)]
                find_user = self.env['res.users'].search(domain)
                if find_user:
                    if find_user[0].has_group('base.group_portal') or find_user[0].has_group('base.group_public'):
                        event_id = attendee.event_id.id
                        ics_file = ics_files.get(event_id)

                        attachment_values = []
                        if ics_file:
                            attachment_values = [
                                (0, 0, {'name': 'invitation.ics',
                                        'mimetype': 'text/calendar',
                                        'datas': base64.b64encode(ics_file)})
                            ]
                        body = mail_template._render_field(
                            'body_html',
                            attendee.ids,
                            compute_lang=True,
                            post_process=True)[attendee.id]
                        subject = mail_template._render_field(
                            'subject',
                            attendee.ids,
                            compute_lang=True)[attendee.id]
                        attendee.event_id.with_context(no_document=True).message_notify(
                            email_from=attendee.event_id.user_id.email_formatted or self.env.user.email_formatted,
                            author_id=attendee.event_id.user_id.partner_id.id or self.env.user.partner_id.id,
                            body=body,
                            subject=subject,
                            partner_ids=attendee.partner_id.ids,
                            email_layout_xmlid='mail.mail_notification_light',
                            attachment_ids=attachment_values,
                            force_send=force_send)
