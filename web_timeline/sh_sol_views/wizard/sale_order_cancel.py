# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import api, fields, models


class SaleOrderCancel(models.TransientModel):
    _inherit = "sale.order.cancel"

    display_purchase_orders_alert = fields.Boolean(
        string="Purchase Order Alert",
        compute='_compute_display_purchase_orders_alert',groups='purchase.group_purchase_user'
    )

