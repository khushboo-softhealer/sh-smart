# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.


from odoo import api, fields, tools,models,_
from datetime import datetime,timedelta
from datetime import date
from odoo.exceptions import AccessError
import logging
_logger = logging.getLogger(__name__)

class ShCheckin(models.Model):
    _name = "sh.check.in"
    _description = "Check-in Menu For BR-enage"

    name = fields.Char("Name",compute='_compute_check_in_name')
    sh_employee_id = fields.Many2one('hr.employee', "Employee Name")
    # sh_check_in_frequency = fields.Char("Check-in Frequeny")
    sh_from_date=fields.Date("From Date")
    sh_to_date=fields.Date("To Date")
    sh_stage = fields.Selection([
            ('draft', 'Draft'),
            ('submitted', 'Submitted'),
        ],default='draft',string='Stage')
    sh_user_id=fields.Many2one("res.users","User")
    sh_question_answer_line = fields.One2many(comodel_name='sh.question.answers',inverse_name='sh_check_in_id',string='Question Answer Line')

    def create_check_in_from_scheduler(self):
        company=self.env.company
        question= self.env['sh.manage.questions']

        limit=0
        final_currently_asked_question=[]
        need_to_run=False

        # Check if it's the first day of the month
        today = datetime.now()
        current_month = today.month
        current_day = datetime.now().strftime('%A').lower()

        # FOR MONTHLY DAY WISE CALCULATIONS
        if self.env.company.sh_question_frequency=='monthly' and self.env.company.sh_repeat_question_queue  and self.env.company.sh_repeat_date:
            if today.day == self.env.company.sh_repeat_date:
                need_to_run=True

                current_date = datetime.now()
                first_day_of_current_month = current_date.replace(day=1)
                last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
                date_to_subtract = self.env.company.sh_repeat_date  
                previous_month_date = last_day_of_previous_month.replace(day=date_to_subtract)


        # FOR WEEKLY DAY WISE CALCULATIONS
        if self.env.company.sh_question_frequency=='weekly' and self.env.company.sh_repeat_question_queue:
            if current_day == self.env.company.sh_repeat_day:
                need_to_run=True

        if need_to_run:
            if company.sh_turn_question_queue_on_off and company.sh_no_of_questions_asked:
                limit=company.sh_no_of_questions_asked
                every_check_in= question.search([('sh_in_every_check_in','=',True),('sh_is_active','=',True)],limit=limit)
                # every_check_in= question.search([('sh_in_every_check_in','=',True)],limit=limit)

                if every_check_in:
                    limit=limit-len(every_check_in)
                    for question in every_check_in:
                        final_currently_asked_question.append(question.id)

                if limit:
                    # last_sequence = question.search([], order='sequence desc', limit=1).sequence
                    # question_records = question.sudo().search([('sh_in_every_check_in','=',False)], order='sequence', limit=limit)
                    last_sequence = question.search([('sh_is_active','=',True)], order='sequence desc', limit=1).sequence
                    question_records = question.sudo().search([('sh_in_every_check_in','=',False),('sh_is_active','=',True)], order='sequence', limit=limit)

                    for record in question_records:
                        final_currently_asked_question.append(record.id)
                        # if last sequence is repeated
                        last_sequence= last_sequence+1
                        record.write({'sequence': last_sequence})

            # for update question records stages
            if final_currently_asked_question:
                already_currently_being_question= self.env['sh.manage.questions'].sudo().search([('sh_question_category','=','currently_being_asked'),('sh_in_every_check_in','=',False)])
                if already_currently_being_question:
                    for old_question in already_currently_being_question:
                        old_question.write({
                            "sh_question_category":'up_next'
                        })

                new_question_list= self.env['sh.manage.questions'].sudo().browse(final_currently_asked_question)
                if new_question_list:
                    for question in new_question_list:
                        if question.sh_question_category !='currently_being_asked':
                            question.write({
                                "sh_question_category":'currently_being_asked'
                            })

            total_employees=self.env['hr.employee'].sudo().search([])
            if final_currently_asked_question and total_employees:
                for employee in total_employees:
                    check_in_vals={
                        'sh_employee_id':employee.id,
                        'sh_to_date':today.strftime('%Y-%m-%d'),
                        # 'sh_from_date':today.strftime('%Y-%m-%d'),
                    }
                    if employee.user_id:
                        check_in_vals.update({
                            'sh_user_id':employee.user_id.id
                        })

                    if self.env.company.sh_question_frequency=='weekly':
                        check_in_vals.update({
                            'sh_from_date':(today - timedelta(days=7)).strftime('%Y-%m-%d'),
                        })
                    if self.env.company.sh_question_frequency=='monthly':
                        check_in_vals.update({
                            'sh_from_date':previous_month_date,
                        })

                    # if self.env.company.sh_question_frequency=='weekly':
                    #     check_in_vals.update({
                    #         'sh_to_date':(today + timedelta(days=7)).strftime('%Y-%m-%d'),
                    #     })
                    # if self.env.company.sh_question_frequency=='monthly':
                    #     check_in_vals.update({
                    #         'sh_to_date':(today + timedelta(days=till_next_month_selected_day_difference)).strftime('%Y-%m-%d'),
                    #     })

                    check_in=self.env['sh.check.in'].sudo().create(check_in_vals)

                    # for push notification of check-in creation
                    if employee.user_id and check_in:
                        self.env['sh.br.engage.push.notification'].create_br_engage_push_notification(user=employee.user_id,name="Check-in Created",description="Check-in Ref - %s"%(check_in.name),res_model="sh.check.in",res_id=check_in.id)


                    for question_id in final_currently_asked_question:
                        question_answer_line_vals={
                            'sh_question_id':question_id,
                            'sh_check_in_id':check_in.id,
                        }
                        self.env['sh.question.answers'].sudo().create(question_answer_line_vals)


    # def _cron_send_check_in_notification(self):

    #     unsubmitted_check_ins = self.search([('sh_stage', '=', 'draft')])
    #     for check_in in unsubmitted_check_ins:

    #         # for send bell notification on pending check in
    #         if check_in.sh_user_id and self.env.company.sh_send_check_in_pending_bell_notification:
    #             self.env['sh.br.engage.push.notification'].create_br_engage_push_notification(user=check_in.sh_user_id,name="Check-in Pending",description="Check-in Ref - %s"%(check_in.name),res_model="sh.check.in",res_id=check_in.id)
        
    #         # for send mail notification on pending check in
    #         if self.env.company.sh_send_check_in_pending_email_notification:
    #             email_values = {
    #                 'email_from': self.env.user.email_formatted,
    #                 'author_id': self.env.user.partner_id.id,
    #             }
    #             template = self.env.ref('sh_br_engaging.sh_email_template_check_in_pending')
    #             template.send_mail(check_in.id,email_values=email_values,force_send=True)

    def _cron_send_check_in_notification(self):

        unsubmitted_check_ins = self.search([('sh_stage', '=', 'draft')])
        # _logger.info(' =----->unsubmitted_check_ins %s' % (unsubmitted_check_ins))
        # for each_record in unsubmitted_check_ins:
        #     _logger.info(' =------>check %s' % (each_record.create_date.date()))
        #     _logger.info(' =------>check %s' % (date.today()))
        employee_will_get_emails = unsubmitted_check_ins.filtered(lambda x:x.create_date.date() != date.today()).mapped('sh_user_id').mapped('partner_id')
        # _logger.info(' =------>employee_will_get_emails %s' % (employee_will_get_emails))
        unsubmitted_check_ins = unsubmitted_check_ins.filtered(lambda x:x.create_date.date() != date.today())
        if self.env.company.sh_send_check_in_pending_bell_notification:
            for check_in in unsubmitted_check_ins:
                if check_in.sh_user_id:
                    self.env['sh.br.engage.push.notification'].create_br_engage_push_notification(user=check_in.sh_user_id,name="Check-in Pending",description="Check-in Ref - %s"%(check_in.name),res_model="sh.check.in",res_id=check_in.id)
            
        #     # for send mail notification on pending check in
        #     # if self.env.company.sh_send_check_in_pending_email_notification:
        #     #     email_values = {
        #     #         'email_from': self.env.user.email_formatted,
        #     #         'author_id': self.env.user.partner_id.id,
        #     #     }
        #     #     template = self.env.ref('sh_br_engaging.sh_email_template_check_in_pending')
        #     #     template.send_mail(check_in.id,email_values=email_values,force_send=True)
        if self.env.company.sh_send_check_in_pending_email_notification:
            
            # ========================================
            mail_server_id=self.env.company.sh_mail_server_id
            if not mail_server_id:
                mail_server_id=self.env['ir.mail_server'].sudo().search([],order='sequence asc' ,limit=1)

            email_formatted=False
            if mail_server_id:               
                email_formatted = tools.formataddr((
                        self.env.company.name or u"False",
                        mail_server_id.sudo().smtp_user
                    ))
            # ========================================

                email_values = {
                    'email_from': email_formatted,
                    'recipient_ids':employee_will_get_emails.ids,
                    'mail_server_id':mail_server_id.id
                }
                template = self.env.ref('sh_br_engaging.sh_email_template_check_in_pending')
                template.sudo().send_mail(self.env.company.id,email_values=email_values,force_send=True)



    def _get_weekday_number(self, weekday):
        weekdays = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}
        return weekdays.get(weekday, 0)

    # to add dynamic name on based on from and to date
    # ================================================
    def _compute_check_in_name(self):
        for rec in self:
            if rec.sh_from_date and rec.sh_to_date:
                start_date_str = rec.sh_from_date.strftime('%b %d')
                end_date_str = rec.sh_to_date.strftime('%b %d')
                rec.name = f"{start_date_str} - {end_date_str}"
            else:
                rec.name=False


    # Open Directly Form View Onclick of menu 
    def open_seprate_form_view(self):
        self.env.user.id
        latest_check_in_records = self.env['sh.check.in'].search([('sh_user_id','=',self.env.user.id)],order='id desc').ids
        if latest_check_in_records :
            return {
                'name': "Check In Form View",
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'views': [(False, 'form')],
                'res_model': "sh.check.in",
                'res_id': latest_check_in_records[:1][0] if latest_check_in_records else False,
                'target': 'current',
            }
        else :
            # return {
            #     'name': "Check In Form View",
            #     'type': 'ir.actions.act_window',
            #     'view_mode': 'list',
            #     'views': [(False, 'list')],
            #     'res_model': "sh.check.in",
            #     'target': 'current',
            # }
            return {
                'name': "Check In Form View",
                'type': 'ir.actions.act_window',
                'view_mode': 'list',
                'views': [(False, 'list')],
                'res_model': "sh.check.in",
                'domain': [('id', 'in', [])],
                'target': 'current',
                'help': _('''<p class="o_view_nocontent">
                    You Have Not Any Check-in
                </p>'''),
            }


    def action_open_form_view(self):

        # if self.user_has_groups('sh_br_engaging.group_br_engage_manager') and self.sh_user_id != self.env.user and self.sh_stage=='draft':
        if self.sh_stage=='draft':
            raise AccessError(_("Still user has not submitted check-in..!"))

        return {
            'name': "Check In Form View",
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'views': [(False, 'form')],
            'res_model': "sh.check.in",
            'res_id': self.id,
            'target': 'current',
        }
    

    def open_all_child_checkin_tree_view(self) :
        # CREATE EMPTY LIST TO STORE THE ALL CHILD IDS INTO THAT
        login_employee_child_ids_list = []
        # CREATE ANOTHER LIST TO STORE THE CHILD EMPLOYEES CHECK-IN RECORD IDS 
        check_in_record_ids_list = []
        current_login_user = self.env.user
        # =======================================================================
        # CHECK IF CURRENT LOGIN USER HAVE MANAGER GROUP ACCESS OR NOT 
        # =======================================================================
        if self.user_has_groups('sh_br_engaging.group_br_engage_manager') :
            return {
                'name': "Team Member Check-ins",
                'type': 'ir.actions.act_window',
                'view_mode': 'list',
                'views': [(False, 'list')],
                'res_model': "sh.check.in",
                # 'domain': [('id', 'in', login_employee_child_ids_list)],
                'target': 'current',
                'help': _('''<p class="o_view_nocontent">
                    No Records Found
                </p>'''),
            }
        # ==================================================================
        # SHOW ALL CHILD MEMBER'S CHECK-IN RECORD IF NOT HAVE MANAGER ACCESS
        # =================================================================
        else :
            login_user_related_employee = current_login_user.employee_id
            if login_user_related_employee : 
                if login_user_related_employee.subordinate_ids :
                    for child in login_user_related_employee.subordinate_ids :
                        login_employee_child_ids_list.append(child.id)
                else : 
                    login_employee_child_ids_list = login_employee_child_ids_list

            for employee in login_employee_child_ids_list :
                check_in_record = self.env['sh.check.in'].search([('sh_employee_id', '=', employee )])
                if check_in_record : 
                    for check_in in check_in_record : 
                        check_in_record_ids_list.append(check_in.id)
            
            logged_in_user_Checkin = self.env['sh.check.in'].search([('sh_employee_id','=',login_user_related_employee.id)])
            for my_check_in in logged_in_user_Checkin:
                check_in_record_ids_list.append(my_check_in.id)

            return {
                    'name': "Team Member Check-ins",
                    'type': 'ir.actions.act_window',
                    'view_mode': 'list',
                    'views': [(False, 'list')],
                    'res_model': "sh.check.in",
                    'domain': [('id', 'in', check_in_record_ids_list)],
                    'target': 'current',
                    'help': _('''<p class="o_view_nocontent">
                        No Records Found
                    </p>'''),
                }


    
                
