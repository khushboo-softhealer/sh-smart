
# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
import requests


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    remote_hr_employee_id = fields.Char("Remote Employee ID",copy=False)
    sh_active = fields.Boolean("SH Active",copy=False)

class HrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    remote_hr_employee_id = fields.Char("Remote Employee ID",copy=False)
    sh_active = fields.Boolean("SH Active",copy=False)


class InheritImportEmployee(models.Model):
    _inherit = "sh.import.base"

    import_employee = fields.Boolean("Import Employee")
    records_per_page_employee = fields.Integer("No of Employee per page")
    current_import_page_employee = fields.Integer("Current Page", default=0)
    is_employee_basic_imported = fields.Boolean(default=False)
    sh_employees=fields.Char("Employees")


    def import_employee_basic(self):
        # Import Other Models to auto connect relation fields.

        # resource.resource
        # self.import_resource_resource()

        # sh.emp.non.technical.skill
        # self.import_sh_emp_non_technical_skill()

        # sh.emp.professional.experience
        # self.import_sh_emp_professional_experience()

        # for edu_qualification_ids (sh.education.qualification)
        self.import_sh_education_qualification()

        # for certification_ids (sh.certification)
        self.import_sh_certification()

        # for asset_ids (sh.asset)
        self.import_sh_asset()

        # for emergency_ids (hr.emp.emmergancy)
        self.import_hr_emp_emmergancy()

        self.import_hr_job()
        self.import_hr_department()
        # language.known (Required Employee ID)
        # self.import_language_known()   


    def import_hr_employee(self):
        ''' ========== Import Employees (hr.employee)  ==================  '''

        confid = self.env['sh.import.base'].search([], limit=1)

        # Import Other Models to import some employees remaining fields.

        # if not confid.is_employee_basic_imported:
        #     # Import Other Models to auto connect relation fields.

        #     # resource.resource
        #     # self.import_resource_resource()

        #     # sh.emp.non.technical.skill
        #     # self.import_sh_emp_non_technical_skill()

        #     # sh.emp.professional.experience
        #     # self.import_sh_emp_professional_experience()

        #     # for edu_qualification_ids (sh.education.qualification)
        #     self.import_sh_education_qualification()

        #     # for certification_ids (sh.certification)
        #     self.import_sh_certification()

        #     # for asset_ids (sh.asset)
        #     self.import_sh_asset()

        #     # for emergency_ids (hr.emp.emmergancy)
        #     self.import_hr_emp_emmergancy()

        #     # language.known (Required Employee ID)
        #     # self.import_language_known()
        #     confid.is_employee_basic_imported = True

        if confid.import_employee:
            confid.current_import_page_employee += 1
            response = requests.get(
                '''%s/api/public/hr.employee?query={%s}&page_size=%s&page=%s''' % (confid.base_url, self.query.get('hr_employee'), confid.records_per_page_employee, confid.current_import_page_employee))

            if response.status_code == 200:
                response_json = response.json()
                count = 0
                failed = 0
                if 'count' in response_json and confid.records_per_page_employee != response_json['count']:
                    confid.import_employee = False
                    confid.current_import_page_employee = 0
                    confid.is_employee_basic_imported = False

                for result in response_json['result']:
                    # try:
                    # if result.get('id') and result.get('id')==78:
                    #     continue
                    domain = [('remote_hr_employee_id', '=', result.get('id'))]
                    find_employee=self.env['hr.employee'].search(domain)
                    employee_vals=self.process_employee_data(result)
                    print("\n\n=====employee_vals",employee_vals)
                    if find_employee:
                        # if 'user_id' in employee_vals:
                        #     del employee_vals['user_id']
                        find_employee.write(employee_vals)
                        print("\n\n=vvvvvvvvv")
                    else:
                        self.env['hr.employee'].create(employee_vals)
                    count += 1
                    # except Exception as e:
                    #     failed += 1
                    #     self.create_fail_log(
                    #         name = result.get('id'),
                    #         field_type = 'hr_employee',
                    #         error = e,
                    #         import_json = result,
                    #     )

                if count > 0:
                    self.create_log(
                        field_type = 'hr_employee', error = "%s Employies Imported Successfully" % (count), state = 'success')
                if failed > 0:
                    self.create_log(
                        field_type = 'hr_employee', error = "%s Employee Failed To Import" % (failed))
            else:
                print("\n\n------------- inside else")
                self.create_log(
                    field_type = 'hr_employee', error = response.text)
                
    def import_filtered_hr_employee(self):
        ''' ========== Import Employees (hr.employee)  ==================  '''

        confid = self.env['sh.import.base'].search([], limit=1)
        if confid.import_employee:
            employees = confid.sh_employees.strip('][').split(', ')
            count=0
            failed=0  
            for employee in employees[0:10]:

                response = requests.get(
                    '''%s/api/public/hr.employee/%s?query={%s}''' % (confid.base_url,employee, self.query.get('hr_employee')))

                if response.status_code == 200:
                    response_json = response.json()
                    count = 0
                    failed = 0

                    for result in response_json['result']:
                        # try:
                        domain = [('remote_hr_employee_id', '=', result.get('id'))]
                        find_employee=self.env['hr.employee'].search(domain)
                        employee_vals=self.process_employee_data(result)
                        if find_employee:
                            find_employee.write(employee_vals)
                        else:
                            self.env['hr.employee'].create(employee_vals)
                        count += 1
                        # except Exception as e:
                        #     failed += 1
                        #     self.create_fail_log(
                        #         name = result.get('id'),
                        #         field_type = 'hr_employee',
                        #         error = e,
                        #         import_json = result,
                        #     )
            confid.sh_employees='['+', '.join([str(elem) for elem in employees[10:]])+']'        
            if count > 0:
                self.create_log(
                    field_type = 'hr_employee', error = "%s Employee Update Successfully" % (count), state = 'success')
            if failed > 0:
                self.create_log(
                    field_type = 'hr_employee', error = "%s Employee Failed To Import" % (failed))
        # else:
        #     print("\n\n\------------- inside else")
        #     self.create_log(
        #         field_type = 'hr_employee', error = response.text)




    def process_employee_data(self, data):
        ''' ============== Prepare Employee Vals ====================== '''
        if data.get('id') in [7,29,55,80,75,70,76,56,30,13,84,33,54,18,42,53,67,69,62,63]:
            active=False
        else:
            active=True
        employee_vals={
            'remote_hr_employee_id': data.get('id'),
            'sh_active': active,
            'additional_note': data.get('additional_note'),
            'certificate': data.get('certificate').get('sh_api_current_state'),
            'color': data.get('color'),
            'display_name': data.get('display_name'),
            'emergency_contact': data.get('emergency_contact'),
            'emergency_phone': data.get('emergency_phone'),
            'gender': data.get('gender').get('sh_api_current_state'),
            'identification_id': data.get('identification_id'),
            'km_home_work': data.get('km_home_work'),
            'marital': data.get('marital').get('sh_api_current_state'),
            'name': data.get('name'),
            'notes': data.get('notes'),
            'passport_id': data.get('passport_id'),
            'permit_no': data.get('permit_no'),
            'place_of_birth': data.get('place_of_birth'),
            'sinid': data.get('sinid'),
            'spouse_complete_name': data.get('spouse_complete_name'),
            'ssnid': data.get('ssnid'),
            'study_field': data.get('study_field'),
            'study_school': data.get('study_school'),
            'tz': data.get('tz').get('sh_api_current_state'),
            'visa_no': data.get('visa_no'),
            'work_email': data.get('work_email'),
            'work_phone': data.get('work_phone'),
            "company_id": 1,
            'pf_acc_no': data.get('pf_acc_no'),
            'skype': data.get('skype'),
            'whatsapp': data.get('whatsapp'),
            'facebook': data.get('facebook'),
            'instagram': data.get('instagram'),
            'twitter': data.get('twitter'),
            'personal_email': data.get('personal_email'),
            'sh_work_hours_notify': data.get('sh_work_hours_notify'),
            'newly_hired_employee': data.get('newly_hired_employee'),
            'payslip_count': data.get('payslip_count'),
            'is_remote_employee': data.get('is_remote_employee'),
            'sh_bank_account': data.get('sh_bank_account'),
            'send_payslip': data.get('send_payslip'),
            'assets_count': data.get('assets_count'),
            'requests_count': data.get('requests_count'),
            'is_address_home_a_company': data.get('is_address_home_a_company'),
            'children': data.get('children'),
            'job_title': data.get('job_title'),
            'mobile_phone': data.get('mobile_phone'),
            'work_email': data.get('work_email'),
            'pin': data.get('pin'),
            'vehicle': data.get('vehicle'),
            'contracts_count': data.get('contracts_count'),
            'remaining_leaves': data.get('remaining_leaves'),
            'leaves_count': data.get('leaves_count'),
            'show_leaves': data.get('show_leaves'),
            'is_absent': data.get('is_absent_totay'),
            'height': data.get('height'),
            'weight': data.get('weight'),
            'age': data.get('age'),
            'is_part_time': data.get('is_part_time'),
            'payslip_count': data.get('payslip_count'),
            'hourly_cost': data.get('timesheet_cost'),
            'sh_attendance_state': data.get('sh_attendance_state').get('sh_api_current_state'),
            'attendance_state': data.get('attendance_state').get('sh_api_current_state'),
            'current_leave_state': data.get('current_leave_state').get('sh_api_current_state'),
            'blood_group': data.get('blood_group').get('sh_api_current_state'),
        }

        # To prevent contraint error.
        if data.get('barcode'):
            find_employee = self.env['hr.employee'].search(
                [('barcode', '=', data.get('barcode'))])
            if not find_employee:
                employee_vals['barcode']=data.get('barcode')

        # ======================== date fields ========================

        # birthday(date)
        self.date_vals(data, employee_vals, data_key = 'birthday')
        # visa_expire(data)
        self.date_vals(data, employee_vals, data_key = 'visa_expire')
        # leave_date_from
        self.date_vals(data, employee_vals, data_key = 'leave_date_from')
        # leave_date_to
        self.date_vals(data, employee_vals, data_key = 'leave_date_to')
        # passport_issue
        self.date_vals(data, employee_vals, data_key = 'passport_issue')
        # passport_expiry
        self.date_vals(data, employee_vals, data_key = 'passport_expiry')
        # joining_date
        self.date_vals(data, employee_vals, data_key = 'joining_date')
        # employment_date
        self.date_vals(data, employee_vals, data_key = 'employment_date')
        # confirmation_date
        self.date_vals(data, employee_vals, data_key = 'confirmation_date')
        # marriage_date
        self.date_vals(data, employee_vals, data_key = 'marriage_date')
        # spouse_birthdate
        self.date_vals(data, employee_vals, data_key = 'spouse_birthdate')
        # date_of_joining
        self.date_vals(data, employee_vals, data_key = 'date_of_joining')

        # ======================== many2one fields ========================

        self.map_many2one_field(
            'res.users', 'remote_res_user_id', data, employee_vals, 'user_id')
        # expense_manager_id
        self.map_many2one_field(
            'hr.employee', 'remote_hr_employee_id', data, employee_vals, 'expense_manager_id')

        # address_home_id(res.partner)
        self.map_many2one_field(
            'res.partner', 'remote_res_partner_id', data, employee_vals, 'address_home_id')
        self.map_many2one_field(
            'res.partner', 'remote_res_partner_id', data, employee_vals, 'address_id')

        # resource_calendar_id
        self.map_many2one_field(
            'resource.calendar', 'remote_resource_calendar_id', data, employee_vals, 'resource_calendar_id')

        # work_country_id
        self.map_country(data, employee_vals, 'work_country_id')
        # country_id
        self.map_country(data, employee_vals)
        # map_country
        self.map_country(data, employee_vals, 'passport_country_id')
        # country_of_birth(res.country)
        self.map_country(data, employee_vals, 'country_of_birth')
        # currency_id{name}
        self.map_currency_id(data, employee_vals)
        self.map_resource_id(data, employee_vals)
        self.map_sh_emp_technical_skill(data, employee_vals)

        # contract_id (find or temp create)
        # if data.get('contract_id'):
        #     if data.get('contract_id').get('id') and data.get('contract_id').get('id') != 0:
        #         domain = [('remote_hr_contract_id', '=',
        #                    data['contract_id']['id'])]
        #         find_contract = self.env['hr.contract'].search(domain)
        #         if find_contract:
        #             employee_vals['contract_id'] = find_contract.id
        #         else:
        #             contract_vals = {
        #                 'remote_hr_contract_id': data['contract_id']['id'],
        #                 'name': data['contract_id']['name'],
        #                 'hr_responsible_id': data['contract_id']['activity_user_id'],
        #                 'wage': data['contract_id']['wage'],
        #             }
        #             if data['contract_id'].get('struct_id'):
        #                 domain = [('remote_hr_payroll_structure_id',
        #                            '=', data['contract_id']['struct_id']['id'])]
        #                 find_struct_id = self.env['hr.payroll.structure'].search(
        #                     domain)
        #                 if find_struct_id:
        #                     contract_vals['struct_id'] = find_struct_id.id
        #                 else:
        #                     hr_payroll_structure_vals = {
        #                         'remote_hr_payroll_structure_id': data['contract_id'].get('struct_id')['id'],
        #                         'name': data['contract_id'].get('struct_id')['name'],
        #                         'code': data['contract_id'].get('struct_id')['code'],
        #                         'company_id': 1,
        #                     }
        #                     hr_payroll_structure_id = self.env['hr.payroll.structure'].create(
        #                         hr_payroll_structure_vals)
        #                     if hr_payroll_structure_id:
        #                         contract_vals['struct_id'] = hr_payroll_structure_id.id

        #             contract_id = self.env['hr.contract'].create(contract_vals)
        #             if contract_id:
        #                 employee_vals['contract_id'] = contract_id.id

        # current_leave_id (hr.leave.type)
        # if data.get('current_leave_id'):
        #     if data['current_leave_id'].get('id') and data['current_leave_id'].get('id') != 0:
        #         domain = ['|', ('remote_leave_type_id', '=', data['current_leave_id'].get(
        #             'id')), ('name', '=', data['current_leave_id'].get('name'))]
        #         find_leave_type = self.env['hr.leave.type'].search(domain)
        #         if find_leave_type:
        #             employee_vals['current_leave_id'] = find_leave_type.id
        #         else:
        #             # Required fields
        #             leave_type_vals = {
        #                 'remote_leave_type_id': data['current_leave_id'].get('id'),
        #                 'name': data['current_leave_id'].get('name'),
        #                 'company_id': 1,
        #                 'color_name': data['current_leave_id'].get('color_name').get('sh_api_current_state'),
        #                 'request_unit': data['current_leave_id'].get('request_unit').get('sh_api_current_state'),
        #                 # Not in v12
        #                 # 'employee_requests': data['current_leave_id'].get('employee_requests').get('sh_api_current_state'),
        #                 # 'requires_allocation': data['current_leave_id'].get('requires_allocation').get('sh_api_current_state'),
        #             }
        #             create_leave_type = self.env['hr.leave.type'].create(
        #                 leave_type_vals)
        #             if create_leave_type:
        #                 employee_vals['current_leave_id'] = create_leave_type.id

        # category_ids{id,name,color,display_name}
        if data.get('category_ids'):
            category_ids_list = []
            for categ in data.get('category_ids'):
                domain = [('remote_emp_tag_id', '=', categ['id'])]
                find_categ = self.env['hr.employee.category'].search(domain)
                if find_categ:
                    category_ids_list.append((4, find_categ.id))
                else:
                    categ_vals = self.prepare_emp_tag_vals(categ)
                    if categ_vals:
                        category_ids_list.append((0, 0, categ_vals))
            if category_ids_list:
                employee_vals['category_ids'] = category_ids_list

        # (hr.employee) coach_id{id,name}
        # self.map_temp_hr_employee(data, employee_vals, 'coach_id')
        if data.get('coach_id'):
            find_employee=self.env['hr.employee'].search([('remote_hr_employee_id','=',data.get('coach_id').get('id'))])
            if find_employee:
                employee_vals['coach_id']=find_employee.id
                employee_vals['leave_manager_id']=find_employee.user_id.id

        if data.get('job_id'):
            find_job=self.env['hr.job'].search([('remote_hr_job_id','=',data.get('job_id'))])
            if find_job:
                employee_vals['job_id']=find_job.id

        if data.get('department_id'):
            find_department=self.env['hr.department'].search([('remote_hr_department_id','=',data.get('department_id'))])
            if find_department:
                employee_vals['department_id']=find_department.id

        # self.map_temp_hr_employee(data, employee_vals, 'coach_id')
        # (hr.employee) reference_by_id{id,name}
        self.map_temp_hr_employee(data, employee_vals, 'reference_by_id')
        # (hr.employee) hr_manager{id,name}
        self.map_temp_hr_employee(data, employee_vals, 'hr_manager')

        # religion_id (sh.employee.religion)
        if data.get('religion_id'):
            if data['religion_id'].get('id') and data['religion_id'].get('id') != 0:
                domain = ['|', ('remote_sh_employee_religion_id', '=', data['religion_id'].get('id')),
                          ('name', '=', data['religion_id'].get('name'))]
                find_religion = self.env['sh.employee.religion'].search(
                    domain, limit=1)
                if find_religion:
                    employee_vals['religion_id'] = find_religion.id
                else:
                    create_religion = self.env['sh.employee.religion'].create({
                        'remote_sh_employee_religion_id': data['religion_id'].get('id'),
                        'name': data['religion_id'].get('name'),
                        'display_name': data['religion_id'].get('display_name'),
                    })
                    if create_religion:
                        employee_vals['religion_id'] = create_religion.id

        # facilities_cmp_ids(sh.company.facilities)
        if data.get('facilities_cmp_ids'):
            facilities_list = []
            for facilities_id in data.get('facilities_cmp_ids'):
                domain = [('remote_sh_company_facilities_id',
                           '=', facilities_id.get('id'))]
                find_facilities = self.env['sh.company.facilities'].search(
                    domain)
                if find_facilities:
                    facilities_list.append((4, find_facilities.id))
                else:
                    facilities_vals = {
                        'remote_sh_company_facilities_id': facilities_id.get('id'),
                        'name': facilities_id.get('name'),
                        'display_name': facilities_id.get('display_name')
                    }
                    facilities_list.append((0, 0, facilities_vals))
            if facilities_list:
                employee_vals['facilities_cmp_ids'] = facilities_list

        # child_ids
        if data.get('child_ids'):
            child_list = []
            for child in data['child_ids']:
                domain = [('remote_hr_employee_id', '=', child['id'])]
                find_child = self.env['hr.employee'].search(domain)
                if find_child:
                    child_list.append((4, find_child.id))
                else:
                    child_vals = self.process_employee_data(child)
                    if child_vals:
                        child_list.append((0, 0, child_vals))
            if child_list:
                employee_vals['child_ids'] = child_list

        # non_tec_skill_ids (sh.emp.non.technical.skill)
        self.map_non_tec_skill_ids(data, employee_vals)
        # pro_expe_ids (sh.emp.professional.experience)
        self.map_pro_expe_ids(data, employee_vals)
        # certification_ids
        self.map_one2many_ids('sh.certification', 'remote_sh_certification_id',
                              data, employee_vals, 'certification_ids')
        # asset_ids (sh.asset)
        self.map_one2many_ids('sh.asset', 'remote_sh_asset_id',
                              data, employee_vals, 'asset_ids')
        # emergency_ids (hr.emp.emmergancy)
        self.map_one2many_ids('hr.emp.emmergancy', 'remote_hr_emp_emmergancy_id',
                              data, employee_vals, 'emergency_ids')
        # edu_qualification_ids (sh.education.qualification)
        self.map_one2many_ids('sh.education.qualification', 'remote_sh_education_qualification_id',
                              data, employee_vals, 'edu_qualification_ids')
        # language_known_ids (language.known)
        # self.map_language_known_ids(data, employee_vals)

        return employee_vals
