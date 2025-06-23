# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
import requests
import json
from datetime import datetime


class InheritImportEmployee(models.Model):
    _inherit = "sh.import.base"

    def import_resource_resource(self):
        ''' ========== Import Resource (resource.resource)  ==================  '''

        confid = self.env['sh.import.base'].search([], limit=1)
        response = requests.get(
            '''%s/api/public/resource.resource?query={id,name,active,resource_type,time_efficiency,tz,display_name,user_id,calendar_id}''' % (confid.base_url))

        if response.status_code == 200:
            response_json = response.json()
            count = 0
            failed = 0

            for result in response_json['result']:
                # try:
                domain = [('remote_resource_resource_id',
                           '=', result.get('id'))]
                find_resource = self.env['resource.resource'].search(domain)
                resource_vals = self.prepare_resource_vals(result)
                if find_resource:
                    find_resource.write(resource_vals)
                else:
                    self.env['resource.resource'].create(resource_vals)
                count += 1

            if count > 0:
                self.create_log(
                    field_type='hr_employee_basic', error="%s Resource Imported Successfully" % (count), state='success')
            if failed > 0:
                self.create_log(
                    field_type='hr_employee_basic', error="%s Resource Failed To Import" % (failed))
        else:
            self.create_log(
                field_type='hr_employee_basic', error=response.text)

    def prepare_resource_vals(self, data):
        resource_vals = {
            "remote_resource_resource_id": data.get('id'),
            "name": data.get('name'),
            "active": data.get('active'),
            "company_id": 1,
            "resource_type": data.get('resource_type').get('sh_api_current_state'),
            "time_efficiency": data.get('time_efficiency'),
            "tz": data.get('tz').get('sh_api_current_state'),
            "display_name": data.get('display_name'),
        }
        self.map_many2one_field(
            'res.users', 'remote_res_user_id', data, resource_vals, 'user_id')
        self.map_many2one_field(
            'resource.calendar', 'remote_resource_calendar_id', data, resource_vals, 'calendar_id')
        return resource_vals
