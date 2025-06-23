# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models


class Product(models.Model):
    _inherit = 'product.product'

    def action_add_change_log_wizard(self):

        return {
            'name': 'Add Change Log',
            'res_model': 'sh.add.change.log.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('sh_mass_update_initial_change_log.add_initial_change_log_form').id,
            'context': {'default_product_ids': [(6, 0, self.env.context.get('active_ids'))]},
            'target': 'new',
            'type': 'ir.actions.act_window'
        }
