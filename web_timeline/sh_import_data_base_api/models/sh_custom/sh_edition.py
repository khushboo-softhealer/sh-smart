# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ShEdition(models.Model):
    _inherit = 'sh.edition'

    remote_sh_edition_id = fields.Char("Remote Edition ID",copy=False)




