# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import api, fields, models


class ChecklistState(models.Model):
    _name = 'sh.checklist.state'
    _description = 'Stages'

    name = fields.Char('Name', copy=False)
    is_default_state = fields.Boolean('Is Default State')

    def _write_is_default_state(self):
        states = self.env['sh.checklist.state'].sudo().search([])
        for state in states:
            if state.id == self.id:
                continue
            state.is_default_state = False

    def write(self, vals):
        status = super(ChecklistState, self).write(vals)
        if vals.get('is_default_state'):
            self._write_is_default_state()
        return status

    @api.model_create_multi
    def create(self, vals_list):
        all_status = super(ChecklistState, self).create(vals_list)
        for state in all_status:
            if state.is_default_state:
                state._write_is_default_state()
        return all_status
