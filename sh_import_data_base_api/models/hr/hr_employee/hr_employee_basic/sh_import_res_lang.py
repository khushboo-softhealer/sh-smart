# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ResLang(models.Model):
    _inherit = 'res.lang'

    remote_res_lang_id = fields.Char("Remote Res Lang ID",copy=False)


class InheritImportEmployee(models.Model):
    _inherit = "sh.import.base"

    def prepare_res_lang_vals(self, data):

        lang_vals = {
            "remote_res_lang_id": data.get('id'),
            "name": data.get('name'),
            "code": data.get('code'),
            "iso_code": data.get('iso_code'),
            "active": data.get('active'),
            "grouping": data.get('grouping'),
            "decimal_point": data.get('decimal_point'),
            "thousands_sep": data.get('thousands_sep'),
            "display_name": data.get('display_name'),
            "date_format": data.get('date_format'),
            "time_format": data.get('time_format'),
            "direction": data.get('direction').get('sh_api_current_state'),
            "week_start": data.get('week_start').get('sh_api_current_state'),
        }

        return lang_vals
