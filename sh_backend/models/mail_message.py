# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields,api
from odoo.tools.translate import html_translate
from odoo.exceptions import ValidationError
from datetime import timedelta, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model_create_multi
    def create(self,vals_list):
        res = super(MailMessage,self).create(vals_list)
        for rec in res:
            listt = []
            subtypes = self.env['mail.message.subtype'].search([('name','=','Note')])
            for subtype in subtypes:
                if subtype and rec.subtype_id.id == subtype.id and rec.model == 'project.task' and rec.message_type =='comment':
                    project_task = self.env['project.task'].browse(rec.res_id)
                    if project_task and not res.remote_mail_message_id:
                        # listt.append(project_task.user_id.id)
                        listt.extend(project_task.user_ids)
                        if self.env.user in listt:
                            listt.remove(self.env.user)

                        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

                        self.env['user.push.notification'].push_notification(list(set(listt)), 'Log Note Created', 'Ref %s:' % (
                            project_task.name), base_url+"/mail/view?model=project.task&res_id="+str(rec.res_id), 'project.task', rec.res_id,'project')
        return res
