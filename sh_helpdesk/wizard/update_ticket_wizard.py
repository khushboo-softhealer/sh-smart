# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, _, api
from odoo.exceptions import UserError


class MassUpdateWizard(models.TransientModel):

    _name = "sh.helpdesk.ticket.mass.update.wizard"
    _description = "Mass Update Wizard"

    check_assign_to = fields.Boolean(string='Asssign To', default=False)
    assign_to = fields.Many2one(
        comodel_name='res.users', string='Assign To', domain=[('share', '=', False)])
    check_sh_display_multi_user = fields.Boolean()
    check_assign_to_multiuser = fields.Boolean(default=False,
                                               string="Assign Multi User")
    ticket_update_type = fields.Selection([
        ('add', 'Add'),
        ('replace', 'Replace'),
    ],
        default="add")
    assign_to_multiuser = fields.Many2many('res.users',
                                           string="Assign Multi Users", domain=[('share', '=', False)])

    check_helpdesks_state = fields.Boolean(default=False, string=" Stage")
    sh_helpdesk_stages = fields.Many2one('sh.helpdesk.stages', string="Stage")

    def update_record(self):

        # <-- ASSIGN TO UPDATE -->
        ticket_ids = self.env['sh.helpdesk.ticket'].sudo().browse(
            self.env.context.get('active_ids'))
        if ticket_ids:
            for ticket in ticket_ids:
                if self.check_assign_to == True:

                    ticket.sudo().write(
                        {'user_id': self.assign_to.id})

                # <-- ASSIGN MULTIUSER UPDATE -->

                if self.check_assign_to_multiuser == True:

                    if self.ticket_update_type == 'add':
                        get_list = []
                        for rec1 in self.assign_to_multiuser:
                            if rec1:
                                get_list.append(rec1.id)
                        ticket.sudo().write(
                            {'sh_user_ids': [(6, 0, get_list)]})

                    if self.ticket_update_type == "replace":
                        ticket.sudo().write(
                            {'sh_user_ids': [(6, 0, self.assign_to_multiuser.ids)]})

                # <-- STATE UPDATE -->

                if self.check_helpdesks_state == True:
                    if self.sh_helpdesk_stages:
                        ticket.stage_id = self.sh_helpdesk_stages.id
