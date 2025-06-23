# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class ShMigrationNotifyMe(models.Model):
    _name = "sh.migration.notify.me"
    _description = "Migration Ticket Notify"

    partner_id = fields.Many2one(
        string='Partner',
        comodel_name='res.partner',
        ondelete='restrict',
    )
     
    product_id = fields.Many2one(
        string='Product',
        comodel_name='product.product',
        ondelete='restrict',
    )

    product_web_url = fields.Char(
        string='Product URL',
    )

    is_notified = fields.Boolean('Is Already Notified', default=False)
    company_id = fields.Many2one('res.company', string='Company', default=lambda x: x.env.company)
