# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ShDegree(models.Model):
    _inherit = 'sh.degree'

    remote_sh_degree_id = fields.Char("Remote Degree Id",copy=False)

