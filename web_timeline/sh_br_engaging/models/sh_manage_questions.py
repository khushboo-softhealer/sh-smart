# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import api, fields, models

class ManageQuestions(models.Model):
    _name = "sh.manage.questions"
    _description = "Model for Create And Manage Questions"

    name = fields.Char("Questions",required=True)
    sh_in_every_check_in = fields.Boolean("In Every Check-In")
    sh_question_category = fields.Selection([
            ('currently_being_asked', 'Currently Being Asked'),
            ('up_next', 'Up Next'),
        ],default='up_next',readonly=True, string="Question Category")
    sh_is_active = fields.Boolean("Active")
    sequence = fields.Integer(help='Used to order Questions in the dashboard view', default=10)
    sh_is_rating_question = fields.Boolean("Is Rating Question")
    sh_how_did_you_feel_question = fields.Boolean("Main Rating Question", default=False)





    