# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import  fields, models,api

class UpdateConfiguration(models.TransientModel):
    _name = "sh.br.custom.configuration"
    _description = "Br Configurations"

    def default_get(self, fields):
        result = super(UpdateConfiguration, self).default_get(fields)
        company_id = self.env.company
        result.update({
            # 'sh_turn_question_queue_on_off': company_id.sh_turn_question_queue_on_off,
            # 'sh_question_frequency': company_id.sh_question_frequency,
            # 'sh_repeat_question_queue': company_id.sh_repeat_question_queue,
            # 'sh_repeat_day': company_id.sh_repeat_day,
            # 'sh_repeat_date': company_id.sh_repeat_date,
            # 'sh_no_of_questions_asked': company_id.sh_no_of_questions_asked,
            # 'sh_send_check_in_pending_email_notification': company_id.sh_send_check_in_pending_email_notification,
            # 'sh_send_check_in_pending_bell_notification': company_id.sh_send_check_in_pending_bell_notification,
            'sh_points_for_each_received_high_five': company_id.sh_points_for_each_received_high_five,
            'sh_points_for_each_given_high_five': company_id.sh_points_for_each_given_high_five,
            # 'sh_wall_of_fame_employee': company_id.sh_wall_of_fame_employee.id,
            # 'sh_wall_of_fame_record_update_date': company_id.sh_wall_of_fame_record_update_date,
            # 'sh_mail_server_id': company_id.sh_mail_server_id.id,
            # 'sh_monthly_meeting_date': company_id.sh_monthly_meeting_date,
        })
        return result

    name=fields.Char('Name')
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
        default=lambda self: self.env.company)
    # sh_turn_question_queue_on_off = fields.Boolean(
    #     "Turn Question Queue On/Off ? ")

    # sh_question_frequency = fields.Selection([
    #         ('weekly', 'Weekly'),
    #         ('monthly', 'Monthly'),
    #     ],default='weekly',string='Question Frequency')

    # sh_repeat_question_queue = fields.Boolean(
    #  string="Repeat Question Queue ?")

    # sh_repeat_day = fields.Selection([
    #     ('monday', 'Monday'),
    #     ('tuesday', 'Tuesday'),
    #     ('wednesday', 'Wednesday'),
    #     ('thursday', 'Thursday'),
    #     ('friday', 'Friday'),
    #     ('saturday', 'Saturday'),
    #     ('sunday', 'Sunday'),
    # ], string='Repeat Every',default='monday')

    # sh_repeat_date = fields.Integer(string='Repeat Date')

    # sh_no_of_questions_asked = fields.Integer(
    #     "No of Questions Asked ", default=1)

    # sh_send_check_in_pending_email_notification = fields.Boolean(
    #  string="Send Mail Notification on Pending Check-in ?")
    
    # sh_send_check_in_pending_bell_notification = fields.Boolean(
    #  string="Send Bell Notification on Pending Check-in ?")
    
    sh_points_for_each_received_high_five = fields.Integer(
     string="Points For Each Received High Five")
    
    sh_points_for_each_given_high_five = fields.Integer(
     string="Points For Each Given High Five")
    
    # sh_wall_of_fame_employee = fields.Many2one('res.users', string="Employee Of The Month")

    # sh_wall_of_fame_record_update_date = fields.Date("Wall Of Fame Record Update Date")
    # sh_mail_server_id = fields.Many2one('ir.mail_server', string='Outgoing Mail Server')
    # sh_monthly_meeting_date = fields.Date("Monthly Meeting Date")


    def update_company_configurations(self):
        company = self.env.company
        company_values = {
            # 'sh_turn_question_queue_on_off': self.sh_turn_question_queue_on_off,
            # 'sh_question_frequency': self.sh_question_frequency,
            # 'sh_repeat_question_queue': self.sh_repeat_question_queue,
            # 'sh_repeat_day': self.sh_repeat_day,
            # 'sh_repeat_date': self.sh_repeat_date,
            # 'sh_no_of_questions_asked': self.sh_no_of_questions_asked,
            # 'sh_send_check_in_pending_email_notification': self.sh_send_check_in_pending_email_notification,
            # 'sh_send_check_in_pending_bell_notification': self.sh_send_check_in_pending_bell_notification,
            'sh_points_for_each_received_high_five': self.sh_points_for_each_received_high_five,
            'sh_points_for_each_given_high_five': self.sh_points_for_each_given_high_five,
            # 'sh_wall_of_fame_employee': self.sh_wall_of_fame_employee.id,
            # 'sh_wall_of_fame_record_update_date': self.sh_wall_of_fame_record_update_date,
            # 'sh_mail_server_id': self.sh_mail_server_id.id,
            # 'sh_monthly_meeting_date': self.sh_monthly_meeting_date,
        }
        company.sudo().write(company_values)