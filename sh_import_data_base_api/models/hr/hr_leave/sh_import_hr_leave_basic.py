# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models
import requests
from datetime import datetime


class InheritImportHelpdeskBase(models.Model):
    _inherit = "sh.import.base"

    def import_basic_hr_leave_cron(self):
        ''' ========== Connect db for import Time Off Basic  ==================  '''
        self.import_hr_employee_category()
        self.import_hr_leave_type()
        self.import_hr_leave_allocation()

    # ==================================== Leave Type ======================================

    def prepare_leave_type_vals(self, leave_type_dict):
        # not found fields: validity_start,validity_stop,group_days_allocation
        prepare_leave_type_vals = {
            'remote_leave_type_id': leave_type_dict.get('id'),
            'name': leave_type_dict.get('name'),
            'company_id': 1,
            'sequence': leave_type_dict.get('sequence'),
            'active': leave_type_dict.get('active'),
            'max_leaves': leave_type_dict.get('max_leaves'),
            'leaves_taken': leave_type_dict.get('leaves_taken'),
            'remaining_leaves': leave_type_dict.get('remaining_leaves'),
            'virtual_remaining_leaves': leave_type_dict.get('virtual_remaining_leaves'),
            'group_days_leave': leave_type_dict.get('group_days_leave'),
            'has_valid_allocation': leave_type_dict.get('valid'),
            'unpaid': leave_type_dict.get('unpaid'),
            'display_name': leave_type_dict.get('display_name'),
            'color_name': leave_type_dict['color_name']['sh_api_current_state'],
            'time_type': leave_type_dict['time_type']['sh_api_current_state'],
            'request_unit': leave_type_dict['request_unit']['sh_api_current_state'],
            # Custom(Added) fields
            'support_document': leave_type_dict.get('sh_leave_attachment'),
            'leave_before_day_alert': leave_type_dict.get('leave_before_day_alert'),
            'leave_before_days': leave_type_dict.get('leave_before_days'),
            'no_of_days': leave_type_dict.get('no_of_days'),
            # 'timesheet_generate': leave_type_dict.get('timesheet_generate'),
            'company_id': 1,
        }

        if leave_type_dict['allocation_type']['sh_api_current_state'] == 'no':
            prepare_leave_type_vals['allocation_validation_type'] = 'no'
        else:
            prepare_leave_type_vals['allocation_validation_type'] = 'officer'

        # from double_validation and validation_type map leave_validation_type field
        if leave_type_dict.get('double_validation'):
            prepare_leave_type_vals['leave_validation_type'] = leave_type_dict['validation_type']['sh_api_current_state']
        else:
            prepare_leave_type_vals['leave_validation_type'] = 'no_validation'

        self.map_many2one_field(
            'project.project', 'remote_project_project_id', leave_type_dict, prepare_leave_type_vals, 'timesheet_project_id')
        self.map_many2one_field(
            'project.task', 'remote_project_task_id', leave_type_dict, prepare_leave_type_vals, 'timesheet_task_id')

        return prepare_leave_type_vals

    def import_hr_leave_type(self):
        ''' ========== Import Time Off Types (hr.leave.type)  ==================  '''

        response = requests.get(
            '''%s/api/public/hr.leave.type?query={%s}''' % (self.base_url, self.query['hr_leave_type']))

        response_json = response.json()

        if response.status_code == 200:
            count = 0
            failed = 0

            for result in response_json['result']:
                try:
                    domain = ['|', ('remote_leave_type_id', '=', result.get('id')),
                              ('name', '=', result.get('name'))]
                    find_leave_type = self.env['hr.leave.type'].search(domain)
                    leave_type_vals = self.prepare_leave_type_vals(result)
                    if find_leave_type:
                        find_leave_type.write(leave_type_vals)
                    else:
                        self.env['hr.leave.type'].create(leave_type_vals)
                    count += 1

                except Exception as e:
                    failed += 1
                    self.create_fail_log(
                        name=result.get('id'),
                        field_type='hr_leave_basic',
                        error=e,
                        import_json=result,
                    )

            if count > 0:
                self.create_leave_log(
                    field_type='hr_leave_basic', error="%s Leave Types Imported Successfully" % (count), state='success')
            if failed > 0:
                self.create_leave_log(
                    field_type='hr_leave_basic', error="%s Leave Types Failed To Import." % (failed))
        else:
            self.create_leave_log(
                field_type='hr_leave_basic', error=response.text)

    # ==================================== Employee Tags ======================================

    def prepare_emp_tag_vals(self, emp_tag_dict):
        prepare_emp_tag_vals = {
            'remote_emp_tag_id': emp_tag_dict.get('id'),
            'name': emp_tag_dict.get('name'),
            'color': emp_tag_dict.get('color'),
            'display_name': emp_tag_dict.get('display_name')
        }
        self.map_employee_ids(emp_tag_dict, prepare_emp_tag_vals)
        return prepare_emp_tag_vals

    def import_hr_employee_category(self):
        ''' ========== Import Employee Category (hr.employee.category)  ==================  '''

        response = requests.get(
            '%s/api/public/hr.employee.category?query={id,name,color,display_name,employee_ids}' % (self.base_url))

        response_json = response.json()

        if response.status_code == 200:
            count = 0
            failed = 0

            for result in response_json['result']:
                try:
                    domain = ['|', ('remote_emp_tag_id', '=', result.get('id')),
                              ('name', '=', result.get('name'))]
                    find_emp_tag = self.env['hr.employee.category'].search(
                        domain)
                    emp_tag_vals = self.prepare_emp_tag_vals(result)
                    if find_emp_tag:
                        find_emp_tag.write(emp_tag_vals)
                    else:
                        self.env['hr.employee.category'].create(emp_tag_vals)
                    count += 1

                except Exception as e:
                    failed += 1
                    self.create_fail_log(
                        name=result.get('id'),
                        field_type='hr_leave_basic',
                        error=e,
                        import_json=result,
                    )

            if count > 0:
                self.create_leave_log(
                    field_type='hr_leave_basic', error="%s Employee Category Imported Successfully" % (count), state='success')
            if failed > 0:
                self.create_leave_log(
                    field_type='hr_leave_basic', error="%s Employee Category Failed To Import." % (failed))
        else:
            self.create_leave_log(
                field_type='hr_leave_basic', error=response.text)

    # ==================================== Leave Allocation ======================================

    def prepare_allocation_vals(self, allocation_dict):
        # not mapped fields: accrual_limit,number_per_interval,unit_per_interval,interval_unit,interval_number
        allocation_vals = {
            'remote_allocation_id': allocation_dict.get('id'),
            'mode_company_id': 1,
            'name': allocation_dict.get('name'),
            'notes': allocation_dict.get('notes'),
            'can_reset': allocation_dict.get('can_reset'),
            'can_approve': allocation_dict.get('can_approve'),
            'display_name': allocation_dict.get('display_name'),
            'state': allocation_dict['state']['sh_api_current_state'],
            'type_request_unit': allocation_dict['type_request_unit']['sh_api_current_state'],
            'holiday_type': allocation_dict['holiday_type']['sh_api_current_state'],
        }
        if allocation_dict.get('number_of_days_display'):
            allocation_vals['number_of_days_display'] = allocation_dict.get(
                'number_of_days_display')
        if allocation_dict.get('number_of_days'):
            allocation_vals['number_of_days'] = allocation_dict.get(
                'number_of_days')
        if allocation_dict.get('number_of_hours_display'):
            allocation_vals['number_of_hours_display'] = allocation_dict.get(
                'number_of_hours_display')
        if allocation_dict.get('duration_display'):
            allocation_vals['duration_display'] = allocation_dict.get(
                'duration_display')

        # To map allocation_type
        if allocation_dict.get('accrual'):
            allocation_vals['allocation_type'] = 'accrual'

        # ======================= Date Fields =======================

        # Map Datetiem to date
        if allocation_dict.get('date_from'):
            date_time = datetime.strptime(
                allocation_dict.get('date_from'), '%Y-%m-%d-%H-%M-%S')
            allocation_vals['date_from'] = date_time.date()
        # Map Datetiem to date
        if allocation_dict.get('date_to'):
            date_time = datetime.strptime(
                allocation_dict.get('date_to'), '%Y-%m-%d-%H-%M-%S')
            allocation_vals['date_to'] = date_time.date()

        self.date_vals(
            allocation_dict, allocation_vals, 'nextcall')

        self.date_vals(
            allocation_dict, allocation_vals, 'date_start')

        self.date_vals(
            allocation_dict, allocation_vals, 'date_end')

        # ======================= Relational Fields =======================

        self.map_many2one_field(
            'hr.leave.type', 'remote_leave_type_id', allocation_dict, allocation_vals, 'holiday_status_id')
        if not allocation_vals.get('holiday_status_id'):
            self.create_fail_log(
                name=allocation_dict.get('id'),
                field_type='hr_leave_basic',
                error='Time of type of this request is missing.',
                import_json=allocation_dict,
            )
            return False

        self.map_many2one_field(
            'hr.employee', 'remote_hr_employee_id', allocation_dict, allocation_vals, 'employee_id')
        if allocation_vals['holiday_type'] == 'employee' and not allocation_vals.get('employee_id'):
            self.create_fail_log(
                name=allocation_dict.get('id'),
                field_type='hr_leave_basic',
                error='The Employee of this request is missing.',
                import_json=allocation_dict,
            )
            return False

        self.map_many2one_field(
            'hr.employee', 'remote_hr_employee_id', allocation_dict, allocation_vals, 'first_approver_id', 'approver_id')

        # department_id
        self.find_department_sort(allocation_dict, allocation_vals)
        if allocation_vals['holiday_type'] == 'department' and not allocation_vals.get('department_id'):
            self.create_fail_log(
                name=allocation_dict.get('id'),
                field_type='hr_leave_basic',
                error='Department of this request is missing.',
                import_json=allocation_dict,
            )
            return False
        self.find_or_create_employee_tag(
            allocation_dict, allocation_vals, 'category_id')
        if allocation_vals['holiday_type'] == 'category' and not allocation_vals.get('category_id'):
            self.create_fail_log(
                name=allocation_dict.get('id'),
                field_type='hr_leave_basic',
                error='Employee Tag of this request is missing.',
                import_json=allocation_dict,
            )
            return False

        # ============ PREAPRE PARTNER'S CHILD PARTNER'S DATA ==============
        if allocation_dict.get('linked_request_ids'):
            child_list = []
            for child in allocation_dict['linked_request_ids']:
                child_vals = self.prepare_allocation_vals(child)
                domain = [('remote_allocation_id', '=', child['id'])]
                find_child = self.env['hr.leave.allocation'].search(domain)
                if not find_child:
                    child_list.append((0, 0, child_vals))
            if child_vals:
                allocation_vals['linked_request_ids'] = child_list

        return allocation_vals

    def is_leave_allocation_can_be_create(self, result):
        if not result.get('id'):
            self.create_fail_log(
                name=result.get('id'),
                field_type='hr_leave_basic',
                error='Id not fount!.',
                import_json=result,
            )
            return False

        if not result.get('holiday_status_id'):
            self.create_fail_log(
                name=result.get('id'),
                field_type='hr_leave_basic',
                error='Time of type of this request is missing.',
                import_json=result,
            )
            return False

        if not result.get('holiday_type'):
            self.create_fail_log(
                name=result.get('id'),
                field_type='hr_leave_basic',
                error='Mode of this request is missing.',
                import_json=result,
            )
            return False
        else:
            if result['holiday_type'] == 'employee':
                if not result.get('employee_id'):
                    self.create_fail_log(
                        name=result.get('id'),
                        field_type='hr_leave_basic',
                        error='The Employee of this request is missing.',
                        import_json=result,
                    )
                    return False
            elif result['holiday_type'] == 'category':
                if not result.get('category_id'):
                    self.create_fail_log(
                        name=result.get('id'),
                        field_type='hr_leave_basic',
                        error='Employee Tag of this request is missing.',
                        import_json=result,
                    )
                    return False
            elif result['holiday_type'] == 'department':
                if not result.get('department_id'):
                    self.create_fail_log(
                        name=result.get('id'),
                        field_type='hr_leave_basic',
                        error='Department of this request is missing.',
                        import_json=result,
                    )
                    return False
        return True

    def import_hr_leave_allocation(self):
        ''' ========== Import Allocations (hr.leave.allocation)  ==================  '''
        config = self.env['sh.import.base'].search([], limit=1)
        api_endpoint = '''%s/api/public/hr.leave.allocation?query={%s}
            ''' % (self.base_url, self.query['hr_leave_allocation'])
        response = requests.get(api_endpoint)

        response_json = response.json()
        if response.status_code == 200:
            count = 0
            failed = 0

            for result in response_json['result']:
                try:
                    if not config.is_leave_allocation_can_be_create(result):
                        failed += 1
                        continue

                    domain = [('remote_allocation_id', '=', result.get('id'))]
                    find_allocation = self.env['hr.leave.allocation'].search(
                        domain)
                    allocation_vals = self.prepare_allocation_vals(result)
                    if not allocation_vals:
                        failed += 1
                        continue
                    if find_allocation:
                        find_allocation.write(allocation_vals)
                    else:
                        self.env['hr.leave.allocation'].create(allocation_vals)
                    count += 1

                except Exception as e:
                    failed += 1
                    self.create_fail_log(
                        name=result.get('id'),
                        field_type='hr_leave_basic',
                        error=e,
                        import_json=result,
                    )

            if count > 0:
                self.create_leave_log(
                    field_type='hr_leave_basic', error="%s Allocations Imported Successfully" % (count), state='success')
            if failed > 0:
                self.create_leave_log(
                    field_type='hr_leave_basic', error="%s Allocations Failed To Import." % (failed))
        else:
            self.create_leave_log(
                field_type='hr_leave_basic', error=response.text)
