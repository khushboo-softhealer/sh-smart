# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
import requests
import json
from datetime import datetime
from datetime import date


class InheritImportHrContract(models.Model):
    _inherit = "sh.import.base"

    def import_hr_payslip(self):
        ''' ========== Connect db for import Payslip  ==================  '''
        confid = self.env['sh.import.base'].search([], limit=1)
        response = requests.get(
            '''%s/api/public/hr.payslip?query={%s}''' % (confid.base_url, self.query_dict['hr_payslip']))
        response_json = response.json()

        if response.status_code == 200:
            count = 0
            for data in response_json['result']:
                payslip_vals = confid.prepare_hr_payslip_vals(data)
                domain = [('remote_hr_payslip_id', '=', data['id'])]
                find_payslip = self.env['hr.payslip'].search(domain)
                # try:
                if find_payslip:
                    count += 1
                    find_payslip.write(payslip_vals)
                else:
                    count += 1
                    create_payslip = self.env['hr.payslip'].create(
                        payslip_vals)

            if count > 0:
                vals = {
                    "name": confid.name,
                    "state": "success",
                    "field_type": "hr_payslip",
                    "error": "%s Hr Payslip Imported Successfully" % (count),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)

        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "hr_payslip",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals)

    def prepare_hr_payslip_vals(self, data):
        ''' ============== Import Payslip ==============  '''
        hr_payslip_vals = {
            'remote_hr_payslip_id': data['id'],
            'name': data['name'],
            'display_name': data['display_name'],
            'note': data['note'],
            'number': data['number'],
            'paid': data['paid'],
            'payslip_count': data['payslip_count'],
            'credit_note': data['credit_note'],

            # -----selection
            'state': data['state']['sh_api_current_state'],
        }

        if data.get('date') != '':
            hr_payslip_vals['date'] = data.get('date')
        if data.get('date_from') != '':
            hr_payslip_vals['date_from'] = data.get('date_from')
        if data.get('date_to') != '':
            hr_payslip_vals['date_to'] = data.get('date_to')

        # ======== Get contract_id if already created or create =========

        if data.get('contract_id') and data['contract_id']['id'] and data['contract_id']['id'] != 0:
            domain = [('remote_hr_contract_id', '=',
                       data['contract_id']['id'])]
            find_contract = self.env['hr.contract'].search(domain)
            if find_contract:
                hr_payslip_vals['contract_id'] = find_contract.id
            else:
                contract_vals = {
                    'remote_hr_contract_id': data['contract_id']['id'],
                    'name': data['contract_id']['name'],
                    'hr_responsible_id': data['contract_id']['activity_user_id'],
                    'wage': data['contract_id']['wage'],
                }
                if data['contract_id'].get('struct_id') and data['contract_id'].get('struct_id') != 0:
                    domain = [('remote_hr_payroll_structure_id', '=',
                               data['contract_id']['struct_id']['id'])]
                    find_struct_id = self.env['hr.payroll.structure'].search(
                        domain)
                    if find_struct_id:
                        contract_vals['struct_id'] = find_struct_id.id
                    else:
                        hr_payroll_structure_vals = {
                            'remote_hr_payroll_structure_id': data['contract_id'].get('struct_id')['id'],
                            'name': data['contract_id'].get('struct_id')['name'],
                            'code': data['contract_id'].get('struct_id')['code'],
                        }
                        hr_payroll_structure_id = self.env['hr.payroll.structure'].create(
                            hr_payroll_structure_vals)
                        if hr_payroll_structure_id:
                            contract_vals['struct_id'] = hr_payroll_structure_id.id

                contract_id = self.env['hr.contract'].create(contract_vals)
                if contract_id:
                    hr_payslip_vals['contract_id'] = contract_id.id

        # ======== Get Employe if already created or create =========

        # if data.get('employee_id') and data['employee_id']['id'] and data['employee_id']['id']!=0:
        #     domain = [('remote_hr_employee_id', '=', data['employee_id']['id'])]
        #     find_employee = self.env['hr.employee'].search(domain)
        #     if find_employee:
        #         hr_payslip_vals['employee_id'] = find_employee.id
        #     else:
        #         employee_vals=self.process_employee_data(data['employee_id'])
        #         employee_id=self.env['hr.employee'].create(employee_vals)
        #         if employee_id:
        #             hr_payslip_vals['employee_id']=employee_id.id

        if data.get('employee_id') and data.get('employee_id') != 0:
            domain = [('remote_hr_employee_id', '=', data['employee_id'])]
            find_employee = self.env['hr.employee'].search(domain)
            if find_employee:
                hr_payslip_vals['employee_id'] = find_employee.id

        # hr_payslip_vals['employee_id'] = 2

        # ============== Manage Journal ==========

        if data.get('journal_id'):
            domain = [('type', '=', data['journal_id']['type']['sh_api_current_state']),
                      ('code', '=', data['journal_id']['code'])]
            find_journal = self.env['account.journal'].search(domain, limit=1)
            if find_journal:
                hr_payslip_vals['journal_id'] = find_journal.id

        # ======== Get details_by_salary_rule_category if already created or create =========

        # if data.get('details_by_salary_rule_category'):
        #     salary_rules_list=[]
        #     for payslip_line in data['details_by_salary_rule_category']:
        #         domain = [('remote_hr_payslip_line_id', '=', payslip_line['id'])]
        #         find_payslip_line = self.env['hr.payslip.line'].search(domain)
        #         if not find_payslip_line:
        #             psyslip_line_vals = self.process_hr_payslip_line(payslip_line)
        #             salary_rules_list.append((0,0,psyslip_line_vals))
        #     hr_payslip_vals['details_by_salary_rule_category'] = salary_rules_list

        if data.get('details_by_salary_rule_category'):
            salary_rules_list = []
            for payslip_line_id in data['details_by_salary_rule_category']:
                domain = [('remote_hr_payslip_line_id', '=', payslip_line_id)]
                find_payslip_line = self.env['hr.payslip.line'].search(domain)
                if find_payslip_line:
                    salary_rules_list.append((4, find_payslip_line.id))
            if salary_rules_list:
                hr_payslip_vals['details_by_salary_rule_category'] = salary_rules_list

        # ======== Get input_line_ids if already created or create =========

        # if data.get('input_line_ids'):
        #     input_ids_list=[]
        #     for payslip_input in data['input_line_ids']:
        #         domain = [('remote_hr_payslip_input_id', '=', payslip_input['id'])]
        #         find_payslip_line = self.env['hr.payslip.input'].search(domain)
        #         if not find_payslip_line:
        #             psyslip_input_vals = self.prepare_hr_payslip_input_vals(payslip_input)
        #             input_ids_list.append((0,0,psyslip_input_vals))
        #     hr_payslip_vals['input_line_ids'] = input_ids_list

        if data.get('input_line_ids'):
            input_ids_list = []
            for payslip_input_id in data['input_line_ids']:
                domain = [('remote_hr_payslip_input_id',
                           '=', payslip_input_id)]
                find_payslip_line = self.env['hr.payslip.input'].search(domain)
                if find_payslip_line:
                    input_ids_list.append((4, find_payslip_line.id))
            hr_payslip_vals['input_line_ids'] = input_ids_list

        # ======== Get line_ids if already created or create =========

        if data.get('line_ids'):
            salary_rules_list = []
            for payslip_line_id in data['line_ids']:
                domain = [('remote_hr_payslip_line_id', '=', payslip_line_id)]
                find_payslip_line = self.env['hr.payslip.line'].search(domain)
                if find_payslip_line:
                    salary_rules_list.append((4, find_payslip_line.id))

            if salary_rules_list:
                hr_payslip_vals['line_ids'] = salary_rules_list

        #  No need to import there is one2many in inverse model
        # ======== Get payslip_run_id if already created or create =========

        # if data.get('payslip_run_id') and data['payslip_run_id']['id'] and data['payslip_run_id']['id']!=0:
        #     domain = [('remote_hr_payslip_run_id', '=', data['payslip_run_id']['id'])]
        #     find_run_id = self.env['hr.payslip.run'].search(domain)
        #     if find_run_id:
        #         hr_payslip_vals['payslip_run_id'] = find_run_id.id
        #     else:
        #         run_id_vals=self.prepare_hr_payslip_run_vals(data['payslip_run_id'])
        #         find_run_id=self.env['hr.payslip.run'].create(run_id_vals)
        #         if find_run_id:
        #             hr_payslip_vals['payslip_run_id']=find_run_id.id

        # ======== Get Struct id if already created or create =========

        if data.get('struct_id') and data.get('struct_id') != 0:
            domain = [('remote_hr_payroll_structure_id',
                       '=', data['struct_id']['id'])]
            find_struct_id = self.env['hr.payroll.structure'].search(domain)
            if find_struct_id:
                hr_payslip_vals['struct_id'] = find_struct_id.id
            else:
                hr_payroll_structure_vals = {
                    'remote_hr_payroll_structure_id': data.get('struct_id')['id'],
                    'name': data.get('struct_id')['name'],
                    'code': data.get('struct_id')['code'],
                }
                hr_payroll_structure_id = self.env['hr.payroll.structure'].create(
                    hr_payroll_structure_vals)
                if hr_payroll_structure_id:
                    hr_payslip_vals['struct_id'] = hr_payroll_structure_id.id

        return hr_payslip_vals
