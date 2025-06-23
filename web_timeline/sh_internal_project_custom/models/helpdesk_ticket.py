# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models

class HelpdeskTicket(models.Model):
    _inherit = 'sh.helpdesk.ticket'

    sh_move_task_to_preapp_store = fields.Boolean('Create Task To PreApp Store')