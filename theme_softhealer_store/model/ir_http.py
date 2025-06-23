# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _get_translation_frontend_modules_name(cls):
        mods = super(IrHttp, cls)._get_translation_frontend_modules_name()
        return mods + ['softhealer_website_base', 'theme_softhealer_store']
