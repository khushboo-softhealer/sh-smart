# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api


class ShCrState(models.Model):
    _name = "sh.cr.state"
    _description = "CR State"

    name = fields.Char('Name', copy=False)
    is_default_state = fields.Boolean('Is Default State')

    def _write_is_default_state(self):
        states = self.env['sh.cr.state'].sudo().search([])
        for state in states:
            if state.id == self.id:
                continue
            state.is_default_state = False

    def write(self, vals):
        status = super(ShCrState, self).write(vals)
        if vals.get('is_default_state'):
            self._write_is_default_state()
        return status

    @api.model_create_multi
    def create(self, vals_list):
        all_status = super(ShCrState, self).create(vals_list)
        for state in all_status:
            if state.is_default_state:
                state._write_is_default_state()
        return all_status
