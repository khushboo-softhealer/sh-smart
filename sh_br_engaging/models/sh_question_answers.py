# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import api, fields, models

class QuestionsAnswers(models.Model):
    _name = "sh.question.answers"
    _description = "Model for Create And Manage Questions"
    _rec_name='sh_question_id'

    sh_question_id = fields.Many2one("sh.manage.questions",string="Question Id")
    sh_answer=fields.Text('Answer')
    sh_check_in_id = fields.Many2one("sh.check.in",string="Check-in Id")
    sh_is_rating_question = fields.Boolean("In Rating Question",related='sh_question_id.sh_is_rating_question')
    sh_low_rating_reason = fields.Text("Reason Of Low Rating")
