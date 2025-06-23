# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import _, api, fields, models, tools
from odoo.tools import email_split


class ShSkipCrmLeadSpam(models.Model):
    _name = "sh.skip.crm.lead"
    _description = "Skip CRM Lead"

    name = fields.Char(string='Email')


class CRMLeadInherit(models.Model):
    _inherit = "crm.lead"

    def action_stop_spaming(self):
        for rec in self:
            if rec.email_from:
                sh_email = email_split(rec.email_from)
                spam_lead_id = self.env['sh.skip.crm.lead'].sudo().create({
                    'name': sh_email[0]
                })
                if spam_lead_id:
                    self.env.user.company_id.sh_skip_crm_lead_ids = [
                        (4, spam_lead_id.id)]

    @api.model
    def message_new(self, msg_dict, custom_values=None):
        if self.env.company.sh_skip_crm_lead_ids:
            email_from = msg_dict.get('from')            
            if email_from:
                email_parts = tools.email_split_tuples(email_from)[0]
                if email_parts[0]:
                    email = email_parts[1]
                    # Check From Email is in Spam List or not ?
                    if email in self.env.company.sh_skip_crm_lead_ids.mapped('name'):
                        # Messate To Be Ingnored
                        self = self.with_context(to_be_ignored = True)
                        return super(CRMLeadInherit, self).message_new(msg_dict, custom_values=custom_values)
    
        return super(CRMLeadInherit, self).message_new(msg_dict, custom_values)
         
    @api.model_create_multi
    def create(self, values):
                
        if self.env.context.get('to_be_ignored'):
            blank_crm_record = self.env['crm.lead'].browse()             
            return blank_crm_record
            
        
        result = super(CRMLeadInherit,self).create(values)

        return result