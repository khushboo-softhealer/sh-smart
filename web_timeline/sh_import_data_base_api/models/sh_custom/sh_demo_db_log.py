# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ShDemoDbLog(models.Model):
    _inherit = 'sh.demo.db.log'

    remote_sh_demo_db_log_id = fields.Char("Remote Demo Db log ID",copy=False)