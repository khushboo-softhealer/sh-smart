# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class TalkingPointsPreviousHistory(models.Model):
    _name = "sh.talking.points.previous.history"
    _description = "Talking Points Previous History"

    name = fields.Char("Talking Points",default='New')
    sh_employee_id = fields.Many2one('hr.employee', "Employee Name")

    sh_your_notes=fields.Text('Your Notes')
    sh_employee_notes=fields.Text("Employee's Note")
    sh_your_private_notes=fields.Text("Your Private Notes")
    sh_user_private_notes=fields.Text("Your Private Notes")
    sh_manage_previous_agenda_line=fields.One2many(comodel_name='sh.talking.agenda.line',inverse_name='sh_previous_talking_point_id',string='Agenda Line')
    sh_stage = fields.Selection([
            ('new', 'NEW'),
            ('completed', 'COMPLETED'),
        ],default='new',string='Stage')
    sh_talking_point_id = fields.Many2one('sh.talking.points', "Talking Point Id")
    
    sh_calender_event_id = fields.Many2one('calendar.event', "Calendar Event Id")

