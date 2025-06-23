# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
import requests
import json
from datetime import datetime


# -------------------- OTHER CODE ----------------------------


class HrEmpEmmergancy(models.Model):
    _inherit = 'hr.emp.emmergancy'

    remote_hr_emp_emmergancy_id = fields.Char("Remote Emp Emmergancy Id",copy=False)


class ShEmpRelation(models.Model):
    _inherit = 'sh.employee.relation'

    remote_sh_employee_relation_id = fields.Char("Remote Emp Relation Id",copy=False)

# ------------------------------------------------------------


class InheritHrEmpEmmergancy(models.Model):
    _inherit = "sh.import.base"
    json_field = fields.Text('JOSN Data')

    def import_hr_emp_emmergancy(self):
        ''' ========== Connect db for hr_emp_emmergancy  ==================  '''
        config = self.env['sh.import.base'].search([], limit=1)

        response = requests.get('''%s/api/public/hr.emp.emmergancy?query={%s}''' % (
            config.base_url, self.query['hr_emp_emmergancy']))
        response_json = response.json()
        self.json_field = response_json

        if response.status_code == 200:
            count = 0
            failed = 0
            for data in response_json['result']:

                try:
                    domain = [('remote_hr_emp_emmergancy_id', '=', data['id'])]
                    find_emp_emmergancy_rec = self.env['hr.emp.emmergancy'].search(
                        domain)
                    emp_emmergancy_vals = config.prepare_hr_emp_emmergancy_vals(
                        data)
                    if find_emp_emmergancy_rec:
                        count += 1
                        find_emp_emmergancy_rec.write(emp_emmergancy_vals)
                    else:
                        count += 1
                        self.env['hr.emp.emmergancy'].create(
                            emp_emmergancy_vals)
                    count += 1
                except Exception as e:
                    failed += 1
                    self.create_fail_log(
                        name=data.get('id'),
                        field_type='hr_employee_basic',
                        error=e,
                        import_json=data,
                    )

            if count > 0:
                self.create_log(
                    field_type='hr_employee_basic', error="%s Emp Emmergancy Contatcs Imported Successfully" % (count), state='success')
            if failed > 0:
                self.create_log(
                    field_type='hr_employee_basic', error="%s Emp Emmergancy Contatcs Failed To Import." % (failed))
        else:
            self.create_log(
                field_type='hr_employee_basic', error=response.text)

    def prepare_hr_emp_emmergancy_vals(self, data):

        emp_emmergancy_vals = {
            "remote_hr_emp_emmergancy_id": data.get('id'),
            "name": data.get('name'),
            "contact_number": data.get('contact_number'),
            "display_name": data.get('display_name')
        }
        self.map_relation_id(data, emp_emmergancy_vals)

        return emp_emmergancy_vals
