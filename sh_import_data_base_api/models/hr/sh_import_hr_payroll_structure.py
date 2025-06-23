# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
import requests
import json
from datetime import datetime

class InheritImportHrPayrollStructure(models.Model):
    _inherit = "sh.import.base"

    def import_hr_payroll_structure(self):   
        ''' ========== Connect db for import Pyyroll  ==================  '''
        confid = self.env['sh.import.base'].search([],limit=1)
        

        response = requests.get('''%s/api/public/hr.payroll.structure?query={%s}''' %(confid.base_url, self.query_dict['hr_payroll_structure']))
        response_json = response.json()

        if response.status_code==200:
            count = 0
            failed = 0
            for data in response_json['result']:
                try:
                    payroll_structure_vals = confid.prepare_hr_payroll_structure_vals(data)
                    domain = [('remote_hr_payroll_structure_id', '=', data['id'])]
                    find_payroll_structure = self.env['hr.payroll.structure'].search(domain)
                    if find_payroll_structure:
                        count += 1
                        find_payroll_structure.write(payroll_structure_vals)                            
                    else:
                        count += 1
                        self.env['hr.payroll.structure'].create(payroll_structure_vals)
                except Exception as e:
                    failed += 1
                    self.create_fail_log(
                        name=data.get('id'),
                        field_type='hr_payroll_structure',
                        error=e,
                        import_json=data,
                    )

            
            if count > 0:              
                vals = {
                    "name": confid.name,
                    "state": "success",
                    "field_type": "hr_payroll_structure",
                    "error": "%s Hr Payroll Structure Imported Successfully" %(count),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)
            if failed > 0:
                self.create_log(field_type='hr_payroll_structure', error="%s Hr Payroll Structure Failed To Import" % (failed))

        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "hr_payroll_structure",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals) 


    def prepare_hr_payroll_structure_vals(self,data):

        hr_payroll_structure_vals={
            'remote_hr_payroll_structure_id' : data['id'],
            'name':data['name'],
            'display_name':data['display_name'],
            'note':data['note'],
            'code':data['code'],
        }

        # ======== Get child ids if already created or create =========

        if data.get('child_ids'):
            child_list = []
            for child in data['child_ids']:
                domain = [('remote_hr_payroll_structure_id', '=', child['id'])]
                find_child = self.env['hr.payroll.structure'].search(domain)
                if not find_child:
                    child_vals = self.prepare_hr_payroll_structure_vals(child)
                    child_list.append((0,0,child_vals))
            hr_payroll_structure_vals['child_ids'] = child_list


        # ======== Get Rules Ids if already created or create =========

        # if data.get('rule_ids'):
        #     rules_ids_list=[]
        #     for rule in data.get('rule_ids'):
        #         domain = [('remote_hr_salary_rule_id', '=', rule['id'])]
        #         find_customer = self.env['hr.salary.rule'].search(domain)
        #         if find_customer:
        #             rules_ids_list.append((4,find_customer.id))
        #         else:
        #             rules_vals=self.process_contact_data(rule)
        #             rule_id=self.env['hr.salary.rule'].create(rules_vals)
        #             if rule_id:
        #                 rules_ids_list.append((4,rule_id.id))  
        #     if rules_ids_list:
        #         hr_payroll_structure_vals['rule_ids']=rules_ids_list  

        if data.get('rule_ids'):
            rules_ids_list=[]
            for rule_id in data.get('rule_ids'):
                domain = [('remote_hr_salary_rule_id', '=', rule_id)]
                find_salary_rule = self.env['hr.salary.rule'].search(domain)
                if find_salary_rule:
                    rules_ids_list.append((4,find_salary_rule.id))
            if rules_ids_list:
                hr_payroll_structure_vals['rule_ids']=rules_ids_list  

        return hr_payroll_structure_vals
