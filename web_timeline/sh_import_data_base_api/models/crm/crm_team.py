# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class CrmTeam(models.Model):
    _inherit = 'crm.team'

    remote_crm_team_id = fields.Char("Remote Crm Team ID",copy=False)