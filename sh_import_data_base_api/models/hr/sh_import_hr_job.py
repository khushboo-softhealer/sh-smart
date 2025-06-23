# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
import requests
import json
from datetime import datetime
import time

class InheritImportBase(models.Model):
    _inherit = "sh.import.base"

    def import_hr_job(self,data):
        hr_job_vals={
            'remote_hr_job_id' : data['id'],
            'name':data['name'],
            'display_name':data['display_name'],
            'description':data['description'],
            'requirements':data['requirements'],
            'expected_employees' : data['expected_employees'],
            'no_of_employee' : data['no_of_employee'],
            'no_of_recruitment' : data['no_of_recruitment'],
            'no_of_hired_employee' : data['no_of_hired_employee'],

            # ----------------------------------------

            'application_count' : data['application_count'],
            'documents_count' : data['documents_count'],
            'max_salary' : data['max_salary'],
            'min_salary' : data['min_salary'],
            'is_seo_optimized' : data['is_seo_optimized'],
            'is_published' : data['is_published'],

            # ----------------------------------------

        }
        # if data.get('department_id') and data['department_id']['id'] and data['department_id']['id']!=0:
        #     domain = [('remote_hr_department_id', '=', data['department_id']['id'])]
        #     find_department = self.env['hr.department'].search(domain)
        #     if find_department:
        #         hr_job_vals['department_id'] = find_department.id
        #     else:
        #         hr_department_vals=self.import_hr_department(data['department_id'])
        #         department_id=self.env['hr.department'].create(hr_department_vals)
        #         if department_id:
        #             hr_job_vals['department_id']=department_id.id

        # ------- HR RESPONSIBLE ID ----------------

        if data.get('hr_responsible_id'):
            domain_by_id = [('remote_res_user_id','=',data['hr_responsible_id'])]
            find_user_id=self.env['res.users'].search(domain_by_id)
            # domain_by_login = [('login','=',data['hr_responsible_id']['login'])]
            # find_user_login=self.env['res.users'].search(domain_by_login)
            if find_user_id:
                hr_job_vals['hr_responsible_id']=find_user_id.id 
            # elif find_user_login:
            #     hr_job_vals['hr_responsible_id']=find_user_login.id 
            # else:
            #     user_vals=self.process_user_data(data['hr_responsible_id'])       
            #     user_id=self.env['res.users'].create(user_vals)
            #     if user_id:
            #         hr_job_vals['hr_responsible_id']=user_id.id

        # ======== Get Partner if already created or create =========
    
        if data.get('address_id'):
            domain = [('remote_res_partner_id', '=', data['address_id'])]
            find_customer = self.env['res.partner'].search(domain)
            if find_customer:
                hr_job_vals['address_id'] = find_customer.id
            # else:
            #     contact_vals=self.process_contact_data(data['address_id'])
            #     partner_id=self.env['res.partner'].create(contact_vals)
            #     if partner_id:
            #         hr_job_vals['address_id']=partner_id.id

        if data.get('employee_ids'):
            employee_list=[]
            for employee_id in data['employee_ids']:
                domain = [('remote_hr_employee_id', '=', employee_id)]
                find_employee = self.env['hr.employee'].search(domain)
                if find_employee:
                    employee_list.append((4,find_employee.id))

            hr_job_vals['employee_ids'] = employee_list

        # ------------ applicant ids ----------------
        
        if data.get('application_ids'):
            applicant_list=[]
            for applicant_id in data['application_ids']:
                domain = [('remote_hr_applicant_id', '=', applicant_id)]
                find_applicant = self.env['hr.applicant'].search(domain)
                if find_applicant:
                    applicant_list.append((4,find_applicant.id))

            hr_job_vals['application_ids'] = applicant_list

        #------------- document_ids -----------------

        # if data.get('document_ids'):
        #     document_list=[]
        #     for document in data['document_ids']:
        #         domain = [('remote_ir_attachment_id', '=', document['id'])]
        #         find_document = self.env['ir.attachment'].search(domain)
        #         if not find_document:
        #             document_vals = self.process_ir_attchment_data(document)
        #             document_list.append((0,0,document_vals))
        #     hr_job_vals['document_ids'] = document_list

        return hr_job_vals                
