# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ShDownloadModuleLog(models.Model):
    _name = "sh.download.module.log"
    _description = "Download Module Log"
    _order = "create_date desc"

    module_ids = fields.Many2many('sh.module', string='Modules')
    for_which = fields.Selection([
        ('project', 'Project'),
        ('ticket', 'Ticket')
    ], string='For Which')
    project_id = fields.Many2one('project.project', string='Project')
    task_id = fields.Many2one('project.task', string='Task')
    ticket_id = fields.Many2one('sh.helpdesk.ticket', string='Ticket')
    is_for_migration = fields.Boolean('Is For Migration')
