# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, api
from datetime import date, datetime, time
from pytz import timezone

class TDSSlabTemplate(models.Model):
    _name = 'tax.slab.template'
    _description = 'Tax Slab Template' 

    name = fields.Char("Name/Reference")
    template_line_ids = fields.One2many('tax.slab.template.line','slab_template_id',string="Lines")
    rebate_taxable_limit = fields.Float("Taxable income")
    rebate_tax_relief_limit = fields.Float("Tax Relief")
    education_cess = fields.Float("Education Cess(%)")


class TDSSlabTemplateLine(models.Model):
    _name = 'tax.slab.template.line'
    _description = 'Tax Slab Template Line' 

    slab_template_id = fields.Many2one('tax.slab.template')
    from_amount = fields.Float("From")
    to_amount = fields.Float("Upto")
    tax_rate = fields.Float("Tax Rate(%)")