# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
import requests
import json
from datetime import datetime

class InheritImportHrRuleImport(models.Model):
    _inherit = "sh.import.base"


    def import_hr_contribution_register(self):   
        ''' ========== Connect db for import hr contribution register id  ==================  '''
        confid = self.env['sh.import.base'].search([],limit=1)
        response = requests.get('''%s/api/public/hr.contribution.register?query={%s}''' %(confid.base_url,self.query_dict['hr_contribution_register']))
        # response = requests.get('''%s/api/public/hr.payslip.line?query={*}''' %(confid.base_url))
        response_json = response.json()

        if response.status_code==200:
            count = 0
            for data in response_json['result']:
                contribution_register_vals = confid.prepare_hr_contribution_register_vals(data)
                domain = [('remote_hr_contribution_register_id', '=', data['id'])]
                contribution_register_id = self.env['hr.contribution.register'].search(domain)
                # try:
                if contribution_register_id:
                    count += 1
                    contribution_register_id.write(contribution_register_vals)                            
                else:
                    count += 1
                    create_payslip_line=self.env['hr.contribution.register'].create(contribution_register_vals)

            if count > 0:
                vals = {
                    "name": confid.name,
                    "state": "success",
                    "field_type": "hr_contribution_register",
                    "error": "%s Hr Contribution Register Imported Successfully" %(count),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)

        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "hr_contribution_register",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals) 


    def prepare_hr_contribution_register_vals(self,data):

        hr_contribution_register_vals={
            'remote_hr_contribution_register_id' : data['id'],
            'name':data['name'],
            'display_name':data['display_name'],
            'note':data['note'],
        }

        # import partner_id if already exist then return

        # if data.get('partner_id'):
        #     domain = [('remote_res_partner_id', '=', data['partner_id']['id'])]
        #     find_customer = self.env['res.partner'].search(domain)
        #     if find_customer:
        #         hr_contribution_register_vals['partner_id'] = find_customer.id
        #     else:
        #         contact_vals=self.process_contact_data(data['partner_id'])
        #         partner_id=self.env['res.partner'].create(contact_vals)
        #         if partner_id:
        #             hr_contribution_register_vals['partner_id']=partner_id.id

        if data.get('partner_id'):
            domain = [('remote_res_partner_id', '=', data['partner_id']['id'])]
            find_customer = self.env['res.partner'].search(domain)
            if find_customer:
                hr_contribution_register_vals['partner_id'] = find_customer.id
            # else:
            #     contact_vals=self.process_contact_data(data['partner_id'])
            #     partner_id=self.env['res.partner'].create(contact_vals)
            #     if partner_id:
            #         hr_contribution_register_vals['partner_id']=partner_id.id

        # ======== Get line_ids if already created or create =========

        # if data.get('register_line_ids'):
        #     payslip_line_list=[]
        #     for payslip_line in data['register_line_ids']:
        #         domain = [('remote_hr_payslip_line_id', '=', payslip_line['id'])]
        #         find_payslip_line = self.env['hr.payslip.line'].search(domain)
        #         if not find_payslip_line:
        #             psyslip_line_vals = self.process_hr_payslip_line(payslip_line)
        #             payslip_line_list.append((0,0,psyslip_line_vals))
        #     hr_contribution_register_vals['register_line_ids'] = payslip_line_list

        if data.get('register_line_ids'):
            payslip_line_list=[]
            for payslip_line_id in data['register_line_ids']:
                domain = [('remote_hr_payslip_line_id', '=', payslip_line_id)]
                find_payslip_line = self.env['hr.payslip.line'].search(domain)
                if find_payslip_line:
                    payslip_line_list.append((4,find_payslip_line.id))

            hr_contribution_register_vals['register_line_ids'] = payslip_line_list

        return  hr_contribution_register_vals
