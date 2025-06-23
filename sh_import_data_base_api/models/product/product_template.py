# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    remote_product_template_id = fields.Char("Remote Product Template ID",copy=False)
    pricelist_exception = fields.Boolean("Pricelist Exception")
    excluded_from_disocunt = fields.Boolean(string="Excluded from Discount")
    sh_active = fields.Boolean(string="Custom Active")

class ProductSupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'

    remote_product_supplierinfo_id = fields.Char("Remote Supplierinfo Id",copy=False)