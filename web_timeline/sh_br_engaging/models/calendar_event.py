# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models,api,_
from datetime import datetime,date
from odoo.exceptions import UserError


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    # === CODE TO ADD THE TRUE AGENDA IN ONE2MANY ===  
    def _default_meeting_agenda_line(self):
        find_true_meeting_agenda = self.env["sh.meeting.agenda"].sudo().search([('sh_is_active','=',True)])
        default_line_list = []
        for true_record in find_true_meeting_agenda : 
            default_line_list.append((0,0,{'name':true_record.id}))
        return default_line_list

    sh_talking_point_id = fields.Many2one('sh.talking.points','Talking Point Id')
    sh_calendar_check_in_id = fields.Many2one('sh.check.in', "Check In", related='sh_talking_point_id.sh_check_in_id')
    sh_is_rescheduled = fields.Boolean('Is Rescheduled')
    sh_previous_talking_point_line = fields.One2many(comodel_name='sh.talking.points.previous.history',inverse_name='sh_calender_event_id',string='Previous Talking Points Line')
    sh_current_talking_point_line = fields.One2many(comodel_name='sh.talking.points',inverse_name='sh_calender_event_id',string='Current Talking Points Line')
    sh_meeting_agenda_line = fields.One2many(comodel_name='sh.temp.meeting.agenda',inverse_name='sh_calender_event_id',string='Meeting Agenda',default=lambda self: self._default_meeting_agenda_line())

    # sh_is_user_attendee=fields.Boolean(
    #     string='Is User Attendee')

    # sh_user_partner_id_in_partners = fields.Boolean(
    #     string='User Partner ID in Partners',
    #     compute='_compute_user_partner_id_in_partners'
    # )

    is_br_user=fields.Boolean('Is BR User',
                              compute='_check_is_br_user')
    
    sh_stage = fields.Selection([
            ('draft', 'Draft'),
            ('completed', 'Completed'),
        ],default='draft',string='Stage')
    

    def action_complete(self):
        for rec in self:
            rec.sh_stage='completed'

    def write(self, vals):
        for rec in self:
            # if rec.sh_stage=='completed':
            #     raise UserError(_('You cannot update completed meeting..!'))
            
            # FOR USER NOTIFICATION WHEN UPDATE MEETING
            if rec.partner_ids and rec.user_id:
                for partner in rec.partner_ids:
                    if partner.user_ids:
                        for user in partner.user_ids:
                            if user.id != rec.user_id.id:
                                self.env['sh.br.engage.push.notification'].create_br_engage_push_notification(user=user,name="Meeting Updated",description="Your Meeting '%s' Updated..!"%(rec.name),res_model="calendar.event",res_id=rec.id)

                if self.env.user.id != rec.sudo().user_id.id:
                    self.env['sh.br.engage.push.notification'].create_br_engage_push_notification(user=rec.sudo().user_id,name="Meeting Updated",description="Your Meeting '%s' Updated..!"%(rec.name),res_model="calendar.event",res_id=rec.id)

        return super(CalendarEvent, self).write(vals)


    @api.depends('is_br_user')
    def _check_is_br_user(self):
        for rec in self:
            current_user = self.env.user
            user_group = self.env.ref('sh_br_engaging.group_br_engage_user')
            manager_group = self.env.ref('sh_br_engaging.group_br_engage_manager')

            if user_group in current_user.groups_id and manager_group not in current_user.groups_id:
                rec.is_br_user=True
            else:
               rec.is_br_user=False



    # @api.depends('partner_ids')
    # def _compute_user_partner_id_in_partners(self):
    #     current_user_partner_id = self.env.user.sudo().partner_id.id
    #     for event in self:
    #         event.sh_user_partner_id_in_partners = current_user_partner_id in event.sudo().partner_ids.ids
    #         event.sh_is_user_attendee = current_user_partner_id in event.sudo().partner_ids.ids



    @api.model_create_multi
    def create(self, vals_list):

        res = super().create(vals_list)

        for meeting in res:
            if meeting.partner_ids and meeting.user_id:
                for partner in meeting.partner_ids:
                    if partner.user_ids:
                        for user in partner.user_ids:
                            # if user.id != meeting.user_id.id:
                            self.env['sh.br.engage.push.notification'].create_br_engage_push_notification(user=user,name="1-on-1s Created",description="Your 1-on-1s Created With %s"%(meeting.user_id.name),res_model="calendar.event",res_id=meeting.id)




            talking_id=meeting.sh_talking_point_id

            #     # for user push notification
            #     if talking_id and talking_id.sh_user_id:
            #         if talking_id.sh_user_id.id==self.env.user.id:
            #             if talking_id.sh_employee_id and talking_id.sh_employee_id.user_id:

            #                 self.env['sh.br.engage.push.notification'].create_br_engage_push_notification(user=talking_id.sh_employee_id.user_id,name="1-on-1s Created",description="Your 1-on-1s Created With %s"%(self.env.user.name),res_model="calendar.event",res_id=res.id)

            #         else:
            #             self.env['sh.br.engage.push.notification'].create_br_engage_push_notification(user=talking_id.sh_user_id,name="1-on-1s Created",description="Your 1-on-1s Created With %s"%(self.env.user.name),res_model="calendar.event",res_id=res.id)
            

            if not meeting.sh_is_rescheduled and meeting.sh_talking_point_id:

                # ON SCHEDULE MEETING WE ARE CONNNECT THIS CREATED EVENT TO TALKING POINT AND AFTER PASSING
                # THIS TALKING EVENT ID TO ITS PREVIOUS LINES WE UPDATE CURRENT TALKING POINT EVENT ID WITH RES ID
                if talking_id:
                    talking_id.sh_calender_event_id=meeting.id
                    
                    # for change talking point date to current date
                    talking_id.sh_create_date=datetime.now()

                    
            if meeting.sh_is_rescheduled:
                
                # NEW
                if talking_id:
                    child_talking_point_vals={
                        'name':talking_id.name,
                        'sh_employee_id':talking_id.sh_employee_id.id,
                        'sh_your_notes':talking_id.sh_your_notes,
                        'sh_employee_notes':talking_id.sh_employee_notes,
                        'sh_your_private_notes':talking_id.sh_your_private_notes,
                        'sh_stage':talking_id.sh_stage,
                        'parent_id':talking_id.id,
                        'sh_user_private_notes':talking_id.sh_user_private_notes,
                        # ==================================
                        # for update old talking point date
                        'sh_create_date':talking_id.sh_create_date,
                        }
                    child_talking_point=self.env['sh.talking.points'].sudo().create(child_talking_point_vals)
                    # ========================================================================================
                    # === CREATE NEW RECORDS IN NEW MODEL SPECIALLY FOR VIEW AGENDA WIZARD ===
                    # ========================================================================================
                    get_one2many_agenda_records = talking_id.sh_manage_agenda_line
                    for agenda_record in get_one2many_agenda_records :
                        # CREATE VALS LIST FOR VIEW AGENDA MODEL 
                        view_agenda_vals = {
                            'sh_view_agenda_id' : agenda_record.sh_agenda_id.id,
                            'sh_view_agenda_description' :agenda_record.sh_talking_point_description,
                            'sh_view_agenda_checked' :agenda_record.sh_checked,
                            'sh_view_agenda_talking_point_id' : child_talking_point.id
                        }
                        view_agenda_record = self.env['sh.talking.point.view.agenda'].sudo().create(view_agenda_vals)
                    # ========================================================================================
                    # ========================================================================================

                    if talking_id.sh_calender_event_id:

                        # update current note to meeting
                        child_talking_point.sh_calender_event_id=talking_id.sh_calender_event_id

                        # add current talking point to current meeting
                        talking_id.sh_calender_event_id=meeting.id


                    if talking_id.child_ids:
                        # for create previous talking point child ids
                        for child in talking_id.child_ids:
                            previous_talking_point_vals={
                                'name':child.name,
                                'sh_employee_id':child.sh_employee_id.id,
                                'sh_your_notes':child.sh_your_notes,
                                'sh_employee_notes':child.sh_employee_notes,
                                'sh_your_private_notes':child.sh_your_private_notes,
                                'sh_stage':child.sh_stage,
                                'sh_talking_point_id':child.id,
                                'sh_user_private_notes':child.sh_user_private_notes,
                                'sh_calender_event_id':meeting.id,
                            }
                            previous_talking_point=self.env['sh.talking.points.previous.history'].sudo().create(previous_talking_point_vals)

                    # for create new records of previous talking points agenda line
                    # if talking_id.sh_manage_agenda_line:
                    #     for agenda in talking_id.sh_manage_agenda_line:
                    #         agenda_line_vals={
                    #             'sh_agenda_id':agenda.sh_agenda_id.id,
                    #             'sh_checked':agenda.sh_checked,
                    #             'sh_previous_talking_point_id':previous_talking_point.id,
                    #             'sh_talking_point_id':False,
                    #         }
                    #         talking_line=self.env['sh.talking.agenda.line'].sudo().create(agenda_line_vals)

                    # for update value in current talking point to fill new again
                    talking_id.sh_your_notes=False
                    talking_id.sh_employee_notes=False
                    talking_id.sh_your_private_notes=False
                    talking_id.sh_user_private_notes=False

                    # for change talking point date to current date
                    talking_id.sh_create_date=datetime.now()

                    # for link current event to current talking points if not done
                    talking_id.sh_calender_event_id=meeting.id

                    # for untick old line records
                    if talking_id.sh_manage_agenda_line:
                        for agenda in talking_id.sh_manage_agenda_line:
                            agenda.sh_checked= False

            
            
        return res


    # def open_conditional_1on1s(self) :

    #     current_user_partner_id = self.env.user.partner_id

    #     one_on_ones_records = self.env["calendar.event"].sudo().search([('partner_ids', 'in', current_user_partner_id.ids)])

    #     # # one_on_ones_records = self.env["calendar.event"].search([('sh_talking_point_id', '!=', False),('sh_is_user_attendee','=',True)])
    #     # one_on_ones_records = self.env["calendar.event"].search([('sh_talking_point_id', '!=', False)])

    #     # if one_on_ones_records :
    #     return {
    #         'name': "Meetings View",
    #         'type': 'ir.actions.act_window',
    #         'view_mode': 'tree',
    #         'views': [(False, 'tree'), (False, 'form')],
    #         'res_model': "calendar.event",
    #         'target': 'current',
    #         'domain': [('id', 'in', one_on_ones_records.ids if one_on_ones_records else [])]
    #     }



    def create_monthly_team_meeting(self):
        company=self.env.company
        current_date = date.today()

        if company.sh_monthly_meeting_date and company.sh_monthly_meeting_date == current_date:

            all_employees=self.env['hr.employee'].sudo().search([])
            for empl in all_employees:
                if empl.user_partner_id and empl.child_ids:

                    meeting_vals={ }
                    if empl.user_id:
                        meeting_vals.update({
                            'user_id':empl.user_id.id
                        })

                    for child_empl in empl.child_ids:
                        if child_empl.user_partner_id:

                            partner_ids=[]
                            partner_ids.append(empl.user_partner_id.id)
                            partner_ids.append(child_empl.user_partner_id.id)

                            meeting_vals.update({
                                'partner_ids':[(6, 0, partner_ids)],
                                'name':'One on One',
                            })
                            self.sudo().create(meeting_vals)

