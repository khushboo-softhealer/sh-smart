# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models


class ShConfirmSalePartner(models.Model):
    _inherit = 'res.partner'

    sh_confirm_sale_is_odoo_customer = fields.Boolean('Is Odoo Customer', default=False, copy=False)
