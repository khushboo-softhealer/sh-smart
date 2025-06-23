# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models


class ShFeedback(models.Model):
    _name = "sh.realtime.feedback"
    _description = "Realtime Feedback Menu For BR-enage"

    sh_realtime_feedback_person = fields.Many2one('res.users', "Who would you like to give feedback to?")
    name = fields.Char("Your Feedback")
    sh_feedback_review_selection = fields.Selection([
            ('public', 'Public'),
            ('manager', 'Manager'),
            ('recepient_only', 'Recipient Only'),
        ],default='public', string="Who will see this feedback?")
    sh_feedback_type = fields.Selection([('give_feedback', 'Give Feedback'),
                                         ('request_feedback', 'Request Feedback')])
    sh_created_by_id = fields.Many2one('res.users', "Created By ")
    sh_create_date = fields.Char("Create Date")
    sh_parent_id = fields.Many2one('sh.realtime.feedback', "Store Parent Id")





    def create(self,vals):
        res = super(ShFeedback,self).create(vals)        
        # self.env['sh.br.engage.push.notification'].new_notification_method_for_test(user=self.env.user,name="Manage Question",description="Manage Question Edited",res_model="sh.manage.questions",res_id=self.id)
        self.env['sh.br.engage.push.notification'].realtime_update_method_for_feedback(user=res.sh_realtime_feedback_person)
        # self.env['sh.br.engage.push.notification'].realtime_update_method_for_feedback(user=res.sh_created_by_id)
        self.env['sh.br.engage.push.notification'].create_br_engage_push_notification(user=res.sh_realtime_feedback_person,name="New Feedback",description="You have new feedback from %s"%(self.env.user.name),res_model="sh.realtime.feedback",res_id=0)
        return res