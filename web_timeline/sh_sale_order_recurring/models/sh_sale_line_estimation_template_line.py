# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class SaleLineEstimationTempalteLine(models.Model):
    _inherit = "sh.sale.line.estimation.template.line"

    sale_recurring_line_id = fields.Many2one('sale.recurring.line','Recurring Sale Order Line Id')