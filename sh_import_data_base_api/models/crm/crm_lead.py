# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    remote_crm_lead_id = fields.Char("Remote lead ID",copy=False)
    
    
