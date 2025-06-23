# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
import requests
import json
from datetime import datetime


class InheritImportHrRuleImport(models.Model):
    _inherit = "sh.import.base"
    json_field = fields.Text('JOSN Data')

    def import_hr_payslip_run(self):
        ''' ========== Connect db for import payslip run  ==================  '''
        config = self.env['sh.import.base'].search([], limit=1)

        response = requests.get('''%s/api/public/hr.payslip.run?query={%s}''' % (
            config.base_url, self.query_dict['hr_payslip_run']))
        response_json = response.json()
        self.json_field = response_json

        if response.status_code == 200:
            count = 0
            for data in response_json['result']:
                payslip_run_vals = config.prepare_hr_payslip_run_vals(data)
                domain = [('remote_hr_payslip_run_id', '=', data['id'])]
                find_payslip_run = self.env['hr.payslip.run'].search(domain)
                # try:
                if find_payslip_run:
                    count += 1
                    find_payslip_run.write(payslip_run_vals)
                else:
                    count += 1
                    create_payslip_run = self.env['hr.payslip.run'].create(
                        payslip_run_vals)

            if count > 0:
                vals = {
                    "name": config.name,
                    "state": "success",
                    "field_type": "hr_payslip_run",
                    "error": "%s Hr Payslip Run Imported Successfully" % (count),
                    "datetime": datetime.now(),
                    "base_config_id": config.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)

        else:
            vals = {
                "name": config.name,
                "state": "error",
                "field_type": "hr_payslip_run",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": config.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals)

    def prepare_hr_payslip_run_vals(self, data):

        hr_payslip_run_vals = {
            'remote_hr_payslip_run_id': data['id'],
            'name': data['name'],
            'display_name': data['display_name'],
            'bank_format': data['bank_format'],
            'bank_ref': data['bank_ref'],
            'credit_note': data['credit_note'],
            'sh_payslip_count': data['sh_payslip_count'],
            'trancation_date': data['trancation_date'],

            # ---selection----
            'state': data['state']['sh_api_current_state'],
        }

        if data.get('date_start') != '':
            hr_payslip_run_vals['date_start'] = data.get('date_start')
        if data.get('date_end') != '':
            hr_payslip_run_vals['date_end'] = data.get('date_end')

        # ============== Manage Journal ==========

        if data.get('journal_id'):
            domain = [('type', '=', data['journal_id']['type']['sh_api_current_state']),
                      ('code', '=', data['journal_id']['code'])]
            find_journal = self.env['account.journal'].search(domain, limit=1)
            if find_journal:
                hr_payslip_run_vals['journal_id'] = find_journal.id

        # # ======== Get slip_ids if already created or create =========

        # if data.get('slip_ids'):
        #     slip_ids_list=[]
        #     for payslip_line in data['slip_ids']:
        #         domain = [('remote_hr_payslip_id', '=', payslip_line['id'])]
        #         find_payslip_line = self.env['hr.payslip'].search(domain)
        #         if not find_payslip_line:
        #             psyslip_line_vals = self.prepare_hr_payslip_vals(payslip_line)
        #             slip_ids_list.append((0,0,psyslip_line_vals))
        #     hr_payslip_run_vals['slip_ids'] = slip_ids_list

        if data.get('slip_ids'):
            slip_ids_list = []
            for payslip_line_id in data['slip_ids']:
                domain = [('remote_hr_payslip_id', '=', payslip_line_id)]
                find_payslip_line = self.env['hr.payslip'].search(domain)
                if find_payslip_line:
                    slip_ids_list.append((4, find_payslip_line.id))
            if slip_ids_list:
                hr_payslip_run_vals['slip_ids'] = slip_ids_list

        # # ======== Get default_payment if already created or create =========

        if data.get('default_payment'):
            default_payment_ids = []
            for payment in data.get('default_payment'):
                domain = [('remote_sh_default_payment_id', '=', payment['id'])]
                find_payment = self.env['sh.default.payment'].search(domain)
                if find_payment:
                    default_payment_ids.append((4, find_payment.id))
                else:
                    default_payment_vals = {
                        'remote_sh_default_payment_id': payment['id'],
                        'name': payment['name'],
                        'display_name': payment['display_name'],
                        'default_formate': payment['default_formate'],
                        'total_amount': payment['total_amount'],
                    }
                    defaukt_payment_id = self.env['sh.default.payment'].create(
                        default_payment_vals)
                    if defaukt_payment_id:
                        default_payment_ids.append((4, defaukt_payment_id.id))
            if default_payment_ids:
                hr_payslip_run_vals['default_payment'] = default_payment_ids

        return hr_payslip_run_vals
