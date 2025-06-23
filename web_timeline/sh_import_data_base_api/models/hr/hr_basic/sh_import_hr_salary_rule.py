# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
import requests
import json
from datetime import datetime


class InheritImportHrPayrollStructure(models.Model):
    _inherit = "sh.import.base"

    # hr.salary.rule

    def import_hr_salary_rule(self):
        ''' ========== Import Salary Rule (hr.salary.rule)  ==================  '''

        response = requests.get('%s/api/public/hr.salary.rule?query={%s}' % (
            self.base_url, self.query_dict.get('hr_salary_rule')))
        response_json = response.json()

        if response.status_code == 200 and response_json.get('error') == '0':
            count = 0

            try:
                for result in response_json['result']:
                    if not result.get('id') or result.get('name') == '':
                        continue
                    domain = ['|', ('remote_hr_salary_rule_id', '=', result.get('id')),
                              ('name', '=', result.get('name'))]
                    find_rec = self.env['hr.salary.rule'].search(domain)
                    vals = self.prepare_hr_salary_rule_vals(result)
                    if find_rec:
                        find_rec.write(vals)
                    else:
                        self.env['hr.salary.rule'].create(vals)
                    count += 1
            except Exception as e:
                self.create_hr_basic_log(error=e)

            if count > 0:
                self.create_hr_basic_log(
                    error="%s 'Salary Rule' Imported Successfully" % (count), state='success')
        else:
            self.create_hr_basic_log(error=response.text)

    def prepare_hr_salary_rule_vals(self, data):

        hr_salary_rule_vals = {
            'remote_hr_salary_rule_id': data['id'],
            'name': data['name'],
            'company_id': 1,
            'display_name': data['display_name'],
            'sequence': data['sequence'],
            'amount_fix': data['amount_fix'],
            'amount_percentage': data['amount_percentage'],
            'amount_percentage_base': data['amount_percentage_base'],
            'amount_python_compute': data['amount_python_compute'],
            'amount_select': data['amount_select']['sh_api_current_state'],
            'code': data.get('code'),
            'quantity': data.get('quantity'),
            'active': data.get('active'),
            'appears_on_payslip': data.get('appears_on_payslip'),
            'condition_range': data.get('condition_range'),
            'condition_python': data.get('condition_python'),
            'condition_range_min': data.get('condition_range_min'),
            'condition_range_max': data.get('condition_range_max'),
            'note': data.get('note'),
            'condition_select': data.get('condition_select')['sh_api_current_state'],
        }

        # account_tax_id (account.tax)
        # analytic_account_id (account.analytic.account)
        # register_id (hr.contribution.register)

        # ======== Get child ids if already created or create =========

        if data.get('child_ids'):
            child_list = []
            for child in data['child_ids']:
                domain = [('remote_hr_salary_rule_id', '=', child['id'])]
                find_child = self.env['hr.salary.rule'].search(domain)
                if not find_child:
                    child_vals = self.prepare_hr_salary_rule_vals(child)
                    child_list.append((0, 0, child_vals))
            hr_salary_rule_vals['child_ids'] = child_list

        # # ======== Get account_credit if already created or create =========

        # if data.get('account_credit') and data['account_credit']['id'] and data['account_credit']['id'] != 0:
        #     domain = [('remote_account_account_id', '=',
        #                data['account_credit']['id'])]
        #     find_account_credit = self.env['account.account'].search(domain)
        #     if find_account_credit:
        #         hr_salary_rule_vals['account_credit'] = find_account_credit.id
        #     else:
        #         account_vals = self.process_account_account_data(
        #             data['account_credit'])
        #         account_credit_id = self.env['account.account'].create(
        #             account_vals)
        #         if account_credit_id:
        #             hr_salary_rule_vals['account_credit'] = account_credit_id.id

        # # ======== Get account_debit if already created or create =========

        # if data.get('account_debit') and data['account_debit']['id'] and data['account_debit']['id'] != 0:
        #     domain = [('remote_account_account_id', '=',
        #                data['account_debit']['id'])]
        #     find_account_debit = self.env['account.account'].search(domain)
        #     if find_account_debit:
        #         hr_salary_rule_vals['account_debit'] = find_account_debit.id
        #     else:
        #         account_vals = self.process_account_account_data(
        #             data['account_debit'])
        #         account_debit_id = self.env['account.account'].create(
        #             account_vals)
        #         if account_debit_id:
        #             hr_salary_rule_vals['account_debit'] = account_debit_id.id

        # ======== Get category_id if already created or create =========

        if data.get('category_id') and data.get('category_id') != 0:
            domain = [('remote_hr_salary_rule_category_id',
                       '=', data['category_id'])]
            find_categ = self.env['hr.salary.rule.category'].search(domain)
            if find_categ:
                hr_salary_rule_vals['category_id'] = find_categ.id

        # if data.get('category_id') and data['category_id']['id'] and data['category_id']['id'] != 0:
        #     domain = [('remote_hr_salary_rule_category_id',
        #                '=', data['category_id']['id'])]
        #     find_rule_cat = self.env['hr.salary.rule.category'].search(domain)
        #     if find_rule_cat:
        #         hr_salary_rule_vals['category_id'] = find_rule_cat.id
        #     else:
        #         rules_cat_vals = self.process_hr_salary_rule_category(
        #             data['category_id'])
        #         rule_cat_id = self.env['hr.salary.rule.category'].create(
        #             rules_cat_vals)
        #         if rule_cat_id:
        #             hr_salary_rule_vals['category_id'] = rule_cat_id.id

        # ======== Get Degree if already created or create =========

        if data.get('input_ids'):
            input_ids_list = []
            for input_id in data.get('input_ids'):
                domain = [('remote_hr_rule_input_id', '=', input_id)]
                find_input = self.env['hr.rule.input'].search(domain)
                if find_input:
                    input_ids_list.append((4, find_input.id))
            if input_ids_list:
                hr_salary_rule_vals['input_ids'] = input_ids_list

        # if data.get('input_ids'):
        #     input_ids_list = []
        #     for input in data.get('input_ids'):
        #         domain = [('remote_hr_rule_input_id', '=', input['id'])]
        #         find_input = self.env['hr.rule.input'].search(domain)
        #         if find_input:
        #             input_ids_list.append((4, find_input.id))
        #         else:
        #             input_vals = self.process_hr_rule_input(input)
        #             input_id = self.env['hr.rule.input'].create(input_vals)
        #             if input_id:
        #                 input_ids_list.append((4, input_id.id))
        #     if input_ids_list:
        #         hr_salary_rule_vals['input_ids'] = input_ids_list

        return hr_salary_rule_vals
