# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api


class AddRemoveFollower(models.TransientModel):
    _name = 'sh.add.remove.followers'
    _description = 'Add/Remove Followers'

    partner_ids = fields.Many2many(
        'res.partner', string='Recipients', required=True)
    follower_action = fields.Selection(
        [('add', 'Add'), ('remove', 'Remove')], default='add', string="Followers Action")

    def action_follower(self):
        active_ids = self.env.context.get('active_ids')
        for active_id in active_ids:
            ticket_id = self.env['sh.helpdesk.ticket'].sudo().browse(active_id)
            if ticket_id:
                if self.follower_action == 'add':
                    ticket_id.message_subscribe(
                        partner_ids=self.partner_ids.ids)
                elif self.follower_action == 'remove':
                    ticket_id.message_unsubscribe(
                        partner_ids=self.partner_ids.ids)
