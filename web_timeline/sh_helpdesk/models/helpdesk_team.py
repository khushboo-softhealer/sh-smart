# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _


class HelpdeskTeam(models.Model):
    _name = 'sh.helpdesk.team'
    _description = 'Helpdesk Team'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    team_head = fields.Many2one('res.users', 'Team Head', required=True, domain=[
                                '|', ('share', '=', False), ('sh_portal_user_access', '!=', False)])
    team_members = fields.Many2many('res.users', string="Team Members", domain=[
                                    '|', ('share', '=', False), ('sh_portal_user_access', '!=', False)])
    sh_resource_calendar_id = fields.Many2one(
        'resource.calendar', string="Working Schedule")
    sla_count = fields.Integer(compute='_compute_helpdesk_sla')

    def _compute_helpdesk_sla(self):
        for record in self:
            record.sla_count = 0
            slas = self.env['sh.helpdesk.ticket'].sudo().search(
                [('team_id', '=', self.id), ('sh_sla_status_ids', '!=', False)])
            record.sla_count = len(slas.ids)

    def action_view_sla(self):
        self.ensure_one()
        slas = self.env['sh.helpdesk.ticket'].sudo().search(
            [('team_id', '=', self.id), ('sh_sla_status_ids', '!=', False)])
        action = self.env.ref('sh_helpdesk.helpdesk_ticket_action').read()[0]
        if len(slas) > 1:
            action['domain'] = [('id', 'in', slas.ids)]
        elif len(slas) == 1:
            action['views'] = [
                (self.env.ref('sh_helpdesk.helpdesk_ticket_form_view').id, 'form')]
            action['res_id'] = slas.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
