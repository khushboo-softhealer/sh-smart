# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models, _, api
from odoo.exceptions import UserError
import requests
import json

class MailChannel(models.Model):
    _inherit = 'mail.channel'

    def _notify_thread(self, message, msg_vals=False, **kwargs):
        res = super(MailChannel, self)._notify_thread(message, msg_vals=msg_vals, **kwargs)
        chatgpt_channel_id = self.env['mail.channel'].sudo().search([('name','=','ChatGPT')],limit=1)
        # chatgpt_channel_id = self.env.ref('sh_odoo_chatgpt_connector.sh_channel_chatgpt')
        sh_user_chatgpt = self.env['res.users'].sudo().search([('login','=','chatgpt')],limit=1)
        # sh_user_chatgpt = self.env.ref("sh_odoo_chatgpt_connector.sh_user_chatgpt")
        sh_partner_chatgpt = self.env['res.partner'].sudo().search([('name','=','ChatGPT')],limit=1)
        # sh_partner_chatgpt = self.env.ref("sh_odoo_chatgpt_connector.sh_partner_chatgpt")
        author_id = msg_vals.get('author_id')
        chatgpt_name = str(sh_partner_chatgpt.name or '') + ', '
        question = msg_vals.get('body')
        
        if not question:
            return res
        
        if author_id != sh_partner_chatgpt.id and msg_vals.get('model', '') == 'mail.channel':
            
            if self.channel_type == 'chat'  and chatgpt_name in msg_vals.get('record_name', ''):
                
                response = self.sh_generate_response(question)
                self.with_user(sh_user_chatgpt).message_post(body=response, message_type='comment', subtype_xmlid='mail.mt_comment')
            
            elif msg_vals.get('res_id', 0) == chatgpt_channel_id.id:
                
                response = self.sh_generate_response(question)
                
                self.with_user(sh_user_chatgpt).message_post(body=response, message_type='comment', subtype_xmlid='mail.mt_comment')
                                
        return res
    
    def sh_generate_response(self,question):
        
        api_key = self.env.company.sh_chatgpt_api_key

        if not api_key:
            raise UserError("Please enter api key in general setting")

        headers = {
                'Content-Type': "application/json",
                'Authorization': "Bearer " + str(api_key)
        }

        data = {
            "model": self.env.company.api_model,
            "messages": [{"role": "user", "content": str(question)}],
            "temperature": 0.2,
            "top_p": 1,
            "max_tokens": 1000,
            "frequency_penalty": 0,
            "presence_penalty": 0,
        }
        try:
            
            response = requests.post(url="https://api.openai.com/v1/chat/completions", headers=headers,data=json.dumps(data),timeout=30)
            if response.status_code == 200:
                return response.json().get('choices')[0].get('message',False).get('content',False)
            else:
                return "Check The API Key. The following error was returned by Chatgpt:" + " " + str(response.json())

        except Exception as e:

            return "<b>Something Went Wrong...</b> <br />"+ str(e)
            

  