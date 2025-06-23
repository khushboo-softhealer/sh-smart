# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models


class TaskStage(models.Model):
    _inherit = "project.task.type"

    sh_draft = fields.Boolean("Draft")
    sh_done = fields.Boolean("Done")
    sh_cancel = fields.Boolean("Cancel")
    sh_is_uat = fields.Boolean("Is UAT")
    sh_is_testing = fields.Boolean("Is Testing")
    sh_is_push_to_main = fields.Boolean('Is Push to Main')