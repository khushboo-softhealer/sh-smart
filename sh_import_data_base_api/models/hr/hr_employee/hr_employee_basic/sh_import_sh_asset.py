# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
import requests
import json
from datetime import datetime


# -------------------- OTHER CODE ----------------------------


class Shasset(models.Model):
    _inherit = 'sh.asset'

    remote_sh_asset_id = fields.Char("Remote Asset Id",copy=False)


class ShassetType(models.Model):
    _inherit = 'sh.asset.type'

    remote_sh_asset_type_id = fields.Char("Remote Asset Type Id",copy=False)

# ------------------------------------------------------------


class InheritImportHrRuleImport(models.Model):
    _inherit = "sh.import.base"
    json_field = fields.Text('JOSN Data')

    def import_sh_asset(self):
        ''' ========== Connect db for import import_sh_certification  ==================  '''
        config = self.env['sh.import.base'].search([], limit=1)

        response = requests.get(
            '''%s/api/public/sh.asset?query={%s}''' % (config.base_url, self.query_dict['sh_asset']))
        response_json = response.json()
        self.json_field = response_json

        if response.status_code == 200:
            count = 0
            failed = 0
            for data in response_json['result']:
                try:
                    sh_asset_vals = config.prepare_sh_asset_vals(data)
                    domain = [('remote_sh_asset_id', '=', data['id'])]
                    find_asset_id = self.env['sh.asset'].search(domain)
                    if not find_asset_id:
                        count += 1
                        self.env['sh.asset'].create(sh_asset_vals)
                    else:
                        if not self.env['sh.asset'].search([('sh_ebs_barcode', '=', sh_asset_vals.get('sh_ebs_barcode'))]):
                            find_asset_id.write(sh_asset_vals)
                            count += 1
                except Exception as e:
                    failed += 1
                    self.create_fail_log(
                        name=data.get('id'),
                        field_type='hr_employee_basic',
                        error=e,
                        import_json=data,
                    )

            if count > 0:
                vals = {
                    "name": config.name,
                    "state": "success",
                    "field_type": "hr_employee_basic",
                    "error": "%s Assets Imported Successfully" % (count),
                    "datetime": datetime.now(),
                    "base_config_id": config.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)

            if failed > 0:
                vals = {
                    "name": config.name,
                    "state": "error",
                    "field_type": "hr_employee_basic",
                    "error": "%s Assets Failed To Imported." % (failed),
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

    def prepare_sh_asset_vals(self, data):

        sh_asset_vals = {
            'remote_sh_asset_id': data['id'],
            'name': data['name'],
            'display_name': data['display_name'],
            'allocated': data['allocated'],
            'amount': data['amount'],
            'bill_number': data['bill_number'],
            'is_child': data['is_child'],
            'is_parent': data['is_parent'],
            'sh_ebs_barcode': data['sh_ebs_barcode'],
            'sh_ebs_barcode_img': data['sh_ebs_barcode_img'],
            'warranty_month': data['warranty_month'],
            # selection
            'state': data['state']['sh_api_current_state'],
        }

        self.date_vals(data, sh_asset_vals, data_key='warranty_date')
        self.date_vals(data, sh_asset_vals, data_key='warranty_expiry_date')

        # ======== Get vendor_id =========

        if data.get('vendor_id'):
            domain = [('remote_res_partner_id', '=', data['vendor_id'])]
            find_customer = self.env['res.partner'].search(domain)
            if find_customer:
                sh_asset_vals['vendor_id'] = find_customer.id

        # ======== Get parent =========

        # if data.get('parent'):
        #     domain = [('remote_sh_asset_id', '=', data['parent']['id'])]
        #     find_asset = self.env['sh.asset'].search(domain)
        #     if find_asset:
        #         sh_asset_vals['parent'] = find_asset.id
        #     else:
        #         prepare_sh_asset_vals = self.prepare_sh_asset_vals(
        #             data['parent'])
        #         create_asset = self.env['sh.asset'].create(
        #             prepare_sh_asset_vals)
        #         if create_asset:
        #             sh_asset_vals['parent'] = create_asset.id

        # ======== Get asset_category_id =========

        if data.get('asset_category_id'):
            domain = [('remote_sh_asset_type_id', '=',
                       data['asset_category_id']['id'])]
            find_assets_cat = self.env['sh.asset.type'].search(domain)
            if find_assets_cat:
                sh_asset_vals['asset_category_id'] = find_assets_cat.id
            else:
                asset_type_vals = {
                    'remote_sh_asset_type_id': data['asset_category_id'].get('id'),
                    'name': data['asset_category_id'].get('name'),
                    'display_name': data['asset_category_id'].get('display_name'),
                }
                asset_category_id = self.env['sh.asset.type'].create(
                    asset_type_vals)
                if asset_category_id:
                    sh_asset_vals['asset_category_id'] = asset_category_id.id

        return sh_asset_vals
