# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

import datetime
from cryptography.fernet import Fernet
from odoo import fields, api, models, _
from odoo.tools.translate import html_translate


class PasswordGenerator(models.Model):
    _name = "password.generator"
    _description = "Password Generator"
    _inherit = ['mail.thread']
    _rec_name = 'username'

    title = fields.Char("Title",  tracking=True,required=True)
    server_tags = fields.Many2many('server.tag','server_id',string='ServerTag')
    username = fields.Char("User name",  tracking=True)
    password = fields.Char("Password", tracking=True)#,inverse='_set_password')
    sh_password = fields.Char("Decrypt Password ",compute='_get_decrypt_password')
    is_password = fields.Boolean('Is Password')
    confirm_password = fields.Char("Confirm Password")
    decrypt_password = fields.Char("Decrypt Password",compute='_get_decrypt_password')
    password_strength=fields.Selection([
        ('0', 'Very Very Low'),
        ('1', 'Very Low'),
        ('2', 'Low'),
        ('3', 'Normal'),
        ('4', 'High'),
        ('5', 'Very High')
    ], string='Password Strength',readonly=True)
    ip =  fields.Char("IP", tracking=True)
    url = fields.Char("Url", tracking=True)
    email = fields.Char("Email")
    phone = fields.Char("Phone")
    partner_id = fields.Many2one('res.partner',string='Partner',  tracking=True)
    sh_notes = fields.Html('Notes', sanitize_attributes=False, translate=html_translate)
    writepass_date = fields.Datetime('Pass. Updated On',readonly=True)
    note = fields.Text("Note")
    encry_key = fields.Char('Encrypt Key')
    fernet_key= fields.Char()
    project_id = fields.Many2one('project.project')

    @api.depends('password')
    def _get_decrypt_password(self):
        for rec in self:
            rec.decrypt_password = ''
            rec.sh_password = ''
            if rec.fernet_key and rec.password:
                key = bytes(rec.fernet_key, 'utf-8')
                f = Fernet(key)
                decrypted = f.decrypt(bytes(rec.password, 'utf-8'))
                rec.decrypt_password = decrypted
                rec.sh_password = decrypted


    # Update Password for Encrypt and Decrypt
    def write(self, values):
        values['writepass_date'] = datetime.datetime.now()
        return super(PasswordGenerator, self).write(values)

    #Create Encrypt and Decrypt Password
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals.update({'writepass_date': datetime.datetime.now()})
        return super(PasswordGenerator, self).create(vals)

    # Generate Password Btn
    def action_password_wizard(self):
        return{
                'type': 'ir.actions.act_window',
                'name':'Password Generator',
                'res_model': 'password.generator.wizard',
                'view_mode': 'form',
                'target': 'new',
            }

    # Show Password Eye Btn
    def action_copy_password(self):
        if self.is_password == False:
            self.is_password = True
            self.sh_password = self.decrypt_password
        elif self.is_password == True:
            self.is_password = False
            self.decrypt_password = self.sh_password

    # URL Open
    def action_url_link(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'name': "Url",
            'target': 'new',
            'url': self.url
        }
