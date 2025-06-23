# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.


from odoo import api, fields, models
from datetime import datetime,timedelta
from datetime import date

class OneonOne(models.Model):
    _name = "sh.one.on.ones"
    _description = "1 on 1"

    name = fields.Char("Name")
    sh_employee_id = fields.Many2one('hr.employee', "Employee Name")
    sh_talking_points_ids = fields.Many2many('sh.talking.points',string="Talking Points Ids")

    sh_your_notes=fields.Text('Your Notes')
    sh_employee_notes=fields.Text("Employee's Note")
    sh_your_private_notes=fields.Text("Your Private Notes")