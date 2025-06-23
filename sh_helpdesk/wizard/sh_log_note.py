# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields

class LogNote(models.Model):
    _name = 'sh.log.note'
    _description = 'Log Note'

    sh_description = fields.Html('Log Note',required=True)


    def action_log(self):
        self.env['mail.message'].sudo().create({
            'subtype_id': self.env.ref('mail.mt_note').id,
            'message_type': 'comment',
            'author_id': self.env.user.partner_id.id,
            'date': fields.Datetime.now(),
            'res_id': self.env.context.get('active_id'),
            'model': 'sh.helpdesk.ticket',
            'body': self.sh_description,
        })
