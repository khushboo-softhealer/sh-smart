# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models


class sale_order(models.Model):
    _inherit = "sale.order"

    def sh_mass_quotation_confirm(self):
        sale_order_obj = self.env['sale.order']
        active_ids = self.env.context.get('active_ids')
        if active_ids:
            for active_id in active_ids:
                search_so_rec = sale_order_obj.search(
                    [('id', '=', active_id)], limit=1)
                if search_so_rec:
                    search_so_rec.action_confirm()
