# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, api
import logging
_logger = logging.getLogger(__name__)

class MailMail(models.Model):
    '''
       PURPOSE : We don't want to send email for specific models
    '''
    _inherit = 'mail.mail'

    @api.model
    def create(self, vals_list):
        try:
            if vals_list and vals_list.get('mail_message_id'):
                message = self.env['mail.message'].browse(vals_list.get('mail_message_id'))
                not_allowed_model = ['hr.leave','hr.leave.allocation']
                Mail = self.env['mail.mail'].browse()
                if message and message.model in not_allowed_model:
                    return Mail
        except Exception as e:
            _logger.error("Error when not allowed to send in secific models ==> %s", e)
            return super(MailMail,self).create(vals_list)
        
        return super(MailMail,self).create(vals_list)