# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from random import randint
from odoo import models, fields


class ShPushModule(models.Model):
    _name = "sh.push.module"
    _description = "Push Modules Details"

    def _get_default_color(self):
        return randint(1, 11)

    color = fields.Integer('Color', default=_get_default_color)
    name = fields.Char(string='Module Name', required=True)
    sh_project_id = fields.Many2one('project.project', string='Project', required=True)
