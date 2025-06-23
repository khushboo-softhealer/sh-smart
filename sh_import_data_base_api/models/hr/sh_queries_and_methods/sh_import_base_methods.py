# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models
from datetime import datetime


class InheritImportBase(models.Model):
    _inherit = "sh.import.base"

    # ========================== Methods ==========================

    def create_hr_basic_log(
        self,
        field_type='hr_basic',
        operation='import',
        error='Not specified any Message...!',
        state='error'
    ):
        confid = self.env['sh.import.base'].search([], limit=1)
        vals = {
            "field_type": field_type,
            "operation": operation,
            "error": error,
            "state": state,
            "name": confid.name,
            "base_config_id": confid.id,
            "datetime": datetime.now(),
        }
        self.env['sh.import.base.log'].create(vals)

    def create_log(
        self,
        field_type='hr_leave',
        operation='import',
        error='Not specified any Message...!',
        state='error'
    ):
        confid = self.env['sh.import.base'].search([], limit=1)
        vals = {
            "field_type": field_type,
            "operation": operation,
            "error": error,
            "state": state,
            "name": confid.name,
            "base_config_id": confid.id,
            "datetime": datetime.now(),
        }
        self.env['sh.import.base.log'].create(vals)

    def create_fail_log(
        self,
        name,
        field_type,
        error='Not specified any error...!',
        import_json={'default_key': 'default_val'},
    ):
        confid = self.env['sh.import.base'].search([], limit=1)
        vals = {
            "name": name,
            "error": error,
            "field_type": field_type,
            "import_json": import_json,
            "base_config_id": confid.id,
            "datetime": datetime.now(),
        }
        self.env['sh.import.failed'].create(vals)

    # ======================= Date/Datetime Fields =======================

    def date_vals(self, data, vals, data_key='date', vals_key=None):
        '''Date:
        if both key same than it's ok to give just one key'''
        if data.get(data_key):
            if not vals_key:
                vals_key = data_key
            vals[vals_key] = datetime.strptime(data.get(data_key), '%Y-%m-%d')

    def datetime_vals(self, data, vals, data_key=None, vals_key=None):
        '''Datetime:
        if both key same than it's ok to give just one key'''
        if data.get(data_key):
            if not vals_key:
                vals_key = data_key
            date_time = datetime.strptime(data.get(data_key), '%Y-%m-%d-%H-%M-%S')
            vals[vals_key] = date_time.strftime('%Y-%m-%d %H:%M:%S')

    # ========================== Res Partner ==========================
    def map_res_partner(self, data, vals, data_key='partner_id', vals_key=None):
        '''res.partner (many2one)'''
        if data.get(data_key) and data.get(data_key) != 0:
            domain = [('remote_res_partner_id', '=', data[data_key])]
            find_partner = self.env['res.partner'].search(domain)
            if find_partner:
                if not vals_key:
                    vals_key = data_key
                vals[vals_key] = find_partner.id

    # ========================== Hr Employee ==========================
    def map_hr_employee(self, data, vals, data_key='employee_id', vals_key=None):
        '''hr.employee (many2one)'''
        if data.get(data_key):
            if data.get(data_key).get('id') and data.get(data_key).get('id') != 0:
                if not vals_key:
                    vals_key = data_key
                domain = [('remote_hr_employee_id', '=', data[data_key]['id'])]
                find_employee = self.env['hr.employee'].search(domain)
                if find_employee:
                    vals[vals_key] = find_employee.id
                else:
                    employee_vals = self.process_employee_data(
                        data[data_key])
                    employee_id = self.env['hr.employee'].create(employee_vals)
                    if employee_id:
                        vals[vals_key] = employee_id.id

    def map_temp_hr_employee(self, data, vals, data_key='employee_id', vals_key=None):
        if data.get(data_key):
            if data[data_key].get('id') and data[data_key].get('id') != 0:
                if not vals_key:
                    vals_key = data_key
                domain = [('remote_hr_employee_id', '=',
                           data[data_key].get('id'))]
                find_employee = self.env['hr.employee'].search(domain)
                print("\n\n====find_employee",find_employee)
                if find_employee:
                    vals[vals_key] = find_employee.id
                else:
                    # Required fields
                    employee_vals = {
                        'remote_hr_employee_id': data[data_key].get('id'),
                        'name': data[data_key].get('name'),
                    }
                    create_employee = self.env['hr.employee'].create(
                        employee_vals)
                    if create_employee:
                        vals[vals_key] = create_employee.id

    # ========================== department_id ==========================
    def find_or_create_department(self, data, vals, data_key='department_id', vals_key=None):
        if data.get(data_key):
            if data.get(data_key).get('id') and data.get(data_key).get('id') != 0:
                if not vals_key:
                    vals_key = data_key
                domain = [('remote_hr_department_id', '=',
                           data[data_key]['id'])]
                find_department = self.env['hr.department'].search(domain)
                if find_department:
                    vals[vals_key] = find_department.id
                else:
                    department_vals = self.import_hr_department(
                        data[data_key])
                    create_department = self.env['hr.department'].create(
                        department_vals)
                    if create_department:
                        vals[vals_key] = create_department.id

    def find_department_sort(self, data, vals, data_key='department_id', vals_key=None):
        if data.get(data_key):
            if data[data_key].get('id') and data[data_key].get('id') != 0:
                if not vals_key:
                    vals_key = data_key
                domain = [('remote_hr_department_id', '=',
                           data[data_key].get('id'))]
                find_department = self.env['hr.department'].search(domain)
                if find_department:
                    vals[vals_key] = find_department.id
                elif data[data_key].get('name') != '':
                    create_department = self.env['hr.department'].create({
                        'remote_hr_department_id': data[data_key].get('id'),
                        'name': data[data_key].get('name'),
                    })
                    if create_department:
                        vals[vals_key] = create_department.id

    # ========================== leave ==========================
    def find_or_create_leave(self, data, vals, data_key=None, vals_key=None):
        if data.get(data_key):
            if data.get(data_key).get('id') and data.get(data_key).get('id') != 0:
                if not vals_key:
                    vals_key = data_key
                domain = [('remote_leave_id', '=',
                           data[data_key]['id'])]
                find_leave = self.env['hr.leave'].search(domain)
                if find_leave:
                    vals[vals_key] = find_leave.id
                else:
                    leave_vals = self.process_hr_leave_vals(
                        data[data_key])
                    create_leave = self.env['hr.leave'].create(
                        leave_vals)
                    if create_leave:
                        vals[vals_key] = create_leave.id

    # ========================== Leave Types ==========================

    def find_or_create_leave_types(self, data, vals, data_key='holiday_status_id', vals_key=None):
        if data.get(data_key):
            if data[data_key]['id'] != 0:
                if not vals_key:
                    vals_key = data_key
                domain = [('remote_leave_type_id', '=',
                           data[data_key]['id'])]
                find_leave_type = self.env['hr.leave.type'].search(domain)
                if find_leave_type:
                    vals[vals_key] = find_leave_type.id
                else:
                    leave_type_vals = self.prepare_leave_type_vals(
                        data[data_key])
                    created_leave_type = self.env['hr.leave.type'].create(
                        leave_type_vals)
                    if created_leave_type:
                        vals[vals_key] = created_leave_type.id

    # ========================== HR Attendance ==========================
    def map_hr_attendance(self, data, vals, data_key='attendance_id', vals_key=None):
        '''hr.attendance (many2one)'''
        if data.get(data_key):
            if data.get(data_key).get('id') and data.get(data_key).get('id') != 0:
                if not vals_key:
                    vals_key = data_key
                domain = [('remote_hr_attendance_id', '=', data.get('id'))]
                find_attendance = self.env['hr.attendance'].search(domain)
                if find_attendance:
                    vals[vals_key] = find_attendance.id
                else:
                    attendance_vals = self.prepare_hr_attendance_vals(
                        data[data_key])
                    create_attendance = self.env['hr.attendance'].create(
                        attendance_vals)
                    if create_attendance:
                        vals[vals_key] = create_attendance.id

    # ========================== Employee Tag ==========================
    def find_or_create_employee_tag(self, data, vals, data_key='employee_tag', vals_key=None):
        '''hr.employee.category (many2one)'''
        if data.get(data_key):
            if data.get(data_key).get('id') and data.get(data_key).get('id') != 0:
                if not vals_key:
                    vals_key = data_key
                domain = ['|', ('remote_emp_tag_id', '=', data.get(data_key).get('id')),
                          ('name', '=', data.get(data_key).get('name'))]
                find_emp_tag = self.env['hr.employee.category'].search(domain)
                if find_emp_tag:
                    vals[vals_key] = find_emp_tag.id
                else:
                    emp_tag_vals = self.prepare_emp_tag_vals(data[data_key])
                    create_emp_tag = self.env['hr.employee.category'].create(
                        emp_tag_vals)
                    if create_emp_tag:
                        vals[vals_key] = create_emp_tag.id

    # ========================== Employee Ids ==========================
    def map_employee_ids(self, data, vals, data_key='employee_ids', vals_key=None):
        '''Default key: employee_ids'''
        if data.get(data_key):
            employee_ids = []
            for employee_id in data.get(data_key):
                if employee_id == 0:
                    continue
                domain = [('remote_hr_employee_id', '=', employee_id)]
                find_emp = self.env['hr.employee'].search(domain)
                if find_emp:
                    employee_ids.append((4, find_emp.id))
            if employee_ids:
                if not vals_key:
                    vals_key = data_key
                vals[vals_key] = employee_ids

    # =========== CHECK RELATED PROJECT EXIST OR NOT IF EXIST IMPORT ============
    def find_or_create_state(self, data, vals, data_key='state_id', vals_key=None):
        '''many2one(res.country.state)'''
        if data.get(data_key):
            if not vals_key:
                vals_key = data_key
            if data[data_key].get('name') and data[data_key].get('code'):
                domain = [('name', '=', data[data_key]['name']),
                          ('code', '=', data[data_key]['code'])]
                find_state = self.env['res.country.state'].search(domain)
                if find_state:
                    vals[vals_key] = find_state.id

    def map_country(self, data, vals, data_key='country_id', vals_key=None):
        '''many2one(res.country)
        default key = country_id'''
        if data.get(data_key) and type(data.get(data_key)) != int and data.get(data_key) != '':
            if not vals_key:
                vals_key = data_key
            country_domain = [('name', '=', data[data_key]['name'])]
            find_country = self.env['res.country'].search(
                country_domain, limit=1)
            if find_country:
                vals[vals_key] = find_country.id

    def map_currency_id(self, data, vals, data_key='currency_id', vals_key=None):
        '''many2one(res.currency)
        default key = currency_id'''
        if data.get(data_key):
            domain = [('name', '=', data.get(data_key).get('name'))]
            find_currency_id = self.env['res.currency'].search(domain, limit=1)
            if find_currency_id:
                if not vals_key:
                    vals_key = data_key
                vals[vals_key] = find_currency_id.id

    # contact_person_ids
    def map_res_partner_ids(self, data, vals, data_key=None, vals_key=None):
        '''many2many(res.partner)'''
        if data.get(data_key):
            partner_ids = []
            for v12_id in data.get(data_key):
                domain = [('remote_res_partner_id', '=', v12_id)]
                find_partner = self.env['res.partner'].search(domain)
                if find_partner:
                    partner_ids.append((4, find_partner.id))
            if partner_ids:
                if not vals_key and data_key:
                    vals_key = data_key
                vals[vals_key] = partner_ids

    # ========================================
    #         map many2one fields
    # ========================================

    #  Map many2one method
    def map_many2one_field(self, model, remote_field, data, vals, data_key, vals_key=None):
        '''
            model (many2one)
            Use when you domain is based on jus remote field.
        '''
        if data.get(data_key) and data.get(data_key) != 0:
            domain = [(remote_field, '=', data[data_key])]
            find_rec = self.env[model].search(domain)
            if find_rec:
                if not vals_key:
                    vals_key = data_key
                vals[vals_key] = find_rec.id

    def map_many2one_field_with_name(self, model, remote_field, data, vals, data_key, vals_key=None):
        '''
            model (many2one)
            required: field_name{id,name}
            Use when you domain is based on remote field,
            as well as name field.
        '''
        if data.get(data_key):
            if data.get(data_key).get('id') != 0 and data[data_key].get('name'):
                domain = ['|', (remote_field, '=', data[data_key].get('id')),
                          ('name', '=', data[data_key].get('name'))]
                find_rec = self.env[model].search(domain)
                if find_rec:
                    if not vals_key:
                        vals_key = data_key
                    vals[vals_key] = find_rec.id

    def map_tax_ids(self, data, vals, data_key='tax_ids', vals_key=None):
        '''tax_ids many2many(account.tax)'''
        if data.get(data_key):
            tax_list = []
            for tax_id in data.get(data_key):
                domain = [('amount', '=', tax_id['amount']),
                          ('type_tax_use', '=', tax_id['type_tax_use']['sh_api_current_state'])]
                find_tax = self.env['account.tax'].search(domain, limit=1)
                if find_tax:
                    tax_list.append((4, find_tax.id))
            if tax_list:
                if not vals_key:
                    vals_key = data_key
                vals[vals_key] = tax_list

    # ==========================
    #         Applicant
    # ==========================

    #  hr.recruitment.stage
    def map_hr_recruitment_stage(self, data, vals, data_key='stage_id', vals_key=None):
        '''hr.recruitment.stage (many2one)'''
        if data.get(data_key) and data.get(data_key) != 0:
            if not vals_key:
                vals_key = data_key
            domain = [('remote_recruitment_stage_id', '=', data[data_key])]
            find_rec_stage = self.env['hr.recruitment.stage'].search(domain)
            if find_rec_stage:
                vals[vals_key] = find_rec_stage.id

    # ===================================
    #         Applicant Basics
    # ===================================

    # ========================== stage_id ==========================
    def find_or_create_college_stage(self, data, vals, data_key='stage_id', vals_key=None):
        ''' stage_id Many2one(sh.college.stages) '''
        if data.get(data_key):
            if data.get(data_key).get('id') and data.get(data_key).get('id') != 0:
                if not vals_key:
                    vals_key = data_key
                domain = [('remote_sh_college_stage_id',
                           '=', data[data_key]['id'])]
                find_college_stage = self.env['sh.college.stages'].search(
                    domain)
                if find_college_stage:
                    vals[vals_key] = find_college_stage.id
                else:
                    college_stage_vals = {
                        'display_name': data[data_key].get('display_name'),
                        'fold': data[data_key].get('fold'),
                        'remote_sh_college_stage_id': data[data_key].get('id'),
                        'name': data[data_key].get('name'),
                        'sequence': data[data_key].get('sequence'),
                    }
                    create_college_stage = self.env['sh.college.stages'].create(
                        college_stage_vals)
                    if create_college_stage:
                        vals[vals_key] = create_college_stage.id
