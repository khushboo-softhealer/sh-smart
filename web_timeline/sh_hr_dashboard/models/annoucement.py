# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, api


class Annoucement(models.Model):
    _name = 'sh.annoucement'
    _description = 'Announcement'
    _order = "sequence,id"
    _rec_name = 'date'

    sequence = fields.Integer(default=10,
                              help="Gives the sequence of annoucmeent")
    name = fields.Html("Annoucement", required="1")
    date = fields.Date("Date", required="1")
    active = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        res = super(Annoucement, self).create(vals_list)
        for vals in vals_list:
            listt = []
            for user in self.env['res.users'].sudo().search([]):
                if user.has_group('hr_attendance.group_hr_attendance'):
                    listt.append(user)
            base_url = self.env['ir.config_parameter'].sudo(
            ).get_param('web.base.url')
            self.env['user.push.notification'].push_notification(
                listt, 'New Annoucement', 'Please Click here / Check Dashboard', base_url+"/mail/view?model=sh.hr.dashboard&res_id="+str(1), 'sh.hr.dashboard', 1, 'hr')
        return res
