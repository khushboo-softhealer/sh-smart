# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models, _, api
import requests
import json
from datetime import datetime
from odoo.exceptions import UserError
from urllib.parse import urlencode
import time 

class ChatgptConfig(models.Model):
    _name = "sh.chatgpt.config"

    name = fields.Char(string = "Name")
    api_key = fields.Char(string = "API Key")
    question = fields.Char(string = "Question")
    response = fields.Text(string = "Response")

    def beautify_message(self,message=False):
        headers = {
                'Content-Type': "application/json",
                'Authorization': "Bearer " + str(self.api_key)
        }
         
        new_msg = str(message) + '\n' "fix spelling mistake, make grammatically correct and add something if necessary to beautify the above message"

        data = {
            "model": self.env.company.api_model,
            "messages": [{"role": "user", "content": new_msg}],
            "temperature": 0.2,
            "top_p": 1,
            "max_tokens": 1000,
            "frequency_penalty": 0,
            "presence_penalty": 0,
        }
        try:
            response = requests.post(url="https://api.openai.com/v1/chat/completions", headers=headers,data=json.dumps(data))
            return response.json().get('choices')[0].get('message',False).get('content',False)

        except Exception as e:
            return "<b>Something Went Wrong...</b> <br />"+ str(e)

    def generate_response(self,question=False):
        
        headers = {
                'Content-Type': "application/json",
                'Authorization': "Bearer " + str(self.api_key)
        }

        if not question:
            question = self.question

        data = {
            "model": self.env.company.api_model,
            "messages": [{"role": "user", "content": str(question)}],
            "temperature": 0.2,
            "top_p": 1,
            "max_tokens": 1000,
            "frequency_penalty": 0,
            "presence_penalty": 0,
        }
        response = requests.post(url="https://api.openai.com/v1/chat/completions", headers=headers,data=json.dumps(data))

        if self.question:
            self.response = response.json().get('choices')[0].get('message',False).get('content',False)
        
        else:
            return response.json().get('choices')[0].get('message',False).get('content',False)
        