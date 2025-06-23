# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

    
class TalkingPointViewAgendaModel(models.Model):
    _name = "sh.talking.point.view.agenda"
    _description = "This model is specailly used to show the agenda with description at talking point form view"

    sh_view_agenda_id = fields.Many2one('sh.manage.agenda',string='Agenda')
    sh_view_agenda_talking_point_id = fields.Many2one('sh.talking.points',string='Talking Point')
    sh_view_agenda_description = fields.Char("Description")
    sh_view_agenda_checked = fields.Boolean("Discussed")