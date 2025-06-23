# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
import requests


class ShEmpProfessionalExperience(models.Model):
    _inherit = 'sh.emp.professional.experience'

    remote_sh_emp_professional_experience_id = fields.Char(
        "Remote Emp Professional Experience ID",copy=False)


class InheritImportEmployee(models.Model):
    _inherit = "sh.import.base"

    def import_sh_emp_professional_experience(self):

        confid = self.env['sh.import.base'].search([], limit=1)
        response = requests.get(
            '''%s/api/public/sh.emp.professional.experience''' % (confid.base_url))

        if response.status_code == 200:
            response_json = response.json()

    def prepare_sh_emp_professional_experience_vals(self, data):
        emp_professional_experience = {
            'remote_sh_emp_professional_experience_id': data.get('id'),
            "location": data.get('location'),
            "display_name": data.get('display_name'),
        }

        if data.get('job_title_id'):
            if data.get('job_title_id').get('id') and data.get('job_title_id').get('id') != 0:
                domain = [('remote_hr_job_id', '=',
                           data['job_title_id']['id'])]
                find_rec = self.env['hr.job'].search(domain)
                if find_rec:
                    emp_professional_experience['job_title_id'] = find_rec.id
                else:
                    rec_vals = {
                        'remote_hr_job_id': data.get('job_title_id').get('id'),
                        'name': data.get('job_title_id').get('name'),
                    }
                    create_rec = self.env['hr.job'].create(rec_vals)
                    if create_rec:
                        emp_professional_experience['job_title_id'] = create_rec.id

        self.date_vals(data, emp_professional_experience,
                       data_key='start_date')
        self.date_vals(data, emp_professional_experience, data_key='end_date')

        return emp_professional_experience
