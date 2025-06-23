# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class CrmLostReason(models.Model):
    _inherit = 'crm.lost.reason'

    remote_crm_lost_reason_id = fields.Char("Remote Crm Lost Reason ID",copy=False)





