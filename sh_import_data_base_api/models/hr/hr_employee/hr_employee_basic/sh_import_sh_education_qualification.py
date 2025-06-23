# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
import requests
import json
from datetime import datetime


# -------------------- OTHER CODE ----------------------------

class HhEducationQualification(models.Model):
    _inherit = 'sh.education.qualification'

    remote_sh_education_qualification_id = fields.Char(
        "Remote Education Qualification Id",copy=False)

# ------------------------------------------------------------


class InheritImportHrRuleImport(models.Model):
    _inherit = "sh.import.base"
    # json_field = fields.Text('JOSN Data')

    def import_sh_education_qualification(self):
        ''' ========== Connect db for import payslip run  ==================  '''
        config = self.env['sh.import.base'].search([], limit=1)

        response = requests.get('''%s/api/public/sh.education.qualification?query={%s}''' % (
            config.base_url, self.query_dict['sh_education_qualification']))
        response_json = response.json()
        self.json_field = response_json

        if response.status_code == 200:
            count = 0
            for data in response_json['result']:
                qualification_vals = config.prepare_sh_education_qualification_vals(
                    data)
                domain = [
                    ('remote_sh_education_qualification_id', '=', data['id'])]
                find_qualification_id = self.env['sh.education.qualification'].search(
                    domain)
                # try:
                if find_qualification_id:
                    count += 1
                    find_qualification_id.write(qualification_vals)
                else:
                    count += 1
                    self.env['sh.education.qualification'].create(
                        qualification_vals)

            if count > 0:
                self.create_log(
                    field_type='hr_employee_basic', error="%s Education Qualification Imported Successfully" % (count), state='success')

        else:
            self.create_log(
                field_type='hr_employee_basic', error=response.text)

    def prepare_sh_education_qualification_vals(self, data):

        sh_education_qualification_vals = {
            'remote_sh_education_qualification_id': data['id'],
            'display_name': data['display_name'],
            'institutes': data['institutes'],
            'score': data['score'],
            'transcript': data['transcript'],
        }

        if data.get('quo_year') != '':
            sh_education_qualification_vals['quo_year'] = data.get('quo_year')

        # # ======== Get edu_employee_id  =========

        # if data.get('edu_employee_id'):
        #     domain = [('remote_hr_employee_id', '=', data['edu_employee_id'])]
        #     find_employee = self.env['hr.employee'].search(domain)
        #     if find_employee:
        #         sh_education_qualification_vals['edu_employee_id'] = find_employee.id

        # # ======== Get degree_id if already created or create =========

        if data.get('degree_id'):
            domain = [('remote_sh_degree_id', '=', data['degree_id']['id'])]
            find_degree = self.env['sh.degree'].search(domain)
            if find_degree:
                sh_education_qualification_vals['degree_id'] = find_degree.id
            else:
                degree_vals = {
                    'remote_sh_degree_id': data['degree_id'].get('id'),
                    'name': data['degree_id'].get('name'),
                    'display_name': data['degree_id'].get('display_name'),
                }
                degree_id = self.env['sh.degree'].create(degree_vals)
                if degree_id:
                    sh_education_qualification_vals['degree_id'] = degree_id.id

        return sh_education_qualification_vals
