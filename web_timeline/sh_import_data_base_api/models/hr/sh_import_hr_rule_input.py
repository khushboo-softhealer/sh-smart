# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
import requests
import json
from datetime import datetime

class InheritImportHrRuleImport(models.Model):
    _inherit = "sh.import.base"

    def process_hr_rule_input(self,data):

        hr_rule_input_vals={
            'remote_hr_rule_input_id' : data['id'],
            'name':data['name'],
            'display_name':data['display_name'],
            'code':data['code'],
        }

        # import input_id if already exist then return

        if data.get('input_id') and data['input_id']['id'] and data['input_id']['id']!=0:
            domain = [('remote_hr_salary_rule_id', '=', data['input_id']['id'])]
            find_input_id = self.env['hr.salary.rule'].search(domain)
            if find_input_id:
                hr_rule_input_vals['input_id'] = find_input_id.id
            else:
                salary_rule_vals=self.prepare_hr_salary_rule_vals(data['input_id'])
                find_input_id=self.env['hr.salary.rule'].create(salary_rule_vals)
                if find_input_id:
                    hr_rule_input_vals['input_id']=find_input_id.id

        return  hr_rule_input_vals
