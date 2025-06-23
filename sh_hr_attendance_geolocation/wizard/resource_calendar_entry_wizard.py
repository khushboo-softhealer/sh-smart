# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models, _
from odoo.exceptions import UserError


class ResourceCalendarEntryWizard(models.TransientModel):
    _name = 'resource.calendar.entry.wizard'
    _description = "Resource Calendar Entry Wizard"

    mon = fields.Boolean('Monday', default=True)
    tue = fields.Boolean('Tuesday', default=True)
    wed = fields.Boolean('Wednesday', default=True)
    thu = fields.Boolean('Thursday', default=True)
    fri = fields.Boolean('Friday', default=True)
    sat = fields.Boolean('Saturday', default=True)
    sun = fields.Boolean('Sunday', default=False)

    sh_break = fields.Float(string='Break', required=True)

    start_date = fields.Date(string='Starting Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    work_from = fields.Float(string='Work from', required=True, index=True,
                             help="Start and End time of working.\n"
                             "A specific value of 24:00 is interpreted as 23:59:59.999999.")
    work_to = fields.Float(string='Work to', required=True)
    day_period = fields.Selection(
        [('morning', 'Morning'), ('afternoon', 'Afternoon')], required=True, default='morning')

    resource_calendar_ids = fields.Many2many('resource.calendar', string='Resource Calendar Ids')

    def _show_message(self, message):
        view = self.env.ref('sh_message.sh_message_wizard')
        context = dict(self._context or {})
        context['message'] = message
        return {
            'name': 'Add / Remove Working Hours',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context
        }

    def _add_entry(self, parent_record):
        entry_vals = {}
        if self.mon:
            if self.day_period == 'morning':
                entry_vals.update({'name':  'Monday Morning'})
            else:
                entry_vals.update({'name':  'Monday Afternoon'})
            entry_vals.update({'dayofweek': '0',
                               'date_from': self.start_date,
                               'date_to': self.end_date,
                               'hour_from': self.work_from,
                               'hour_to': self.work_to,
                               'day_period': self.day_period,
                               'sh_break': self.sh_break,
                               'sh_wroked_hours': self.work_to -self.work_from
                               })
            parent_record.write({'attendance_ids': [(0, 0,  entry_vals)]})
        if self.tue:
            if self.day_period == 'morning':
                entry_vals.update({'name':  'Tuesday Morning'})
            else:
                entry_vals.update({'name':  'Tuesday Afternoon'})
            entry_vals.update({'dayofweek': '1',
                               'date_from': self.start_date,
                               'date_to': self.end_date,
                               'hour_from': self.work_from,
                               'hour_to': self.work_to,
                               'day_period': self.day_period,
                               'sh_break': self.sh_break,
                               'sh_wroked_hours': self.work_to -self.work_from
                               })
            parent_record.write({'attendance_ids': [(0, 0,  entry_vals)]})

        if self.wed:
            if self.day_period == 'morning':
                entry_vals.update({'name':  'Wednesday Morning'})
            else:
                entry_vals.update({'name':  'Wednesday Afternoon'})
            entry_vals.update({'dayofweek': '2',
                               'date_from': self.start_date,
                               'date_to': self.end_date,
                               'hour_from': self.work_from,
                               'hour_to': self.work_to,
                               'day_period': self.day_period,
                               'sh_break': self.sh_break,
                               'sh_wroked_hours': self.work_to -self.work_from
                               })
            parent_record.write({'attendance_ids': [(0, 0,  entry_vals)]})

        if self.thu:
            if self.day_period == 'morning':
                entry_vals.update({'name':  'Thursday Morning'})
            else:
                entry_vals.update({'name':  'Thursday Afternoon'})
            entry_vals.update({'dayofweek': '3',
                               'date_from': self.start_date,
                               'date_to': self.end_date,
                               'hour_from': self.work_from,
                               'hour_to': self.work_to,
                               'day_period': self.day_period,
                               'sh_break': self.sh_break,
                               'sh_wroked_hours': self.work_to -self.work_from
                               })
            parent_record.write({'attendance_ids': [(0, 0,  entry_vals)]})

        if self.fri:
            if self.day_period == 'morning':
                entry_vals.update({'name':  'Friday Morning'})
            else:
                entry_vals.update({'name':  'Friday Afternoon'})
            entry_vals.update({'dayofweek': '4',
                               'date_from': self.start_date,
                               'date_to': self.end_date,
                               'hour_from': self.work_from,
                               'hour_to': self.work_to,
                               'day_period': self.day_period,
                               'sh_break': self.sh_break,
                               'sh_wroked_hours': self.work_to -self.work_from
                               })
            parent_record.write({'attendance_ids': [(0, 0,  entry_vals)]})

        if self.sat:
            if self.day_period == 'morning':
                entry_vals.update({'name':  'Saturday Morning'})
            else:
                entry_vals.update({'name':  'Saturday Afternoon'})
            entry_vals.update({'dayofweek': '5',
                               'date_from': self.start_date,
                               'date_to': self.end_date,
                               'hour_from': self.work_from,
                               'hour_to': self.work_to,
                               'day_period': self.day_period,
                               'sh_break': self.sh_break,
                               'sh_wroked_hours': self.work_to -self.work_from
                               })
            parent_record.write({'attendance_ids': [(0, 0,  entry_vals)]})

        if self.sun:
            if self.day_period == 'morning':
                entry_vals.update({'name':  'Sunday Morning'})
            else:
                entry_vals.update({'name':  'Sunday Afternoon'})
            entry_vals.update({'dayofweek': '6',
                               'date_from': self.start_date,
                               'date_to': self.end_date,
                               'hour_from': self.work_from,
                               'hour_to': self.work_to,
                               'day_period': self.day_period,
                               'sh_break': self.sh_break,
                               'sh_wroked_hours': self.work_to -self.work_from
                               })
            parent_record.write({'attendance_ids': [(0, 0,  entry_vals)]})

    def sh_add_entry(self):
        if not self.resource_calendar_ids:
            parent_id = self.env.context.get("active_id")
            parent_model = self.env.context.get("active_model")
            parent_record = self.env[parent_model].browse(parent_id)
            self._add_entry(parent_record)
            return
        for resource_calendar in self.resource_calendar_ids:
            self._add_entry(resource_calendar)

    def _remove_entry(self, parent_record):
        parent_id = parent_record.id
        data_contain_flag = False
        
        if self.mon:
            remove_domain_mon = [('calendar_id', '=', parent_id), ('date_from', '=', self.start_date),  (
                'date_to', '=', self.end_date), ('hour_from', '=', self.work_from), ('hour_to', '=', self.work_to),
                ('day_period', '=', self.day_period), ('sh_break', '=', self.sh_break), ('dayofweek', '=', 0)]
            remove_lines = parent_record.attendance_ids.search(
                remove_domain_mon)
            if remove_lines:
                data_contain_flag = True
                remove_lines.unlink()

        if self.tue:

            remove_domain_tue = [('calendar_id', '=', parent_id), ('date_from', '=', self.start_date),  (
                'date_to', '=', self.end_date), ('hour_from', '=', self.work_from), ('hour_to', '=', self.work_to),
                ('day_period', '=', self.day_period), ('sh_break', '=', self.sh_break), ('dayofweek', '=', 1)]

            remove_lines = parent_record.attendance_ids.search(
                remove_domain_tue)
            if remove_lines:
                data_contain_flag = True
                remove_lines.unlink()

        if self.wed:
            remove_domain_wed = [('calendar_id', '=', parent_id), ('date_from', '=', self.start_date),  (
                'date_to', '=', self.end_date), ('hour_from', '=', self.work_from), ('hour_to', '=', self.work_to),
                ('day_period', '=', self.day_period), ('sh_break', '=', self.sh_break), ('dayofweek', '=', 2)]

            remove_lines = parent_record.attendance_ids.search(
                remove_domain_wed)
            if remove_lines:
                data_contain_flag = True
                remove_lines.unlink()

        if self.thu:
            remove_domain_thu = [('calendar_id', '=', parent_id), ('date_from', '=', self.start_date),  (
                'date_to', '=', self.end_date), ('hour_from', '=', self.work_from), ('hour_to', '=', self.work_to),
                ('day_period', '=', self.day_period), ('sh_break', '=', self.sh_break), ('dayofweek', '=', 3)]

            remove_lines = parent_record.attendance_ids.search(
                remove_domain_thu)
            if remove_lines:
                data_contain_flag = True
                remove_lines.unlink()

        if self.fri:
            remove_domain_fri = [('calendar_id', '=', parent_id), ('date_from', '=', self.start_date),  (
                'date_to', '=', self.end_date), ('hour_from', '=', self.work_from), ('hour_to', '=', self.work_to),
                ('day_period', '=', self.day_period), ('sh_break', '=', self.sh_break), ('dayofweek', '=', 4)]

            remove_lines = parent_record.attendance_ids.search(
                remove_domain_fri)
            if remove_lines:
                data_contain_flag = True
                remove_lines.unlink()

        if self.sat:
            remove_domain_sat = [('calendar_id', '=', parent_id), ('date_from', '=', self.start_date),  (
                'date_to', '=', self.end_date), ('hour_from', '=', self.work_from), ('hour_to', '=', self.work_to),
                ('day_period', '=', self.day_period), ('sh_break', '=', self.sh_break), ('dayofweek', '=', 5)]

            remove_lines = parent_record.attendance_ids.search(
                remove_domain_sat)
            if remove_lines:
                data_contain_flag = True
                remove_lines.unlink()

        if self.sun:
            remove_domain_sun = [('calendar_id', '=', parent_id), ('date_from', '=', self.start_date),  (
                'date_to', '=', self.end_date), ('hour_from', '=', self.work_from), ('hour_to', '=', self.work_to),
                ('day_period', '=', self.day_period), ('sh_break', '=', self.sh_break), ('dayofweek', '=', 6)]

            remove_lines = parent_record.attendance_ids.search(
                remove_domain_sun)
            if remove_lines:
                data_contain_flag = True
                remove_lines.unlink()
                
        if not data_contain_flag:        
            # raise UserError(_("There is no match for this data !"))
            return f"\n{parent_record.name} (ID-{parent_id})\nThere is no match for this data !\n"

    def sh_remove_entry(self):
        if not self.resource_calendar_ids:
            parent_id = self.env.context.get("active_id")
            parent_model = self.env.context.get("active_model")
            parent_record = self.env[parent_model].browse(parent_id)
            self._remove_entry(parent_record)
            return
        message = ''
        for resource_calendar in self.resource_calendar_ids:
            remove_message = self._remove_entry(resource_calendar)
            if remove_message:
                message += remove_message
        if message:
            return self._show_message(message)