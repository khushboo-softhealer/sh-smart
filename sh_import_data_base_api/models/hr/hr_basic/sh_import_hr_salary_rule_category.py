# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
import requests
import json
from datetime import datetime


class InheritImportHrPayrollStructure(models.Model):
    _inherit = "sh.import.base"

    def import_hr_salary_rule_category(self):
        ''' ========== Import Hr Salary Rule Category (hr.salary.rule.category)  ==================  '''

        response = requests.get('%s/api/public/hr.salary.rule.category?query={%s}' % (
            self.base_url, self.query_dict.get('hr_salary_rule_category')))
        response_json = response.json()

        if response.status_code == 200 and response_json.get('error') == '0':
            count = 0

            try:
                for result in response_json['result']:
                    if not result.get('id') or result.get('name') == '':
                        continue
                    domain = ['|', ('remote_hr_salary_rule_category_id', '=', result.get('id')),
                              ('name', '=', result.get('name'))]
                    find_rec = self.env['hr.salary.rule.category'].search(
                        domain)
                    vals = self.process_hr_salary_rule_category(result)
                    if find_rec:
                        find_rec.write(vals)
                    else:
                        self.env['hr.salary.rule.category'].create(vals)
                    count += 1
            except Exception as e:
                self.create_hr_basic_log(error=e)

            if count > 0:
                self.create_hr_basic_log(
                    error="%s 'Salary Rule Category' Imported Successfully" % (count), state='success')
        else:
            self.create_hr_basic_log(error=response.text)

    def process_hr_salary_rule_category(self, data):

        hr_salary_rule_category_vals = {
            'remote_hr_salary_rule_category_id': data.get('id'),
            'company_id': 1,
            'name': data.get('name'),
            'display_name': data.get('display_name'),
            'code': data.get('code'),
            'note': data.get('note'),
        }

        # ======== Get child ids if already created or create =========
        if data.get('children_ids'):
            child_list = []
            for child in data.get('children_ids'):
                domain = [
                    ('remote_hr_salary_rule_category_id', '=', child['id'])]
                find_child = self.env['hr.salary.rule.category'].search(domain)
                if find_child:
                    child_list.append((4, find_child.id))
                else:
                    child_vals = self.process_hr_salary_rule_category(child)
                    child_list.append((0, 0, child_vals))
            hr_salary_rule_category_vals['children_ids'] = child_list

        return hr_salary_rule_category_vals
