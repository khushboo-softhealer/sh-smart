# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, tools, _
import re
from odoo.exceptions import UserError

emails_split = re.compile(r"[;,\n\r]+")

class SurveyInvite(models.TransientModel):
    _inherit = 'survey.invite'

    def action_invite(self):
        """ Process the wizard content and proceed with sending the related
            email(s), rendering any template patterns on the fly if needed """
        self.ensure_one()
        Partner = self.env['res.partner']

        # compute partners and emails, try to find partners for given emails
        valid_partners = self.partner_ids
        langs = set(valid_partners.mapped('lang')) - {False}
        if len(langs) == 1:
            self = self.with_context(lang=langs.pop())
        valid_emails = []
        for email in emails_split.split(self.emails or ''):
            partner = False
            email_normalized = tools.email_normalize(email)
            if email_normalized:
                limit = None if self.survey_users_login_required else 1
                partner = Partner.search([('email_normalized', '=', email_normalized)], limit=limit)
            if partner:
                valid_partners |= partner
            else:
                email_formatted = tools.email_split_and_format(email)
                if email_formatted:
                    valid_emails.extend(email_formatted)

        if not valid_partners and not valid_emails:
            raise UserError(_("Please enter at least one valid recipient."))

        answers = self._prepare_answers(valid_partners, valid_emails)
        for answer in answers:
            result = self._send_mail(answer)
            mail_server_id = self.env['ir.mail_server'].sudo().search(
                        [('smtp_user', '=', 'career@softhealer.com')], limit=1)
            if mail_server_id:
                result.mail_server_id = mail_server_id.id
                result.reply_to = mail_server_id.smtp_user
            result.send()

        return {'type': 'ir.actions.act_window_close'}