# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    allow_overlap = fields.Boolean("Allow Meeting Overlap")
    calendar_group_templates = fields.Many2many(
        'sh.calendar.group.template', string="Calendar Group Template")
    create_new_group = fields.Boolean("Create Septate Group")
    new_group_name = fields.Char("Group Name")

    @api.onchange('calendar_group_templates')
    def onchange_calendar_group_templates(self):
        if self.calendar_group_templates:
            for template in self.calendar_group_templates:
                for partner in template.partner_ids:
                    self.partner_ids = [(4, partner.id)]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            partner_list = []
            if vals.get('name'):
                if 'Time Off' in vals['name']:
                    vals['allow_overlap'] = True
            if 'allow_overlap' in vals:
                if not vals['allow_overlap']:
                    if 'partner_ids' in vals and 'start' in vals:
                        vals_start = datetime.strptime(
                            vals['start'], "%Y-%m-%d %H:%M:%S")
                        vals_stop = datetime.strptime(
                            vals['stop'], "%Y-%m-%d %H:%M:%S")
                        for data in vals['partner_ids'][0][2]:
                            partner = self.env['res.partner'].browse(data)
                            domain = [('partner_ids', 'in', partner.ids)]
                            get_meetings = self.env['calendar.event'].search(
                                domain, limit=1)
                            if get_meetings:

                                if get_meetings.start and get_meetings.stop:
                                    if get_meetings.start < vals_start < get_meetings.stop:
                                        if partner not in partner_list:

                                            partner_list.append(partner)
                                    if get_meetings.start < vals_stop < get_meetings.stop:
                                        if partner not in partner_list:
                                            partner_list.append(partner)

                                    if vals_start < get_meetings.start < vals_stop:
                                        if partner not in partner_list:
                                            partner_list.append(partner)

                                    if vals_start < get_meetings.stop < vals_stop:
                                        if partner not in partner_list:
                                            partner_list.append(partner)

                    if partner_list:
                        partners = ''
                        for rec in partner_list:
                            partners = partners + rec.name + ','
                        raise UserError(
                            _("%s will be in meeting") % (partners))

        res = super(CalendarEvent, self).create(vals_list)
        if res.create_new_group:
            group_vals = {
                'name': res.new_group_name if res.new_group_name else res.name,
                'partner_ids': [(6, 0, res.partner_ids.ids)]
            }
            self.env['sh.calendar.group.template'].create(group_vals)
        listt = []

        for partner in res.partner_ids:
            user = self.env['res.users'].search(
                [('partner_id', '=', partner.id)])
            if user != self.env.user:
                listt.append(user)

        base_url = self.env['ir.config_parameter'].sudo(
        ).get_param('web.base.url')

        self.env['user.push.notification'].push_notification(list(set(listt)), 'Meeting Created',
                                                           f'Ref {res.name}:', base_url+"/mail/view?model=calendar.event&res_id="+str(res.id), 'calendar.event', res.id, 'hr')
        return res

    def write(self, vals):
        for record in self:
            if '__contexts' in self.env.context:
                for con in self.env.context['__contexts']:
                    if 'from_ui' in con:
                        if con['from_ui']:
                            raise UserError(
                                _("You are not allowed to edit from here"))

            if not vals.get("allow_overlap", False):
                if 'partner_ids' in vals:
                    partners = self.env['res.partner'].browse(
                        vals['partner_ids'][0][2])
                else:
                    partners = record.partner_ids

                start = record.start
                print("N\n\n",start)
                if vals.get("start", False):
                    start = datetime.strptime(
                        vals.get("start"), "%Y-%m-%d %H:%M:%S")
                stop = record.stop
                if vals.get("stop", False):
                    stop = datetime.strptime(vals.get("stop"), "%Y-%m-%d %H:%M:%S")

                partner_list = []
                for partner in partners:
                    domain = [('partner_ids', 'in', partner.ids)]
                    get_meetings = self.env['calendar.event'].search(domain)
                    for rec in get_meetings:
                        if rec.id != record.id:
                            if rec.start and rec.stop:
                                if rec.start < start < rec.stop:
                                    if partner not in partner_list:
                                        partner_list.append(partner)
                                if rec.start < stop < rec.stop:
                                    if partner not in partner_list:
                                        partner_list.append(partner)
                                if start < rec.start < stop:
                                    if partner not in partner_list:
                                        partner_list.append(partner)
                                if start < rec.stop < stop:
                                    if partner not in partner_list:
                                        partner_list.append(partner)
                if partner_list:
                    partners = ''
                    for rec in partner_list:
                        partners = partners + rec.name + ','
                    raise UserError(_("%s will be in meeting") % (partners))

            listt = []

            if vals.get('partner_ids'):
                partner_ids = vals.get('partner_ids')[0][2]
                for partner_id in partner_ids:
                    user = self.env['res.users'].search(
                        [('partner_id', '=', partner_id)])
                    if user != self.env.user:
                        listt.append(user)

            elif vals.get('start') or vals.get('duration'):
                for partner in record.partner_ids:
                    user = self.env['res.users'].search(
                        [('partner_id', '=', partner.id)])
                    if user != self.env.user:
                        listt.append(user)

            if vals.get('create_new_group'):
                group_name = ''
                if vals.get('new_group_name'):
                    group_name = vals.get('new_group_name')
                elif vals.get('name'):
                    group_name = vals.get('name')
                else:
                    group_name = record.name
                if vals.get('partner_ids'):
                    partner_ids = vals.get('partner_ids')[0][2]
                else:
                    partner_ids = record.partner_ids.ids

                domain = [('name', '=', group_name)]
                already = self.env['sh.calendar.group.template'].search(domain)
                if not already:
                    group_vals = {
                        'name': group_name,
                        'partner_ids': [(6, 0, partner_ids)]
                    }
                    self.env['sh.calendar.group.template'].create(group_vals)
            base_url = self.env['ir.config_parameter'].sudo(
            ).get_param('web.base.url')

            self.env['user.push.notification'].push_notification(list(set(
                listt)), 'Meeting Updated', f'Ref {record.name}:', base_url+"/mail/view?model=calendar.event&res_id="+str(record.id), 'calendar.event', record.id, 'hr')

        res = super(CalendarEvent, self).write(vals)
        return res

    @api.model
    def default_get(self, fields_list):
        get_minutes = self.env['calendar.alarm'].search(
            [('duration', '=', '15'), ('interval', '=', 'minutes')])
        res = super(CalendarEvent, self).default_get(fields_list)
        if get_minutes:
            res.update({
                'alarm_ids': [(6, 0, get_minutes.ids)],
            })
        res.update({'privacy': 'private', })
        return res
