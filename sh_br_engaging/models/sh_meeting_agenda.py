# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class MeetingAgenda(models.Model):
    _name = "sh.meeting.agenda"
    _description = "Meeting Agenda"

    name = fields.Char("Talking Point",required=True)
    sh_is_active = fields.Boolean("Active")
    # sh_calender_event_id = fields.Many2one('calendar.event', "Calendar Event Id")




    # def unlink(self):
    #     for record in self:
    #         agenda_line_ids = self.env['sh.talking.agenda.line'].search([('sh_agenda_id', '=' ,record.id)])
    #         if agenda_line_ids :
    #             agenda_line_ids.unlink()

    #     ret = super(MeetingAgenda, self).unlink()
    #     return ret

# === CREATE NEW MODEL FOR SHOW ACTIVE AGENDAS IN MEETING (ONE2MANY PURPOSE) ===
    
class MeetingTempAgenda(models.Model):
    _name = "sh.temp.meeting.agenda"
    _description = "Meeting Agenda"

    name = fields.Many2one("sh.meeting.agenda","Talking Point",required=True)
    sh_is_active = fields.Boolean("Active")
    sh_calender_event_id = fields.Many2one('calendar.event', "Calendar Event Id")
    sh_description = fields.Text('Description')