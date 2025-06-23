# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import  fields, models

class TalkingPointAgenda(models.TransientModel):
    _name = "sh.view.talking.point.wizard"
    _description = "Model for View Agenda in Talking Points"

    sh_talking_point_view_agenda_ids=fields.Many2many('sh.talking.point.view.agenda',string='Agenda Ids')
