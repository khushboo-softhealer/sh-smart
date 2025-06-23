# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
import requests
import json
from datetime import datetime

class InheritImportBase(models.Model):
    _inherit = "sh.import.base"
    
    def import_mail_message_subtype(self):
        confid = self.env['sh.import.base'].search([],limit=1)
        response = requests.get('''%s/api/public/mail.message.subtype?query={*,parent_id{*}}''' %(confid.base_url))
        response_json = response.json()
        if response.status_code == 200:
            count = 0
            for subtype in response_json['result']:
                domain = [('remote_mail_message_subtype_id', '=', subtype['id'])]
                find_subtype = self.env['mail.message.subtype'].search(domain)
                message_subtype={
                    'remote_mail_message_subtype_id':subtype['id'],
                    'default':subtype['default'],
                    'hidden':subtype['hidden'],
                    'internal':subtype['internal'],
                    'display_name':subtype['display_name'],
                    'name':subtype['name'],
                    'relation_field':subtype['relation_field'],
                    'res_model':subtype['res_model'],
                    'sequence':subtype['sequence'],
                    'description':subtype['description'],
                }
                if find_subtype:
                    count += 1
                    find_subtype.write(message_subtype)
                else:
                    self.env['mail.message.subtype'].create(message_subtype)
                    count += 1
                    
            for subtype in response_json['result']:
                if subtype.get('parent_id'):
                    find_subtype = self.env['mail.message.subtype'].search([('remote_mail_message_subtype_id', '=', subtype['id'])])
                    domain = [('remote_mail_message_subtype_id', '=', subtype['parent_id']['id'])]
                    find_parent_subtype = self.env['mail.message.subtype'].search(domain,limit=1)    
                    if find_parent_subtype and find_subtype:
                        find_subtype.update({
                            'parent_id':find_parent_subtype.id,
                        })   
                    
            if count > 0:              
                vals = {
                    "name": confid.name,
                    "state": "success",
                    "field_type": "message_subtype",
                    "error": "%s Message Subtype Imported Successfully" %(count),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)
        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "message_subtype",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals)     
            