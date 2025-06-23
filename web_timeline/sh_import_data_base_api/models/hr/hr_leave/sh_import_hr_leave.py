# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.


from odoo import models, fields
import requests
import json
from datetime import datetime
is_import_basic_leave = True

class InheritImportBase(models.Model):
    _inherit = "sh.import.base"

    is_import_leaves = fields.Boolean("Import Leaves")
    leave_records_per_page = fields.Integer(
        " No of records per page", default=1)
    current_import_page_leave = fields.Integer("Current Time off Page", default=0)

    def import_hr_leave(self):
        confid = self.env['sh.import.base'].search([], limit=1)
        # confid.import_hr_attendance_cron()
        global is_import_basic_leave

        if is_import_basic_leave:
            confid.import_basic_hr_leave_cron()
            is_import_basic_leave = False
        if confid.is_import_leaves:
            confid.current_import_page_leave += 1

            response = requests.get('''%s/api/public/hr.leave?query={%s}&filter=[["state", "!=", "refuse"]]&page_size=%s&page=%s''' % (
                confid.base_url, self.query['hr_leave'], confid.leave_records_per_page, confid.current_import_page_leave))
            response_json = response.json()
            if response.status_code == 200 and response_json.get('result'):

                # ======= CHECK RECORD PER PAGE IS NOT EQUAL TO COUNT THEN IMPORT LEAVE FALSE =============

                if 'count' in response_json and confid.leave_records_per_page != response_json['count']:
                    confid.is_import_leaves = False
                    confid.current_import_page_leave = 0
                    is_import_basic_leave = True

                count = 0
                failed = 0

                for leave in response_json['result']:
                    # try:
                    if not leave.get('id'):
                        continue
                    if not self.is_leave_can_be_create(leave):
                        failed += 1
                        continue
                    if leave.get('id') in [3740,3791,3789]:
                        continue
                    domain = [('remote_leave_id', '=', leave['id'])]
                    find_leave = self.env['hr.leave'].search(domain)
                    leave_vals = self.process_hr_leave_vals(leave)
                    if not leave_vals:
                        failed += 1
                        continue
                    if find_leave:
                        count +=1
                        # find_leave.write(leave_vals)
                        # continue
                        # print("n\n\========44444444====find_leave",find_leave)
                        # if find_leave.state in ('confirm', 'validate'):
                        #     try:    
                        #         find_leave.action_refuse()
                        #     except Exception as e:
                        #         print(e)
                        # if leave_vals.get('employee_id'):
                        #     # To prevent error from
                        #     # employee_ids += vals['employee_id']
                        #     if leave_vals.get('employee_id') in find_leave.employee_id.ids:
                        #         del leave_vals['employee_id']
                        # try:
                        #     find_leave.write(leave_vals)
                        # except Exception as e:
                        #     print(e)
                    else:
                        try:
                            find_leave = self.env['hr.leave'].create(
                                leave_vals)
                            count +=1
                        except ValueError:
                            if 'request_hour_from' in leave_vals:
                                del leave_vals['request_hour_from']
                            if 'request_hour_to' in leave_vals:
                                del leave_vals['request_hour_to']
                            find_leave = self.env['hr.leave'].create(
                                leave_vals)
                            count +=1
                        except Exception as e:
                            failed += 1
                            self.create_fail_log(
                                name=leave.get('id'),
                                field_type='hr_leave',
                                error=e,
                                import_json=leave,
                            )
                        
                    # try:
                    find_leave.write(
                    {'state': leave['state']['sh_api_current_state']})
                    # except Exception as e:
                    #     print(e)
                    
                    count += 1

                    # except Exception as e:
                    #     failed += 1
                    #     self.create_fail_log(
                    #         name=leave.get('id'),
                    #         field_type='hr_leave',
                    #         error=e,
                    #         import_json=leave,
                    #     )

                if count > 0:
                    self.create_leave_log(
                        error="%s Time Off Imported Successfully" % (count), state='success')
                if failed > 0:
                    self.create_leave_log(
                        field_type='hr_leave', error="%s Time Off Failed To Import." % (failed))
            else:
                if response.status_code == 200 and response_json.get('result') == []:
                    confid.is_import_leaves = False
                    confid.current_import_page_leave = 0
                    is_import_basic_leave = True
                    self.create_leave_log(error='No records found!')
                else:
                    self.create_leave_log(error=response.text)

    def process_hr_leave_vals(self, leave_dict):
        '''Create vals dict for Time Off.'''

        prepare_leave_vals = {
            'remote_leave_id': leave_dict.get('id'),
            'mode_company_id': 1,
            # 'sh_state':leave_dict.get('state').get('sh_api_current_state'),
            # ---------- Selection fields ----------
            # 'state': leave_dict['state']['sh_api_current_state'],
            'validation_type': leave_dict['validation_type']['sh_api_current_state'],
            'tz': leave_dict['tz']['sh_api_current_state'],
            'holiday_type': leave_dict['holiday_type']['sh_api_current_state'],
            'leave_type_request_unit': leave_dict['leave_type_request_unit']['sh_api_current_state'],
            'request_hour_from': leave_dict['custom_hour_from'],
            'request_hour_to': leave_dict['custom_hour_to'],
            'request_date_from_period': leave_dict['request_date_from_period']['sh_api_current_state'],
            # ---------- Other fields ----------
            'name': leave_dict.get('name'),
            'report_note': leave_dict.get('report_note'),
            'tz_mismatch': leave_dict.get('tz_mismatch'),
            'notes': leave_dict.get('notes'),
            'number_of_days': leave_dict.get('number_of_days'),
            'number_of_days_display': leave_dict.get('number_of_days_display'),
            'number_of_hours_display': leave_dict.get('number_of_hours_display'),
            # 'duration_display': leave_dict.get('duration_display'),
            'can_reset': leave_dict.get('can_reset'),
            'can_approve': leave_dict.get('can_approve'),
            'request_unit_half': leave_dict.get('request_unit_half'),
            'request_unit_hours': leave_dict.get('request_unit_hours'),
            'activity_summary': leave_dict.get('activity_summary'),
            'display_name': leave_dict.get('display_name'),
            # ---------- Added after ----------
            'created_leave': leave_dict.get('created_leave'),
            'automatic': leave_dict.get('automatic'),
            'sh_timesheet_count': leave_dict.get('sh_timesheet_count'),
            'sh_attendance_count': leave_dict.get('sh_attendance_count'),
            'leaves_count': leave_dict.get('leaves_count'),
            'leave_taken_3_month': leave_dict.get('leave_taken_3_month'),
            # 'custom_hour_from': leave_dict.get('custom_hour_from'),
            # 'custom_hour_to': leave_dict.get('custom_hour_to'),
            'available_leaves': leave_dict.get('available_leaves'),
            'total_taken_leave_in_current_contract': leave_dict.get('total_taken_leave_in_current_contract'),
            'bool_field': leave_dict.get('bool_field'),
            'alert_leave': leave_dict.get('alert_leave'),
            'leave_days': leave_dict.get('leave_days'),
            'warning': leave_dict.get('warning'),
            'is_desc_hide': leave_dict.get('is_desc_hide'),
            'is_required_attach': leave_dict.get('leave_attach'),
            'is_sick_leave': leave_dict.get('is_sick_leave'),
        }

        if leave_dict.get('number_of_days_display'):
            prepare_leave_vals['number_of_days_display'] = leave_dict.get(
                'number_of_days_display')
        if leave_dict.get('number_of_days'):
            prepare_leave_vals['number_of_days'] = leave_dict.get(
                'number_of_days')
        if leave_dict.get('number_of_hours_display'):
            prepare_leave_vals['number_of_hours_display'] = leave_dict.get(
                'number_of_hours_display')
        if leave_dict.get('duration_display'):
            prepare_leave_vals['duration_display'] = leave_dict.get(
                'duration_display')
        # =========== Added after ===========
        self.date_vals(
            leave_dict, prepare_leave_vals, 'request_date_from')
        self.date_vals(
            leave_dict, prepare_leave_vals, 'request_date_to')

        #  prepare Timesheet Data
        if leave_dict.get('timesheet_ids'):
            timesheet_list = self.process_timesheet_data(
                leave_dict.get('timesheet_ids'))
            if timesheet_list:
                prepare_leave_vals['timesheet_ids'] = timesheet_list

        # ======================= Date/Datetime Fields =======================

        self.datetime_vals(
            leave_dict, prepare_leave_vals, 'date_from')
        self.datetime_vals(
            leave_dict, prepare_leave_vals, 'date_to')

        # ======================= Relational(many2one) Fields =======================
        self.map_many2one_field(
            'res.users', 'remote_res_user_id', leave_dict, prepare_leave_vals, 'user_id')

        # Employee
        self.map_many2one_field(
            'hr.employee', 'remote_hr_employee_id', leave_dict, prepare_leave_vals, 'employee_id')
        if prepare_leave_vals['holiday_type'] == 'employee' and not prepare_leave_vals.get('employee_id'):
            self.create_fail_log(
                name=leave_dict.get('id'),
                field_type='hr_leave',
                error='Can not prepare required fields(Employee) for the Leave.',
                import_json=leave_dict,
            )
            return False

        

        # Leave Type
        self.map_many2one_field(
            'hr.leave.type', 'remote_leave_type_id', leave_dict, prepare_leave_vals, 'holiday_status_id')
        if not prepare_leave_vals.get('holiday_status_id'):

            
            self.create_fail_log(
                name=leave_dict.get('id'),
                field_type='hr_leave',
                error='Can not prepare required fields(Time Off Type) for the Leave.',
                import_json=leave_dict,
            )
            return False
        
        # department_id
        self.find_department_sort(leave_dict, prepare_leave_vals)
        if prepare_leave_vals['holiday_type'] == 'department' and not prepare_leave_vals.get('department_id'):
            self.create_fail_log(
                name=leave_dict.get('id'),
                field_type='hr_leave',
                error='Can not prepare required fields(Department) for the Leave.',
                import_json=leave_dict,
            )
            return False
        
        # ======================= Relational Fields =======================

        self.map_many2one_field(
            'hr.employee', 'remote_hr_employee_id', leave_dict, prepare_leave_vals, 'manager_id')

        self.map_many2one_field(
            'hr.employee', 'remote_hr_employee_id', leave_dict, prepare_leave_vals, 'first_approver_id')

        self.map_many2one_field(
            'hr.employee', 'remote_hr_employee_id', leave_dict, prepare_leave_vals, 'second_approver_id')

        self.find_or_create_employee_tag(
            leave_dict, prepare_leave_vals, 'category_id')
        if prepare_leave_vals['holiday_type'] == 'category' and not prepare_leave_vals.get('category_id'):
            self.create_fail_log(
                name=leave_dict.get('id'),
                field_type='hr_leave',
                error='Can not prepare required fields(Employee Tag) for the Leave.',
                import_json=leave_dict,
            )
            return False
        

        # ============ PREAPRE PARTNER'S CHILD PARTNER'S DATA ==============
        if leave_dict.get('linked_request_ids'):
            child_list = []
            for child in leave_dict['linked_request_ids']:
                child_vals = self.process_hr_leave_vals(child)
                domain = [('remote_leave_id', '=', child['id'])]
                find_child = self.env['hr.leave'].search(domain)
                if not find_child:
                    child_list.append((0, 0, child_vals))
            if child_vals:
                prepare_leave_vals['linked_request_ids'] = child_list

        return prepare_leave_vals

    def create_leave_log(
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

    def is_leave_can_be_create(self, result):
        if not result.get('holiday_status_id'):
            self.create_fail_log(
                name=result.get('id'),
                field_type='hr_leave',
                error='Time of type of this request is missing.',
                import_json=result,
            )
            return False

        if not result.get('holiday_type'):
            self.create_fail_log(
                name=result.get('id'),
                field_type='hr_leave',
                error='Mode of this request is missing.',
                import_json=result,
            )
            return False
        else:
            if result['holiday_type'] == 'employee':
                if not result.get('employee_id'):
                    self.create_fail_log(
                        name=result.get('id'),
                        field_type='hr_leave',
                        error='The Employee of this request is missing.',
                        import_json=result,
                    )
                    return False
            elif result['holiday_type'] == 'category':
                if not result.get('category_id'):
                    self.create_fail_log(
                        name=result.get('id'),
                        field_type='hr_leave',
                        error='Employee Tag of this request is missing.',
                        import_json=result,
                    )
                    return False
            elif result['holiday_type'] == 'department':
                if not result.get('department_id'):
                    self.create_fail_log(
                        name=result.get('id'),
                        field_type='hr_leave',
                        error='Department of this request is missing.',
                        import_json=result,
                    )
                    return False
        return True
