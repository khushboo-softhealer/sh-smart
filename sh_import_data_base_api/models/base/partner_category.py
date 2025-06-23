# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class PartnerCategory(models.Model):
    _inherit = 'partner.category'

    remote_partner_category_id = fields.Char("Remote Partner Category ID",copy=False)
