# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
import requests
import json
from datetime import datetime


# -------------------- OTHER CODE ----------------------------


class ShCertification(models.Model):
    _inherit = 'sh.certification'

    remote_sh_certification_id = fields.Char("Remote Certification Id",copy=False)

# ------------------------------------------------------------


class InheritImportHrRuleImport(models.Model):
    _inherit = "sh.import.base"
    json_field = fields.Text('JOSN Data')

    def import_sh_certification(self):
        ''' ========== Connect db for import import_sh_certification  ==================  '''
        config = self.env['sh.import.base'].search([], limit=1)

        response = requests.get('''%s/api/public/sh.certification?query={%s}''' % (
            config.base_url, self.query_dict['sh_certification']))
        response_json = response.json()
        self.json_field = response_json

        if response.status_code == 200:
            count = 0
            for data in response_json['result']:
                sh_certification_vals = config.prepare_sh_certification_vals(
                    data)
                domain = [('remote_sh_certification_id', '=', data['id'])]
                find_certification_id = self.env['sh.certification'].search(
                    domain)
                # try:
                if find_certification_id:
                    count += 1
                    find_certification_id.write(sh_certification_vals)
                else:
                    count += 1
                    self.env['sh.certification'].create(sh_certification_vals)

            if count > 0:
                vals = {
                    "name": config.name,
                    "state": "success",
                    "field_type": "hr_employee_basic",
                    "error": "%s Certification Imported Successfully" % (count),
                    "datetime": datetime.now(),
                    "base_config_id": config.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)

        else:
            vals = {
                "name": config.name,
                "state": "error",
                "field_type": "hr_employee_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": config.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals)

    def prepare_sh_certification_vals(self, data):

        sh_certification_vals = {
            'remote_sh_certification_id': data['id'],
            'display_name': data['display_name'],
            'course': data['course'],
            'level_completion': data['level_completion'],
            'certificate': data['certificate'],

        }

        self.date_vals(data, sh_certification_vals, data_key='comp_year')

        return sh_certification_vals
