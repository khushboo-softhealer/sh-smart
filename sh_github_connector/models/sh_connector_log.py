# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, _
from odoo.exceptions import UserError


class ShConnectorLog(models.Model):
    _name = "sh.connector.log"
    _description = "Connector Log"
    _order = 'id desc'

    # name = fields.Char("Name")
    message = fields.Char("Message")
    datetime = fields.Datetime("Date & Time")
    connector_obj_id = fields.Many2one(
        'sh.github.connector', string='Connector Ref')
    field_type = fields.Selection([
        ('-', '-'),
        ('auth', 'Authentication'),
        ('repo', 'Repo'),
        ('branch', 'Branch'),
        ('module', 'Module'),
        ('index', 'Index'),
        ('product', 'Product'),
        ('p_queue', 'Product Queue'),
    ], "Field Type")
    state = fields.Selection([
        ('success', 'Success'),
        ('error', 'Failed'),
        ('sync', 'Sync'),
    ], string='State')
    operation = fields.Selection([
        ('import', 'Import'),
        ('auth', 'Token Generation'),
        ('sync', 'Sync'),
        ('cron', 'Cron'),
        ('notify', 'Notify')
    ], string='Operation')
