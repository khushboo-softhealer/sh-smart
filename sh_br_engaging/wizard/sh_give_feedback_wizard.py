# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import _, api, fields, models
from datetime import datetime
from odoo.exceptions import UserError,ValidationError

class GiveFeedback(models.TransientModel):
    _name = "sh.give.feedback.wizard"
    _description = "Model for Store Give Feedback Records"

    sh_give_feedback_person = fields.Many2one('res.users', "Who would you like to give feedback to?")
    # sh_give_feedback_person_test = fields.Many2one('hr.employee', "Who would you like to give feedback to?")
    name = fields.Text("Your Feedback")
    sh_feedback_review_selection = fields.Selection([
            ('public', 'Public'),
            ('manager', 'Manager'),
            ('recepient_only', 'Recipient Only'),
        ],default='manager', string="Who will see this feedback?")
    

    def action_give_feedback(self):
        # Get the current date
        current_date = datetime.now()
        if self.name and self.sh_give_feedback_person and self.sh_feedback_review_selection :
            # Format the current date into character.
            formatted_date = current_date.strftime("%d %B, %Y")
            realtime_feedback_vals={
                            'sh_realtime_feedback_person':self.sh_give_feedback_person.id,
                            'name':self.name,
                            'sh_feedback_review_selection': self.sh_feedback_review_selection,
                            'sh_feedback_type' : 'give_feedback',
                            'sh_created_by_id' : self.env.user.id,
                            'sh_create_date' : formatted_date,
                        }
            self.env['sh.realtime.feedback'].sudo().create(realtime_feedback_vals)
            return {'type': 'ir.actions.client', 'tag': 'soft_reload'}
        else :
            raise ValidationError(_('Please Fill Required Fields'))
    
    def discard_give_feedback(self) :
        return {'type': 'ir.actions.client', 'tag': 'soft_reload'}