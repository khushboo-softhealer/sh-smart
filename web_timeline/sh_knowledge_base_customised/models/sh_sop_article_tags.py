# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from random import randint

class SOPArticalTags(models.Model):
    _name = 'sh.sop.article.tags'
    _description = 'SOP Article Tags'
    
    def _default_color(self):
        return randint(1, 11)
    name=fields.Char(string="Name")
    color = fields.Integer('Color Index', default=lambda self: self._default_color())