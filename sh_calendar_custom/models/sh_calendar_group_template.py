# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class CalendarGroupTemplate(models.Model):
    _name = 'sh.calendar.group.template'
    _description = "Custom template Can be created for specific group"

    name = fields.Char(string="Name", required=True)
    partner_ids = fields.Many2many('res.partner', string="Attendees", domain=[
                                   ('user_ids', '!=', False)])
