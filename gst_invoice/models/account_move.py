# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = "account.move"

    gst_status = fields.Selection([
                                ('not_uploaded', 'Not Uploaded'),
                                ('ready_to_upload', 'Ready to upload'),
                                ('uploaded', 'Uploaded to govt'),
                                ('filed', 'Filed')
                            ],
                            string='GST Status',
                            default="not_uploaded",
                            copy=False,
                            help="status will be consider during gst import, "
            )
    invoice_type = fields.Selection([
                                ('b2b', 'B2B'),
                                ('b2cl', 'B2CL'),
                                ('b2cs', 'B2CS'),
                                ('b2bur', 'B2BUR'),
                                ('import', 'IMPS/IMPG'),
                                ('isd','B2B (ISD)'),
                                ('export', 'Export'),
                                ('cdnr', 'CDNR'),
                                ('cdnur', 'CDNUR'),
                            ],
                            copy=False,
                            string='Invoice Type', compute="_compute_invoice_type", store=True
            )
    export_type = fields.Selection([
                                ('regular', 'Regular'),
                                ('sez_with_payment', 'SEZ supplies with payment'),
                                ('sez_without_payment', 'SEZ supplies without payment'),
                                ('deemed', 'Deemed Exp'),
                                ('intra_state_igst', 'Intra-State supplies attracting IGST'),
                            ],
                            string='Export Type',
                            default='regular',
                            required=True
            )
    export = fields.Selection([
                                ('WPAY', 'WPay'),
                                ('WOPAY', 'WoPay')
                            ],
                            string='Export'
            )
    bonded_wh = fields.Selection([
                                ('Y', 'Yes'),
                                ('N', 'No')
                            ],
                            string='Sale from Bonded WH',
                            default='N',
                            help='When goods will be kept in bonded warehouses and later cleared from there',
            )
    itc_eligibility = fields.Selection([
                                ('Inputs', 'Inputs'),
                                ('Capital goods', 'Capital goods'),
                                ('Input services', 'Input services'),
                                ('Ineligible', 'Ineligible'),
                            ],
                            string='ITC Eligibility',
                            default='Ineligible'
            )
    reverse_charge = fields.Boolean(
                        string='Reverse Charge',
                        help="Allow reverse charges for b2b invoices")
    pre_gst = fields.Boolean(
                        string='Pre GST',
                        help="Allow pre gst for cdnr invoices")
    inr_total = fields.Float(string='INR Total')



    @api.depends('move_type','partner_id','inr_total')
    def _compute_invoice_type(self):
        code = self.env.company.state_id.code
        for invoiceObj in self:
            country_code = invoiceObj.partner_id.country_id.code == 'IN'
            if invoiceObj.move_type in ['in_refund', 'out_refund']:
                if country_code and invoiceObj.partner_id.vat:
                    invoiceObj.invoice_type = 'cdnr'
                else:
                    if not country_code:
                        invoiceObj.invoice_type = 'cdnur'
                        if not invoiceObj.export:
                            invoiceObj.export = 'WOPAY'
                    elif invoiceObj.partner_id.state_id.code != code and invoiceObj.inr_total >= 250000:
                        invoiceObj.invoice_type = 'cdnur'
                    else:
                        invoiceObj.invoice_type = 'b2cs'
            elif invoiceObj.move_type == 'in_invoice':
                if invoiceObj.partner_id.l10n_in_gst_treatment == 'isd':
                    invoiceObj.invoice_type = 'isd'
                else:
                    if country_code:
                        if invoiceObj.partner_id.l10n_in_gst_treatment in ['regular','composition','deemed_export','uin_holders','special_economic_zone']:
                            invoiceObj.invoice_type = 'b2b'
                        else:
                            invoiceObj.invoice_type = 'b2bur'
                    else:
                        invoiceObj.invoice_type = 'import'
            else:
                if country_code:
                    if invoiceObj.partner_id.l10n_in_gst_treatment in ['regular','composition','deemed_export','uin_holders','special_economic_zone','isd']:
                        invoiceObj.invoice_type = 'b2b'
                    elif invoiceObj.inr_total >= 250000 and invoiceObj.partner_id.state_id.code != code:
                        invoiceObj.invoice_type = 'b2cl'
                        if not invoiceObj.bonded_wh:
                            invoiceObj.bonded_wh = 'no'
                    else:
                        invoiceObj.invoice_type = 'b2cs'
                else:
                    invoiceObj.invoice_type = 'export'
                    if not invoiceObj.export:
                        invoiceObj.export = 'WOPAY'

