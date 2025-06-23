# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api

class Task(models.Model):
    _inherit = 'project.task'

    sh_ticket_ids = fields.Many2many('sh.helpdesk.ticket', string='Tickets ')
