# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ShHelpdeskSla(models.Model):
    _inherit = 'sh.helpdesk.sla'

    remote_sh_helpdesk_sla_id = fields.Char("Remote Helpdesk Sla ID",copy=False)