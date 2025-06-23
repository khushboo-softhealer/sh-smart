# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields


class ResUser(models.TransientModel):
    _name = "sh.claim.user.wizard"
    _description = 'Claim User Wizard'

    user_id = fields.Many2one(
        'res.users', string="Claim Responsible User", required=True)
    product_ids = fields.Many2many('product.template')

    def assign_user(self):
        self.product_ids.write({'copyright_claim_user': self.user_id.id})
