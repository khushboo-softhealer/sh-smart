# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class CrmStage(models.Model):
    _inherit = 'crm.stage'

    remote_crm_stage_id = fields.Char("Remote Crm Stage ID",copy=False)