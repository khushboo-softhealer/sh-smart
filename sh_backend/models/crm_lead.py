# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields,api
from odoo.tools.translate import html_translate


class Lead(models.Model):
    _inherit = "crm.lead"
    
    product_id = fields.Many2one('product.template', string="Product")

    @api.model_create_multi
    def create(self,vals_list):
        res = super(Lead,self).create(vals_list)
        for rec in res:
            users = res.env['res.users'].search([])
            listt = []
            for user in users:
                if user.has_group('sales_team.group_sale_manager'):
                    listt.append(user)
            if not self.env.user in listt:
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                self.env['user.push.notification'].push_notification(listt,'New Lead Created','Lead Reference: %s:'% (rec.name),base_url+"/mail/view?model=crm.lead&res_id="+str(rec.id),'crm.lead',rec.id,'sale')
        return res
