# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import api, fields, models, modules, tools, _
from odoo.exceptions import AccessDenied


class Module(models.Model):
    _inherit = "ir.module.module"

    def button_immediate_install(self):

        if not self.env.user.has_group("sh_base_module_security.sh_group_base_install"):
            raise AccessDenied()
        else:
            rec = super().button_immediate_install()
            return rec

    def button_immediate_upgrade(self):

        if not self.env.user.has_group("sh_base_module_security.sh_group_base_upgrade"):
            raise AccessDenied()
        else:
            rec = super().button_immediate_upgrade()
            return rec


class BaseModuleUninstall(models.TransientModel):
    _inherit = "base.module.uninstall"

    def action_uninstall(self):

        if not self.env.user.has_group(
            "sh_base_module_security.sh_group_base_uninstall"
        ):
            raise AccessDenied()
        else:
            rec = super().action_uninstall()
            return rec
