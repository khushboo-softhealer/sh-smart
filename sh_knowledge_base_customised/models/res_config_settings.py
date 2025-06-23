# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

class ResCompany(models.Model):
    _inherit = 'res.company'
    

    sh_draft_sop_id=fields.Many2one("sh.sop.stages",string="Draft")
    sh_submit_manager_id=fields.Many2one("sh.sop.stages",string="Submit To Manager")
    sh_approved_id=fields.Many2one("sh.sop.stages",string="Approved")
    sh_reject_id=fields.Many2one("sh.sop.stages",string="Reject")

class ResCompany(models.TransientModel):
    _inherit = 'res.config.settings'
    sh_draft_sop_id=fields.Many2one(related="company_id.sh_draft_sop_id",readonly=False,string="Draft")
    sh_submit_manager_id=fields.Many2one(related="company_id.sh_submit_manager_id",readonly=False,string="Submit To Manager")
    sh_approved_id=fields.Many2one(related="company_id.sh_approved_id",readonly=False,string="Approved")
    sh_reject_id=fields.Many2one(related="company_id.sh_reject_id",readonly=False,string="Reject")