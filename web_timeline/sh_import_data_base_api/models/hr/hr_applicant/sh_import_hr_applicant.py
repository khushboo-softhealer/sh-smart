# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields
import requests
from datetime import datetime


class InheritImportBase(models.Model):
    _inherit = "sh.import.base"

    is_import_applicant = fields.Boolean("Import Applicants")
    applicant_records_per_page = fields.Integer("No of records per page")
    current_import_page_applicant = fields.Integer("Current Applicant Page", default=0)
    application_ids=fields.Char("Applications")


    def create_recruitment_log(
        self,
        field_type='hr_applicant',
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

    def process_hr_applicant_vals(self, result):

        # Required field 'name'
        if not result.get('name'):
            return False

        # ========================== Normal Fields ==========================

        vals = {
            'remote_hr_applicant_id': result.get('id'),
            'company_id': 1,
            'name': result.get('name'),
            'partner_name': result.get('partner_name'),
            'email_from': result.get('email_from'),
            'email_cc': result.get('email_cc'),
            'partner_phone': result.get('partner_phone'),
            'partner_mobile': result.get('partner_mobile'),
            'salary_expected': result.get('salary_expected'),
            'salary_proposed': result.get('salary_proposed'),
            'description': result.get('description'),
            'active': result.get('active'),
            'color': result.get('color'),
            'day_close': result.get('day_close'),
            'day_open': result.get('day_open'),
            'delay_close': result.get('delay_close'),
            'display_name': result.get('display_name'),
            'employee_name': result.get('employee_name'),
            'probability': result.get('probability'),
            'salary_proposed_extra': result.get('salary_proposed_extra'),
            'salary_expected_extra': result.get('salary_expected_extra'),
            'user_email': result.get('user_email'),
            'legend_blocked': result.get('legend_blocked'),
            'legend_done': result.get('legend_done'),
            'legend_normal': result.get('legend_normal'),
            # ======= Added after =======
            'attachment_number': result.get('attachment_number'),
            'sh_hr_placement_is_confirm': result.get('sh_hr_placement_is_confirm'),
            'hide_button_bool': result.get('hide_button_bool'),
            'interview_type': result.get('interview_type').get('sh_api_current_state'),
        }

        # ======================= Date/Datetime Fields =======================
        self.datetime_vals(result, vals, 'sh_hr_placement_schedule_datetime')

        if result.get('availability'):
            date_time = datetime.strptime(
                result.get('availability'), '%Y-%m-%d')
            vals['availability'] = date_time

        if result.get('date_closed'):
            date_time = datetime.strptime(
                result.get('date_closed'), '%Y-%m-%d-%H-%M-%S')
            date_time = date_time.strftime('%Y-%m-%d %H:%M:%S')
            vals['date_closed'] = date_time

        if result.get('date_last_stage_update'):
            date_time = datetime.strptime(
                result.get('date_last_stage_update'), '%Y-%m-%d-%H-%M-%S')
            date_time = date_time.strftime('%Y-%m-%d %H:%M:%S')
            vals['date_last_stage_update'] = date_time

        if result.get('date_open'):
            date_time = datetime.strptime(
                result.get('date_open'), '%Y-%m-%d-%H-%M-%S')
            date_time = date_time.strftime('%Y-%m-%d %H:%M:%S')
            vals['date_open'] = date_time

        # ======================= Selection Fields =======================

        if result.get('priority'):
            vals['priority'] = result['priority']['sh_api_current_state']

        if result.get('kanban_state'):
            vals['kanban_state'] = result['kanban_state']['sh_api_current_state']

        # ======================= Relational(many2one) Fields =======================

        self.map_many2one_field(
            'res.users', 'remote_res_user_id', result, vals, 'user_id')
        self.map_many2one_field(
            'sh.placement', 'remote_sh_placement_id', result, vals, 'placement_id')
        self.map_many2one_field(
            'sh.college', 'remote_sh_college_id', result, vals, 'college_id')
        self.map_employee_ids(result, vals, 'interview_ids')
        self.map_many2one_field(
            'sh.proposal.reject.reasons', 'remote_sh_proposal_reject_reason_id', result, vals, 'reject_reason_id')

        if result.get('type_id'):
            if result['type_id']['id'] != 0:
                domain = ['|', ('remote_degree_id', '=', result['type_id']['id']),
                          ('name', '=', result['type_id']['name'])]
                find_rec = self.env['hr.recruitment.degree'].search(domain)
                if find_rec:
                    vals['type_id'] = find_rec.id
                else:
                    degree_vals = {
                        'remote_degree_id': result['type_id']['id'],
                        'name': result['type_id']['name'],
                        'display_name': result['type_id']['display_name'],
                        'sequence': result['type_id']['sequence'],
                    }
                    created_degree = self.env['hr.recruitment.degree'].create(
                        degree_vals)
                    if created_degree:
                        vals['type_id'] = created_degree.id

        if result.get('source_id'):
            if result['source_id']['id'] != 0:
                domain = ['|', ('remote_source_id', '=', result['source_id']['id']),
                          ('name', '=', result['source_id']['name'])]
                find_rec = self.env['utm.source'].search(domain)
                if find_rec:
                    vals['source_id'] = find_rec.id
                else:
                    source_vals = {
                        'remote_source_id': result['source_id']['id'],
                        'name': result['source_id']['name'],
                        'display_name': result['source_id']['display_name'],
                    }
                    created_rec = self.env['utm.source'].create(source_vals)
                    if created_rec:
                        vals['source_id'] = created_rec.id

        if result.get('medium_id'):
            if result['medium_id']['id'] != 0:
                domain = ['|', ('remote_medium_id', '=', result['medium_id']['id']),
                          ('name', '=', result['medium_id']['name'])]
                find_rec = self.env['utm.medium'].search(domain)
                if find_rec:
                    vals['medium_id'] = find_rec.id

        self.map_many2one_field(
            'hr.employee', 'remote_hr_employee_id', result, vals, 'emp_id')
        self.map_res_partner(result, vals)
        self.map_hr_recruitment_stage(result, vals, 'last_stage_id')
        self.map_many2one_field(
            'hr.recruitment.stage', 'remote_recruitment_stage_id', result, vals, 'stage_id')
        self.find_department_sort(result, vals)
        # self.map_many2one_field(
        #     'hr.job', 'remote_hr_job_id', result, vals, 'job_id')


        # ======================= Relational(many2many) Fields =======================

        if result.get('categ_ids'):
            if len(result.get('categ_ids')) > 0:
                categ_ids = []
                for categ in result.get('categ_ids'):
                    domain = ['|', ('remote_category_id', '=', categ.get('id')),
                              ('name', '=', categ.get('name'))]
                    find_rec = self.env['hr.applicant.category'].search(
                        domain)
                    if find_rec:
                        categ_ids.append((4, find_rec.id))
                    else:
                        categ_vals = {
                            'remote_category_id': categ.get('id'),
                            'name': categ.get('name'),
                            'color': categ.get('color'),
                            'display_name': categ.get('display_name'),
                        }
                        categ_rec = self.env['hr.applicant.category'].create(
                            categ_vals)
                        if categ_rec:
                            categ_ids.append((4, categ_rec.id))
                if categ_ids:
                    vals['categ_ids'] = categ_ids

        return vals

    def import_hr_applicant(self):
        confid = self.env['sh.import.base'].search([], limit=1)

        confid.current_import_page_applicant += 1

        # response = requests.get(
        #     '%s/api/public/hr.applicant?query={%s}&page_size=%s&page=%s' % (confid.base_url, self.query.get('hr_applicant'), confid.applicant_records_per_page, confid.current_import_page_applicant))
        response = requests.get(
            '%s/api/public/hr.applicant?query={%s}' % (confid.base_url, self.query.get('hr_applicant')))
        response_json = response.json()

        if response.status_code == 200 and not response_json.get('error') != '0':

            # ======= CHECK RECORD PER PAGE IS NOT EQUAL TO COUNT THEN IMPORT APPLICANT FALSE =============

            # if confid.applicant_records_per_page != response_json['count']:
            #     confid.is_import_applicant = False
            #     confid.current_import_page_applicant = 0

            count = 0
            fail = 0

            for applicant in response_json['result']:
                try:
                    if not applicant.get('id'):
                        continue
                    domain = [
                        ('remote_hr_applicant_id', '=', applicant['id'])]
                    find_applicant = self.env['hr.applicant'].search(
                        domain)
                    applicant_vals = self.process_hr_applicant_vals(
                        applicant)
                    if not applicant_vals:
                        continue
                    if find_applicant:
                        find_applicant.sudo().write(applicant_vals)
                    else:
                        self.env['hr.applicant'].sudo().create(
                            applicant_vals)
                    count += 1

                except Exception as e:
                    fail += 1
                    self.create_fail_log(
                        name=applicant.get('id'),
                        field_type='hr_applicant',
                        error=e,
                        import_json=applicant,
                    )

            if count > 0:
                self.create_recruitment_log(
                    error="%s Hr Applicants Imported Successfully" % (count), state='success')
            if fail > 0:
                self.create_recruitment_log(
                    field_type='hr_applicant', error="%s Applicants Failed To Import." % (fail))
        else:
            self.create_recruitment_log(error=response.text)


    def import_hr_applicant_filtered(self):
        confid = self.env['sh.import.base'].search([],limit=1)
        if confid.application_ids:   
            applications = confid.application_ids.strip('][').split(', ')
            count=0
            fail=0  
            for application in applications[0:50]:
                # confid.current_import_page_applicant += 1

                # response = requests.get(
                #     '%s/api/public/hr.applicant?query={%s}&page_size=%s&page=%s' % (confid.base_url, self.query.get('hr_applicant'), confid.applicant_records_per_page, confid.current_import_page_applicant))
                response = requests.get(
                    '%s/api/public/hr.applicant/%s?query={%s}&filter=["|",["active","=",true],["active","=",false]]' % (confid.base_url,application, self.query.get('hr_applicant')))
                response_json = response.json()
                print("\n\n======response_json",response_json)
                if response.status_code == 200 and not response_json.get('error') != '0':

                    # ======= CHECK RECORD PER PAGE IS NOT EQUAL TO COUNT THEN IMPORT APPLICANT FALSE =============

                    # if confid.applicant_records_per_page != response_json['count']:
                    #     confid.is_import_applicant = False
                    #     confid.current_import_page_applicant = 0

                    # count = 0
                    # fail = 0

                    for applicant in response_json['result']:
                        # try:
                        if not applicant.get('id'):
                            continue
                        domain = [
                            ('remote_hr_applicant_id', '=', applicant['id'])]
                        find_applicant = self.env['hr.applicant'].search(
                            domain)
                        applicant_vals = self.process_hr_applicant_vals(
                            applicant)
                        if not applicant_vals:
                            continue
                        if find_applicant:
                            find_applicant.sudo().write(applicant_vals)
                        else:
                            self.env['hr.applicant'].sudo().create(
                                applicant_vals)
                        count += 1

                        # except Exception as e:
                        #     fail += 1
                        #     self.create_fail_log(
                        #         name=applicant.get('id'),
                        #         field_type='hr_applicant',
                        #         error=e,
                        #         import_json=applicant,
                            # )
            confid.application_ids='['+', '.join([str(elem) for elem in applications[50:]])+']'
            if count > 0:
                self.create_recruitment_log(
                    error="%s Hr Applicants Imported Successfully" % (count), state='success')
            if fail > 0:
                self.create_recruitment_log(
                    field_type='hr_applicant', error="%s Applicants Failed To Import." % (fail))
        # else:
        #     self.create_recruitment_log(error=response.text)
