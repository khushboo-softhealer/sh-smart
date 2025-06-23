# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ShCopyrightClaim(models.Model):
    _inherit = 'sh.copyright.claim'

    remote_sh_copyright_claim_id = fields.Char("Remote Copyright Claim ID",copy=False)