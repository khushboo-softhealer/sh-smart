# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models,api
from odoo.exceptions import ValidationError


class ManageBadge(models.Model):
    _name = "sh.manage.badge"
    _description = "Manage Badges"

    name = fields.Char("Badge",required=True)
    sh_is_active = fields.Boolean("Active")

    @api.constrains('name')
    def _check_no_spaces(self):
        for badge in self:
            if ' ' in badge.name:
                raise ValidationError("Badge name cannot contain spaces.")
