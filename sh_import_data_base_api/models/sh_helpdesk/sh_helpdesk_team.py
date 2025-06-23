# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ShHelpdeskTeam(models.Model):
    _inherit = 'sh.helpdesk.team'

    remote_sh_helpdesk_team_id = fields.Char("Remote Helpdesk Team ID",copy=False)