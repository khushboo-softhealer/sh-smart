# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
import requests
import json
from datetime import datetime


class LanguageKnown(models.Model):
    _inherit = 'language.known'

    remote_language_known_id = fields.Char("Remote Language Known ID",copy=False)


class InheritImportEmployee(models.Model):
    _inherit = "sh.import.base"

    def import_language_known(self):

        confid = self.env['sh.import.base'].search([], limit=1)
        response = requests.get(
            '''%s/api/public/sh.emp.technical.skill''' % (confid.base_url))

        if response.status_code == 200:
            response_json = response.json()

    def prepare_language_known_vals(self, data):
        resource_vals = {
            "remote_language_known_id": data.get('id'),
            "can_read": data.get('can_read'),
            "can_write": data.get('can_write'),
            "can_speak": data.get('can_speak'),
            "display_name": data.get('display_name'),
        }
        self.map_language_id(data, resource_vals, 'language')
        return resource_vals
