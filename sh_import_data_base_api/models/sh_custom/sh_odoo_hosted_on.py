# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ShOdooHostedOn(models.Model):
    _inherit = 'sh.odoo.hosted.on'

    remote_sh_odoo_hosted_id = fields.Char("Remote Odoo Hosted ID",copy=False)

