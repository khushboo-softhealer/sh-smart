# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import models


class SaleOrderPartnerCateg(models.Model):
    _inherit = 'sale.order'

    def action_lock_sale_order(self):
        context = self.env.context.get('active_ids')
        sale_obj = self.search([('id', 'in', context)])

        for sale in sale_obj:
            sale.action_done()
