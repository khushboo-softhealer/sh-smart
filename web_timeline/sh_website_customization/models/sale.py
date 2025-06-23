# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies

from odoo import fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    website_id = fields.Many2one('website', string='Website', readonly=False,
                                 help='Website through which this order was placed for eCommerce orders.')
    