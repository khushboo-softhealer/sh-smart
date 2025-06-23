# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models
from odoo.exceptions import ValidationError


class College(models.Model):
    _name = 'sh.college'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'College Data'

    name = fields.Char(required=True)
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State',
                               ondelete='cascade', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one(
        'res.country', string='Country', ondelete='cascade')

    contact_person_ids = fields.Many2many(
        comodel_name='res.partner')

    colloge_contact_no = fields.Char("College Contact Number")
    tpo_contact_no = fields.Char("TPO Contact Number")
    email = fields.Char("Email")
    stage_id = fields.Many2one('sh.college.stages', string='Stage',
                               ondelete='cascade', tracking=True, index=True, copy=False)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "College name already exists !"),
        ('colloge_contact_no_uniq', 'unique (colloge_contact_no)',
         "College Contact Number already exists !"),
        ('email_uniq', 'unique (email)', "Email already exists !"),
    ]

    def change_state_action(self):
        context = self.env.context or {}
        if context and context.get("active_ids", False):
            active_ids = context.get('active_ids')
            college = self.env["sh.college"].browse(active_ids)
            if college:
                college.sudo().write({
                    "stage_id": self.stage_id.id,
                })

    def change_state_action(self):
        if self.env.user.has_group('hr_recruitment.group_hr_recruitment_manager'):
            return {
                'name': 'Mass Update College Stage',
                'res_model': 'sh.college.change.stages.wizard',
                'view_mode': 'form',
                'view_id': self.env.ref('sh_hr_placement.mass_update_college_stage_form').id,
                'target': 'new',
                'type': 'ir.actions.act_window',
                'context': {'default_college_ids': [(6, 0, self.env.context.get('active_ids'))]}
            }
        else:
            raise ValidationError(
                'You are not Authorised to perform this action !')
