# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sh_move_task_to_preapp_store = fields.Boolean('Create Task To PreApp Store')