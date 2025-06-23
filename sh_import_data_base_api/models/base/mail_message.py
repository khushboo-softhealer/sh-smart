# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
import requests

class MailMessage(models.Model):
    _inherit = 'mail.message'

    remote_mail_message_id = fields.Char("Remote Mail Message ID",copy=False)

    # temp_boolean = fields.Boolean("Boolean")

    def process_mail_message_ids(self):
        active_ids = self.env['mail.message'].browse(self.env.context.get('active_ids'))
        print("N\n\n",active_ids)
        if active_ids:

            confid = self.env['sh.import.base'].search([],limit=1)
            for active_id in active_ids:
                response = requests.get('''%s/api/public/mail.message/%s?query={id,message_id,author_id}''' %(confid.base_url,active_id.remote_mail_message_id))
                response_json = response.json() 
                print("\n\n====response_json",response_json)
                if response.status_code == 200:
                    count = 0
                    failed = 0                
                    for data in response_json['result']:
                        domain = [('remote_mail_message_id', '=', data['id'])]
                        message_obj = self.env['mail.message'].search(domain,limit=1) 
                        print("message_obj find message_obj",message_obj)
                        author = False
                        if data.get('author_id'):
                            print("\n\n====message.get('author_id')",data.get('author_id'))
                            domain = [('remote_res_partner_id', '=', data['author_id'])]
                            find_customer = self.env['res.partner'].search(domain,limit=1)
                            if find_customer:
                                author = find_customer.id

                        if message_obj:
                            message_obj.write({
                                'message_id':data.get('message_id'),
                                'author_id':author
                            })
                            count += 1 
                        else:
                            failed+=1 
 


class MailTrackingValue(models.Model):
    _inherit = 'mail.tracking.value'

    remote_mail_tracking_value_id = fields.Char("Remote Mail Tracking Value ID",copy=False)  
    

