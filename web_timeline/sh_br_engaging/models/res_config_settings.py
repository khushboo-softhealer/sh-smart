# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    # sh_turn_question_queue_on_off = fields.Boolean(
    #     "Turn Question Queue On/Off ? ", default=True)

    # sh_question_frequency = fields.Selection([
    #         ('weekly', 'Weekly'),
    #         ('monthly', 'Monthly'),
    #     ],default='weekly')

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


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # sh_turn_question_queue_on_off = fields.Boolean(
    #     "Turn Question Queue On/Off? ",
    #     related="company_id.sh_turn_question_queue_on_off",readonly=False)

    # sh_question_frequency = fields.Selection([
    #         ('weekly', 'Weekly'),
    #         ('monthly', 'Monthly'),
    #     ],related="company_id.sh_question_frequency",readonly=False)

    # sh_repeat_question_queue = fields.Boolean(
    #     related="company_id.sh_repeat_question_queue", string="Repeat Question Queue ?", readonly=False)

    # sh_repeat_day = fields.Selection([
    #     ('monday', 'Monday'),
    #     ('tuesday', 'Tuesday'),
    #     ('wednesday', 'Wednesday'),
    #     ('thursday', 'Thursday'),
    #     ('friday', 'Friday'),
    #     ('saturday', 'Saturday'),
    #     ('sunday', 'Sunday'),
    # ], string='Repeat Every',
    # related="company_id.sh_repeat_day",readonly=False)

    # sh_repeat_date = fields.Integer(string='Repeat Date',
    # related="company_id.sh_repeat_date",readonly=False)

    # sh_no_of_questions_asked = fields.Integer(
    #     "No of Questions Asked ",related="company_id.sh_no_of_questions_asked",readonly=False)

    # sh_send_check_in_pending_email_notification = fields.Boolean(
    #  string="Send Mail Notification on Pending Check-in ?",related="company_id.sh_send_check_in_pending_email_notification",readonly=False)

    # sh_send_check_in_pending_bell_notification = fields.Boolean(
    #  string="Send Bell Notification on Pending Check-in ?",related="company_id.sh_send_check_in_pending_bell_notification",readonly=False)
    
    sh_points_for_each_received_high_five = fields.Integer(
     string="Points For Each Received High Five",related="company_id.sh_points_for_each_received_high_five",readonly=False)
    
    sh_points_for_each_given_high_five = fields.Integer(
     string="Points For Each Given High Five",related="company_id.sh_points_for_each_given_high_five",readonly=False)
    
    # sh_wall_of_fame_employee = fields.Many2one('res.users',related="company_id.sh_wall_of_fame_employee",readonly=False)
    # sh_wall_of_fame_record_update_date = fields.Date(string="Wall Of Fame Record Update Date", related="company_id.sh_wall_of_fame_record_update_date",readonly=False)
    # sh_mail_server_id = fields.Many2one(related="company_id.sh_mail_server_id",readonly=False)
    # sh_monthly_meeting_date = fields.Date("Monthly Meeting Date",related="company_id.sh_monthly_meeting_date",readonly=False)
