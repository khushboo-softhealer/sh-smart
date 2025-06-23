# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
import requests
import json
from datetime import datetime
from datetime import date

class InheritImportHrContract(models.Model):
    _inherit = "sh.import.base"

    import_attendance=fields.Boolean("Import Attendance")
    records_per_page_attendance = fields.Integer("No of Attendance per page")
    current_import_page_attendance = fields.Integer("Current Attendance Page",default=0) 

    sh_import_filter_attendance=fields.Boolean("Import Filtered Attendance")  
    sh_from_date_attendance=fields.Datetime(" From Date")
    sh_to_date_attendance=fields.Datetime(" To Date") 
    sh_import_attendance_ids=fields.Char("Attendance ids") 




    def import_hr_attendance_modification_request_cron(self):   
        ''' ========== Connect db for import Attendance basic  ==================  '''
        confid = self.env['sh.import.base'].search([],limit=1)
        if confid.import_attendance:
            confid.current_import_page_attendance += 1

            api_endpoint = '''%s/api/public/sh.attendance.modification.request?query={*}&page_size=%s&page=%s''' %(confid.base_url,confid.records_per_page_attendance,confid.current_import_page_attendance)
            response = requests.get(api_endpoint)

            response_json = response.json()
            if response.status_code==200:
                count = 0
                if 'count' in response_json and confid.records_per_page_employee != response_json['count']:
                    confid.import_employee = False
                    confid.current_import_page_employee = 0
                for data in response_json['result']:
                    attendance_req_vals = confid.prepare_hr_attendance_modification_request_vals(data)
                    if not attendance_req_vals:
                        continue
                    domain = [('remote_sh_attendance_modification_request_id', '=', data['id'])]
                    find_attendance_req = self.env['sh.attendance.modification.request'].search(domain)
                    # try:
                    if find_attendance_req:
                        count += 1
                        find_attendance_req.write(attendance_req_vals)                            
                    else:
                        count += 1
                        create_attendance_req=self.env['sh.attendance.modification.request'].create(attendance_req_vals)
                
                if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "hr_attendance",
                        "error": "%s Hr Attendance Modification Request Imported Successfully" %(count),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)

            else:
                vals = {
                    "name": confid.name,
                    "state": "error",
                    "field_type": "hr_attendance",
                    "error": response.text,
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals) 




    def prepare_hr_attendance_modification_request_vals(self,data):
        ''' ============== Import Contracts ==============  '''
        hr_attendance_req_vals={
            'remote_sh_attendance_modification_request_id' : data['id'],
            'checkin_alert':data['checkin_alert'],
            'checkout_alert' : data['checkout_alert'],
            'display_name' : data['display_name'],
            'less_timesheet_alert' : data['less_timesheet_alert'],
            'name' : data['name'],
            'reason' : data['reason'],
            'rejection_reason' : data['rejection_reason'],
            'sh_attendance_count' : data['sh_attendance_count'],
            'sh_leave_count' : data['sh_leave_count'],
            'sh_timesheet_count' : data['sh_timesheet_count'],

            'state' : data.get('state').get('sh_api_current_state'),
            'type' : data.get('type').get('sh_api_current_state'),
            
        }
        if data.get('activity_user_id') and data.get('activity_user_id')!=0:
            domain_by_id = [('remote_res_user_id','=',data['activity_user_id'])]
            find_user_id=self.env['res.users'].search(domain_by_id)
            
            # ======== CHECK IF USER IS CREATED OR NOT IF CREATE THEN RETURN ELSE CREATE =======
            
            if find_user_id:
                hr_attendance_req_vals['activity_user_id']=find_user_id.id 

        if data.get('attendance_id') and data.get('attendance_id')!=0:
            domain_by_id = [('remote_hr_attendance_id','=',data['attendance_id'])]
            find_attendance_id=self.env['hr.attendance'].search(domain_by_id)
            
            # ======== CHECK IF USER IS CREATED OR NOT IF CREATE THEN RETURN ELSE CREATE =======
            
            if find_attendance_id:
                hr_attendance_req_vals['attendance_id']=find_attendance_id.id 

        if data.get('date'):
            date_time=datetime.strptime(data.get('date'),'%Y-%m-%d')
            date_check_in=date_time.strftime('%Y-%m-%d')
            hr_attendance_req_vals['date'] = date_check_in

        if data.get('updated_value'):
            date_time=datetime.strptime(data.get('updated_value'),'%Y-%m-%d-%H-%M-%S')
            date_check_in=date_time.strftime('%Y-%m-%d %H:%M:%S')
            hr_attendance_req_vals['updated_value'] = date_check_in

        if data.get('updated_value_checkout'):
            date_time=datetime.strptime(data.get('updated_value_checkout'),'%Y-%m-%d-%H-%M-%S')
            date_check_in=date_time.strftime('%Y-%m-%d %H:%M:%S')
            hr_attendance_req_vals['updated_value_checkout'] = date_check_in

        if data.get('employee_id') and data['employee_id']!=0:
            domain = [('remote_hr_employee_id', '=', data['employee_id'])]
            find_employee = self.env['hr.employee'].search(domain)
            if find_employee:
                hr_attendance_req_vals['employee_id'] = find_employee.id

        if data.get('user_id') and data['user_id']!=0:
            domain_by_id = [('remote_res_user_id','=',data['user_id']),'|',('active','=',True),('active','=',False)]
            find_user_id=self.env['res.users'].search(domain_by_id)
            if find_user_id:
                hr_attendance_req_vals['user_id'] = find_user_id.id


        return hr_attendance_req_vals






    def import_attendance_filtered_to_queue(self):
        ''' ========== Import Filtered Attendance 
        between from date and end date ==================  ''' 
        confid = self.env['sh.import.base'].search([],limit=1)  
        if confid.sh_import_filter_attendance:
            response = requests.get('''%s/api/public/hr.attendance?query={id,write_date}&filter=[["write_date",">=","%s"],["write_date","<=","%s"]]''' 
                %(confid.base_url,str(confid.sh_from_date_attendance),str(confid.sh_to_date_attendance)))
            response_json = response.json()
            if response_json.get('result'):
                confid.sh_import_attendance_ids=[r['id'] for r in response_json.get('result')]
            else:
                confid.sh_import_attendance_ids=False

    def import_attendance_from_queue(self):   
        ''' ========== Import Attendance ==================  '''
        confid = self.env['sh.import.base'].search([],limit=1)
        if confid.sh_import_filter_attendance and confid.sh_import_attendance_ids:   
            orders = confid.sh_import_attendance_ids.strip('][').split(', ')
            if len(orders) > 0 and orders[0]:   
                count=0
                failed=0
                for attendance_id in orders[0:100]:
                    attendance_query = '''%s/api/public/hr.attendance/%s?query={%s}''' %(confid.base_url,attendance_id,self.query_dict['hr_attendance'])
                    response = requests.get(attendance_query)
                    response_json = response.json()
                    if response.status_code==200:
                        already_attendance=False
                        payment_list=[]
                        for data in response_json.get('result'):
                            domain = [('remote_hr_attendance_id', '=', data['id'])]
                            already_attendance = self.env['hr.attendance'].search(domain)
                            attendance_vals=self.prepare_hr_attendance_vals(data)
                            invoice_dict={}
                            if already_attendance:
                                already_attendance.write(attendance_vals)
                            else:
                                created_attendance=self.env['hr.attendance'].create(attendance_vals)

                            count += 1
                    else:
                        vals = {
                            "name": confid.name,
                            "state": "error",
                            "field_type": "order",
                            "error": response.text,
                            "datetime": datetime.now(),
                            "base_config_id": confid.id,
                            "operation": "import"
                        }
                        self.env['sh.import.base.log'].create(vals)

                if count > 0:              
                        vals = {
                            "name": confid.name,
                            "state": "success",
                            "field_type": "hr_attendance",
                            "error": "%s Hr Attendance Imported Successfully" %(count),
                            "datetime": datetime.now(),
                            "base_config_id": confid.id,
                            "operation": "import"
                        }
                        self.env['sh.import.base.log'].create(vals)
                    # except Exception as e:
                    #     failed += 1
                    #     vals = {
                    #         "name": data['id'],
                    #         "error": e,
                    #         "import_json" : data,
                    #         "field_type": "order",                           
                    #         "datetime": datetime.now(),
                    #         "base_config_id": confid.id,
                    #     }
                    #     self.env['sh.import.failed'].create(vals)
                confid.sh_import_attendance_ids='['+', '.join([str(elem) for elem in orders[100:]])+']'


    def import_hr_attendance_cron(self):   
        ''' ========== Connect db for import Attendance basic  ==================  '''
        confid = self.env['sh.import.base'].search([],limit=1)
        if confid.import_attendance:
            confid.current_import_page_attendance += 1

            api_endpoint = '''%s/api/public/hr.attendance?query={%s}&page_size=%s&page=%s''' %(confid.base_url,self.query_dict['hr_attendance'],confid.records_per_page_attendance,confid.current_import_page_attendance)
            response = requests.get(api_endpoint)


            response_json = response.json()
            if response.status_code==200:
                count = 0
                if 'count' in response_json and confid.records_per_page_employee != response_json['count']:
                    confid.import_employee = False
                    confid.current_import_page_employee = 0
                for data in response_json['result']:
                    attendance_vals = confid.prepare_hr_attendance_vals(data)
                    if not attendance_vals:
                        continue
                    domain = [('remote_hr_attendance_id', '=', data['id'])]
                    find_attendance = self.env['hr.attendance'].search(domain)
                    # try:
                    if find_attendance:
                        count += 1
                        find_attendance.write(attendance_vals)                            
                    else:
                        count += 1
                        create_attendance=self.env['hr.attendance'].create(attendance_vals)
                
                if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "hr_attendance",
                        "error": "%s Hr Attendance Imported Successfully" %(count),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)

            else:
                vals = {
                    "name": confid.name,
                    "state": "error",
                    "field_type": "hr_attendance",
                    "error": response.text,
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals) 
            
    def prepare_hr_attendance_vals(self,data):
        ''' ============== Import Contracts ==============  '''
        hr_attendance_vals={
            'remote_hr_attendance_id' : data['id'],
            'display_name':data['display_name'],
            'worked_hours' : data['worked_hours'],

            # -----custom fields ---------------

            'att_duration' : data['att_duration'],
            'check_in_url' : data['check_in_url'],
            'check_out_url' : data['check_out_url'],
            'in_latitude' : data['in_latitude'],
            'in_longitude' : data['in_longitude'],
            'message_in' : data['message_in'],
            'message_out' : data['message_out'],
            'other_data' : data['other_data'],
            'out_latitude' : data['out_latitude'],
            'out_longitude' : data['out_longitude'],
            'sh_break_reason' : data['sh_break_reason'],
            'sh_break_duration' : data['sh_break_duration'],
            'sh_break_over' : data['sh_break_over'],
            'sh_duration' : data['sh_duration'],
            'sh_remark' : data['sh_remark'],
            'total_time' : data['total_time'],
        }

        if data.get('check_in'):
            date_time=datetime.strptime(data.get('check_in'),'%Y-%m-%d-%H-%M-%S')
            date_check_in=date_time.strftime('%Y-%m-%d %H:%M:%S')
            hr_attendance_vals['check_in'] = date_check_in

        if data.get('check_out'):
            date_time=datetime.strptime(data.get('check_out'),'%Y-%m-%d-%H-%M-%S')
            date_check_out=date_time.strftime('%Y-%m-%d %H:%M:%S')
            hr_attendance_vals['check_out'] = date_check_out

        # ------ custom fields ------------

        if data.get('sh_break_start_date'):
            hr_attendance_vals['sh_break_start_date'] = data.get('sh_break_start_date')

        if data.get('sh_break_start'):
            date_time=datetime.strptime(data.get('sh_break_start'),'%Y-%m-%d-%H-%M-%S')
            date_time=date_time.strftime('%Y-%m-%d %H:%M:%S')
            hr_attendance_vals['sh_break_start'] = date_time

        if data.get('sh_break_end'):
            date_time=datetime.strptime(data.get('sh_break_end'),'%Y-%m-%d-%H-%M-%S')
            date_time=date_time.strftime('%Y-%m-%d %H:%M:%S')
            hr_attendance_vals['sh_break_end'] = date_time


        # ======== Get Employe if already created or create =========

        # if data.get('employee_id') and data['employee_id']['id'] and data['employee_id']['id']!=0:
        #     domain = [('remote_hr_employee_id', '=', data['employee_id']['id'])]
        #     find_employee = self.env['hr.employee'].search(domain)
        #     if find_employee:
        #         hr_attendance_vals['employee_id'] = find_employee.id
        #     else:
        #         employee_vals=self.process_employee_data(data['employee_id'])
        #         employee_id=self.env['hr.employee'].create(employee_vals)
        #         if employee_id:
        #             hr_attendance_vals['employee_id']=employee_id.id 

        if data.get('employee_id'):
            domain = [('remote_hr_employee_id', '=', data['employee_id'])]
            find_employee = self.env['hr.employee'].search(domain)
            if find_employee:
                hr_attendance_vals['employee_id'] = find_employee.id

            # temp_code
            else:
                self.create_fail_log(
                    name=data.get('id'),
                    field_type='hr_attendance',
                    error='Employee not fount!',
                    import_json=data,
                )
                return False
            #     hr_attendance_vals['employee_id'] = 2


        # ======== Get Department if already created or create =========

        # if data.get('department_id') and data['department_id']['id'] and data['department_id']['id']!=0:
        #     domain = [('remote_hr_department_id', '=', data['department_id']['id'])]
        #     find_department = self.env['hr.department'].search(domain)
        #     if find_department:
        #         hr_attendance_vals['department_id'] = find_department.id
        #     else:
        #         hr_department_vals=self.import_hr_department(data['department_id'])
        #         department_id=self.env['hr.department'].create(hr_department_vals)
        #         if department_id:
        #             hr_attendance_vals['department_id']=department_id.id

        if data.get('department_id') and data.get('department_id')!=0:
            domain = [('remote_hr_department_id', '=', data['department_id'])]
            find_department = self.env['hr.department'].search(domain)
            if find_department:
                hr_attendance_vals['department_id'] = find_department.id

        return hr_attendance_vals
