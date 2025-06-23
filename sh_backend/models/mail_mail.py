# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, api, _

class Mail(models.Model):
    _inherit = 'mail.mail'

    def send(self, auto_commit=False, raise_exception=False):
        for rec in self:
            if rec.model == 'hr.leave':
                rec.cancel()
                return
            elif rec.model == 'project.task':
                if rec.message_type == 'email' or rec.message_type=='user_notification':
                    rec.cancel()
                    return
                elif rec.message_type == 'comment':
                    if rec.subtype_id.id == self.env.ref('mail.mt_comment').id:
                        record_id = self.env[rec.model].sudo().search([('id','=',rec.res_id)],limit=1)
                        if record_id and record_id.project_id.sh_send_email:
                            return super(Mail, self).send()
                        elif record_id and not record_id.project_id.sh_send_email:
                            rec.cancel()
                    else:
                        return super(Mail, self).send()
                else:
                    rec.cancel()
                    return
            else:
                return super(Mail, self).send()
