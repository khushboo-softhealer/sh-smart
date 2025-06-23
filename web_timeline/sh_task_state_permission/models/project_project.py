# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models, _


class ShStateProjectProject(models.Model):
    _inherit = 'project.project'

    sh_restrict_stage_movement = fields.Boolean(
        'Restrict Department Wise Stage Movement')
