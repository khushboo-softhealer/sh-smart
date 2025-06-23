# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ShLicense(models.Model):
    _inherit = 'sh.license'

    remote_sh_license_id = fields.Char("Remote License ID",copy=False)


