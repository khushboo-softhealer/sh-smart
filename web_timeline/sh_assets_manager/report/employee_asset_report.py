# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import api, models


class EmployeeAssetReport(models.AbstractModel):
    _name = 'report.sh_assets_manager.assets_employee_report_doc'
    _description = "Employee Asset Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'doc_ids': data.get('ids'),
            'doc_model': data.get('model'),
            'dic_assets': data['dic_assets'],
        }
