# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ShDepends(models.Model):
    _inherit = 'sh.depends'

    remote_sh_depends_id = fields.Char("Remote Depends ID",copy=False)
