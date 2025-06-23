from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    sh_partner_ticket_count = fields.Integer(
        compute='_compute_partner_ticket_count')

    def _compute_partner_ticket_count(self):
        for rec in self:
            rec.sh_partner_ticket_count = 0
            tickets = self.env['sh.helpdesk.ticket'].sudo().search(
                [('partner_id', '=', rec.id)])
            if tickets:
                rec.sh_partner_ticket_count = len(tickets.ids)

    def action_view_partner_ticket(self):
        self.ensure_one()
        tickets = self.env['sh.helpdesk.ticket'].sudo().search(
            [('partner_id', '=', self.id)])
        action = self.env.ref(
            "sh_helpdesk.helpdesk_ticket_action").read()[0]
        if len(tickets) > 1:
            action['domain'] = [('id', 'in', tickets.ids)]
        elif len(tickets) == 1:
            form_view = [
                (self.env.ref('sh_helpdesk.helpdesk_ticket_form_view').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + \
                    [(state, view)
                     for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = tickets.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
