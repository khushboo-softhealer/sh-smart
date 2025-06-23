# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    sh_crm_customer_replied = fields.Boolean('Stage change when customer replied ?')
    sh_crm_staff_replied = fields.Boolean('Stage change when staff replied ?')
    sh_crm_customer_replied_stage_id = fields.Many2one('crm.stage',string='Customer Replied Stage')
    sh_crm_staff_replied_stage_id = fields.Many2one('crm.stage',string='Staff Replied Stage')

class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_crm_customer_replied = fields.Boolean('Stage change when customer replied ?',related='company_id.sh_crm_customer_replied',readonly=False)
    sh_crm_staff_replied = fields.Boolean('Stage change when staff replied ?',related='company_id.sh_crm_staff_replied',readonly=False)
    sh_crm_customer_replied_stage_id = fields.Many2one('crm.stage',string='Customer Replied Stage',related='company_id.sh_crm_customer_replied_stage_id',readonly=False)
    sh_crm_staff_replied_stage_id = fields.Many2one('crm.stage',string='Staff Replied Stage',related='company_id.sh_crm_staff_replied_stage_id',readonly=False)