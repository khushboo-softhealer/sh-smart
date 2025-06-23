# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ShRequiredStatus(models.Model):
    _inherit = 'sh.required.apps'

    remote_sh_required_apps_id = fields.Char("Required Apps ID",copy=False)