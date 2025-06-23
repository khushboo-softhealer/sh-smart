# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models,api
from datetime import datetime

class TalkingPoints(models.Model):
    _name = "sh.talking.points"
    _description = "Talking Points"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char("1-on-1s",default='New',compute='_compute_talking_point_name')
    sh_employee_id = fields.Many2one('hr.employee', "Employee Name")

    sh_your_notes=fields.Text('Your Notes')
    sh_employee_notes=fields.Text("Employee's Note")
    sh_your_private_notes=fields.Text("Your Private Notes")
    sh_user_private_notes=fields.Text("Your Private Notes")
    sh_manage_agenda_line=fields.One2many(comodel_name='sh.talking.agenda.line',inverse_name='sh_talking_point_id',string='Agenda Line')
    sh_stage = fields.Selection([
            ('new', 'NEW'),
            ('completed', 'COMPLETED'),
        ],default='new',string='Stage')
    
    # sh_previous_talking_point_line=fields.One2many(comodel_name='sh.talking.points.previous.history',inverse_name='sh_talking_point_id',string='Previous Talking Points Line')
    sh_calender_event_id = fields.Many2one('calendar.event', "Calendar Event Id")
    sh_check_in_id = fields.Many2one('sh.check.in', "Check In Id")

    sh_create_date=fields.Date("Create Date")
    # sh_create_date=fields.Date("Create Date",default=lambda self: fields.Date.context_today(self))
    sh_total_event_count=fields.Integer('Total Events Count', compute='_total_event_count')
    sh_user_id = fields.Many2one('res.users', "User Name")


    parent_id = fields.Many2one('sh.talking.points', string='Parent Talking Point', index=True, ondelete='cascade')
    child_ids = fields.One2many('sh.talking.points', 'parent_id', string='Child Talking Points')
    is_auto_create=fields.Boolean('Is Auto Created',default=False)

    def _compute_talking_point_name(self):

        # for add formate in sep 22, 2023 for kanban view
        # ===============================================
        for record in self:
            record.name = 'New'
            if record.sh_create_date:
                date_obj = record.sh_create_date
                formatted_date = date_obj.strftime("%b %d, %Y")
                record.name = formatted_date
            else:
                record.name = 'New'

    def _total_event_count(self):
        for rec in self:
            events=self.env['calendar.event'].sudo().search([('sh_talking_point_id','=',rec.id)])
            if events:
                rec.sh_total_event_count=len(events)
            else:
                rec.sh_total_event_count=0


    # === ADD NOTIFICATION FUNCTIONALITY WHEN CREATED === 
    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for talking in res:
            related_employee = talking.sh_employee_id
            current_login_user = talking.sh_user_id
            self.env['sh.br.engage.push.notification'].create_br_engage_push_notification(user=related_employee.user_id,name="1on1s Created",description="Your 1on1s is created with - %s"%(current_login_user),res_model="sh.talking.points",res_id=talking.id)
            self.env['sh.br.engage.push.notification'].create_br_engage_push_notification(user=current_login_user,name="1on1s Created",description="Your 1on1s is created with - %s"%(related_employee.user_id.name),res_model="sh.talking.points",res_id=talking.id)
        return res