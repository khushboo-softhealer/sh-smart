# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models


class InheritImportBase(models.Model):
    _inherit = "sh.import.base"

    # ==========================
    #         Employee
    # ==========================

    def map_relation_id(self, data, vals, data_key='relation_id', vals_key=None):
        ''' relation_id Many2one(sh.employee.relation) '''
        if data.get(data_key):
            if data.get(data_key).get('id') and data.get(data_key).get('id') != 0:
                if not vals_key:
                    vals_key = data_key
                domain = [('remote_sh_employee_relation_id',
                           '=', data[data_key]['id'])]
                find_rec = self.env['sh.employee.relation'].search(
                    domain)
                if find_rec:
                    vals[vals_key] = find_rec.id
                else:
                    rec_vals = {
                        'remote_sh_employee_relation_id': data.get(data_key).get('id'),
                        'name': data.get(data_key).get('name'),
                        'display_name': data.get(data_key).get('display_name')
                    }
                    create_rec = self.env['sh.employee.relation'].create(
                        rec_vals)
                    if create_rec:
                        vals[vals_key] = create_rec.id

    def map_one2many_ids(self, model, remote_field, data, vals, data_key, vals_key=None):
        '''one2many'''
        if data.get(data_key):
            ids_list = []
            for rec_id in data.get(data_key):
                find_rec = self.env[model].search(
                    [(remote_field, '=', rec_id)])
                if find_rec:
                    ids_list.append((4, find_rec.id))
            if ids_list:
                if not vals_key and data_key:
                    vals_key = data_key
                vals[vals_key] = ids_list

    # pro_expe_ids (sh.emp.professional.experience)
    def map_pro_expe_ids(self, data, vals, data_key='pro_expe_ids', vals_key=None):
        '''one2many (sh.emp.professional.experience)'''
        if data.get(data_key):
            relational_list = []
            for line in data.get(data_key):
                if line.get('id') != 0:
                    domain = [
                        ('remote_sh_emp_professional_experience_id', '=', line.get('id'))]
                    find_rec = self.env['sh.emp.professional.experience'].search(
                        domain)
                    if find_rec:
                        relational_list.append((4, find_rec.id))
                    else:
                        line_vals = self.prepare_sh_emp_professional_experience_vals(
                            line)
                        relational_list.append((0, 0, line_vals))
            if relational_list:
                if not vals_key and data_key:
                    vals_key = data_key
                vals[vals_key] = relational_list

    # non_tec_skill_ids (sh.emp.non.technical.skill)
    def map_non_tec_skill_ids(self, data, vals, data_key='non_tec_skill_ids', vals_key=None):
        '''one2many (sh.emp.non.technical.skill)'''
        if data.get(data_key):
            relational_list = []
            for line in data.get(data_key):
                if line.get('id') != 0:
                    domain = [
                        ('remote_sh_emp_non_technical_skill_id', '=', line.get('id'))]
                    find_rec = self.env['sh.emp.non.technical.skill'].search(
                        domain)
                    if find_rec:
                        relational_list.append((4, find_rec.id))
                    else:
                        line_vals = self.prepare_sh_emp_non_technical_skill_vals(
                            line)
                        relational_list.append((0, 0, line_vals))
            if relational_list:
                if not vals_key and data_key:
                    vals_key = data_key
                vals[vals_key] = relational_list

    def map_edu_qualification_ids(self, data, vals, data_key='edu_qualification_ids', vals_key=None):
        '''one2many (sh.education.qualification)'''
        if data.get(data_key):
            relational_list = []
            for line in data.get(data_key):
                if line.get('id') != 0:
                    domain = [
                        ('remote_sh_education_qualification_id', '=', line.get('id'))]
                    find_rec = self.env['sh.education.qualification'].search(
                        domain)
                    if find_rec:
                        relational_list.append((4, find_rec.id))
                    else:
                        line_vals = self.prepare_sh_education_qualification_vals(
                            line)
                        relational_list.append((0, 0, line_vals))
            if relational_list:
                if not vals_key and data_key:
                    vals_key = data_key
                vals[vals_key] = relational_list

    # skill_ids (one2many) sh.emp.technical.skill
    def map_sh_emp_technical_skill(self, data, vals, data_key='skill_ids', vals_key=None):
        ''' one2many (sh.emp.technical.skill) '''
        if data.get(data_key):
            relational_list = []
            for line in data.get(data_key):
                if line.get('id') != 0:
                    domain = [
                        ('remote_sh_emp_technical_skill_id', '=', line.get('id'))]
                    find_rec = self.env['sh.emp.technical.skill'].search(
                        domain)
                    if find_rec:
                        relational_list.append((4, find_rec.id))
                    else:
                        line_vals = {
                            "remote_sh_emp_technical_skill_id": line.get('id'),
                            "level": line.get('level').get('sh_api_current_state'),
                            "display_name": line.get('display_name'),
                        }
                        self.map_skill_id(line, line_vals)
                        relational_list.append((0, 0, line_vals))
            if relational_list:
                if not vals_key and data_key:
                    vals_key = data_key
                vals[vals_key] = relational_list

    def map_skill_id(self, data, vals, data_key='skill_id', vals_key=None):
        ''' skill_id Many2one(sh.technical.skill) '''
        if data.get(data_key):
            if data.get(data_key).get('id') and data.get(data_key).get('id') != 0:
                if not vals_key:
                    vals_key = data_key
                domain = [('remote_sh_technical_skill_id',
                           '=', data[data_key]['id'])]
                find_rec = self.env['sh.technical.skill'].search(
                    domain)
                if find_rec:
                    vals[vals_key] = find_rec.id
                else:
                    rec_vals = {
                        'remote_sh_technical_skill_id': data.get(data_key).get('id'),
                        'name': data.get(data_key).get('name'),
                        'display_name': data.get(data_key).get('display_name')
                    }
                    create_rec = self.env['sh.technical.skill'].create(
                        rec_vals)
                    if create_rec:
                        vals[vals_key] = create_rec.id

    # language_known_ids
    def map_language_known_ids(self, data, vals, data_key='language_known_ids', vals_key=None):
        ''' one2many (language.known) '''
        if data.get(data_key):
            relational_list = []
            for lang in data.get(data_key):
                if lang.get('id') != 0:
                    domain = [
                        ('remote_language_known_id', '=', lang.get('id'))]
                    find_rec = self.env['language.known'].search(domain)
                    if find_rec:
                        relational_list.append((4, find_rec.id))
                    else:
                        lang_vals = self.prepare_language_known_vals(lang)
                        if lang_vals:
                            relational_list.append((0, 0, lang_vals))
            if relational_list:
                if not vals_key and data_key:
                    vals_key = data_key
                vals[vals_key] = relational_list

    def map_resource_id(self, data, vals, data_key='resource_id', vals_key=None):
        ''' resource_id Many2one(resource.resource) '''
        if data.get(data_key):
            if data.get(data_key).get('id') and data.get(data_key).get('id') != 0:
                if not vals_key:
                    vals_key = data_key
                domain = [('remote_resource_resource_id',
                           '=', data[data_key]['id'])]
                find_resource = self.env['resource.resource'].search(
                    domain)
                if find_resource:
                    vals[vals_key] = find_resource.id
                else:
                    resource_vals = self.prepare_resource_vals(
                        data.get(data_key))
                    create_resource = self.env['resource.resource'].create(
                        resource_vals)
                    if create_resource:
                        vals[vals_key] = create_resource.id

    def map_language_id(self, data, vals, data_key='language_id', vals_key=None):
        ''' language_id Many2one(res.lang) '''
        if data.get(data_key):
            if data.get(data_key).get('id') and data.get(data_key).get('id') != 0:
                if not vals_key:
                    vals_key = data_key
                domain = ['|', ('remote_res_lang_id', '=', data[data_key]
                                ['id']), ('code', '=', data[data_key].get('code'))]
                find_rec = self.env['res.lang'].search(domain)
                if find_rec:
                    vals[vals_key] = find_rec.id
                else:
                    prepare_vals = self.prepare_res_lang_vals(
                        data.get(data_key))
                    create_rec = self.env['res.lang'].create(
                        prepare_vals)
                    if create_rec:
                        vals[vals_key] = create_rec.id
