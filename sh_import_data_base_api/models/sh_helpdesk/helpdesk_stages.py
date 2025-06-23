# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class HelpdeskStages(models.Model):
    _inherit = 'sh.helpdesk.stages'

    remote_sh_helpdesk_stages_id = fields.Char("Remote Helpdesk Stages ID",copy=False)