# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class TalkingAgendaLine(models.Model):
    _name = "sh.talking.agenda.line"
    _description = "Talking Agenda Line"
    _rec_name='sh_agenda_id'

    sh_agenda_id = fields.Many2one('sh.manage.agenda','Agenda Id',required=True)
    sh_talking_point_id = fields.Many2one('sh.talking.points','Talking Point Id')
    sh_checked=fields.Boolean('Checked')
    sh_talking_point_description = fields.Char("Description")

    sh_previous_talking_point_id = fields.Many2one('sh.talking.points.previous.history','Previous Talking Point Id')
    

   