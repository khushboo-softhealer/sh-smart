# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api


class SaleUpdate(models.TransientModel):
    _name = 'sh.sale.update.wizard'
    _description = "Mass sale update"

    sh_replied_status = fields.Selection([('staff_replied','Staff Replied'),('customer_replied','Customer Replied'),('running','Running'),('closed','Closed')],string="Replied Status ",required=True)
    sh_replied_status_id = fields.Many2one('sh.replied.status','Replied Status',required=True)

    def action_update(self):
        self.ensure_one()
        if self.env.context.get('active_ids'):
            sale_ids = self.env[self.env.context.get('active_model')].sudo().browse(self.env.context.get('active_ids'))
            if sale_ids:
                for sale in sale_ids:
                    sale.sh_replied_status_id = self.sh_replied_status_id.id
                    sale.sh_replied_status = self.sh_replied_status

