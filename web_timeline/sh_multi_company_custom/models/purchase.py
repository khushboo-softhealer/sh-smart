# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    company_alert = fields.Boolean(
        string="",compute='_company_alert_onchange')
    
    @api.model
    def default_get(self, fields):
        res = super(PurchaseOrder, self).default_get(fields)
        company_alert = False
        if self.env.company.name == 'Softhealer Technologies Private Limited':
            company_alert = True
        else:
            company_alert = False
        res.update({
            'company_alert': company_alert,
        })
        return res

    def _company_alert_onchange(self):
        for rec in self:
            
            rec.company_alert = False
            if rec.company_id.name == 'Softhealer Technologies Private Limited':
                rec.company_alert = True
            else:
                rec.company_alert = False