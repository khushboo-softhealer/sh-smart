# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
import requests
import json
from datetime import datetime

class InheritImportHrdepartment(models.Model):
    _inherit = "sh.import.base"

    def prepare_hr_department(self,data):

        hr_department_vals={
            'remote_hr_department_id' : data['id'],
            'name':data['name'],
            'display_name':data['display_name'],
            'color':data['color'],
            'complete_name':data['complete_name'],
            'note':data['note'],

            # ----------------------------
            'expected_employee':data['expected_employee'],
            'expense_sheets_to_approve_count':data['expense_sheets_to_approve_count'],
            'new_applicant_count':data['new_applicant_count'],
            'absence_of_today':data['absence_of_today'],
            'allocation_to_approve_count':data['allocation_to_approve_count'],
            'new_hired_employee':data['new_hired_employee'],
            'total_employee':data['total_employee'],
            # 'leave_to_approve_count':data['leave_to_approve_count'],
            'leave_to_approve_count':data.get('leave_to_approve_count'),

            # -----custom fields-------------


            # 'message_attachment_count':data['message_attachment_count'],
            # 'message_has_error':data['message_has_error'],
            # 'message_has_error_counter':data['message_has_error_counter'],
            # 'message_needaction_counter':data['message_needaction_counter'],
            # 'message_needaction':data['message_needaction'],
            # 'message_is_follower':data['message_is_follower'],

            # 'member_ids' : data['member_ids'],
            # 'parent_id' : data['parent_id'],
            # 'child_ids' : data['child_ids'],
            # 'manager_id' : data['manager_id'],
            # 'job_ids' : data['manager_id'],
        }

        # ======== Get Manager if already created or create =========        

        if data.get('manager_id'):
            domain = [('remote_hr_employee_id', '=', data['manager_id'])]
            find_employee = self.env['hr.employee'].search(domain)
            if find_employee:
                hr_department_vals['manager_id'] = find_employee.id
            # else:
            #     employee_vals=self.process_employee_data(data['manager_id'])
            #     employee_id=self.env['hr.employee'].create(employee_vals)
            #     if employee_id:
            #         hr_department_vals['manager_id']=employee_id.id

         # ======== Get Parent Id if already created or create =========        

        # if data.get('parent_id') and data['parent_id']['id'] and data['parent_id']['id']!=0:
        #     domain = [('remote_hr_department_id', '=', data['parent_id']['id'])]
        #     find_department = self.env['hr.department'].search(domain)
        #     if find_department:
        #         hr_department_vals['parent_id'] = find_department.id
        #     else:
        #         department_vals=self.prepare_hr_department(data['parent_id'])
        #         parent_id=self.env['hr.department'].create(department_vals)
        #         if parent_id:
        #             hr_department_vals['parent_id']=parent_id.id

         # ======== Get Parent Id if already created or create =========        

        if data.get('member_ids'):
            employee_list=[]
            for employee_id in data['member_ids']:
                domain = [('remote_hr_employee_id', '=', employee_id)]
                find_employee = self.env['hr.employee'].search(domain)
                if find_employee:
                    employee_list.append((4,find_employee.id))
            hr_department_vals['member_ids'] = employee_list



        # ======== Get Parent Id if already created or create =========

        if data.get('child_ids'):
            child_list = []
            for child in data['child_ids']:
                child_vals = self.prepare_hr_department(child)
                domain = [('remote_hr_department_id', '=', child['id'])]
                find_child = self.env['hr.department'].search(domain)
                if not find_child:
                    child_vals = self.prepare_hr_department(child)
                    child_list.append((0,0,child_vals))
                else:
                    child_list.append((4,find_child.id))

            hr_department_vals['child_ids'] = child_list

        # ======== Get Job ids if already created or create =========        

        if data.get('jobs_ids'):
            job_list = []
            for job_id in data['jobs_ids']:
                domain = [('remote_hr_job_id', '=', job_id)]
                find_job = self.env['hr.job'].search(domain)
                if find_job:
                    job_list.append((4,find_job.id))

            hr_department_vals['jobs_ids'] = job_list

        # ======== Chatter Codde  =========        

        # if data.get('message_ids'):
        #     message_list=self.process_message_data(data.get('message_ids'))
        #     if message_list:
        #         hr_department_vals['message_ids']=message_list

        # if data.get('message_main_attachment_id'):
        #     attchment=self.process_ir_attchment_data(data.get('message_main_attachment_id'))
        #     if attchment:
        #         if attchment.get('res_model') and attchment['res_model']=='helpdesk.ticket':
        #             attchment['res_model']='sh.helpdesk.ticket'
        #         main_attachment=self.env['ir.attachment'].create(attchment)
        #         hr_department_vals['message_main_attachment_id']=main_attachment.id

        # if data.get('message_partner_ids'):
        #     partner_list=[]
        #     for m_partner in data.get('message_partner_ids'):
        #         domain = [('remote_res_partner_id', '=',m_partner['id'])]
        #         find_customer = self.env['res.partner'].search(domain)
                
        #         if find_customer:
        #             partner_list.append((4,find_customer.id))
        #         else:
        #             contact_vals=self.process_contact_data(m_partner)
        #             partner_id=self.env['res.partner'].create(contact_vals)
        #             if partner_id:
        #                 partner_list.append((4,partner_id.id))
                        
        #     hr_department_vals['message_partner_ids']=partner_list

        return hr_department_vals
