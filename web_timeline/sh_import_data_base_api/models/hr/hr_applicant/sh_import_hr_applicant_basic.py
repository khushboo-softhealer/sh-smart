# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models
import requests
from datetime import datetime

class InheritImportHelpdeskBase(models.Model):
    _inherit = "sh.import.base"

    def import_basic_hr_applicant_cron(self):
        ''' ========== Connect db for import Hr Applicant Basic  ==================  '''

        self.import_sh_proposal_reject_reasons()
        self.import_sh_college()
        self.import_sh_placement()
        self.import_hr_recruitment_degree()
        self.import_utm_source()
        
        self.import_hr_applicant_category()
        self.import_recruitment_stage()

    # ================================================================================================

    def import_sh_proposal_reject_reasons(self):
        ''' ========== Import Reject Reasons (sh.proposal.reject.reasons)  ==================  '''

        response = requests.get(
            '%s/api/public/sh.proposal.reject.reasons?query={id,name,display_name}' % (self.base_url))
        response_json = response.json()

        if response.status_code == 200 and response_json.get('error') == '0':
            count = 0
            fail = 0

            for result in response_json['result']:
                try:

                    if not result.get('id'):
                        continue
                    domain = [
                        ('remote_sh_proposal_reject_reason_id', '=', result.get('id'))]
                    find_reject = self.env['sh.proposal.reject.reasons'].search(
                        domain)
                    reject_vals = {
                        'remote_sh_proposal_reject_reason_id': result.get('id'),
                        'name': result.get('name'),
                        'display_name': result.get('display_name'),
                    }
                    if find_reject:
                        find_reject.write(reject_vals)
                    else:
                        self.env['sh.proposal.reject.reasons'].create(
                            reject_vals)
                    count += 1

                except Exception as e:
                    fail += 1
                    self.create_fail_log(
                        name=result.get('id'),
                        field_type='hr_applicant_basic',
                        error=e,
                        import_json=result,
                    )

            if count > 0:
                self.create_recruitment_log(
                    field_type='hr_applicant_basic', error="%s Reject Reasons Imported Successfully." % (count), state='success')
            if fail > 0:
                self.create_recruitment_log(
                    field_type='hr_applicant_basic', error="%s Reject Reasons Failed To Import." % (fail))
        else:
            self.create_recruitment_log(
                field_type='hr_applicant_basic', error=response.text)

    # ================================================================================================

    def prepare_sh_college_vals(self, data):
        if not data.get('name'):
            return False
        college_vals = {
            "remote_sh_college_id": data.get('id'),
            "name": data.get('name'),
            "street": data.get('street'),
            "street2": data.get('street2'),
            "zip": data.get('zip'),
            "city": data.get('city'),
            "tpo_contact_no": data.get('tpo_contact_no'),
            "display_name": data.get('display_name'),
        }

        # To prevent not null constraints errors.
        if data.get('colloge_contact_no'):
            college_vals['colloge_contact_no'] = data.get('colloge_contact_no')
        if data.get('email'):
            college_vals['email'] = data.get('email')

        self.find_or_create_college_stage(data, college_vals)
        self.find_or_create_state(data, college_vals)
        self.map_country(data, college_vals)
        self.map_res_partner_ids(data, college_vals, 'contact_person_ids')

        return college_vals

    def import_sh_college(self):
        ''' ========== Import College (sh.college)  ==================  '''

        response = requests.get(
            '%s/api/public/sh.college?query={%s}' % (self.base_url, self.query.get('sh_college')))
        response_json = response.json()
        print("\n\n======response_json",response_json)
        if response.status_code == 200 and response_json.get('error') == '0':
            count = 0
            fail = 0

            for result in response_json['result']:
                try:
                    if not result.get('id') or result.get('name') == '':
                        continue
                    domain = ['|', ('remote_sh_college_id', '=', result.get('id')),
                                ('name', '=', result.get('name'))]
                    find_college = self.env['sh.college'].search(domain)
                    placement_vals = self.prepare_sh_college_vals(result)
                    if not placement_vals:
                        continue
                    if find_college:
                        find_college.write(placement_vals)
                    else:
                        self.env['sh.college'].create(placement_vals)
                    count += 1

                except Exception as e:
                    fail += 1
                    # self.create_fail_log(
                    #     name=result.get('id'),
                    #     field_type='hr_applicant_basic',
                    #     error=e,
                    #     import_json=result,
                    # )

            # if count > 0:
            #     vals = {
            #         "name": self.name,
            #         "state": "success",
            #         "field_type": "hr_applicant",
            #         "error": "Collage Imported Successfully",
            #         "datetime": datetime.now(),
            #         "base_config_id": self.id,
            #         "operation": "import"
            #     }
            #     self.env['sh.import.base.log'].create(vals)
                # self.create_recruitment_log(
                #     field_type='hr_applicant_basic', error="%s College Imported Successfully" % (count), state='success')
            # if fail > 0:
            #     vals = {
            #         "name": self.name,
            #         "state": "error",
            #         "field_type": "hr_applicant",
            #         "error": "%s College Failed To Import." % (fail),
            #         "datetime": datetime.now(),
            #         "base_config_id": self.id,
            #         "operation": "import"
            #     }
            #     self.env['sh.import.base.log'].create(vals)
                # self.create_recruitment_log(
                #     field_type='hr_applicant_basic', error="%s College Failed To Import." % (fail))
        # else:
        #     self.create_recruitment_log(
        #         field_type='hr_applicant_basic', error=response.text)

    def prepare_placement_line_data(self, data):
        '''
            PREPARE ONE2MANY VALUES FOR PLACEMENT LINE CONNECTED TO
            PLACEMENT , TICKET
        '''
        placement_line_list = []
        for placement in data:
            domain = [('remote_sh_placement_line_id',
                       '=', placement.get('id'))]
            find_placement_line = self.env['sh.placement.line'].search(domain)
            placement_line_vals = {
                "total_candidate_applied": placement.get('total_candidate_applied'),
                "selected_candidate": placement.get('selected_candidate'),
                "present_candidate": placement.get('present_candidate'),
                "absent_candidate": placement.get('absent_candidate'),
                "remote_sh_placement_line_id": placement.get('id'),
                "display_name": placement.get('display_name'),
            }
            self.map_many2one_field(
                'sh.college', 'remote_sh_college_id', placement, placement_line_vals, 'college_id')

            if find_placement_line:
                find_placement_line.write(placement_line_vals)
                placement_line_list.append((4, find_placement_line.id))
            else:
                placement_line_list.append((0, 0, placement_line_vals))
        return placement_line_list

    def prepare_placement_vals(self, result):
        placement_vals = {
            'remote_sh_placement_id': result.get('id'),
            'name': result.get('name'),
            'display_name': result.get('display_name'),
            'note': result.get('note'),
        }
        self.date_vals(result, placement_vals)

        # ============== Prepare placement_line Data =================
        if result.get('placement_line'):
            placement_line_list = self.prepare_placement_line_data(
                result.get('placement_line'))
            if placement_line_list:
                placement_vals['placement_line'] = placement_line_list

        return placement_vals

    def import_sh_placement(self):
        ''' ========== Import Placement (sh.placement)  ==================  '''

        response = requests.get(
            '%s/api/public/sh.placement?query={%s}' % (self.base_url, self.query['sh_placement']))
        response_json = response.json()

        if response.status_code == 200 and response_json.get('error') == '0':
            count = 0
            fail = 0

            for result in response_json.get('result'):
                try:
                    if not result.get('id') or result.get('name') == '':
                        continue
                    domain = ['|', ('remote_sh_placement_id', '=', result.get('id')),
                              ('name', '=', result.get('name'))]
                    find_placement = self.env['sh.placement'].search(domain)
                    placement_vals = self.prepare_placement_vals(result)
                    if find_placement:
                        find_placement.write(placement_vals)
                    else:
                        self.env['sh.placement'].create(placement_vals)
                    count += 1

                except Exception as e:
                    fail += 1
                    self.create_fail_log(
                        name=result.get('id'),
                        field_type='hr_applicant_basic',
                        error=e,
                        import_json=result,
                    )

            if count > 0:
                self.create_recruitment_log(
                    field_type='hr_applicant_basic', error="%s Placement Imported Successfully" % (count), state='success')
            if fail > 0:
                self.create_recruitment_log(
                    field_type='hr_applicant_basic', error="%s Placement Failed To Import." % (fail))
        else:
            self.create_recruitment_log(
                field_type='hr_applicant_basic', error=response.text)

    def import_hr_recruitment_degree(self):
        ''' ========== Import Degree (hr.recruitment.degree)  ==================  '''

        response = requests.get(
            '%s/api/public/hr.recruitment.degree?query={id,name,sequence,display_name}' % (self.base_url))
        response_json = response.json()

        if response.status_code == 200 and response_json.get('error') == '0':
            count = 0
            fail = 0

            for result in response_json['result']:
                try:
                    if not result.get('id') or result.get('name') == '':
                        continue
                    domain = ['|', ('remote_degree_id', '=', result.get('id')),
                              ('name', '=', result.get('name'))]
                    find_rec = self.env['hr.recruitment.degree'].search(
                        domain)
                    vals = {
                        'remote_degree_id': result.get('id'),
                        'name': result.get('name'),
                        'display_name': result.get('display_name'),
                        'sequence': result.get('sequence'),
                    }
                    if find_rec:
                        find_rec.write(vals)
                    else:
                        self.env['hr.recruitment.degree'].create(vals)
                    count += 1

                except Exception as e:
                    fail += 1
                    self.create_fail_log(
                        name=result.get('id'),
                        field_type='hr_applicant_basic',
                        error=e,
                        import_json=result,
                    )

            if count > 0:
                self.create_recruitment_log(
                    field_type='hr_applicant_basic', error="%s Degree Imported Successfully" % (count), state='success')
            if fail > 0:
                self.create_recruitment_log(
                    field_type='hr_applicant_basic', error="%s Degree Failed To Import." % (fail))
        else:
            self.create_recruitment_log(
                field_type='hr_applicant_basic', error=response.text)

    def import_utm_source(self):
        ''' ========== Import Source (utm.source)  ==================  '''

        response = requests.get(
            '%s/api/public/utm.source?query={id,name,display_name}' % (self.base_url))
        response_json = response.json()

        if response.status_code == 200 and response_json.get('error') == '0':
            count = 0
            fail = 0

            for result in response_json['result']:
                try:
                    if not result.get('id') or result.get('name') == '':
                        continue
                    domain = ['|', ('remote_source_id', '=', result.get('id')),
                              ('name', '=', result.get('name'))]
                    find_rec = self.env['utm.source'].search(domain)
                    vals = {
                        'remote_source_id': result.get('id'),
                        'name': result.get('name'),
                        'display_name': result.get('display_name'),
                    }
                    if find_rec:
                        find_rec.write(vals)
                    else:
                        self.env['utm.source'].create(vals)
                    count += 1
                except Exception as e:
                    fail += 1
                    self.create_fail_log(
                        name=result.get('id'),
                        field_type='hr_applicant_basic',
                        error=e,
                        import_json=result,
                    )

            if count > 0:
                self.create_recruitment_log(
                    field_type='hr_applicant_basic', error="%s Source Imported Successfully" % (count), state='success')
            if fail > 0:
                self.create_recruitment_log(
                    field_type='hr_applicant_basic', error="%s Source Failed To Import." % (fail))
        else:
            self.create_recruitment_log(
                field_type='hr_applicant_basic', error=response.text)

    def import_utm_medium(self):
        ''' ========== Import Mediums (utm.medium)  ==================  '''

        response = requests.get(
            '%s/api/public/utm.medium?query={id,name,display_name,active}' % (self.base_url))
        response_json = response.json()

        if response.status_code == 200 and response_json.get('error') == '0':
            count = 0
            fail = 0

            for result in response_json['result']:
                try:
                    if not result.get('id') or result.get('name') == '':
                        continue
                    domain = ['|', ('remote_medium_id', '=', result.get('id')),
                              ('name', '=', result.get('name'))]
                    find_rec = self.env['utm.medium'].search(domain)
                    vals = {
                        'remote_medium_id': result.get('id'),
                        'name': result.get('name'),
                        'display_name': result.get('display_name'),
                        'active': result.get('active'),
                    }
                    if find_rec:
                        find_rec.write(vals)
                    else:
                        self.env['utm.medium'].create(vals)
                    count += 1
                except Exception as e:
                    fail += 1
                    self.create_fail_log(
                        name=result.get('id'),
                        field_type='hr_applicant_basic',
                        error=e,
                        import_json=result,
                    )

            if count > 0:
                self.create_recruitment_log(
                    field_type='hr_applicant_basic', error="%s Medium Imported Successfully" % (count), state='success')
            if fail > 0:
                self.create_recruitment_log(
                    field_type='hr_applicant_basic', error="%s Medium Failed To Import." % (fail))
        else:
            self.create_recruitment_log(
                field_type='hr_applicant_basic', error=response.text)

    def import_hr_applicant_category(self):
        ''' ========== Import Categoty (hr.applicant.category,display_name)  ==================  '''

        response = requests.get(
            '%s/api/public/hr.applicant.category?query={id,name,color,display_name}' % (self.base_url))
        response_json = response.json()

        if response.status_code == 200 and response_json.get('error') == '0':
            count = 0
            fail = 0

            for result in response_json['result']:
                try:
                    if not result.get('id') or result.get('name') == '':
                        continue
                    domain = ['|', ('remote_category_id', '=', result.get('id')),
                              ('name', '=', result.get('name'))]
                    find_rec = self.env['hr.applicant.category'].search(domain)
                    vals = {
                        'remote_category_id': result.get('id'),
                        'name': result.get('name'),
                        'color': result.get('color'),
                        'display_name': result.get('display_name'),
                    }
                    if find_rec:
                        find_rec.write(vals)
                    else:
                        self.env['hr.applicant.category'].create(vals)
                    count += 1
                except Exception as e:
                    fail += 1
                    self.create_fail_log(
                        name=result.get('id'),
                        field_type='hr_applicant_basic',
                        error=e,
                        import_json=result,
                    )

            if count > 0:
                self.create_recruitment_log(
                    field_type='hr_applicant_basic', error="%s Category Imported Successfully" % (count), state='success')
            if fail > 0:
                self.create_recruitment_log(
                    field_type='hr_applicant_basic', error="%s Category Failed To Import." % (fail))
        else:
            self.create_recruitment_log(
                field_type='hr_applicant_basic', error=response.text)

    def prepare_recruitment_stage_vals(self, result):
        if not result.get('name') or result.get('id') == 0:
            return False

        vals = {
            "remote_recruitment_stage_id": result.get('id'),
            "name": result.get('name'),
            "sequence": result.get('sequence'),
            "requirements": result.get('requirements'),
            "fold": result.get('fold'),
            "legend_blocked": result.get('legend_blocked'),
            "legend_done": result.get('legend_done'),
            "legend_normal": result.get('legend_normal'),
            "display_name": result.get('display_name'),
        }

        if result.get('job_id'):
            if result['job_id']['id'] != 0:
                job_ids = []
                domain = ['|', ('remote_hr_job_id', '=', result['job_id']['id']),
                          ('name', '=', result['job_id']['name'])]
                find_rec = self.env['hr.job'].search(domain)
                if find_rec:
                    job_ids.append((4, find_rec.id))
                else:
                    job_vals = {
                        'remote_hr_job_id': result['job_id']['id'],
                        'name': result['job_id']['name'],
                    }
                    if job_vals:
                        job_ids.append((0, 0, job_vals))
                if job_ids:
                    vals['job_ids'] = job_ids

        return vals

    def import_recruitment_stage(self):
        ''' ========== Import Stages (hr.recruitment.stage)  ==================  '''
        response = requests.get('%s/api/public/hr.recruitment.stage?query={%s}' % (
            self.base_url, self.query.get('hr_recruitment_stage')))
        response_json = response.json()

        if response.status_code == 200 and response_json.get('error') == '0':
            count = 0
            fail = 0

            for result in response_json['result']:
                try:
                    if not result.get('id') or result.get('name') == '':
                        continue
                    domain = ['|', ('remote_recruitment_stage_id', '=', result.get('id')),
                              ('name', '=', result.get('name'))]
                    find_rec = self.env['hr.recruitment.stage'].search(domain)
                    vals = self.prepare_recruitment_stage_vals(result)
                    if not vals:
                        continue
                    if find_rec:
                        find_rec.write(vals)
                    else:
                        self.env['hr.recruitment.stage'].create(vals)
                    count += 1
                except Exception as e:
                    fail += 1
                    self.create_fail_log(
                        name=result.get('id'),
                        field_type='hr_applicant_basic',
                        error=e,
                        import_json=result,
                    )

            if count > 0:
                self.create_recruitment_log(
                    field_type='hr_applicant_basic', error="%s Stages Imported Successfully" % (count), state='success')
            if fail > 0:
                self.create_recruitment_log(
                    field_type='hr_applicant_basic', error="%s Stages Failed To Import." % (fail))
        else:
            self.create_recruitment_log(
                field_type='hr_applicant_basic', error=response.text)
