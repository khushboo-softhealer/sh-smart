# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models, _, api
import requests
import json
from datetime import datetime
from odoo.exceptions import UserError
from urllib.parse import urlencode
import time 
from odoo.tools import html2plaintext


class ResCompany(models.Model):
    _inherit = "res.company"

    sh_chatgpt_api_key = fields.Char("API Key")
    type_of_command_id = fields.Many2one('sh.type.of.command',string="Type of Command")
    type_of_language_id = fields.Many2one('sh.type.of.language',string="Type of Lanugage")
    style_id = fields.Many2one('sh.style',string="Style")
    length_id = fields.Many2one('sh.length',string="Length")
    api_model = fields.Char('API Model')

    def generate_response(self,message,api_key):
        
        
        headers = {
                'Content-Type': "application/json",
                'Authorization': "Bearer " + str(api_key)
        }

        data = {
            "model": self.env.company.api_model,
            "messages": [{"role": "user", "content": str(message)}],
            "temperature": 0.2,
            "top_p": 1,
            "max_tokens": 1000,
            "frequency_penalty": 0,
            "presence_penalty": 0,
        }
        try:
            response = requests.post(url="https://api.openai.com/v1/chat/completions", headers=headers,data=json.dumps(data))
            if response.status_code == 200:
                return response.json().get('choices')[0].get('message',False).get('content',False)
            else:
                return "Check The API Key. The following error was returned by Chatgpt:" + " " + str(response.json())
        
        except Exception as e:
            return "Something Went Wrong..."+ str(e)

    @api.model
    def draft_response(self,res_model,res_id):

        api_key = self.env.company.sh_chatgpt_api_key

        if not api_key:
            raise UserError("Please enter api key in general setting")

        message_ids = self.env['mail.message'].sudo().search([('subtype_id', '!=', self.env.ref(
                    'mail.mt_note').id), ('res_id', '=', res_id), ('model', '=', res_model)])
        
        message =''

        for message_id in message_ids:
            message += str(message_id.author_id.name) + ':' + html2plaintext(message_id.body or "") + "\n" 

        input_msg = message

        message += ' \n Above is the history of conversation prepare draft reply which i can sent'
        response = self.generate_response(message,api_key)

        return input_msg,response

    @api.model
    def summarize_response(self,res_model,res_id):

        api_key = self.env.company.sh_chatgpt_api_key

        if not api_key:
            raise UserError("Please enter api key in general setting")

        message_ids = self.env['mail.message'].sudo().search([('subtype_id', '!=', self.env.ref(
                    'mail.mt_note').id), ('res_id', '=', res_id), ('model', '=', res_model)])
        
        message = 'Below is the history of conversation can you please summarize \n'

        for message_id in message_ids:
            message += str(message_id.author_id.name) + ':' + html2plaintext(message_id.body or "") + "\n" 

        response = self.generate_response(message,api_key)

        return response

    @api.model
    def sh_get_data(self):

        api_key = self.env.company.sh_chatgpt_api_key
        api_model = self.env.company.api_model
        if not api_key:
            raise UserError("Please enter api key in ChatGpt Settings")

        commands = self.env['sh.type.of.command'].search([])      
        languages = self.env['sh.type.of.language'].search([])
        styles = self.env['sh.style'].search([])
        lengths = self.env['sh.length'].search([])  
        translate_to_languages = self.env['sh.translate.to.language'].search([])                 

        commands_dict = {}
        languages_dict = {}
        styles_dict = {}
        lengths_dict = {}
        translate_to_languages_dict = {}

        if self.env.user.enable_type_of_command:
            commands_dict = {command.id: command.name + str(command.description or ' ') for command in commands}
        
        if self.env.user.enable_type_of_language:
            languages_dict =  {language.id: language.name + str(language.description or ' ') for language in languages}
        
        if self.env.user.enable_style:
            styles_dict =  {style.id: style.name + str(style.description or ' ') for style in styles}
        
        if self.env.user.enable_length:
            lengths_dict =  {length.id: length.name + str(length.description or ' ') for length in lengths}
        
        if self.env.user.enable_translate_to_language:
            translate_to_languages_dict =  {translate_to_lan.id: translate_to_lan.name + str(translate_to_lan.description or ' ') for translate_to_lan in translate_to_languages}

        default_values = []
        default_values.append(self.env.user.type_of_command_id.id)
        default_values.append(self.env.user.type_of_language_id.id)
        default_values.append(self.env.user.length_id.id)
        default_values.append(self.env.user.style_id.id)
        default_values.append(self.env.user.sh_translate_to_language.id)

        return commands_dict,languages_dict,styles_dict,lengths_dict,translate_to_languages_dict,api_key,default_values,api_model

class ResConfigSetting(models.TransientModel):
    _inherit = "res.config.settings"


    sh_chatgpt_api_key = fields.Char(related='company_id.sh_chatgpt_api_key',readonly=False)
    type_of_command_id = fields.Many2one(related='company_id.type_of_command_id',readonly=False)
    type_of_language_id = fields.Many2one(related='company_id.type_of_language_id',readonly=False)
    style_id = fields.Many2one(related='company_id.style_id',readonly=False)
    length_id = fields.Many2one(related='company_id.length_id',readonly=False)
    api_model = fields.Char(related='company_id.api_model',readonly=False)
