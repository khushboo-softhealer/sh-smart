# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class CrmTag(models.Model):
    _inherit = 'crm.tag'

    remote_crm_tag_id = fields.Char("Remote Crm tag ID",copy=False)