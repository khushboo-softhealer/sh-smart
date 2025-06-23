# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
import requests
import json
from datetime import datetime

class InheritImportHrPayrollStructure(models.Model):
    _inherit = "sh.import.base"


    def import_hr_payslip_line(self):   
        ''' ========== Connect db for import Payslip Line  ==================  '''
        confid = self.env['sh.import.base'].search([],limit=1)
        response = requests.get('''%s/api/public/hr.payslip.line?query={%s}''' %(confid.base_url,self.query_dict['hr_payslip_line']))
        # response = requests.get('''%s/api/public/hr.payslip.line?query={*}''' %(confid.base_url))
        response_json = response.json()

        if response.status_code==200:
            count = 0
            for data in response_json['result']:
                payslip_line_vals = confid.prepare_hr_payslip_line_vals(data)
                domain = [('remote_hr_payslip_line_id', '=', data['id'])]
                find_payslip_line = self.env['hr.payslip.line'].search(domain)
                # try:
                if find_payslip_line:
                    count += 1
                    find_payslip_line.write(payslip_line_vals)                            
                else:
                    count += 1
                    create_payslip_line=self.env['hr.payslip.line'].create(payslip_line_vals)

            if count > 0:
                vals = {
                    "name": confid.name,
                    "state": "success",
                    "field_type": "hr_payslip_line",
                    "error": "%s Hr Payslip line Imported Successfully" %(count),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)

        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "hr_payslip_line",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals) 

    def prepare_hr_payslip_line_vals(self,data):

        hr_payslip_line_vals={
            'remote_hr_payslip_line_id' : data['id'],
            'name':data['name'],
            'display_name':data['display_name'],
            'note':data['note'],
            'code':data['code'],
            'quantity':data['quantity'],
            'rate':data['rate'],
            'total':data['total'],
            'sequence':data['sequence'],
            'condition_python':data['condition_python'],
            'condition_range':data['condition_range'],
            'condition_range_max':data['condition_range_max'],
            'condition_range_min':data['condition_range_min'],
            'appears_on_payslip':data['appears_on_payslip'],
            'amount':data['amount'],
            'amount_fix':data['amount_fix'],
            'amount_percentage':data['amount_percentage'],
            'amount_percentage_base':data['amount_percentage_base'],
            'amount_python_compute':data['amount_python_compute'],

            # selection
            'condition_select':data['condition_select']['sh_api_current_state'],
            'amount_select':data['amount_select']['sh_api_current_state'],
        }

        # ======== Get account_credit if already created or create =========

        # if data.get('account_credit') and data['account_credit']['id'] and data['account_credit']['id']!=0:
        #     domain = [('remote_account_account_id', '=', data['account_credit']['id'])]
        #     find_account_credit = self.env['account.account'].search(domain)
        #     if find_account_credit:
        #         hr_payslip_line_vals['account_credit'] = find_account_credit.id
        #     else:
        #         account_vals=self.process_account_account_data(data['account_credit'])
        #         account_credit_id=self.env['account.account'].create(account_vals)
        #         if account_credit_id:
        #             hr_payslip_line_vals['account_credit']=account_credit_id.id 

        # ======== Get account_debit if already created or create =========

        # if data.get('account_debit') and data['account_debit']['id'] and data['account_debit']['id']!=0:
        #     domain = [('remote_account_account_id', '=', data['account_debit']['id'])]
        #     find_account_debit = self.env['account.account'].search(domain)
        #     if find_account_debit:
        #         hr_payslip_line_vals['account_debit'] = find_account_debit.id
        #     else:
        #         account_vals=self.process_account_account_data(data['account_debit'])
        #         account_debit_id=self.env['account.account'].create(account_vals)
        #         if account_debit_id:
        #             hr_payslip_line_vals['account_debit']=account_debit_id.id 

        # ======== Get category_id if already created or create =========

        if data.get('category_id') and data.get('category_id')!=0:
            domain = [('remote_hr_salary_rule_category_id', '=', data['category_id'])]
            find_rule_cat = self.env['hr.salary.rule.category'].search(domain)
            if find_rule_cat:
                hr_payslip_line_vals['category_id'] = find_rule_cat.id


        # ======== Get slip_id if already created or create =========

        # if data.get('slip_id') and data['slip_id']['id'] and data['slip_id']['id']!=0:
        #     domain = [('remote_hr_payslip_id', '=', data['slip_id']['id'])]
        #     find_payslip = self.env['hr.payslip'].search(domain)
        #     if find_payslip:
        #         hr_payslip_line_vals['slip_id'] = find_payslip.id
        #     else:
        #         payslip_vals={
        #             'remote_hr_payslip_id':data['slip_id']['id'],
        #             'employee_id':2,
        #         }

        #         payslip_id=self.env['hr.payslip'].create(payslip_vals)
        #         if payslip_id:
        #             hr_payslip_line_vals['slip_id']=payslip_id.id


        if data.get('slip_id') and data['slip_id']['id'] and data['slip_id']['id']!=0:
            domain = [('remote_hr_payslip_id', '=', data['slip_id']['id'])]
            find_payslip = self.env['hr.payslip'].search(domain)
            if find_payslip:
                hr_payslip_line_vals['slip_id'] = find_payslip.id
            else:
                payslip_vals = {
                    'remote_hr_payslip_id': data['slip_id']['id'],
                    'name': data['name'],
                    'date_from': data['slip_id']['date_from'],
                    'date_to': data['slip_id']['date_to'],
                }
                # employee_id
                if data['slip_id'].get('employee_id') and data['slip_id'].get('employee_id') !=0:
                    domain = [('remote_hr_employee_id', '=', data['slip_id']['employee_id'])]
                    find_employee_id = self.env['hr.employee'].search(domain)
                    if find_employee_id:
                        payslip_vals['employee_id'] = find_employee_id.id
                    
                    #  temp_code
                    else:
                        payslip_vals['employee_id'] = 2


                # journal_id
                if data['slip_id'].get('journal_id') and data['slip_id'].get('journal_id') !=0:
                    domain = [('remote_account_journal_id', '=', data['slip_id']['journal_id'])]
                    find_journal_id = self.env['account.journal'].search(domain)
                    if find_journal_id:
                        payslip_vals['journal_id'] = find_journal_id.id
                          
                payslip_id=self.env['hr.payslip'].create(payslip_vals)
                if payslip_id:
                    hr_payslip_line_vals['slip_id']=payslip_id.id 

        # ======== Get child ids if already created or create =========

        # if data.get('child_ids'):
        #     child_list = []
        #     for child in data['child_ids']:
        #         domain = [('remote_hr_salary_rule_id', '=', child['id'])]
        #         find_child = self.env['hr.salary.rule'].search(domain)
        #         if not find_child:
        #             child_vals = self.prepare_hr_salary_rule_vals(child)
        #             child_list.append((0,0,child_vals))
        #     hr_payslip_line_vals['child_ids'] = child_list

        if data.get('child_ids'):
            child_list = []
            for child in data['child_ids']:
                domain = [('remote_hr_salary_rule_id', '=', child['id'])]
                find_child = self.env['hr.salary.rule'].search(domain)
                if find_child:
                    child_list.append((4,find_child.id))
            hr_payslip_line_vals['child_ids'] = child_list

        # ======== Get contract_id if already created or create =========

        if data.get('contract_id') and data['contract_id']['id'] and data['contract_id']['id']!=0:
            domain = [('remote_hr_contract_id', '=', data['contract_id']['id'])]
            find_contract = self.env['hr.contract'].search(domain)
            if find_contract:
                hr_payslip_line_vals['contract_id'] = find_contract.id
            else:
                # contract_vals=self.prepare_hr_contract_vals(data['contract_id'])
                contract_vals = {
                    'remote_hr_contract_id': data['contract_id']['id'],
                    'name': data['contract_id']['name'],
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
                    hr_payslip_line_vals['contract_id']=contract_id.id 

        # ======== Get Employe if already created or create =========

        if data.get('employee_id') and data.get('employee_id')!=0:
            domain = [('remote_hr_employee_id', '=', data['employee_id'])]
            find_employee = self.env['hr.employee'].search(domain)
            if find_employee:
                hr_payslip_line_vals['employee_id'] = find_employee.id

        # ======== Get input_ids if already created or create =========
    
        # if data.get('input_ids'):
        #     input_ids_list=[]
        #     for input in data.get('input_ids'):
        #         domain = [('remote_hr_rule_input_id', '=', input['id'])]
        #         find_input = self.env['hr.rule.input'].search(domain)
        #         if find_input:
        #             input_ids_list.append((4,find_input.id))
        #         else:
        #             input_vals=self.process_hr_rule_input(input)       
        #             input_id=self.env['hr.rule.input'].create(input_vals)
        #             if input_id:
        #                 input_ids_list.append((4,input_id.id))  
        #     if input_ids_list:
        #         hr_payslip_line_vals['input_ids']=input_ids_list

        if data.get('input_ids'):
            input_ids_list=[]
            for input_id in data.get('input_ids'):
                domain = [('remote_hr_rule_input_id', '=', input_id)]
                find_input = self.env['hr.rule.input'].search(domain)
                if find_input:
                    input_ids_list.append((4,find_input.id))

            if input_ids_list:
                hr_payslip_line_vals['input_ids']=input_ids_list

        # ======== Get salary_rule_id if already created or create =========

        # if data.get('salary_rule_id') and data.get('salary_rule_id')!=0:
        #     domain = [('remote_hr_salary_rule_id', '=', data['salary_rule_id'])]
        #     find_salary_rule_id = self.env['hr.salary.rule'].search(domain)
        #     if find_salary_rule_id:
        #         hr_payslip_line_vals['salary_rule_id'] = find_salary_rule_id.id
        hr_payslip_line_vals['salary_rule_id'] = 2


        # ======== Get register_id if already created or create =========

        # if data.get('register_id') and data.get('register_id')!=0:
        #     domain = [('remote_hr_contribution_register_id', '=', data['register_id'])]
        #     find_contribution_register_id = self.env['hr.contribution.register'].search(domain)
        #     if find_contribution_register_id:
        #         hr_payslip_line_vals['register_id'] = find_contribution_register_id.id
        #     else:
        #         hr_contribution_register_vals=self.prepare_hr_contribution_register_vals(data['register_id'])
        #         find_contribution_register_id=self.env['hr.contribution.register'].create(hr_contribution_register_vals)
        #         if find_contribution_register_id:
        #             hr_payslip_line_vals['register_id']=find_contribution_register_id.id

        return hr_payslip_line_vals
