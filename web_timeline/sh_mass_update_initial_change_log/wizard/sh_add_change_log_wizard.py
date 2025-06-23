# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields


class UpdateIntialChangeLog(models.TransientModel):
    _name = 'sh.add.change.log.wizard'
    _description = 'Add Change Log'

    date = fields.Date("Date", default=fields.Date.today())
    log_type = fields.Selection(
        [('fix', 'Fix'), ('add', 'Add'), ('update', 'Update')], string="Type", default='add')
    version = fields.Char("Version", default="16.0.1")
    details = fields.Char("Details", default="Initial Release")

    def add_change_log(self):
        product_ids = self.env.context.get('default_product_ids')
        if product_ids and product_ids[0] and product_ids[0][2]:
            products = product_ids[0][2]
            for product in products:
                self.env['product.change.log'].create({
                    'date': self.date,
                    'log_type': self.log_type,
                    'version': self.version,
                    'details': self.details,
                    'product_variant_id': product
                })
