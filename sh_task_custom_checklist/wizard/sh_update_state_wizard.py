# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields


class ShUpdateStateWizard(models.TransientModel):
    _name = 'sh.update.state.wizard'
    _description = 'Mass Update Accepted State'

    state_ids = fields.Many2many(
        'sh.checklist.state', string='Accepted in State')
    chechlist_ids = fields.Many2many('task.custom.checklist', string='Checklists')

    def btn_mass_update_state(self):
        state_list = [(4, state.id) for state in self.state_ids]
        for checklist in self.chechlist_ids:
            checklist.sudo().write({
                'accepted_state_ids': state_list
            })