# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.


from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    sh_replied_status = fields.Selection([('staff_replied','Staff Replied'),('customer_replied','Customer Replied'),('running','Running'),('closed','Closed')],string="Replied Status")
    sh_replied_status_id = fields.Many2one('sh.replied.status',string='Replied Status ', index=True, group_expand='_read_group_replied_stage_ids',tracking=True)

    @api.model
    def _read_group_replied_stage_ids(self, stages, domain, order):
        all_stages = self.env['sh.replied.status'].sudo().search([])
        search_domain = [('id', 'in', all_stages.ids)]

        # perform search
        stage_ids = stages._search(
            search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)