# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

import random
from cryptography.fernet import Fernet
from odoo import fields, api, models, _
from odoo.exceptions import UserError
from password_strength import PasswordStats


class PasswordGeneratorWizard(models.Model):
    _name = "password.generator.wizard"
    _description = "PWD Generation Wizard"
    _rec_name = 'pass_id'

    pass_id = fields.Many2one('password.generator',string="Password Id")
    type_id= fields.Many2one('password.type.pattern',string="Password Pattern")

    def generate_passwd(self):
        lower_alphabet = "abcdefghijklmnopqrstuvwxyz"
        upper_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        digit = "1234567890"
        symbol = r"!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"

        password = ""
        random.seed()
        COMBINED_LIST = ""
        if self.type_id.pattern_type_ids:
            for pattern in self.type_id.pattern_type_ids:
                if pattern.id == self.env.ref('sh_password_generator.type_lowercase').id:
                    COMBINED_LIST += lower_alphabet
                if pattern.id == self.env.ref('sh_password_generator.type_upercase').id:
                    COMBINED_LIST+=upper_alphabet
                if pattern.id == self.env.ref('sh_password_generator.type_digit').id:
                    COMBINED_LIST+=digit
                if pattern.id == self.env.ref('sh_password_generator.type_symbol').id:
                    COMBINED_LIST+=symbol

            for i in range(self.type_id.password_length):
                next_index = random.randrange(len(COMBINED_LIST))
                password = password + COMBINED_LIST[next_index]
            return password
        else:
            raise UserError("Please Select Password Pattern")

    # generate a new password Btn:
    def generate_password_wizard(self):

        active_id = self.env.context.get('active_id')
        for pas_wd in self.pass_id.browse(active_id):
            password = self.generate_passwd()
            message = password.encode()
            key = Fernet.generate_key()
            f = Fernet(key)
            encrypted = f.encrypt(message)
            pas_wd.fernet_key = key
            pas_wd.password = encrypted
            pas_wd.encry_key = key
            decrypted = f.decrypt(encrypted)
            pas_wd.decrypt_password = decrypted
            pas_wd.confirm_password = pas_wd.password
            pas_wd.sh_password = decrypted
            pas_wd._get_decrypt_password()
            stats = PasswordStats(password)
            if float(stats.strength())>0.6:
                pas_wd.password_strength = '5'
            elif float(stats.strength())<=0.6 and float(stats.strength())>0.5:
                pas_wd.password_strength = '4'
            elif float(stats.strength())<=0.5 and float(stats.strength())>0.4:
                pas_wd.password_strength = '3'
            elif float(stats.strength())<=0.4 and float(stats.strength())>0.3:
                pas_wd.password_strength = '2'
            elif float(stats.strength())<=0.3:
                pas_wd.password_strength = '1'

            return True
