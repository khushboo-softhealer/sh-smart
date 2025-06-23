# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
import requests
import json
from datetime import datetime

class InheritImportHrRuleImport(models.Model):
    _inherit = "sh.import.base"


    def import_hr_payslip_input(self):   
        ''' ========== Connect db for import Payslip Input  ==================  '''
        confid = self.env['sh.import.base'].search([],limit=1)
        response = requests.get('''%s/api/public/hr.payslip.input?query={%s}''' %(confid.base_url,self.query_dict['hr_payslip_input']))
        response_json = response.json()

        if response.status_code==200:
            count = 0
            for data in response_json['result']:
                payslip_input_vals = confid.prepare_hr_payslip_input_vals(data)
                domain = [('remote_hr_payslip_input_id', '=', data['id'])]
                find_payslip_input = self.env['hr.payslip.input'].search(domain)
                # try:
                if find_payslip_input:
                    count += 1
                    find_payslip_input.write(payslip_input_vals)                            
                else:
                    count += 1
                    create_payslip_input=self.env['hr.payslip.input'].create(payslip_input_vals)

            if count > 0:
                vals = {
                    "name": confid.name,
                    "state": "success",
                    "field_type": "hr_payslip_input",
                    "error": "%s Hr Payslip Input Imported Successfully" %(count),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)

        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "hr_payslip_input",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals) 


    def prepare_hr_payslip_input_vals(self,data):

        hr_payslip_input_vals={
            'remote_hr_payslip_input_id' : data['id'],
            'name':data['name'],
            'display_name':data['display_name'],
            'code':data['code'],
            'amount':data['amount'],
            'sequence':data['sequence'],
        }

        # ======== Get payslip_id if already created or create =========

        # if data.get('payslip_id') and data['payslip_id']['id'] and data['payslip_id']['id']!=0:
        #     domain = [('remote_hr_payslip_id', '=', data['payslip_id']['id'])]
        #     find_payslip = self.env['hr.payslip'].search(domain)
        #     if find_payslip:
        #         hr_payslip_input_vals['payslip_id'] = find_payslip.id
        #     else:
        #         payslip_vals=self.prepare_hr_payslip_vals(data['payslip_id'])
        #         payslip_id=self.env['hr.payslip'].create(payslip_vals)
        #         if payslip_id:
        #             hr_payslip_input_vals['payslip_id']=payslip_id.id

        if data.get('payslip_id') and data['payslip_id']['id'] and data['payslip_id']['id']!=0:
            domain = [('remote_hr_payslip_id', '=', data['payslip_id']['id'])]
            find_payslip = self.env['hr.payslip'].search(domain)
            if find_payslip:
                hr_payslip_input_vals['payslip_id'] = find_payslip.id
            else:
                payslip_vals = {
                    'remote_hr_payslip_id': data['payslip_id']['id'],
                    'name': data['name'],
                    'date_from': data['payslip_id']['date_from'],
                    'date_to': data['payslip_id']['date_to'],
                }
                # employee_id
                if data['payslip_id'].get('employee_id') and data['payslip_id'].get('employee_id') !=0:
                    domain = [('remote_hr_employee_id', '=', data['payslip_id']['employee_id'])]
                    find_employee_id = self.env['hr.employee'].search(domain)
                    if find_employee_id:
                        payslip_vals['employee_id'] = find_employee_id.id
                    
                    #  temp_code
                    else:
                        payslip_vals['employee_id'] = 2

                # journal_id
                if data['payslip_id'].get('journal_id') and data['payslip_id'].get('journal_id') !=0:
                    domain = [('remote_account_journal_id', '=', data['payslip_id']['journal_id'])]
                    find_journal_id = self.env['account.journal'].search(domain)
                    if find_journal_id:
                        payslip_vals['journal_id'] = find_journal_id.id
                          
                payslip_id=self.env['hr.payslip'].create(payslip_vals)
                if payslip_id:
                    hr_payslip_input_vals['payslip_id']=payslip_id.id 

        # ======== Get contract_id if already created or create =========

        if data.get('contract_id') and data['contract_id']['id'] and data['contract_id']['id']!=0:
            domain = [('remote_hr_contract_id', '=', data['contract_id']['id'])]
            find_contract = self.env['hr.contract'].search(domain)
            if find_contract:
                hr_payslip_input_vals['contract_id'] = find_contract.id
            else:
                # contract_vals=self.prepare_hr_contract_vals(data['contract_id'])
                contract_vals = {
                    'remote_hr_contract_id': data['contract_id']['id'],
                    'name': data['name'],
                    'hr_responsible_id': data['contract_id']['activity_user_id'],
                    'wage': data['contract_id']['wage'],
                }
                if data['contract_id'].get('struct_id') and data['contract_id'].get('struct_id') !=0:
                    domain = [('remote_hr_payroll_structure_id', '=', data['contract_id']['struct_id']['id'])]
                    find_struct_id = self.env['hr.payroll.structure'].search(domain)
                    if find_struct_id:
                        contract_vals['struct_id'] = find_struct_id.id
                    else:
                        # hr_payroll_structure_vals=self.prepare_hr_payroll_structure_vals(data['struct_id'])
                        hr_payroll_structure_vals = {
                            'remote_hr_payroll_structure_id': data['contract_id'].get('struct_id')['id'],
                            'name': data['contract_id'].get('struct_id')['name'],
                            'code': data['contract_id'].get('struct_id')['code'],
                            }
                        hr_payroll_structure_id=self.env['hr.payroll.structure'].create(hr_payroll_structure_vals)
                        if hr_payroll_structure_id:
                            contract_vals['struct_id']=hr_payroll_structure_id.id                    

                contract_id=self.env['hr.contract'].create(contract_vals)
                if contract_id:
                    hr_payslip_input_vals['contract_id']=contract_id.id 

        return  hr_payslip_input_vals
