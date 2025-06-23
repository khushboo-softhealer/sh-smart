# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models
import pytz
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta

class MeetingRooms(models.Model):
    _name="meeting.rooms"
    _description = "Meeting Rooms"

    name=fields.Char("Meeting Room Name")
    sh_booked_meeting=fields.Boolean(string="Booked Meeting",compute="compute_sh_meeting_rooms")
    meeting_count =fields.Integer(string="meeting Count")
    sh_image=fields.Image(string="Image",store=True)
    sh_member=fields.Integer(string="Minimum Attendees")
    is_conference_room=fields.Boolean(string="Is Conference Room")

    @api.depends('sh_booked_meeting')
    def compute_sh_meeting_rooms(self):        
        for rec in self:             
            rec.sh_booked_meeting=False            
            start_date=(fields.Datetime.today() + relativedelta(hours=0,minutes=0,seconds=0)).date()
            end_date=(fields.Datetime.today() + relativedelta(hours=23,minutes=59,seconds=59))
            calender_objs = self.env['calendar.event'].sudo().search([('sh_meeting_room_id','=',rec.id)])                                 
            if calender_objs:
                count=0
                for calender in calender_objs:                   
                    new_order_date_utc=calender.start.replace(tzinfo=pytz.UTC).astimezone(pytz.timezone(self.env.user.tz or 'UTC'))
                    new_order_date_utc=datetime.strptime(new_order_date_utc.strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")                                       
                    if new_order_date_utc.date() >= start_date:
                            count+=1
                rec.sh_booked_meeting=True 
                rec.write({'meeting_count':count})
            else:
                rec.write({'meeting_count':0})                      

    def sh_book_room_action(self):
        ctx=dict(self.env.context)
        ctx.update({'default_sh_meeting_room_id':self.id})
        return {
                'type': 'ir.actions.act_window',
                'name':"Create Meeting",
                'res_model': 'calendar.event',
                'view_mode': 'form',
                'view_id': self.env.ref('calendar.view_calendar_event_form').id,
                'target': 'new',
                'context':ctx,
            }
    def sh_book_calender_action(self):       
        calender_objs = self.env['calendar.event'].sudo().search([('sh_meeting_room_id','=',self.id)])                             
        if calender_objs:
            count=[]
            start_date=(fields.Datetime.today() + relativedelta(hours=0,minutes=0,seconds=0)).date()
            for calender in calender_objs:                   
                new_order_date_utc=calender.start.replace(tzinfo=pytz.UTC).astimezone(pytz.timezone(self.env.user.tz or 'UTC'))
                new_order_date_utc=datetime.strptime(new_order_date_utc.strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")                               
                if new_order_date_utc.date() >= start_date:
                    count.append(calender.id)
            domain=[('id','in',count)]
        else:
            domain=[('id','in',[])]
        return {
                'type': 'ir.actions.act_window',
                'name':"Meetings",
                'res_model': 'calendar.event',
                'view_mode': 'calendar',
                'views': [(False, 'calendar')],
                'view_id': False,
                'target': 'new',
                'domain':domain
            }