# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
import requests
import json
from datetime import datetime


class InheritImportHrRuleImport(models.Model):
    _inherit = "sh.import.base"

    # hr.rule.input

    def import_hr_rule_input(self):
        ''' ========== Import Hr Rule Input (hr.rule.input)  ==================  '''

        response = requests.get(
            '%s/api/public/hr.rule.input?query={%s}' % (self.base_url, self.query_dict.get('hr_rule_input')))
        response_json = response.json()

        if response.status_code == 200 and response_json.get('error') == '0':
            count = 0

            try:
                for result in response_json['result']:
                    if not result.get('id') or result.get('name') == '':
                        continue
                    domain = ['|', ('remote_hr_rule_input_id', '=', result.get('id')),
                              ('name', '=', result.get('name'))]
                    find_rec = self.env['hr.rule.input'].search(domain)
                    vals = self.process_hr_rule_input(result)
                    if find_rec:
                        find_rec.write(vals)
                    else:
                        self.env['hr.rule.input'].create(vals)
                    count += 1
            except Exception as e:
                self.create_hr_basic_log(error=e)

            if count > 0:
                self.create_hr_basic_log(
                    error="%s 'Rule Input' Imported Successfully" % (count), state='success')
        else:
            self.create_hr_basic_log(error=response.text)

    def process_hr_rule_input(self, data):

        hr_rule_input_vals = {
            'remote_hr_rule_input_id': data['id'],
            'name': data['name'],
            'display_name': data['display_name'],
            'code': data['code'],
        }

        # import input_id if already exist then return

        if data.get('input_id'):
            if data['input_id'].get('id') and data['input_id'].get('id') != 0:
                domain = [('remote_hr_salary_rule_id', '=',
                           data['input_id'].get('id'))]
                find_input_id = self.env['hr.salary.rule'].search(domain)
                if find_input_id:
                    hr_rule_input_vals['input_id'] = find_input_id.id
                else:
                    # just required fields
                    salary_rule_vals = {
                        'remote_hr_salary_rule_id': data['input_id'].get('id'),
                        'name': data['input_id'].get('name'),
                        'code': data['input_id'].get('code'),
                        'condition_python': data['input_id'].get('condition_python'),
                        'condition_select': data['input_id'].get('condition_select')['sh_api_current_state'],
                        'amount_select': data['input_id'].get('amount_select')['sh_api_current_state'],
                    }
                    if data['input_id'].get('category_id'):
                        domain = [('remote_hr_salary_rule_category_id', '=',
                                   data['input_id'].get('category_id'))]
                        find_categ = self.env['hr.salary.rule.category'].search(
                            domain)
                        if find_categ:
                            salary_rule_vals['category_id'] = find_categ.id
                    create_input_id = self.env['hr.salary.rule'].create(
                        salary_rule_vals)
                    if create_input_id:
                        hr_rule_input_vals['input_id'] = create_input_id.id

        return hr_rule_input_vals

        # if data.get('input_id') and data['input_id']['id'] and data['input_id']['id'] != 0:
        #     domain = [('remote_hr_salary_rule_id',
        #                '=', data['input_id']['id'])]
        #     find_input_id = self.env['hr.salary.rule'].search(domain)
        #     if find_input_id:
        #         hr_rule_input_vals['input_id'] = find_input_id.id
        #     else:
        #         salary_rule_vals = self.prepare_hr_salary_rule_vals(
        #             data['input_id'])
        #         find_input_id = self.env['hr.salary.rule'].create(
        #             salary_rule_vals)
        #         if find_input_id:
        #             hr_rule_input_vals['input_id'] = find_input_id.id

        # return hr_rule_input_vals
