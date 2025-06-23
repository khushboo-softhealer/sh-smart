# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, api, _


class ResCompany(models.Model):
    _inherit = 'res.company'
    
    resource_calendar_id = fields.Many2one('resource.calendar', string="Resource Calendar Id")



class res_config_settings(models.TransientModel):
    _inherit = 'res.config.settings'

    resource_calendar_id = fields.Many2one('resource.calendar', string="Resource Calendar Id", readonly=False, related='company_id.resource_calendar_id')
