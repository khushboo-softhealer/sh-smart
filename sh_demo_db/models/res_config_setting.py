# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    sh_expired_demo_db = fields.Integer('Demo DB Expired (Hours)')
    sh_demo_type_id = fields.Many2one('sh.helpdesk.ticket.type',string='Demo Ticket Type')
    sh_demo_stage_id = fields.Many2one('sh.helpdesk.stages',string="Demo DB Ticket Stage")
    sh_demo_db_user_ids = fields.Many2many('res.users','rel_user_demo_ids',string='Demo Responsible Users')
    sh_demo_limit = fields.Integer('Demo DB limit to delete at a time')
    sh_db_drop_activity_assign_id = fields.Many2one('res.users',string='Delete Demo Exception Activity Assign To',domain=[('share','=',False)])

class HelpdeskSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    sh_expired_demo_db = fields.Integer('Demo DB Expired (Hours)',readonly=False,related='company_id.sh_expired_demo_db')
    sh_demo_type_id = fields.Many2one('sh.helpdesk.ticket.type',string='Demo Ticket Type',related='company_id.sh_demo_type_id',readonly=False)
    sh_demo_stage_id = fields.Many2one('sh.helpdesk.stages',string="Demo DB Ticket Stage",related='company_id.sh_demo_stage_id',readonly=False)
    sh_demo_db_user_ids = fields.Many2many('res.users',string='Demo Responsible Users',related='company_id.sh_demo_db_user_ids',readonly=False)
    sh_demo_limit = fields.Integer('Demo DB limit to delete at a time',related='company_id.sh_demo_limit',readonly=False)
    sh_db_drop_activity_assign_id = fields.Many2one('res.users',string='Delete Demo Exception Activity Assign To',related='company_id.sh_db_drop_activity_assign_id',readonly=False,domain=[('share','=',False)])