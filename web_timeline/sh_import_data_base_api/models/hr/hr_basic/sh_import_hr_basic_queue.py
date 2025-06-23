# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields
import requests


class HeBasicQueue(models.Model):
    _inherit = "sh.import.base"

    sh_import_hr_payslip_line_ids = fields.Char("Payslip line ids")
    sh_is_import_hr_basic = fields.Boolean("Import Hr Basic to Queue")
    sh_from_date_hr_basic = fields.Datetime("From Date")
    sh_to_date_hr_basic = fields.Datetime("To Date")


    def import_hr_basic_to_queue(self):
        '''Import Hr Basic To Queue'''

        self.import_payslip_line_and_filtered_to_queue()


    def import_hr_basic_from_queue(self):
        '''Import Hr Basic From Queue'''

        self.import_payslip_line_from_queue()


    def import_payslip_line_and_filtered_to_queue(self):
        ''' ========== Import Filtered Payslip Line between from date and end date ==================  '''
        confid = self.env['sh.import.base'].search([],limit=1)
        if confid.sh_is_import_hr_basic:
            response = requests.get('''%s/api/public/hr.payslip.line?query={id,write_date}&filter=[["write_date",">=","%s"],["write_date","<=","%s"]]''' %(confid.base_url, str(confid.sh_from_date_hr_basic), str(confid.sh_to_date_hr_basic)))
            response_json = response.json()
            if response_json.get('result'):
                confid.sh_import_hr_payslip_line_ids = [r['id'] for r in response_json.get('result')]


    def import_payslip_line_from_queue(self):
        ''' ========== Import Payslip Line ==================  '''
        confid = self.env['sh.import.base'].search([],limit=1)
        if confid.sh_is_import_hr_basic and confid.sh_import_hr_payslip_line_ids:   
            payslip_lines = confid.sh_import_hr_payslip_line_ids.strip('][').split(', ')

            if not payslip_lines[0]:
                confid.sh_is_import_hr_basic = False
                confid.sh_import_hr_payslip_line_ids = False
                return False

            count=0
            failed=0
            failed_dict = {}

            for payslip_line_id in payslip_lines[0:10]:
                response = requests.get('''%s/api/public/hr.payslip.line/%s?query={%s}''' %(confid.base_url, payslip_line_id,self.query_dict['hr_payslip_line']))
                response_json = response.json()

                if response.status_code==200:
                    for data in response_json['result']:
                        try:
                            payslip_line_vals = confid.prepare_hr_payslip_line_vals(data)
                            domain = [('remote_hr_payslip_line_id', '=', data['id'])]
                            find_payslip_line = self.env['hr.payslip.line'].search(domain)
                            if find_payslip_line:
                                find_payslip_line.write(payslip_line_vals)                            
                            else:
                                self.env['hr.payslip.line'].create(payslip_line_vals)
                            count += 1
                        except Exception as e:
                            failed_dict[payslip_line_id] = e
                            failed += 1
                    confid.sh_import_hr_payslip_line_ids='['+', '.join([str(elem) for elem in payslip_lines[10:]])+']'

            if count > 0:
                self.create_log(field_type='hr_payslip_line', error="%s Hr Payslip line Imported Successfully" % (count), state='success')
            if failed > 0:
                failed_dict['Total Failed'] = failed
                self.create_log(field_type='hr_payslip_line', error=failed_dict)

            confid.sh_import_hr_payslip_line_ids = '['+', '.join(
                [str(elem) for elem in payslip_lines[10:]])+']'
