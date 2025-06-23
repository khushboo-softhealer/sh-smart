# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models


class purchase_order(models.Model):
    _inherit = "purchase.order"

    def sh_mass_rfq_confirm(self):
        purchase_order_obj = self.env['purchase.order']
        active_ids = self.env.context.get('active_ids')
        if active_ids:
            for active_id in active_ids:
                search_po_rec = purchase_order_obj.search(
                    [('id', '=', active_id)], limit=1)
                if search_po_rec:
                    search_po_rec.button_confirm()
