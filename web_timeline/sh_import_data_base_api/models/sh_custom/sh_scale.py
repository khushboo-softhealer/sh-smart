# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ShDepends(models.Model):
    _inherit = 'sh.scale'

    remote_sh_scale_id = fields.Char("Remote Scale ID",copy=False)






