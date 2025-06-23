# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.http import request

class ResUsers(models.Model):
    _inherit = 'res.users'

    enable_type_of_command = fields.Boolean(string="Enable Type of command")
    enable_type_of_language = fields.Boolean(string="Enable Type of Language")
    enable_style = fields.Boolean(string="Enable Style")
    enable_length = fields.Boolean(string="Enable Length")
    enable_translate_to_language = fields.Boolean(string="Enable Translate to Language")
    type_of_command_id = fields.Many2one('sh.type.of.command',string="Type of Command")
    type_of_language_id = fields.Many2one('sh.type.of.language',string="Type of Lanugage")
    style_id = fields.Many2one('sh.style',string="Style")
    length_id = fields.Many2one('sh.length',string="Length") 
    sh_translate_to_language = fields.Many2one('sh.translate.to.language',string="Translate to Language")
    show_summary_button = fields.Boolean(string = "Show Summary Button in chatter ? ")
    auto_generate_response = fields.Boolean(string = "Auto Generate Response?")

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + ['type_of_command_id','type_of_language_id','style_id','length_id','show_summary_button','auto_generate_response','enable_type_of_command','enable_type_of_language','enable_style','enable_length','enable_translate_to_language']
    