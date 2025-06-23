# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
import requests
import json
from datetime import datetime


class ShEmpNonTechnicalSkill(models.Model):
    _inherit = 'sh.emp.non.technical.skill'

    remote_sh_emp_non_technical_skill_id = fields.Char(
        "Remote Emp Non Technical Skill ID",copy=False)


class ShNonTechnicalSkill(models.Model):
    _inherit = 'sh.non.technical.skill'

    remote_sh_non_technical_skill_id = fields.Char(
        "Remote Non Technical Skill ID",copy=False)


class InheritImportEmployee(models.Model):
    _inherit = "sh.import.base"

    def import_sh_emp_non_technical_skill(self):

        confid = self.env['sh.import.base'].search([], limit=1)
        response = requests.get(
            '''%s/api/public/sh.emp.non.technical.skill''' % (confid.base_url))

        if response.status_code == 200:
            response_json = response.json()

    def prepare_sh_emp_non_technical_skill_vals(self, data):

        non_tech_skill_vals = {
            "remote_sh_emp_non_technical_skill_id": data.get('id'),
            "level": data.get('level').get('sh_api_current_state'),
            "display_name": data.get('display_name'),
        }
        # (sh.non.technical.skill) many2one
        if data.get('non_tec_skill_id'):
            if data.get('non_tec_skill_id').get('id') and data.get('non_tec_skill_id').get('id') != 0:
                domain = [('remote_sh_non_technical_skill_id',
                           '=', data['non_tec_skill_id']['id'])]
                find_rec = self.env['sh.non.technical.skill'].search(domain)
                if find_rec:
                    non_tech_skill_vals['non_tec_skill_id'] = find_rec.id
                else:
                    rec_vals = {
                        'remote_sh_non_technical_skill_id': data.get('non_tec_skill_id').get('id'),
                        'name': data.get('non_tec_skill_id').get('name'),
                        'display_name': data.get('non_tec_skill_id').get('display_name')
                    }
                    create_rec = self.env['sh.non.technical.skill'].create(
                        rec_vals)
                    if create_rec:
                        non_tech_skill_vals['non_tec_skill_id'] = create_rec.id

        return non_tech_skill_vals
