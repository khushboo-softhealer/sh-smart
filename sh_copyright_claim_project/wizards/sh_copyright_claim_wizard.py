# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class CopyrightClaimWizard(models.TransientModel):
    _name = 'sh.copyright.claim.wizard'
    _description = "Copyright ClaimWizard"

    date_from = fields.Date(string='Date From', required=True,
                            default=lambda self: fields.Date.to_string(date.today().replace(day=1)))
    date_to = fields.Date(string='Date To', required=True,
                          default=lambda self: fields.Date.to_string((datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()))
    task_ids = fields.Many2many('project.task', string='Task')

    def sh_print_report(self):
        if not self.task_ids:
            parent_id = self.env.context.get("active_id")
            d = self.env['sh.copyright.claim'].search([
                ('task_id', '=', parent_id),
                ('create_date', '>=', self.date_from),
                ('create_date', '<=', self.date_to)
            ])
        else:
            d = self.env['sh.copyright.claim'].search([
                ('task_id', 'in', self.task_ids.ids),
                ('create_date', '>=', self.date_from),
                ('create_date', '<=', self.date_to)
            ])
        datas = {
            'ids': d.ids,
            'model': 'sh.copyright.claim',
            'form': {'claim': d}
        }
        return self.env.ref('sh_copyright_claim_project.sh_claim_details_report_action').report_action(d.ids, data=datas)
