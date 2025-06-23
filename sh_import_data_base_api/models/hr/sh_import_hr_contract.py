# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
import requests
import json
from datetime import datetime
from datetime import date


class InheritImportHrContract(models.Model):
    _inherit = "sh.import.base"

    is_import_hr = fields.Boolean("Import HR")
    records_per_page_hr = fields.Integer(
        "No of records per page(HR)", default=1)
    current_import_page_hr = fields.Integer("Current HR Page", default=0)
    is_imported_basic_hr = fields.Boolean(default=True)

    def sh_import_hr_basic(self):
        self.import_basic_contract_cron()

        self.import_hr_payroll_structure()
        self.import_hr_expense_cron()
        self.import_hr_applicant()



    def import_hr_contract_cron(self):
        ''' ========== Connect db for import Contract  ==================  '''

        confid = self.env['sh.import.base'].search([], limit=1)
        if confid.is_imported_basic_hr:
            
            confid.is_imported_basic_hr = False

        if confid.is_import_hr:
            confid.current_import_page_hr += 1
            response = requests.get('''%s/api/public/hr.contract?query={%s}&page_size=%s&page=%s''' % (
                confid.base_url, self.query_dict['hr_contract'], confid.records_per_page_hr, confid.current_import_page_hr))
            
            # response = requests.get('''%s/api/public/hr.contract?query={id,name,employee_id,sh_annexure_b_notes,sh_contract_bond_detail_report,signature_date}&page_size=%s&page=%s''' % (
            #     confid.base_url, confid.records_per_page_hr, confid.current_import_page_hr))
            
            response_json = response.json()
            if response.status_code == 200:

                if 'count' in response_json and confid.records_per_page_hr != response_json['count']:
                    confid.is_import_hr = False
                    confid.current_import_page_hr = 0
                    confid.is_imported_basic_hr = True

                count = 0
                failed = 0
                for data in response_json['result']:
                    if not data.get('id')==29:
                        
                        contract_vals = confid.prepare_hr_contract_vals(data)
                        domain = [('remote_hr_contract_id', '=', data['id']),'|',('active','=',True),('active','=',False)]
                        find_contract = self.env['hr.contract'].search(domain)
                        # try:
                        if find_contract:
                            count += 1
                            find_contract.write(contract_vals)
                        else:
                            count += 1
                            self.env['hr.contract'].create(contract_vals)
                    # except Exception as e:
                    #     failed += 1
                    #     self.create_fail_log(
                    #         name=data.get('id'),
                    #         field_type='hr_contract',
                    #         error=e,
                    #         import_json=data,
                    #     )

                if count > 0:
                    self.create_log(
                        field_type='hr_contract', error="%s Contract Imported Successfully" % (count), state='success')
                if failed > 0:
                    self.create_log(
                        field_type='hr_contract', error="%s Contract Failed To Import" % (failed))
            else:
                self.create_log(
                    field_type='hr_contract', error=response.text)

    def prepare_hr_contract_vals(self, data):
        ''' ============== Import Contracts ==============  '''
        state=data.get('state')['sh_api_current_state']

        if data.get('state')['sh_api_current_state']=='pending':
            state='close'   

        hr_contract_vals = {
            'remote_hr_contract_id': data.get('id'),
            'name': data.get('name'),
            'display_name': data.get('display_name'),
            'wage': data.get('wage'),
            'visa_no': data.get('visa_no'),
            'permit_no': data.get('permit_no'),
            'notes': data.get('notes'),
            'period': data.get('period'),
            'cheque_amount': data.get('cheque_amount'),
            'cheque_number': data.get('cheque_number'),
            'contract_period': data.get('contract_period'),
            'days_extend': data.get('days_extend'),
            'digital_signature': data.get('digital_signature'),
            'leave_payment_done': data.get('leave_payment_done'),
            'sh_annexure_b_notes':data.get('sh_annexure_b_notes'),

            # selection
            'state':state ,
            'bond': data.get('bond')['sh_api_current_state'],
            'bond_duration': data.get('bond_duration')['sh_api_current_state'],
            'contract_type': data.get('contract_type')['sh_api_current_state'],
            'sh_contract_bond_detail_report':data.get('sh_contract_bond_detail_report')
        }

        if data.get('date'):
            date_time=datetime.strptime(data.get('date'),'%Y-%m-%d')
            date_time=date_time.strftime('%Y-%m-%d')
            hr_contract_vals['date'] = date_time
        if data.get('date_start'):
            date_time=datetime.strptime(data.get('date_start'),'%Y-%m-%d')
            date_time=date_time.strftime('%Y-%m-%d')
            hr_contract_vals['date_start'] = date_time
        if data.get('date_end'):
            date_time=datetime.strptime(data.get('date_end'),'%Y-%m-%d')
            date_time=date_time.strftime('%Y-%m-%d')
            hr_contract_vals['date_end'] = date_time

        if data.get('signature_date'):
            date_time=datetime.strptime(data.get('signature_date'),'%Y-%m-%d')
            date_time=date_time.strftime('%Y-%m-%d')
            hr_contract_vals['signature_date'] = date_time
        
        if data.get('trial_date_end'):
            date_time=datetime.strptime(data.get('trial_date_end'),'%Y-%m-%d')
            date_time=date_time.strftime('%Y-%m-%d')
            hr_contract_vals['trial_date_end'] = date_time

        # ======== Get Employe if already created or create =========

        if data.get('employee_id'):
            domain = [('remote_hr_employee_id', '=', data.get('employee_id'))]
            find_employee = self.env['hr.employee'].search(domain)
            if find_employee:
                hr_contract_vals['employee_id'] = find_employee.id
            else:
                print("\n\n\n\n else contract====>",find_employee)
        else:
            print("\n\n\n\n else contract 22222222222====>")

        # ======== Get Department if already created or create =========

        if data.get('department_id'):
            domain = [('remote_hr_department_id', '=', data.get('department_id'))]
            find_department = self.env['hr.department'].search(domain)
            if find_department:
                hr_contract_vals['department_id'] = find_department.id

        # ======== Get job if already created or create =========

        if data.get('job_id'):
            domain = [('remote_hr_job_id', '=', data.get('job_id'))]
            find_job_id = self.env['hr.job'].search(domain)
            if find_job_id:
                hr_contract_vals['job_id'] = find_job_id.id

        # ======== Get resource calender if already created or create =========

        if data.get('resource_calendar_id') and data.get('resource_calendar_id') != 0:
            domain = [('remote_resource_calendar_id', '=',
                       data.get('resource_calendar_id'))]
            find_resource_calendar = self.env['resource.calendar'].search(
                domain)
            if find_resource_calendar:
                hr_contract_vals['resource_calendar_id'] = find_resource_calendar.id

        # if data.get('resource_calendar_id') and data.get('resource_calendar_id')['id'] and data['resource_calendar_id']['id']!=0:
        #     domain = [('remote_resource_calendar_id', '=', data.get('resource_calendar_id')['id'])]
        #     find_resource_calendar = self.env['resource.calendar'].search(domain)
        #     if find_resource_calendar:
        #         hr_contract_vals['resource_calendar_id']=find_resource_calendar.id
        #     else:
        #         resource_calendar_vals = self.process_resource_calendar_data(data.get('resource_calendar_id'))
        #         create_calendar_id=self.env['resource.calendar'].create(resource_calendar_vals)
        #         hr_contract_vals['resource_calendar_id']=create_calendar_id.id

        # ======== Get contract type calender if already created or create =========

        if data.get('type_id'):
            domain = [('remote_hr_contract_type_id', '=', data.get('type_id'))]
            find_contract_type_id = self.env['hr.contract.type'].search(domain)
            if find_contract_type_id:
                hr_contract_vals['contract_type_id'] = find_contract_type_id.id

        # ======== Get Degree if already created or create =========

        if data.get('degree_ids'):
            degree_ids_list = []
            for degree_id in data.get('degree_ids'):
                domain = [('remote_sh_degree_id', '=', degree_id)]
                find_degree = self.env['sh.degree'].search(domain)
                if find_degree:
                    degree_ids_list.append((4, find_degree.id))
            if degree_ids_list:
                hr_contract_vals['degree_ids'] = degree_ids_list

        # ======== Get Struct id if already created or create =========

        if data.get('struct_id') and data.get('struct_id') != 0:
            domain = [('remote_hr_payroll_structure_id',
                       '=', data['struct_id'])]
            find_struct_id = self.env['hr.payroll.structure'].search(domain)
            if find_struct_id:
                hr_contract_vals['struct_id'] = find_struct_id.id

        # ======== Get journal_id if already created or create =========

        if data.get('journal_id'):
            domain = [('type', '=', data['journal_id']['type']['sh_api_current_state']),
                      ('code', '=', data['journal_id']['code'])]
            find_journal = self.env['account.journal'].search(domain, limit=1)
            if find_journal:
                hr_contract_vals['journal_id'] = find_journal.id

        if data.get('allocation_id'):
            domain = [('remote_allocation_id', '=', data.get('allocation_id').get('id'))]
            find_allocation = self.env['hr.leave.allocation'].search(
                domain)
            allocation_vals = self.prepare_allocation_vals(data.get('allocation_id'))
            if allocation_vals:
                if find_allocation:
                    find_allocation.write(allocation_vals)
                    hr_contract_vals['allocation_id'] = find_allocation.id
                else:
                    find_allocation=self.env['hr.leave.allocation'].create(allocation_vals)
                    if find_allocation:
                        hr_contract_vals['allocation_id'] = find_allocation.id    

        # ======== Get sh_contract_goal_ids if already created or create =========

        if data.get('sh_contract_goal_ids'):
            goals_ids_list = []
            for goal in data.get('sh_contract_goal_ids'):
                domain = [('remote_hr_contract_goals_id', '=', goal['id'])]
                find_goal = self.env['hr.contract.goals'].search(domain)
                if find_goal:
                    goals_ids_list.append((4, find_goal.id))
                else:
                    goal_vals = {
                        'remote_hr_contract_goals_id': goal.get('id'),
                        'name': goal.get('name'),
                        'display_name': goal.get('display_name'),
                        'sequence': goal.get('sequence'),
                    }
                    goal_id = self.env['hr.contract.goals'].create(goal_vals)
                    if goal_id:
                        goals_ids_list.append((4, goal_id.id))
            if goals_ids_list:
                hr_contract_vals['sh_contract_goal_ids'] = goals_ids_list

        # ======== Get sh_contract_improvement_ids if already created or create =========

        if data.get('sh_contract_improvement_ids'):
            improvement_ids_list = []
            for improvement in data.get('sh_contract_improvement_ids'):
                domain = [('remote_hr_contract_improvement_id',
                           '=', improvement['id'])]
                find_improvement = self.env['hr.contract.improvement'].search(
                    domain)
                if find_improvement:
                    improvement_ids_list.append((4, find_improvement.id))
                else:
                    improvement_vals = {
                        'remote_hr_contract_improvement_id': improvement.get('id'),
                        'name': improvement.get('name'),
                        'display_name': improvement.get('display_name'),
                        'sequence': improvement.get('sequence'),
                    }
                    improve_id = self.env['hr.contract.improvement'].create(
                        improvement_vals)
                    if improve_id:
                        improvement_ids_list.append((4, improve_id.id))
            if improvement_ids_list:
                hr_contract_vals['sh_contract_improvement_ids'] = improvement_ids_list

        return hr_contract_vals
