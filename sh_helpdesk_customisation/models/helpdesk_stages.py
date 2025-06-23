# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

import logging
from odoo.exceptions import UserError
from odoo import models, fields,api
_logger = logging.getLogger(__name__)

class HelpdeskStagesCustomisation(models.Model):
    _inherit = 'sh.helpdesk.stages'
    
    sh_res_users_ids = fields.Many2many('res.users', string='Responsible Users',domain=[('share','=',False)])
    sh_helpdesk_ticket_type_id = fields.Many2one('sh.helpdesk.ticket.type', string='Ticket Type')
    sh_remove_responsible_user = fields.Boolean('Remove Other Responsible Users')