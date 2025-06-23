# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models


class ShPasswordManagerProject(models.Model):
    _inherit = 'project.project'

    sh_password_generator_line = fields.One2many('password.generator', 'project_id', string='Password Line')
