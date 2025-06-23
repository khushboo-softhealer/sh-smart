# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ShVersion(models.Model):
    _inherit = 'sh.version'

    remote_sh_version_id = fields.Char("Remote Version ID",copy=False)





