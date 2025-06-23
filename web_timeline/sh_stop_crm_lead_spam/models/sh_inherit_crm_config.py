# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import _, api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sh_skip_crm_lead_ids = fields.Many2many(
        'sh.skip.crm.lead', string='Skip spaming lead auto generate', readonly=False)


class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_skip_crm_lead_ids = fields.Many2many(
        'sh.skip.crm.lead', related='company_id.sh_skip_crm_lead_ids', string='Skip Spaming lead auto generate', readonly=False)
