# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
import requests
import json
from datetime import datetime

class InheritImportHrPayrollStructure(models.Model):
    _inherit = "sh.import.base"

    def process_hr_salary_rule_category(self,data):

        hr_salary_rule_category_vals={
            'remote_hr_salary_rule_category_id' : data['id'],
            'name':data['name'],
            'display_name':data['display_name'],
            'code':data['code'],
            'note':data['note'],

        }
        # ======== Get child ids if already created or create =========

        if data.get('children_ids'):
            child_list = []
            for child in data['children_ids']:
                domain = [('remote_hr_salary_rule_category_id', '=', child['id'])]
                find_child = self.env['hr.salary.rule.category'].search(domain)
                if not find_child:
                    child_vals = self.import_hr_salary_rule_category(child)
                    child_list.append((0,0,child_vals))
            hr_salary_rule_category_vals['children_ids'] = child_list

        return  hr_salary_rule_category_vals
