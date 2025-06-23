# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields
import requests
from datetime import datetime


class InheritImportContractBase(models.Model):
    _inherit = "sh.import.base"

    def import_basic_contract_cron(self):
        ''' ========== Connect db for import contract type basic  ==================  '''
        confid = self.env['sh.import.base'].search([], limit=1)
        response = requests.get(
            '''%s/api/public/hr.contract.type''' % (confid.base_url))
        response_json = response.json()

        if response.status_code == 200:
            # pass

            self.import_hr_salary_rule_category()
            self.import_hr_rule_input()
            self.import_hr_salary_rule()

            self.import_hr_payslip_line()
            self.import_hr_contribution_register()
            self.import_hr_payslip_input()
            self.import_hr_payslip()
            self.import_hr_payslip_work_day()
            self.import_hr_payslip_run()
            self.import_hr_contract_type()
            self.import_sh_degree()
            self.import_hr_job()
            self.import_hr_department()
            self.import_basic_hr_applicant_cron()
            # self.import_basic_hr_leave_cron()

        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "contract_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals)

    def import_hr_contract_type(self):
        ''' ========== Import Contract Type (hr.contract.type)  ==================  '''

        confid = self.env['sh.import.base'].search([], limit=1)
        response = requests.get(
            '%s/api/public/hr.contract.type?query={id,name,sequence,display_name}' % (confid.base_url))
        response_json = response.json()


        if response.status_code == 200:
            count = 0
            for result in response_json['result']:
                domain = [('remote_hr_contract_type_id', '=', result['id'])]
                find_rec = self.env['hr.contract.type'].search(domain)
                contract_vals = {
                    'remote_hr_contract_type_id': result.get('id'),
                    'name': result.get('name'),
                    'display_name': result.get('display_name'),
                    'sequence': result.get('sequence'),
                }
                if find_rec:
                    count += 1
                    find_rec.write(contract_vals)
                else:
                    self.env['hr.contract.type'].create(contract_vals)
                    count += 1

            if count > 0:
                vals = {
                    "name": confid.name,
                    "state": "success",
                    "field_type": "contract_basic",
                    "error": "%s Contract Type Imported Successfully" % (count),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)
        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "contract_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals)

    def import_sh_degree(self):
        ''' ========== Import Degree (sh.degree)  ==================  '''

        confid = self.env['sh.import.base'].search([], limit=1)
        response = requests.get(
            '%s/api/public/sh.degree?query={id,name,display_name}' % (confid.base_url))
        response_json = response.json()

        if response.status_code == 200:
            count = 0
            for result in response_json['result']:
                domain = [('remote_sh_degree_id', '=', result['id'])]
                find_rec = self.env['sh.degree'].search(domain)
                degree_vals = {
                    'remote_sh_degree_id': result.get('id'),
                    'name': result.get('name'),
                    'display_name': result.get('display_name'),
                }
                if find_rec:
                    count += 1
                    find_rec.write(degree_vals)
                else:
                    self.env['sh.degree'].create(degree_vals)
                    count += 1

            if count > 0:
                vals = {
                    "name": confid.name,
                    "state": "success",
                    "field_type": "degree_basic",
                    "error": "%s Degree Imported Successfully" % (count),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)
        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "degree_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals)

    def import_hr_job(self):
        ''' ========== Import Contract Type (hr.job)  ==================  '''

        confid = self.env['sh.import.base'].search([], limit=1)
        response = requests.get(
            '%s/api/public/hr.job?query={id,name,display_name,description,requirements,expected_employees,no_of_employee,no_of_recruitment,no_of_hired_employee,application_count,documents_count,max_salary,min_salary,is_seo_optimized,is_published,hr_responsible_id,address_id,employee_ids,application_ids}' % (confid.base_url))
        response_json = response.json()

        if response.status_code == 200:
            count = 0
            for data in response_json['result']:
                domain = [('remote_hr_job_id', '=', data['id'])]
                find_job = self.env['hr.job'].search(domain)
                hr_job_vals = {
                    'remote_hr_job_id': data['id'],
                    'name': data['name'],
                    'display_name': data['display_name'],
                    'description': data['description'],
                    'requirements': data['requirements'],
                    'expected_employees': data['expected_employees'],
                    'no_of_employee': data['no_of_employee'],
                    'no_of_recruitment': data['no_of_recruitment'],
                    'no_of_hired_employee': data['no_of_hired_employee'],
                    'company_id': 1,

                    # ----------------------------------------

                    'application_count': data['application_count'],
                    'documents_count': data['documents_count'],
                    'max_salary': data['max_salary'],
                    'min_salary': data['min_salary'],
                    'is_seo_optimized': data['is_seo_optimized'],
                    'is_published': data['is_published'],

                }

                # ------- HR RESPONSIBLE ID ----------------

                if data.get('hr_responsible_id'):
                    domain_by_id = [
                        ('remote_res_user_id', '=', data['hr_responsible_id'])]
                    find_user_id = self.env['res.users'].search(domain_by_id)
                    if find_user_id:
                        hr_job_vals['hr_responsible_id'] = find_user_id.id

                # ======== Get Partner if already created or create =========

                if data.get('address_id'):
                    domain = [('remote_res_partner_id',
                               '=', data['address_id'])]
                    find_customer = self.env['res.partner'].search(domain)
                    if find_customer:
                        hr_job_vals['address_id'] = find_customer.id

                if data.get('employee_ids'):
                    employee_list = []
                    for employee_id in data['employee_ids']:
                        domain = [('remote_hr_employee_id', '=', employee_id)]
                        find_employee = self.env['hr.employee'].search(domain)
                        if find_employee:
                            employee_list.append((4, find_employee.id))

                    hr_job_vals['employee_ids'] = employee_list

                # ------------ applicant ids ----------------

                if data.get('application_ids'):
                    applicant_list = []
                    for applicant_id in data['application_ids']:
                        domain = [
                            ('remote_hr_applicant_id', '=', applicant_id)]
                        find_applicant = self.env['hr.applicant'].search(
                            domain)
                        if find_applicant:
                            applicant_list.append((4, find_applicant.id))

                    hr_job_vals['application_ids'] = applicant_list

                # ------------- document_ids -----------------

                # if data.get('document_ids'):
                #     document_list=[]
                #     for document in data['document_ids']:
                #         domain = [('remote_ir_attachment_id', '=', document['id'])]
                #         find_document = self.env['ir.attachment'].search(domain)
                #         if not find_document:
                #             document_vals = self.process_ir_attchment_data(document)
                #             document_list.append((0,0,document_vals))
                #     hr_job_vals['document_ids'] = document_list

                if find_job:
                    count += 1
                    find_job.write(hr_job_vals)
                else:
                    self.env['hr.job'].create(hr_job_vals)
                    count += 1

            if count > 0:
                vals = {
                    "name": confid.name,
                    "state": "success",
                    "field_type": "job_basic",
                    "error": "%s Job Imported Successfully" % (count),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)
        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "job_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals)

    # def import_sh_degree(self):
    #     ''' ========== Import Degree (sh.degree)  ==================  '''

    #     confid = self.env['sh.import.base'].search([],limit=1)
    #     response = requests.get('%s/api/public/sh.degree?query={id,name,display_name}' % (confid.base_url))
    #     response_json = response.json()

    #     print("\n\n\n\n\n response_json degreee",response_json)
    #     if response.status_code==200:
    #         count = 0
    #         for result in response_json['result']:
    #             domain = [('remote_sh_degree_id', '=', result['id'])]
    #             find_rec = self.env['sh.degree'].search(domain)
    #             degree_vals={
    #                 'remote_sh_degree_id': result.get('id'),
    #                 'name': result.get('name'),
    #                 'display_name': result.get('display_name'),
    #             }
    #             if find_rec:
    #                 count += 1
    #                 find_rec.write(degree_vals)
    #             else:
    #                 self.env['sh.degree'].create(degree_vals)
    #                 count += 1

    #         if count > 0:
    #                 vals = {
    #                     "name": confid.name,
    #                     "state": "success",
    #                     "field_type": "degree_basic",
    #                     "error": "%s Degree Imported Successfully" %(count),
    #                     "datetime": datetime.now(),
    #                     "base_config_id": confid.id,
    #                     "operation": "import"
    #                 }
    #                 self.env['sh.import.base.log'].create(vals)
    #     else:
    #         vals = {
    #             "name": confid.name,
    #             "state": "error",
    #             "field_type": "degree_basic",
    #             "error": response.text,
    #             "datetime": datetime.now(),
    #             "base_config_id": confid.id,
    #             "operation": "import"
    #         }
    #         self.env['sh.import.base.log'].create(vals)

    def import_hr_department(self):
        ''' ========== import_hr_department ()  ==================  '''

        confid = self.env['sh.import.base'].search([], limit=1)
        response = requests.get('%s/api/public/hr.department?query={id,name,display_name,color,complete_name,note,expected_employee,expense_sheets_to_approve_count,new_applicant_count,absence_of_today,allocation_to_approve_count,new_hired_employee,total_employee,leave_to_approve_count,manager_id,member_ids,jobs_ids,child_ids{id,name,display_name,color,complete_name,note,expected_employee,expense_sheets_to_approve_count,new_applicant_count,absence_of_today,allocation_to_approve_count,new_hired_employee,total_employee,leave_to_approve_count,manager_id,member_ids,jobs_ids}}' % (confid.base_url))
        response_json = response.json()

        if response.status_code == 200:
            count = 0
            for data in response_json['result']:
                # domain = ['|', ('remote_hr_department_id', '=', data['id']), ('display_name', '=', data['display_name'])]
                domain = [('remote_hr_department_id', '=', data['id'])]
                find_rec = self.env['hr.department'].search(domain)
                hr_department_vals = {
                    'remote_hr_department_id': data['id'],
                    'name': data['name'],
                    'display_name': data['display_name'],
                    'color': data['color'],
                    'complete_name': data['complete_name'],
                    'note': data['note'],

                    # ----------------------------
                    'expected_employee': data['expected_employee'],
                    'expense_sheets_to_approve_count': data['expense_sheets_to_approve_count'],
                    'new_applicant_count': data['new_applicant_count'],
                    'absence_of_today': data['absence_of_today'],
                    'allocation_to_approve_count': data['allocation_to_approve_count'],
                    'new_hired_employee': data['new_hired_employee'],
                    'total_employee': data['total_employee'],
                    'leave_to_approve_count': data['leave_to_approve_count'],

                }

                # ======== Get Manager if already created or create =========

                if data.get('manager_id'):
                    domain = [('remote_hr_employee_id',
                               '=', data['manager_id'])]
                    find_employee = self.env['hr.employee'].search(domain)
                    if find_employee:
                        hr_department_vals['manager_id'] = find_employee.id

                # ======== Get Parent Id if already created or create =========

                if data.get('member_ids'):
                    employee_list = []
                    for employee_id in data['member_ids']:
                        domain = [('remote_hr_employee_id', '=', employee_id)]
                        find_employee = self.env['hr.employee'].search(domain)
                        if find_employee:
                            employee_list.append((4, find_employee.id))
                    hr_department_vals['member_ids'] = employee_list

                # ======== Get Child_ids if already created or create =========

                if data.get('child_ids'):
                    child_list = []
                    for child in data['child_ids']:
                        child_vals = self.prepare_hr_department(child)
                        domain = [
                            ('remote_hr_department_id', '=', child['id'])]
                        find_child = self.env['hr.department'].search(domain)
                        if not find_child:
                            child_vals = self.prepare_hr_department(child)
                            child_list.append((0, 0, child_vals))
                        else:
                            child_list.append((4, find_child.id))

                    hr_department_vals['child_ids'] = child_list

                # ======== Get Job ids if already created or create =========

                if data.get('jobs_ids'):
                    job_list = []
                    for job_id in data['jobs_ids']:
                        domain = [('remote_hr_job_id', '=', job_id)]
                        find_job = self.env['hr.job'].search(domain)
                        if find_job:
                            job_list.append((4, find_job.id))

                    hr_department_vals['jobs_ids'] = job_list

                if find_rec:
                    count += 1
                    find_rec.write(hr_department_vals)
                else:
                    self.env['hr.department'].create(hr_department_vals)
                    count += 1

            if count > 0:
                vals = {
                    "name": confid.name,
                    "state": "success",
                    "field_type": "department_basic",
                    "error": "%s Departments Imported Successfully" % (count),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)
        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "department_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals)
