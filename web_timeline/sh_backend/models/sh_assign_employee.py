# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, api

class ShAssignEmployee(models.TransientModel):

    _name = "sh.assign.employee"
    _description = "Sh Assign Employee"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    partner_ids = fields.Many2many("res.partner", string="Recipients")
    assigned_user_ids = fields.Many2many("res.users", string = "Responsible Users ",domain=[('share', '=', False)])

    def add_followers(self):

        context = dict(self._context or {})
        active_id = context.get('active_id', False)
        if active_id:
            project = self.env['project.project'].sudo().browse(active_id)
            if self.assigned_user_ids:
                for user_id in self.assigned_user_ids:
                    project.sudo().write({'responsible_user_ids':[(4,user_id.id)]})
