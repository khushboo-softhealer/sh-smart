# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import api, fields, models, _


class Partner(models.Model):
    _inherit = "res.partner"


    l10n_in_gst_treatment = fields.Selection(selection_add=[
            ('isd','Input Service Distributor (ISD)'),
        ])


class AccountTax(models.Model):

    _inherit = "account.tax"

    l10n_in_tax_type = fields.Selection([('gst','GST'),('exempt','Exempt'),('nil','Nill Rated'),('tds','TDS'),('tcs','TCS'),('cess','CESS')], "Tax Type", default="gst")
    l10n_in_gst_import = fields.Boolean("Import tax ", help="Tick this if this tax is import tax. Only for Indian accounting")
