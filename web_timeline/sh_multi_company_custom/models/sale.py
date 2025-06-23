# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    company_alert = fields.Boolean(
        string="",compute='_company_alert_onchange')
    
    @api.model
    def default_get(self, fields):
        res = super(SaleOrder, self).default_get(fields)
        company_alert = False
        if self.env.company.name == 'Softhealer Technologies Private Limited':
            company_alert = True
        else:
            company_alert = False
        res.update({
            'company_alert': company_alert,
        })
        return res

    # @api.onchange('company_id')
    # @api.depends('company_id')
    def _company_alert_onchange(self):
        for rec in self:
            
            rec.company_alert = False
            if rec.company_id.name == 'Softhealer Technologies Private Limited':
                rec.company_alert = True
            else:
                rec.company_alert = False


    @api.constrains('company_id')
    def _check_company_for_TL(self):
        """ TL cannot create sale order in SS or ST """
        if not self.company_id.name == 'Softhealer Technologies Private Limited' and self.env.user.has_group('sh_multi_company_custom.tl_restrict_company_group'):
            raise ValidationError('Please make sure company is not Softhealer Technologies Private Limited !')


