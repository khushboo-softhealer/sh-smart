# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    remote_res_partner_id = fields.Char("Remote Partner ID",copy=False)

class ResPartnerCategory(models.Model):
    _inherit = 'res.partner.category'

    remote_res_partner_category_id = fields.Char("Remote Partner Category ID",copy=False)