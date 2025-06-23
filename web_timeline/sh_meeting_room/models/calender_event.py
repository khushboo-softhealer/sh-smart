# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models,_
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from collections import defaultdict


class CalenderEventInherit(models.Model):
    _inherit = 'calendar.event'

    sh_meeting_room_id=fields.Many2one("meeting.rooms",string="Meeting Room")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'sh_meeting_room_id' in vals and vals['sh_meeting_room_id']:
                meeting_obj=self.env['meeting.rooms'].sudo().search([('id','=',vals['sh_meeting_room_id'])])
                calender_objs = self.env['calendar.event'].sudo().search([('sh_meeting_room_id','=',vals['sh_meeting_room_id'])]) 
                if calender_objs:
                    for cal in calender_objs:
                        if vals['start'] >= cal.start.strftime(DEFAULT_SERVER_DATETIME_FORMAT) and vals['start'] < cal.stop.strftime(DEFAULT_SERVER_DATETIME_FORMAT):
                            raise UserError(_('You cannot Create Meeting at this time !'))                               
                if meeting_obj.is_conference_room:
                    if meeting_obj.sh_member <= len(vals['partner_ids'][0][-1]):
                        pass
                    else:
                        raise UserError(_('Your Meeting attendees is less please check !'))
        return super().create(vals_list)    
