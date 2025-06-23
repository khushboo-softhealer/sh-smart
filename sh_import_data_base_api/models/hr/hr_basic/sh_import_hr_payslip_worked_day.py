# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
import requests
import json
from datetime import datetime

class InheritImportHrRuleImport(models.Model):
    _inherit = "sh.import.base"

    json_field = fields.Text('JOSN Data')

    def import_hr_payslip_work_day(self):   
        ''' ========== Connect db for import payslip run  ==================  '''
        config = self.env['sh.import.base'].search([],limit=1)
    

        response = requests.get('''%s/api/public/hr.payslip.worked_days?query={%s}''' %(config.base_url, self.query_dict['hr_payslip_work_day']))
        response_json = response.json()
        self.json_field = response_json
        if response.status_code==200:
            count = 0
            for data in response_json['result']:
                payslip_work_day_vals = config.prepare_hr_payslip_worked_day_vals(data)
                domain = [('remote_hr_payslip_worked_days_id', '=', data['id'])]
                find_payslip_work_days = self.env['hr.payslip.worked_days'].search(domain)
                # try:
                if find_payslip_work_days:
                    count += 1
                    find_payslip_work_days.write(payslip_work_day_vals)                            
                else:
                    count += 1
                    create_payslip_run=self.env['hr.payslip.worked_days'].create(payslip_work_day_vals)
            
            if count > 0:              
                vals = {
                    "name": config.name,
                    "state": "success",
                    "field_type": "hr_payslip_work_days",
                    "error": "%s Hr Payslip Work Days Imported Successfully" %(count),
                    "datetime": datetime.now(),
                    "base_config_id": config.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)

        else:
            vals = {
                "name": config.name,
                "state": "error",
                "field_type": "hr_payslip_work_days",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": config.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals) 


    def prepare_hr_payslip_worked_day_vals(self,data):

        hr_payslip_work_day_vals={
            'remote_hr_payslip_worked_days_id' : data['id'],
            'name':data['name'],
            'display_name':data['display_name'],
            'code':data['code'],
            'number_of_hours':data['number_of_hours'],
            'number_of_days':data['number_of_days'],
            'sequence':data['sequence'],
        }

        # ======== Get payslip_id if already created or create =========

        if data.get('payslip_id') and data.get('payslip_id')!=0:
            domain = [('remote_hr_payslip_id', '=', data['payslip_id'])]
            find_payslip = self.env['hr.payslip'].search(domain)
            if find_payslip:
                hr_payslip_work_day_vals['payslip_id'] = find_payslip.id

        # if data.get('payslip_id') and data['payslip_id']['id'] and data['payslip_id']['id']!=0:
        #     domain = [('remote_hr_payslip_id', '=', data['payslip_id']['id'])]
        #     find_payslip = self.env['hr.payslip'].search(domain)
        #     if find_payslip:
        #         hr_payslip_work_day_vals['payslip_id'] = find_payslip.id
        #     else:
        #         payslip_vals=self.prepare_hr_payslip_vals(data['payslip_id'])
        #         payslip_id=self.env['hr.payslip'].create(payslip_vals)
        #         if payslip_id:
        #             hr_payslip_work_day_vals['payslip_id']=payslip_id.id


        # # ======== Get contract_id if already created or create =========

        if data.get('contract_id') and data['contract_id']['id'] and data['contract_id']['id']!=0:
            domain = [('remote_hr_contract_id', '=', data['contract_id']['id'])]
            find_contract = self.env['hr.contract'].search(domain)
            if find_contract:
                hr_payslip_work_day_vals['contract_id'] = find_contract.id
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
                    hr_payslip_work_day_vals['contract_id']=contract_id.id 

        return  hr_payslip_work_day_vals
