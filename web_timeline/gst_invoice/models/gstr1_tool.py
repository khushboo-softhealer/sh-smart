# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

import base64
import csv
import io
import json
import zipfile
from urllib.parse import unquote_plus
import xlwt
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons.gst_invoice.models.gstr_columns import GSTTYPECOLUMN
import logging
_logger = logging.getLogger(__name__)

GSTTypeList = ['b2b','b2bur','b2cs','b2cl','export','cdnr','cdnur','imps','impg','exemp','hsn','docs','xls']
exempDataDict = {'INTRB2B': 'Inter-State supplies to registered persons', 'INTRAB2B': 'Intra-State supplies to registered persons', 'INTRB2C': 'Inter-State supplies to unregistered persons', 'INTRAB2C':  'Intra-State supplies to unregistered persons'}

def _unescape(text):
    try:
        text = unquote_plus(text.encode('utf8'))
        return text
    except Exception as e:
        return text

class Gstr1Tool(models.Model):

    _name = 'gstr1.tool'
    _description = 'GSTR1 Tool'
    _inherit = ['mail.thread']

    def _get_gst_attachments(self):
        attachments = []
        for gst_type in GSTTypeList:
            attachment = getattr(self, '%s_attachment' % gst_type)
            if attachment:
                attachments.append(attachment.id)
        if self.json_attachment:
            attachments.append(self.json_attachment.id)
        return attachments

    @api.depends('b2b_attachment', 'b2cs_attachment', 'b2bur_attachment',
                 'b2cl_attachment', 'imps_attachment', 'impg_attachment',
                 'export_attachment', 'cdnr_attachment', 'cdnur_attachment',
                 'hsn_attachment', 'exemp_attachment', 'docs_attachment',  'json_attachment','xls_attachment')
    def _get_attachment_count(self):
        attachments = self._get_gst_attachments()
        self.update({'attachment_count': len(attachments)})

    @api.depends('invoice_lines')
    def _get_invoice_count(self):
        for gst in self:
            gst.update({'invoices_count': len(gst.invoice_lines)})

    def _get_gst_type(self):
        return [('gstr1', 'GSTR1')]

    _gst_type_selection = lambda self, * \
        args, **kwargs: self._get_gst_type(*args, **kwargs)

    name = fields.Char(string='GST Invoice')
    gst_type = fields.Selection(string='GST Type', selection=_gst_type_selection,
                                help="GST Typr. ex : ('gstr1', 'gstr2' ...)", default='gstr1')
    reverse_charge = fields.Boolean(string='Reverse Charge', help="Allow reverse charges for b2b invoices")
    counter_filing_status = fields.Boolean(string='Counter Party Filing Status', default=True,
                                           help="Select when counter party has filed for b2b and cdnr invoices")
    period_id = fields.Many2one('account.period', tracking=True, string='Period')
    status = fields.Selection(
        [('not_uploaded', 'Not uploaded'),
         ('ready_to_upload', 'Ready to upload'),
         ('uploaded', 'Uploaded to govt'), ('filed', 'Filed')],
        string='Status', default="not_uploaded", tracking=True, help="status will be consider during gst import, ")
    cgt = fields.Float(string='Current Gross Turnover', tracking=True, help="Current Gross Turnover")
    gt_amount = fields.Float(string='Gross Turnover', tracking=True, help="Gross Turnover till current date")
    date_from = fields.Date(string='Date From', help="Date starting range for filter")
    date_to = fields.Date(string='Date To', help="Date end range for filter")
    invoice_lines = fields.Many2many('account.move', 'gst_account_invoice', 'gst_id', 'account_inv_id',string='Customer Invoices', help="Invoices belong to selected period.")
    b2b_attachment = fields.Many2one('ir.attachment', help="B2B Invoice Attachment")
    b2bur_attachment = fields.Many2one('ir.attachment', help="B2BUR Invoice Attachment")
    b2cs_attachment = fields.Many2one('ir.attachment', help="B2CS Invoice Attachment")
    b2cl_attachment = fields.Many2one('ir.attachment', help="B2CL Invoice Attachment")
    export_attachment = fields.Many2one('ir.attachment', help="Export Invoice Attachment")
    imps_attachment = fields.Many2one('ir.attachment', help="IMPS Invoice Attachment")
    impg_attachment = fields.Many2one('ir.attachment', help="IMPG Invoice Attachment")
    exemp_attachment = fields.Many2one('ir.attachment', help="EXEMP Invoice Attachment")
    docs_attachment = fields.Many2one('ir.attachment', help="DOCS Invoice Attachment")
    hsn_attachment = fields.Many2one('ir.attachment', help="HSN Data Attachment")
    cdnr_attachment = fields.Many2one('ir.attachment', help="CDNR Data Attachment")
    cdnur_attachment = fields.Many2one('ir.attachment', help="CDNUR Data Attachment")
    json_attachment = fields.Many2one('ir.attachment', help="json data attachment")
    xls_attachment = fields.Many2one('ir.attachment', help="XLS data attachment")
    attachment_count = fields.Integer(string='# of Attachments', compute='_get_attachment_count',
                                      readonly=True, help="Number of attachments")
    invoices_count = fields.Integer(string='# of Invoices', compute='_get_invoice_count',
                                    readonly=True, help="Number of invoices")
    itc_eligibility = fields.Selection([
        ('Inputs', 'Inputs'),
        ('Capital goods', 'Capital goods'),
        ('Input services', 'Input services'),
        ('Ineligible', 'Ineligible'),
    ], string='ITC Eligibility', default='Ineligible')
    company_id = fields.Many2one('res.company', string='Company', change_default=True,
                                 required=True, readonly=True,default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('gstr1.tool')
        return super(Gstr1Tool, self).create(vals_list)

    def unlink(self):
        for obj in self:
            if obj.status != 'not_uploaded':
                raise UserError("GST invoice can't be delete as invoices are already generated.")
        return super(Gstr1Tool, self).unlink()
    
    def check_gst_dates(self, gst_type):
        res = self.period_id.date_start > self.date_from or self.period_id.date_start > self.date_to or self.period_id.date_stop < self.date_to or self.period_id.date_stop < self.date_from
        return res

    def write(self, vals):
        res = super(Gstr1Tool, self).write(vals)
        for obj in self:
            if obj.date_from and obj.date_to:
                if obj.check_gst_dates(obj.gst_type):
                    raise UserError("Date should belong to selected period")
                if obj.date_from > obj.date_to:
                    raise UserError("End date should greater than or equal to starting date")
        return res

    def onchange(self, values, field_name, field_onchange):
        ctx = dict(self._context or {})
        ctx['current_id'] = values.get('id')
        return super(Gstr1Tool, self.with_context(ctx)).onchange(values, field_name, field_onchange)

    def reset(self):
        totalInvoices = len(self.invoice_lines)
        for gst_type in GSTTypeList:
            attachment = getattr(self, '%s_attachment' % gst_type)
            if attachment:
                attachment.unlink()
        if self.hsn_attachment:
            self.hsn_attachment.unlink()
        if self.json_attachment:
            self.json_attachment.unlink()
        if self.xls_attachment:
            self.xls_attachment.unlink()
        self.status = 'not_uploaded'
        self.updateInvoiceStatus('not_uploaded')
        if self.gst_type == 'gstr1':
            self.fetchInvoices()
        body = '<b>RESET </b>: {} GST Invoices'.format(totalInvoices)
        self.message_post(body=_(body), subtype_xmlid='mail.mt_comment')
        return True

    def action_view_invoice(self):
        invoices = self.mapped('invoice_lines')
        action = self.env.ref('gst_invoice.customer_invoice_list_action').read()[0]
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            action['views'] = [(self.env.ref('account.view_move_form').id, 'form')]
            action['res_id'] = invoices.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
    
    def action_view_invoice_lines(self):
        invoices = self.mapped('invoice_lines')
        action = self.env.ref('gst_invoice.customer_invoice_line_list_action').read()[0]
        if len(invoices) >= 1:
            action['domain'] = [('id', 'in', invoices.invoice_line_ids.filtered(lambda l: l.product_id).ids)]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    def action_view_attachment(self):
        attachments = self._get_gst_attachments()
        action = self.env.ref('gst_invoice.gst_attachments_action').read()[0]
        if len(attachments) > 1:
            action['domain'] = [('id', 'in', attachments)]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    @api.onchange('period_id', 'date_from', 'date_to')
    def _compute_invoice_lines(self):
        domain = {}
        filter = []
        ctx = dict(self._context or {})
        if ctx.get('current_id'):
            filter = [('id', '!=', ctx.get('current_id'))]
        invoiceType = ['out_invoice', 'out_refund','in_refund']
        invoiceObjs = self.getInvoiceObjs(filter, invoiceType)
        self.updateGSTInvoiceLines(invoiceObjs)
        domain.update({
            'invoice_lines': [('id', 'in', invoiceObjs.ids)],
        })
        return {'domain': domain}

    def fetchInvoices(self):
        filter = [('id', '!=', self.id)]
        invoiceObjs = self.getInvoiceObjs(filter, ['out_invoice', 'out_refund','in_refund'])
        self.invoice_lines = [(6, 0, invoiceObjs.ids)]
        if invoiceObjs:
            self.updateInvoiceCurrencyRate(invoiceObjs)
            self.updateGSTInvoiceLines(invoiceObjs)
        return True

    def fetchSupplierInvoices(self):
        filter = [('id', '!=', self.id)]
        invoiceObjs = self.getInvoiceObjs(filter, ['in_invoice', 'in_refund'])
        self.invoice_lines = [(6, 0, invoiceObjs.ids)]
        if invoiceObjs:
            self.updateInvoiceCurrencyRate(invoiceObjs)
            self.updateGSTInvoiceLines(invoiceObjs)
        return True

    def updateInvoiceCurrencyRate(self, invoiceObjs):
        for invoiceObj in invoiceObjs:
            currency = invoiceObj.currency_id
            amount_total = invoiceObj.amount_total
            if currency.name != 'INR':
                company_currency = invoiceObj.company_id.currency_id
                conversion = currency._get_conversion_rate(currency,company_currency,invoiceObj.company_id, invoiceObj.invoice_date)
                amount_total = amount_total* conversion
            invoiceObj.inr_total = amount_total
        return True

    def updateGSTInvoiceLines(self, invoiceObjs):
        code = self.env.company.state_id.code
        for invoiceObj in invoiceObjs:
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
        return True

    def getInvoiceObjs(self, extrafilter=[], invoiceType=[]):
        invoiceObjs = self.env['account.move']
        gstObjs = self.search(extrafilter)
        invoiceIds = gstObjs and gstObjs.mapped(
            'invoice_lines') and gstObjs.mapped('invoice_lines').ids or []
        if self.period_id:
            filter = ['|',
                      '&', '&', ('move_type', 'in', ['out_invoice', 'out_refund']),
                      ('invoice_date', '>=', self.period_id.date_start),
                      ('invoice_date', '<=', self.period_id.date_stop),
                      '&', '&', ('move_type', 'in', ['in_invoice', 'in_refund']),
                      ('date', '>=', self.period_id.date_start),
                      ('date', '<=', self.period_id.date_stop),
                      ('move_type', 'in', invoiceType),
                      ('company_id', '=', self.company_id.id),
                      ('state', 'in', ['posted']),
                      ]
            if not self.date_from:
                self.date_from = self.period_id.date_start
                self.date_to = self.period_id.date_stop
            if self.date_from and self.date_to:
                if self.period_id.date_start > self.date_from \
                        or self.period_id.date_start > self.date_to \
                        or self.period_id.date_stop < self.date_to \
                        or self.period_id.date_stop < self.date_from:
                    raise UserError(_("Date should belong to selected period"))
                if self.date_from > self.date_to:
                    raise UserError(
                        _("End date should greater than or equal to starting date"))
                filter += ['|',
                           '&', '&', ('move_type', 'in', ['out_invoice', 'out_refund']),
                           ('invoice_date', '>=', self.date_from),
                           ('invoice_date', '<=', self.date_to),
                           '&', '&', ('move_type', 'in', ['in_invoice', 'in_refund']),
                           ('date', '>=', self.date_from),
                           ('date', '<=', self.date_to),
                           ]
            if invoiceIds:
                filter.append(('id', 'not in', invoiceIds))
            invoiceObjs = invoiceObjs.search(filter)
        return invoiceObjs

    def updategst1Worksheet(self, worksheet, maindata, columns=[]):
        col = 0
        for column in columns:
            worksheet.write(0, col, column)
            col+=1
        row = 1 if columns else 0
        for data in maindata:
            col = 0
            for d in data:
                worksheet.write(row, col, d) 
                col +=1
            row += 1
        return worksheet
    
    def generateCsv(self):
        """ This function is used to create & save all the csv & json file in as attachment"""
        invoiceObjs = self.invoice_lines
        name = self.name
        if self.xls_attachment:
            self.xls_attachment = False
        gstinCompany = self.env.company.vat
        fp = (self.period_id.code or '').replace('/', '')
        jsonData = {
            "gstin": gstinCompany,
            "fp": fp,
            "version": "GST3.0.4",
            "hash": "hash",
        }
        gstType = self.gst_type
        if invoiceObjs:
            workbook = xlwt.Workbook('%s.xlsx'%(name), {'in_memory': True})
            typeDict = {}
            invoiceIds = invoiceObjs.ids
            for invoiceObj in invoiceObjs:
                if typeDict.get(invoiceObj.invoice_type):
                    typeDict.get(invoiceObj.invoice_type).append(invoiceObj.id)
                else:
                    typeDict[invoiceObj.invoice_type] = [invoiceObj.id]
            typeList = self.getTypeList()
            for invoice_type, active_ids in typeDict.items():
                if invoice_type in typeList:
                    continue
                respData = self.exportCsv(active_ids, invoice_type, name, gstType)
                attachment = respData[0]
                jsonInvoiceData = respData[1]
                maindata = respData[2]
                worksheet = workbook.add_sheet(invoice_type)
                if invoice_type == 'b2b':
                    columns = GSTTYPECOLUMN.get('%s_%s'%(invoice_type,gstType))
                    worksheet = self.updategst1Worksheet(worksheet, maindata, columns)
                    jsonData.update({invoice_type: jsonInvoiceData})
                    self.b2b_attachment = attachment.id
                if invoice_type == 'b2bur':
                    columns = GSTTYPECOLUMN.get(invoice_type)
                    worksheet = self.updategst1Worksheet(worksheet, maindata, columns)
                    jsonData.update({invoice_type: jsonInvoiceData})
                    self.b2bur_attachment = attachment.id
                if invoice_type == 'b2cs':
                    columns = GSTTYPECOLUMN.get(invoice_type)
                    worksheet = self.updategst1Worksheet(worksheet, maindata, columns)
                    self.b2cs_attachment = attachment.id
                    jsonData.update({invoice_type: jsonInvoiceData})
                if invoice_type == 'b2cl':
                    columns = GSTTYPECOLUMN.get(invoice_type)
                    worksheet = self.updategst1Worksheet(worksheet, maindata, columns)
                    jsonData.update({invoice_type: jsonInvoiceData})
                    self.b2cl_attachment = attachment.id
                if invoice_type == 'import':
                    columns = GSTTYPECOLUMN.get('imps')
                    worksheet = self.updategst1Worksheet(worksheet, maindata, columns)
                    columns = GSTTYPECOLUMN.get('impg')
                    worksheet = self.updategst1Worksheet(worksheet, maindata, columns)
                    impsAttach = attachment[0]
                    impsJsonInvoiceData = attachment[1]
                    impgAttach = jsonInvoiceData[0]
                    impgJsonInvoiceData = jsonInvoiceData[1]
                    jsonData.update({'imp_s': impsJsonInvoiceData,
                                    'imp_g': impgJsonInvoiceData})
                    if impsAttach:
                        self.imps_attachment = impsAttach.id
                    if impgAttach:
                        self.impg_attachment = impgAttach.id
                if invoice_type == 'export':
                    columns = GSTTYPECOLUMN.get(invoice_type)
                    worksheet = self.updategst1Worksheet(worksheet, maindata, columns)
                    jsonData.update({'exp': {'exp_typ': 'WOPAY',
                                    'inv': jsonInvoiceData}})
                    self.export_attachment = attachment.id
                if invoice_type == 'cdnr':
                    columns = GSTTYPECOLUMN.get('%s_%s'%(invoice_type,gstType))
                    worksheet = self.updategst1Worksheet(worksheet, maindata, columns)
                    jsonData.update({invoice_type: jsonInvoiceData})
                    self.cdnr_attachment = attachment.id
                if invoice_type == 'cdnur':
                    columns = GSTTYPECOLUMN.get('%s_%s'%(invoice_type,gstType))
                    worksheet = self.updategst1Worksheet(worksheet, maindata, columns)
                    jsonData.update({invoice_type: jsonInvoiceData})
                    self.cdnur_attachment = attachment.id

            if not self.exemp_attachment:
                worksheet = workbook.add_sheet('exemp')
                respExempData = self.exportCsv(invoiceIds, 'exemp', name, gstType)
                if respExempData:
                    exempAttachment = respExempData[0]
                    jsonInvoiceData = respExempData[1]
                    maindata = respExempData[2]
                    columns = GSTTYPECOLUMN.get('exemp')
                    worksheet = self.updategst1Worksheet(worksheet, maindata, columns)
                    jsonData.update({'nil': {'inv': jsonInvoiceData}})
                    if exempAttachment:
                            self.exemp_attachment = exempAttachment.id
            if not self.docs_attachment and self.gst_type == 'gstr1':
                invoices = self.env['account.move'].search( ['|',
                      '&', '&', ('move_type', 'in', ['out_invoice', 'out_refund','in_refund']),
                      ('invoice_date', '>=', self.period_id.date_start),
                      ('invoice_date', '<=', self.period_id.date_stop),
                      '&', '&', ('move_type', 'in', ['out_invoice', 'out_refund','in_refund']),
                      ('date', '>=', self.period_id.date_start),
                      ('date', '<=', self.period_id.date_stop),
                      ('move_type', 'in', ['out_invoice', 'out_refund','in_refund']),
                      ('company_id', '=', self.company_id.id),
                      ('state', 'in', ['posted','cancel']),
                      ])
                respDocsData = self.exportCsv(invoices.ids, 'docs', name, gstType)
                worksheet = workbook.add_sheet('docs')
                if respDocsData:
                    docsAttachment = respDocsData[0]
                    jsonInvoiceData = respDocsData[1]
                    maindata = respDocsData[2]
                    columns = GSTTYPECOLUMN.get('docs')
                    worksheet = self.updategst1Worksheet(worksheet, maindata, columns)
                    jsonData.update({'doc_issue':jsonInvoiceData})
                    if docsAttachment:
                            self.docs_attachment = docsAttachment.id

            if not self.hsn_attachment:
                respHsnData = self.exportCsv(invoiceIds, 'hsn', name,
                        gstType)
                if respHsnData:
                    hsnAttachment = respHsnData[0]
                    jsonInvoiceData = respHsnData[1]
                    jsonData.update({'hsn': {'data': jsonInvoiceData}})
                    if hsnAttachment:
                        self.hsn_attachment = hsnAttachment.id
            if not self.json_attachment:
                if jsonData:
                    jsonData = json.dumps(jsonData, indent=4, sort_keys=False)
                    base64Data = base64.b64encode(jsonData.encode('utf-8'))
                    jsonAttachment = False
                    json_name = "returns_%s%s%s_R1_%s_offline"%(str(self.date_from.day).zfill(2), str(self.date_from.month).zfill(2), self.date_from.year, self.company_id.vat)
                    zip_buffer = io.BytesIO()
                    try:
                        jsonFileName = "{}.json".format(json_name)
                        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                            zip_file.writestr(jsonFileName, jsonData)
                        jsonAttachment = self.env['ir.attachment'].create({
                            'datas': base64.b64encode(zip_buffer.getvalue()),
                            'type': 'binary',
                            'res_model': 'gstr1.tool',
                            'res_id': self.id,
                            'db_datas':  "{}.zip".format(json_name),
                            'store_fname':  "{}.zip".format(json_name),
                            'name':  "{}.zip".format(json_name),
                            })
                    except ValueError:
                        return jsonAttachment
                    if jsonAttachment:
                        self.json_attachment = jsonAttachment.id
            if not self._context.get('export_type') or self._context.get('export_type') == 'xls_attachment':
                fp = io.BytesIO()
                workbook.save(fp)
                workbook_data = fp.getvalue()
                base64Data = base64.b64encode(workbook_data)
                work_data = self.env['ir.attachment'].create({
                                    'datas': base64Data,
                                    'type': 'binary',
                                    'res_model': 'gstr1.tool',
                                    'res_id': self.id,
                                    'db_datas': '%s.xlsx'%(name),
                                    'store_fname': '%s.xlsx'%(name),
                                    'name': '%s.xlsx'%(name),
                                    })
                self.xls_attachment = work_data.id
            self.status = 'ready_to_upload'
        message = "Your gst & hsn csv are successfully generated"
        partial = self.env['message.wizard'].create({'text': message})
        return {
            'name': ("Information"),
            'view_mode': 'form',
            'res_model': 'message.wizard',
            'view_id': self.env.ref('gst_invoice.message_wizard_form1').id,
            'res_id': partial.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
        }

    def getTypeList(self):
        typeList = []
        for gst_type in GSTTypeList:
            attachment = getattr(self, '%s_attachment' % gst_type)
            if attachment:
                typeList.append(gst_type)
        return typeList

    def export_gst_attachment(self):
        if self._context.get('export_type'):
            export_type = self._context.get('export_type')
            if hasattr(self, '%s' % export_type):
                attachment = getattr(self, '%s' % export_type)
                if not attachment:
                    self.generateCsv()
                attachment = getattr(self, '%s' % export_type)
                if not attachment:
                    raise UserError("CSV of %s invoice is not present"%((export_type.split('_')[0])).upper())
                return {'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=1'% attachment.id, 'target': 'new'}

    def uploadGST(self):
        partial = self.env['message.wizard'].create(
            {'text': 'GST Invoice is successfully uploaded'})
        self.status = 'uploaded'
        self.updateInvoiceStatus('uploaded')
        return {
            'name': ("Information"),
            'view_mode': 'form',
            'res_model': 'message.wizard',
            'view_id': self.env.ref('gst_invoice.message_wizard_form1').id,
            'res_id': partial.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
        }

    def filedGST(self):
        partial = self.env['message.wizard'].create(
            {'text': 'GST Invoice is successfully Filed'})
        self.status = 'filed'
        self.updateInvoiceStatus('filed')
        return {
            'name': ("Information"),
            'view_mode': 'form',
            'res_model': 'message.wizard',
            'view_id': self.env.ref('gst_invoice.message_wizard_form1').id,
            'res_id': partial.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
        }

    def updateInvoiceStatus(self, status):
        self.invoice_lines.write({'gst_status': status})
        return True

    @api.model
    def exportCsv(self, active_ids, invoice_type, gstToolName, gstType):
        if invoice_type == 'import':
            impsData = self.getInvoiceData(active_ids, 'imps', gstType)
            mainData = impsData[0]
            impsAttachment = self.prepareCsv(mainData, 'imps', gstToolName, gstType)
            impsJsonData = impsData[1]
            impgData = self.getInvoiceData(active_ids, 'impg', gstType)
            mainData = impgData[0]
            impgAttachment = self.prepareCsv(mainData, 'impg', gstToolName, gstType)
            impgJsonData = impgData[1]
            return [[impsAttachment, impsJsonData], [impgAttachment, impgJsonData]]
        respData = self.getInvoiceData(active_ids, invoice_type, gstType)
        mainData = respData[0]
        jsonData = respData[1]
        attachment = self.prepareCsv(mainData, invoice_type, gstToolName, gstType)
        return [attachment, jsonData, mainData]

    def prepareCsv(self, mainData, invoice_type, gstToolName, gstType):
        attachment = False
        if mainData:
            fp = io.StringIO()
            writer = csv.writer(fp, quoting=csv.QUOTE_NONE, escapechar='\\')
            if invoice_type in ['b2b','cdnr', 'cdnur']:
                columns = GSTTYPECOLUMN.get('%s_%s'%(invoice_type,gstType))
                writer.writerow(columns)
            else:
                columns = GSTTYPECOLUMN.get(invoice_type)
                writer.writerow(columns)
            for lineData in mainData:
                writer.writerow([_unescape(name) for name in lineData])
            fp.seek(0)
            data = fp.read()
            fp.close()
            attachment = self.generateAttachment(
                data, invoice_type, gstToolName)
        return attachment

    def generateAttachment(self, data, invoice_type, gstToolName):
        attachment = False
        base64Data = base64.b64encode(data.encode('utf-8'))
        store_fname = '{}_{}.csv'.format(invoice_type, gstToolName)
        try:
            attachment = self.env['ir.attachment'].create({
                'datas': base64Data,
                'type': 'binary',
                'res_model': 'gstr1.tool',
                'res_id': self.id,
                'db_datas': store_fname,
                'store_fname': store_fname,
                'name': store_fname
            })
        except ValueError:
            return attachment
        return attachment

    def getexempData(self, invoiceObj,sply_ty, exempDict={}):
        """ This function return data for Table 8A, 8B, 8C, 8D - Nil Rated Supplies in json format"""
        nil_supplies_price, exempt_supplies_price, non_gst_supplies_price = 0.0, 0.0, 0.0
        if invoiceObj:
            sign = -1 if invoiceObj.move_type == 'out_refund' else 1
            non_gst_supplies = invoiceObj.invoice_line_ids.filtered(lambda line: line.product_id and not line.tax_ids )
            if non_gst_supplies:
                for non in non_gst_supplies:
                    non_gst_supplies_price += non.price_subtotal
            for line in invoiceObj.invoice_line_ids.filtered(lambda l: l.product_id):
                nil_supplies = line.tax_ids.filtered(lambda t: t.l10n_in_tax_type == 'nil' and t.amount == 0.0)
                if nil_supplies:
                    nil_supplies_price += line.price_subtotal
                exempt_supplies = line.tax_ids.filtered(lambda t: t.l10n_in_tax_type == 'exempt')
                if exempt_supplies:
                    exempt_supplies_price += line.price_subtotal
        
        if sply_ty in exempDict:
            exempDict[sply_ty]['expt_amt'] += sign *exempt_supplies_price
            exempDict[sply_ty]['nil_amt'] += sign * nil_supplies_price
            exempDict[sply_ty]['ngsup_amt'] += sign *non_gst_supplies_price
        else:
            exempDict[sply_ty] = {'nil_amt': sign * nil_supplies_price, 'expt_amt':sign * exempt_supplies_price,'ngsup_amt': sign * non_gst_supplies_price}
        return exempDict

    def getJournalDict(self, invoices):
        journal_dict = {'out_invoice':{},'in_invoice':{},'in_refund':{},'out_refund':{}}
        for invoice in invoices.sorted('id'):
            if invoice.journal_id.id in journal_dict[invoice.move_type]:
                journal_dict[invoice.move_type][invoice.journal_id.id].append(invoice.id)
            else:
                journal_dict[invoice.move_type][invoice.journal_id.id] = [invoice.id]
        return journal_dict

    def getDocDataDict(self, docsDataLST, invoices):
        journal_dict = self.getJournalDict(invoices)
        count = 0
        docs_data , docs_dict_data= [], []
        for value in docsDataLST:
            type = value[0] if isinstance(value, list) else False
            doc_dict = []
            count += 1
            docs_data_dict = {'doc_num':count,'doc_typ':value}
            data_list = [value[-1]] if isinstance(value, list) else [value]
            if isinstance(value, list):
                num_count = count
                for journal in journal_dict[type]:
                    moves = self.env['account.move'].browse(journal_dict[type][journal])
                    cancel_invoice = len(moves.filtered(lambda l: l.state == 'cancel'))
                    doc_dict.append({"num":num_count,"to":moves[0].name,"from":moves[-1].name,"totnum":len(moves),"cancel":cancel_invoice,"net_issue":len(moves)- cancel_invoice})
                    num_count += 1
                    new_data_list = data_list + [moves[0].name,moves[-1].name,len(moves),cancel_invoice ]
                    docs_data.append(new_data_list)
            else:
                docs_data.append(data_list)
            docs_data_dict['docs'] = doc_dict
            docs_dict_data.append(docs_data_dict) 
        return (docs_dict_data, docs_data)

    def getB2Bdata(self, invoiceObj, invoiceNumber, invoiceDate, invoiceTotal, code,reverseCharge,jsonInvType, stateName, invType_val, gstType, invoiceType, invoiceJsonDate, b2bDataDict, data, invData):
        customerName = invoiceObj.partner_id.name
        invData = {
            "inum": invoiceNumber,
            "idt": invoiceDate,
            "val": invoiceTotal,
            "pos": code,
            "rchrg": reverseCharge,
            "inv_typ": jsonInvType
        }
        gstrData = [invoiceObj.l10n_in_gstin, invoiceNumber, invoiceDate,
                    invoiceTotal, stateName, reverseCharge, invType_val]
        if gstType == 'gstr1':
            gstrData = [invoiceObj.l10n_in_gstin, customerName, invoiceNumber,
                        invoiceDate, invoiceTotal, stateName, reverseCharge, 0.0, invType_val, '']
        data.extend(gstrData)
        respData = self.getGSTInvoiceData(
            invoiceObj, invoiceType, data, gstType)
        data = respData[0]
        invData['itms'] = respData[1]
        invData['idt'] = invoiceJsonDate
        if b2bDataDict.get(invoiceObj.l10n_in_gstin):
            b2bDataDict[invoiceObj.l10n_in_gstin].append(invData)
        else:
            b2bDataDict[invoiceObj.l10n_in_gstin] = [invData]
        return (b2bDataDict, data, invData)

    def getB2burdata(self, invoiceObj, gstcompany_id, invoiceNumber, invoiceDate, invoiceTotal, code, stateName,  gstType, invoiceType, invoiceJsonDate, b2burDataDict, data, invData):
        sply_ty = 'INTER'
        sply_type = 'Inter State'
        if invoiceObj.partner_id.state_id.code != gstcompany_id.state_id.code:
            sply_ty = 'INTRA'
            sply_type = 'Intra State'
        invData = {
            "inum": invoiceNumber,
            "idt": invoiceDate,
            "val": invoiceTotal,
            "pos": code,
            "sply_ty": sply_ty
        }
        supplierName = invoiceObj.partner_id.name
        data.extend([supplierName, invoiceNumber,
                        invoiceDate, invoiceTotal, stateName, sply_type])
        respData = self.getGSTInvoiceData(
            invoiceObj, invoiceType, data, gstType)
        data = respData[0]
        invData['itms'] = respData[1]
        invData['idt'] = invoiceJsonDate
        if b2burDataDict.get(supplierName):
            b2burDataDict[supplierName].append(invData)
        else:
            b2burDataDict[supplierName] = [invData]
            return (b2burDataDict, data, invData)

    def getB2cldata(self, invoiceObj,  invoiceNumber, invoiceDate, invoiceTotal, code, stateName,  gstType, invoiceType, invoiceJsonDate, b2clJsonDataDict, data,invData):
        invData = {
            "inum": invoiceNumber,
            "idt": invoiceDate,
            "val": invoiceTotal,
        }
        data.extend([invoiceNumber, invoiceDate,
                        invoiceTotal, stateName, 0.0])
        respData = self.getGSTInvoiceData(
            invoiceObj, invoiceType, data, gstType)
        data = respData[0]
        invData['itms'] = respData[1]
        invData['idt'] = invoiceJsonDate
        if b2clJsonDataDict.get(code):
            b2clJsonDataDict[code].append(invData)
        else:
            b2clJsonDataDict[code] = [invData]
        return (b2clJsonDataDict, data, invData)

    def getB2csdata(self, invoiceObj, code, stateName,  gstType, invoiceType,  b2csDataDict,b2csJsonDataDict, data,invData):
        invData = {'pos': code}
        b2bData = ['OE', stateName]
        respData = self.getGSTInvoiceData(invoiceObj,
                invoiceType, b2bData, gstType)
        b2bData = respData[0]
        rateDataDict = respData[2]
        rateJsonDict = respData[3]
        if b2csDataDict.get(stateName):
            for key in rateDataDict.keys():
                if b2csDataDict.get(stateName).get(key):
                    for key1 in rateDataDict.get(key).keys():
                        if key1 in ['rt']:
                            continue
                        if b2csDataDict.get(stateName).get(key).get(key1):
                            b2csDataDict.get(stateName).get(key)[key1] = b2csDataDict.get(
                                stateName).get(key)[key1] + rateDataDict.get(key)[key1]
                        else:
                            b2csDataDict.get(stateName).get(
                                key)[key1] = rateDataDict.get(key)[key1]
                else:
                    b2csDataDict.get(stateName)[
                        key] = rateDataDict[key]
        else:
            b2csDataDict[stateName] = rateDataDict
        if b2csJsonDataDict.get(code):
            for key in rateJsonDict.keys():
                if b2csJsonDataDict.get(code).get(key):
                    for key1 in rateJsonDict.get(key).keys():
                        if b2csJsonDataDict.get(code).get(key).get(key1):
                            if key1 in ['rt', 'sply_ty', 'typ']:
                                continue
                            b2csJsonDataDict.get(code).get(key)[key1] = b2csJsonDataDict.get(
                                code).get(key)[key1] + rateJsonDict.get(key)[key1]
                            b2csJsonDataDict.get(code).get(key)[key1] = round(
                                b2csJsonDataDict.get(code).get(key)[key1], 2)
                        else:
                            b2csJsonDataDict.get(code).get(
                                key)[key1] = rateJsonDict.get(key)[key1]
                else:
                    b2csJsonDataDict.get(code)[key] = rateJsonDict[key]
        else:
            b2csJsonDataDict[code] = rateJsonDict
        if respData[1]:
            invData.update(respData[1][0])
        return (b2csJsonDataDict, b2csDataDict, data, invData)

    def getimpsdata(self, invoiceObj, invoiceNumber, invoiceDate, invoiceTotal,   gstType, invoiceType, invoiceJsonDate, jsonData, data,invData):
        state = self.env.company.state_id
        code = _unescape(state.l10n_in_tin) or 0
        sname = _unescape(state.name)
        stateName = "{}-{}".format(code, sname)
        invData = {
            "inum": invoiceNumber,
            "idt": invoiceDate,
            "ival": invoiceTotal,
            "pos": code
        }
        data.extend([invoiceNumber, invoiceDate,
                        invoiceTotal, stateName])
        respData = self.getGSTInvoiceData(
            invoiceObj, invoiceType, data, gstType)
        data = respData[0]
        invData['itms'] = respData[1]
        invData['idt'] = invoiceJsonDate
        jsonData.append(invData)
        return (jsonData, data, invData )

    def getimpgdata(self, invoiceObj, invoiceNumber, invoiceDate, invoiceTotal,   gstType, invoiceType, invoiceJsonDate, jsonData, data,invData):
        companyGST = self.env.company.vat
        portcode = ''
        if invoiceObj.l10n_in_shipping_port_code_id:
            portcode = invoiceObj.l10n_in_shipping_port_code_id.name
        invData = {
            "boe_num": invoiceNumber,
            "boe_dt": invoiceJsonDate,
            "boe_val": invoiceTotal,
            "port_code": portcode,
            "stin": companyGST,
            'is_sez': 'Y'
        }
        data.extend([portcode, invoiceNumber, invoiceDate,
                        invoiceTotal, 'Imports', companyGST])
        respData = self.getGSTInvoiceData(
            invoiceObj, invoiceType, data, gstType)
        data = respData[0]
        invData['itms'] = respData[1]
        jsonData.append(invData)
        return (jsonData, data, invData )

    def getexportdata(self, invoiceObj, invoiceNumber, invoiceDate, invoiceTotal,   gstType, invoiceType, invoiceJsonDate, jsonData, data, invData):
        portcode = ''
        if invoiceObj.l10n_in_shipping_port_code_id:
            portcode = invoiceObj.l10n_in_shipping_port_code_id.name
        shipping_bill_number = invoiceObj.l10n_in_shipping_bill_number or ''
        shipping_bill_date = invoiceObj.l10n_in_shipping_bill_date and invoiceObj.l10n_in_shipping_bill_date.strftime(
            '%d-%m-%Y') or ''
        invData = {
            "inum": invoiceNumber,
            "idt": invoiceDate,
            "val": invoiceTotal,
            "sbpcode": portcode,
            "sbnum": shipping_bill_number,
            "sbdt": shipping_bill_date,
        }
        data.extend([
            invoiceObj.export, invoiceNumber, invoiceDate,
            invoiceTotal, portcode, shipping_bill_number,
            shipping_bill_date, 0.0
        ])
        respData = self.getGSTInvoiceData(
            invoiceObj, invoiceType, data, gstType)
        data = respData[0]
        invData['itms'] = respData[1]
        invData['idt'] = invoiceJsonDate
        jsonData.append(invData)
        return (jsonData, data, invData )
    
    def getcreditdata(self, invoiceObj, invoiceNumber, gstcompany_id, code, reverseCharge, jsonInvType, originalInvNumber, stateName, invType_val, originalInvJsonDate, invoiceDate, invoiceTotal, gstType, invoiceType, invoiceJsonDate, cdnrDataDict, cdnurDataDict, data,invData):
        # _logger.info("======invoiceObj====%r", invoiceNumber)
        if self.gst_type == 'gstr1':
            sign = -1 if invoiceObj.move_type in ('out_refund') else 1
        customerName = invoiceObj.partner_id.name
        pre_gst = 'N'
        if invoiceObj.pre_gst:
            pre_gst = 'Y'
        invoiceObjRef = invoiceObj.ref or ''
        reasonList = invoiceObjRef.split(',')
        reasonNote = reasonList[1].strip() if len(
            reasonList) > 1 else invoiceObjRef
        sply_ty = 'INTER'
        sply_type = 'Inter State'
        if invoiceObj.partner_id.state_id.code != gstcompany_id.state_id.code:
            sply_ty = 'INTRA'
            sply_type = 'Intra State'
        invData = {
            "nt_num": invoiceNumber,
            "nt_dt": invoiceJsonDate,
            "ntty": "C" if invoiceObj.move_type =='out_refund' else 'D',
            "val": sign * invoiceTotal,
            "pos": code,
        }
        if invoiceType == 'cdnr':
            invData.update({
                "rchrg": reverseCharge,
                "inv_typ": jsonInvType,
            })
            gstrData = [invoiceObj.l10n_in_gstin, invoiceNumber, invoiceDate, originalInvNumber,
                        originalInvJsonDate, reverseCharge, 'D', reasonNote, sply_type, invoiceTotal]
            if gstType == 'gstr1':
                gstrData = [invoiceObj.l10n_in_gstin, customerName, invoiceNumber,
                            invoiceDate, "C" if invoiceObj.move_type =='out_refund' else 'D', stateName, reverseCharge, invType_val, sign * invoiceTotal, 0.0]
        else:
            country_code = invoiceObj.partner_id.country_id.code == 'IN'
            if country_code:
                ur_type = 'B2CL'
            else:
                ur_type = 'EXPWOP'
                if invoiceObj.export == 'WPAY':
                    ur_type = 'EXPWP'
            invData['typ'] = ur_type
            gstrData = [ur_type, invoiceNumber, invoiceDate,
                        "C" if invoiceObj.move_type =='out_refund' else 'D', stateName, sign* invoiceTotal, 0.0]
        data.extend(gstrData)
        respData = self.getGSTInvoiceData(
            invoiceObj, invoiceType, data, gstType)
        # _logger.info("======%r", respData)
        data = respData[0]
        invData['itms'] = respData[1]
        if invoiceType == 'cdnr':
            if cdnrDataDict.get(invoiceObj.l10n_in_gstin):
                cdnrDataDict[invoiceObj.l10n_in_gstin].append(invData)
            else:
                cdnrDataDict[invoiceObj.l10n_in_gstin] = [invData]
        else:
            cdnurDataDict['cdnur'].append(invData)
        return (cdnrDataDict, cdnurDataDict, data, invData )

    def getInvoiceData(self, active_ids, invoiceType, gstType):
        mainData ,jsonData = [] , []
        count = 0
        b2csDataDict, b2csJsonDataDict, b2clJsonDataDict, b2burDataDict, b2bDataDict, cdnrDataDict, hsnDict, hsnDataDict, exempDict, docsDataDict = {} ,{}, {}, {}, {}, {}, {}, {}, {}, {}
        exempDict = {'INTRB2B':{"nil_amt":0,"expt_amt":0,"ngsup_amt":0},'INTRAB2B':{"nil_amt":0,"expt_amt":0,"ngsup_amt":0},'INTRB2C':{"nil_amt":0,"expt_amt":0,"ngsup_amt":0},'INTRAB2C':{"nil_amt":0,"expt_amt":0,"ngsup_amt":0}}
        docsDataLST = [['out_invoice','Invoices for outward supply'], ['in_invoice','Invoices for inward supply from unregistered person'], ['in_refund','Debit Note'],['out_refund','Credit Note'],'Revised Invoice','Receipt Voucher','Payment Voucher','Refund Voucher','Delivery Challan for job work','Delivery Challan for supply on approval','Delivery Challan in case of liquid gas','Delivery Challan in case other than by way of supply (excluding at S no. 9 to 11)']
        cdnurDataDict = {'cdnur': []}
        reverseChargeMain = self.reverse_charge and 'Y' or 'N'
        counterFilingStatus = self.counter_filing_status and 'Y' or 'N'
        gstcompany_id = self.company_id or self.env.company
        invoiceObjs = self.env['account.move'].browse(active_ids)
        for invoiceObj in invoiceObjs.sorted('id'):
            invData = {}
            reverseCharge = 'Y' if invoiceObj.reverse_charge else 'N' if reverseChargeMain == 'N' else reverseChargeMain
            invType = invoiceObj.export_type or 'regular'
            invType_val = dict(invoiceObj._fields['export_type'].selection).get(
                invoiceObj.export_type)
            jsonInvType = 'R'
            if invType == 'sez_with_payment':
                jsonInvType = 'SEWP'
            elif invType == 'sez_without_payment':
                jsonInvType = 'SEWOP'
            elif invType == 'deemed':
                jsonInvType = 'DE'
            elif invType == 'intra_state_igst':
                jsonInvType = 'CBW'
            currency = invoiceObj.currency_id
            invoiceNumber = invoiceObj.name or ''
            if len(invoiceNumber) > 16:
                invoiceNumber = invoiceNumber[-16:]
            invoiceDate = invoiceObj.move_type in [
                'out_invoice', 'out_refund','in_refund'] and invoiceObj.date or invoiceObj.invoice_date
            invoiceJsonDate = invoiceDate.strftime('%d-%m-%Y')
            invoiceDate = invoiceDate.strftime('%d-%b-%Y')
            originalInvNumber, originalInvDate, originalInvJsonDate = '', '', ''
            originalInvObj = invoiceObj.reversed_entry_id
            if originalInvObj:
                originalInvNumber = originalInvObj.name or ''
                if len(originalInvNumber) > 16:
                    originalInvNumber = originalInvNumber[-16:]
                originalInvDate = originalInvObj.move_type in [
                    'out_invoice', 'out_refund','in_refund'] and originalInvObj.date or originalInvObj.invoice_date
                originalInvJsonDate = originalInvDate.strftime('%d-%b-%Y')
                originalInvDate = originalInvDate.strftime('%d-%m-%Y')
            invoiceTotal = invoiceObj.amount_total
            invoiceTotal = sum([sum(self.getTaxedAmount(invoiceLineObj.tax_ids, invoiceLineObj.price_subtotal / invoiceLineObj.quantity, currency, invoiceLineObj, invoiceObj)) for invoiceLineObj in invoiceObj.invoice_line_ids.filtered(lambda l: l.product_id)]) 
            invoiceObj.inr_total = invoiceTotal
            invoiceTotal = round(invoiceTotal, 2)
            state = invoiceObj.partner_id.state_id
            code = _unescape(state.l10n_in_tin) or 0
            sname = _unescape(state.name)
            stateName = "{}-{}".format(code, sname)
            data = []
            if invoiceType == 'b2b':
                b2bDataDict, data, invData = self.getB2Bdata(invoiceObj, invoiceNumber, invoiceDate, invoiceTotal, code,reverseCharge,jsonInvType, stateName, invType_val, gstType, invoiceType, invoiceJsonDate, b2bDataDict, data, invData)
            elif invoiceType == 'b2bur':
                b2burDataDict, data, invData = self.getB2burdata(invoiceObj, gstcompany_id, invoiceNumber, invoiceDate, invoiceTotal, code, stateName,  gstType, invoiceType, invoiceJsonDate, b2burDataDict, data, invData)
            elif invoiceType == 'b2cl':
                b2clJsonDataDict, data, invData = self.getB2cldata(invoiceObj,  invoiceNumber, invoiceDate, invoiceTotal, code, stateName,  gstType, invoiceType, invoiceJsonDate, b2clJsonDataDict, data, invData)                
            elif invoiceType == 'b2cs':
                b2csJsonDataDict, b2csDataDict, data, invData = self.getB2csdata(invoiceObj, code, stateName,  gstType, invoiceType,  b2csDataDict,b2csJsonDataDict, data,invData)                
            elif invoiceType == 'imps':
                jsonData, data,invData = self.getimpsdata(invoiceObj, invoiceNumber, invoiceDate, invoiceTotal,   gstType, invoiceType, invoiceJsonDate, jsonData, data,invData) 
            elif invoiceType == 'impg':
                jsonData, data,invData = self.getimpgdata(invoiceObj, invoiceNumber, invoiceDate, invoiceTotal, gstType, invoiceType, invoiceJsonDate, jsonData, data,invData) 
            elif invoiceType == 'export':
                jsonData, data,invData = self.getexportdata(invoiceObj, invoiceNumber, invoiceDate, invoiceTotal, gstType, invoiceType, invoiceJsonDate, jsonData, data,invData) 
            elif invoiceType in ['cdnr', 'cdnur']:
                cdnrDataDict, cdnurDataDict, data, invData = self.getcreditdata(invoiceObj, invoiceNumber, gstcompany_id, code, reverseCharge, jsonInvType, originalInvNumber, stateName, invType_val, originalInvJsonDate, invoiceDate, invoiceTotal, gstType, invoiceType, invoiceJsonDate, cdnrDataDict, cdnurDataDict, data,invData) 
            elif invoiceType == 'hsn':
                if invoiceObj.move_type in ['out_invoice','out_refund','in_refund']:
                    respData = self.getHSNData(
                        invoiceObj, count, hsnDict, hsnDataDict)
                    data = respData[0]
                    jsonData.extend(respData[1])
                    hsnDict = respData[2]
                    hsnDataDict = respData[3]
                invoiceObj.gst_status = 'ready_to_upload'
            elif invoiceType == 'exemp':
                if invoiceObj.partner_id.country_id.code == 'IN' and invoiceObj.move_type != 'in_refund':
                    if invoiceObj.partner_id.l10n_in_gst_treatment in ['regular','composition','deemed_export','uin_holders','special_economic_zone'] and invoiceObj.partner_id.state_id == self.company_id.state_id:
                        sply_ty = 'INTRAB2B'
                        exempDict = self.getexempData(invoiceObj,sply_ty, exempDict)
                    elif invoiceObj.partner_id.l10n_in_gst_treatment in ['regular','composition','deemed_export','uin_holders','special_economic_zone'] and invoiceObj.partner_id.state_id != self.company_id.state_id:
                        sply_ty = 'INTRB2B'
                        exempDict = self.getexempData(invoiceObj,sply_ty, exempDict)
                    elif invoiceObj.partner_id.l10n_in_gst_treatment in ['unregistered', 'consumer'] and invoiceObj.partner_id.state_id == self.company_id.state_id:
                        sply_ty = 'INTRAB2C'
                        exempDict = self.getexempData(invoiceObj,sply_ty, exempDict)
                    elif invoiceObj.partner_id.l10n_in_gst_treatment in ['unregistered', 'consumer'] and invoiceObj.partner_id.state_id != self.company_id.state_id:
                        sply_ty = 'INTRB2C'
                        exempDict = self.getexempData(invoiceObj,sply_ty, exempDict)

            if data:
                mainData.extend(data)
        if exempDict and invoiceType == 'exemp':
            exemp_data, exempmainDict = [], []
            for value in exempDict:
                data_list = [exempDataDict.get(value)] + list(exempDict[value].values())
                exemp_data.append(data_list)
                exemp_dict = {'sply_ty':value, **exempDict.get(value)}
                exempmainDict.append(exemp_dict)
            mainData.extend(exemp_data)
            jsonData = exempmainDict
        if docsDataLST and invoiceType == 'docs':            
            docs_dict_data, docs_data = self.getDocDataDict(docsDataLST, invoiceObjs)
            docsDataDict.update({'doc_det':docs_dict_data})
            mainData.extend(docs_data)
            jsonData = docsDataDict
        if b2csJsonDataDict:
            for pos, val in b2csJsonDataDict.items():
                for line in val.values():
                    line['pos'] = pos
                    jsonData.append(line)
        if b2csDataDict:
            b2csData = []
            for state, data in b2csDataDict.items():
                for rate, val in data.items():
                    b2csData.append(['OE', state, 0.0, rate, round(
                        val['taxval'], 2), round(val['cess'], 2), ''])
            mainData = b2csData
        if b2bDataDict:
            for (ctin, inv) in b2bDataDict.items():
                jsonData.append({'ctin': ctin, 'inv': inv})  
        if b2burDataDict:
            for (ctin, inv) in b2burDataDict.items():
                jsonData.append({'inv': inv})
        if b2clJsonDataDict:
            for (pos, inv) in b2clJsonDataDict.items():
                jsonData.append({'pos': pos, 'inv': inv})
        if cdnrDataDict:
            for (ctin, nt) in cdnrDataDict.items():
                jsonData.append({'ctin': ctin, 'nt': nt}) 
        if cdnurDataDict:
            if cdnurDataDict.get('cdnur'):
                jsonData = cdnurDataDict['cdnur']
        if hsnDict:
            vals = hsnDict.values()
            hsnMainData = []
            for val in vals:
                hsnMainData.extend(val.values())
            mainData = hsnMainData
        if hsnDataDict:
            vals = hsnDataDict.values()
            hsnMainData = []
            for val in vals:
                hsnMainData.extend(val.values())
            jsonData = hsnMainData
        return [mainData, jsonData]

    def getGSTInvoiceData(self, invoiceObj, invoiceType, data, gstType=''):
        jsonItemData = []
        count = 0
        rateDataDict = {}
        rateDict = {}
        rateJsonDict = {}
        itcEligibility = 'Ineligible'
        if self.gst_type == 'gstr1':
            sign = -1 if invoiceObj.move_type in ('out_refund') else 1
        ctx = dict(self._context or {})
        for invoiceLineObj in invoiceObj.invoice_line_ids.filtered(lambda l: l.product_id):
            if invoiceLineObj.product_id:
                if invoiceLineObj.product_id.type == 'service':
                    if invoiceType == 'impg':
                        continue
                else:
                    if invoiceType == 'imps':
                        continue
            else:
                if invoiceType == 'impg':
                    continue
            invoiceLineData = self.getInvoiceLineData(data, invoiceLineObj, invoiceObj, invoiceType)
            if invoiceLineData:
                rate = invoiceLineData[2]
                rateAmount = invoiceLineData[3]
                if invoiceLineData[1]:
                    invoiceLineData[1]['txval'] = rateAmount
                if gstType == 'gstr1':
                    csamt = invoiceLineData[1].get('csamt') or 0.0
                    if rate not in rateDict.keys():
                        rateDataDict[rate] = {
                            'rt': rate,
                            'taxval': sign * rateAmount,
                            'cess': csamt
                        }
                    else:
                        rateDataDict[rate]['taxval'] = rateDataDict[rate]['taxval'] + sign *rateAmount
                        rateDataDict[rate]['cess'] = rateDataDict[rate]['cess'] + csamt
                if rate not in rateJsonDict.keys():
                    rateJsonDict[rate] = invoiceLineData[1]
                else:
                    for key in invoiceLineData[1].keys():
                        if key in ['rt', 'sply_ty', 'typ', 'elg']:
                            continue
                        if rateJsonDict[rate].get(key):
                            rateJsonDict[rate][key] = rateJsonDict[rate][key] + invoiceLineData[1][key]
                            rateJsonDict[rate][key] = round(rateJsonDict[rate][key], 2)
                        else:
                            rateJsonDict[rate][key] = invoiceLineData[1][key]
                invData = []
                if gstType == 'gstr1':
                    invData = invoiceLineData[0] + [rateDataDict[rate]['taxval']]
                if invoiceType in ['b2b', 'cdnr']:
                    if gstType == 'gstr1':
                        invData = invData + [0.0]
                elif invoiceType == 'b2bur':
                    if itcEligibility != 'Ineligible':
                        invData = invData + [0.0] + [itcEligibility] + [
                            rateDataDict[rate]['igst']
                        ] + [rateDataDict[rate]['cgst']] + [
                            rateDataDict[rate]['sgst']
                        ] + [rateDataDict[rate]['cess']]
                    else:
                        invData = invData + [0.0] + [itcEligibility] + [0.0] * 4
                elif invoiceType in ['imps', 'impg']:
                    if itcEligibility != 'Ineligible':
                        invData = invData + [0.0] + [itcEligibility] + [
                            rateDataDict[rate]['igst']
                        ] + [rateDataDict[rate]['cess']]
                    else:
                        invData = invData + [0.0] + [itcEligibility] + [0.0] + [0.0]
                elif invoiceType in ['b2cs', 'b2cl']:
                    invData = invData + [0.0, '']
                rateDict[rate] = invData
        mainData = rateDict.values()
        if rateJsonDict:
            for jsonData in rateJsonDict.values():
                count = count + 1
                if invoiceType in ['b2b', 'b2bur', 'cdnr'] and gstType == 'gstr2':
                    jsonItemData.append({
                        "num": count,
                        'itm_det': jsonData,
                        "itc": {
                            "elg": "no",
                            "tx_i": 0.0,
                            "tx_s": 0.0,
                            "tx_c": 0.0,
                            "tx_cs": 0.0
                        }
                    })
                elif invoiceType in ['imps', 'impg']:
                    jsonItemData.append({
                        "num": count,
                        'itm_det': jsonData,
                        "itc": {
                            "elg": "no",
                            "tx_i": 0.0,
                            "tx_cs": 0.0
                        }
                    })
                else:
                    jsonItemData.append({"num": count, 'itm_det': jsonData})
        return [mainData, jsonItemData, rateDataDict, rateJsonDict]

    def getInvoiceLineData(self, invoiceLineData, invoiceLineObj, invoiceObj, invoiceType):
        lineData = []
        jsonLineData = {}
        taxedAmount = 0.0
        rate = 0.0
        rateAmount = 0.0
        currency = invoiceObj.currency_id or None
        price = invoiceLineObj.price_subtotal / invoiceLineObj.quantity if invoiceLineObj.quantity > 0 else 0.0
        rateObjs = invoiceLineObj.tax_ids.filtered(lambda l: l.l10n_in_tax_type not in ['tds','tcs'])
        if rateObjs:
            for rateObj in rateObjs:
                if rateObj.amount_type == "group":
                    for childObj in rateObj.children_tax_ids:
                        rate = childObj.amount * 2
                        lineData.append(rate)
                        break
                else:
                    rate = rateObj.amount
                    lineData.append(rate)
                break
            taxData = self.getTaxedAmount(
                rateObjs, price, currency, invoiceLineObj, invoiceObj)
            rateAmount = taxData[1]
            rateAmount = round(rateAmount, 2)
            taxedAmount = taxData[0]
            cess_tax = taxData[2]
            jsonLineData = self.getGstTaxData(invoiceObj,
                    invoiceLineObj, rateObjs, taxedAmount, invoiceType)
            jsonLineData['csamt'] = cess_tax
        else:
            rateAmount = invoiceLineObj.price_subtotal
            rateAmount = rateAmount
            if currency.name != 'INR':
                company_currency = invoiceObj.company_id.currency_id
                conversion = currency._get_conversion_rate(currency,company_currency,invoiceObj.company_id, invoiceObj.invoice_date)
                rateAmount = rateAmount * conversion
            rateAmount = round(rateAmount, 2)
            lineData.append(0)
            jsonLineData = self.getGstTaxData(invoiceObj,
                    invoiceLineObj, False, taxedAmount, invoiceType)
        data = invoiceLineData + lineData
        return [data, jsonLineData, rate, rateAmount]

    def getHSNData(self, invoiceObj, count, hsnDict={}, hsnDataDict={}):
        mainData = []
        jsonData = []
        currency = invoiceObj.currency_id or None
        ctx = dict(self._context or {})
        if self.gst_type == 'gstr1':
            sign = -1 if invoiceObj.move_type in ('out_refund') else 1

        for invoiceLineObj in invoiceObj.invoice_line_ids.filtered(lambda l: l.product_id):
            quantity = invoiceLineObj.quantity or 1.0
            price = invoiceLineObj.price_subtotal / quantity
            taxedAmount, cgst, sgst, igst, rt ,csamt = 0.0, 0.0, 0.0, 0.0, 0, 0.0
            rateObjs = invoiceLineObj.tax_ids
            if rateObjs:
                taxData = self.getTaxedAmount(
                    rateObjs, price, currency, invoiceLineObj, invoiceObj)
                rateAmount = taxData[1]
                taxedAmount = taxData[0]
                csamt = taxData[2]
                taxedAmount = round(taxedAmount, 2)
                rateObj = rateObjs[0]
                if rateObj.amount_type == "group":
                    rt = rateObj.children_tax_ids and rateObj.children_tax_ids[0].amount * 2 or 0
                    cgst, sgst = round(taxedAmount / 2, 2), round(taxedAmount / 2, 2)
                else:
                    rt = rateObj.amount
                    igst = round(taxedAmount, 2)
            invUntaxedAmount = round(invoiceLineObj.price_subtotal, 2)
            if currency.name != 'INR':
                company_currency = invoiceObj.company_id.currency_id
                conversion = currency._get_conversion_rate(currency,company_currency,invoiceObj.company_id, invoiceObj.invoice_date)
                invUntaxedAmount = round(invoiceLineObj.price_subtotal * conversion, 2)
            productObj = invoiceLineObj.product_id
            hsnvalue = productObj.l10n_in_hsn_code or ''
            hsnVal = hsnvalue.replace('.', '') or 'False'
            hsnName = ''
            uqc = 'OTH'
            if productObj.uom_id:
                uom = productObj.uom_id.id
                uqcObj = self.env['uom.mapping'].search([('uom', '=', uom)])
                if uqcObj:
                    uqc = uqcObj[0].name.code
            hsnTuple = (uqc, rt)
            invQty = sign * invoiceLineObj.quantity
            invUntaxedAmount *= sign
            igst *= sign
            cgst *= sign
            sgst *= sign
            csamt *= sign
            if hsnDataDict.get(hsnVal):
                hsnTupleDict = hsnDataDict.get(hsnVal).get(hsnTuple) or {}
                if hsnTupleDict:
                    if hsnTupleDict.get('qty'):
                        invQty += hsnTupleDict.get('qty')
                        hsnTupleDict['qty'] = invQty
                    else:
                        hsnTupleDict['qty'] = invQty
                    if hsnTupleDict.get('txval'):
                        invUntaxedAmount = round(hsnTupleDict.get('txval') + invUntaxedAmount, 2)
                        hsnTupleDict['txval'] = invUntaxedAmount
                    else:
                        invUntaxedAmount = round(invUntaxedAmount, 2)
                        hsnTupleDict['txval'] = invUntaxedAmount
                    if hsnTupleDict.get('iamt'):
                        igst = round(hsnTupleDict.get('iamt') + igst, 2)
                        hsnTupleDict['iamt'] = igst
                    else:
                        igst = round(igst, 2)
                        hsnTupleDict['iamt'] = igst
                    if hsnTupleDict.get('camt'):
                        cgst = round(hsnTupleDict.get('camt') + cgst, 2)
                        hsnTupleDict['camt'] = cgst
                    else:
                        cgst = round(cgst, 2)
                        hsnTupleDict['camt'] = cgst
                    if hsnTupleDict.get('samt'):
                        sgst = round(hsnTupleDict.get('samt') + sgst, 2)
                        hsnTupleDict['samt'] = sgst
                    else:
                        sgst = round(sgst, 2)
                        hsnTupleDict['samt'] = sgst
                    if hsnTupleDict.get('csamt'):
                        csamt = round(hsnTupleDict.get('csamt') + csamt, 2)
                        hsnTupleDict['samt'] = csamt
                else:
                    count += 1
                    hsnDataDict.get(hsnVal)[hsnTuple] = {
                        'num': count,
                        'hsn_sc': hsnVal,
                        'desc': hsnName,
                        'uqc': uqc,
                        'qty': invQty,
                        'rt': rt,
                        'txval': invUntaxedAmount,
                        'iamt': igst,
                        'camt': cgst,
                        'samt': sgst,
                        'csamt': csamt
                    }
            else:
                count += 1
                hsnDataDict[hsnVal] = {
                    hsnTuple: {
                        'num': count,
                        'hsn_sc': hsnVal,
                        'desc': hsnName,
                        'uqc': uqc,
                        'qty': invQty,
                        'rt': rt,
                        'txval': invUntaxedAmount,
                        'iamt': igst,
                        'camt': cgst,
                        'samt': sgst,
                        'csamt': csamt
                    }
                }
            invoice_total = invUntaxedAmount+ igst+ cgst+ sgst+ csamt
            hsnvalue = productObj.l10n_in_hsn_code or ''
            hsnData = [
                hsnvalue.replace('.', ''), hsnName, uqc, invQty,
                invoice_total, rt, invUntaxedAmount, igst, cgst, sgst, csamt
            ]
            if hsnDict.get(hsnVal):
                hsnDict.get(hsnVal)[hsnTuple] = hsnData
            else:
                hsnDict[hsnVal] = {hsnTuple: hsnData}
            mainData.append(hsnData)
        return [mainData, jsonData, hsnDict, hsnDataDict]

    def getTaxedAmount(self, rateObjs, price, currency, invoiceLineObj, invoiceObj):
        taxedAmount = 0.0
        total_excluded = 0.0
        cess_amount = 0.0
        rateObjs = rateObjs.filtered(lambda l: l.l10n_in_tax_type not in ['tds','tcs'])
        cess_tax = rateObjs.filtered(lambda l: l.l10n_in_tax_type in ['cess'])
        taxes = (rateObjs-cess_tax).compute_all(price, currency, invoiceLineObj.quantity,
                                     product=invoiceLineObj.product_id, partner=invoiceObj.partner_id)
        cess_taxes = (cess_tax).compute_all(price, currency, invoiceLineObj.quantity,
                                     product=invoiceLineObj.product_id, partner=invoiceObj.partner_id)
        if cess_taxes:
            cess_amount = cess_taxes.get('total_included') - cess_taxes.get('total_excluded')
        if taxes:
            total_included = taxes.get('total_included') or 0.0
            total_excluded = taxes.get('total_excluded') or 0.0
            taxedAmount = total_included - total_excluded
            if any (tax.l10n_in_reverse_charge or (tax.amount_type == 'group' and tax.children_tax_ids and any(child_tax_id.l10n_in_reverse_charge for child_tax_id in tax.children_tax_ids)) for tax in rateObjs):
                for tax in taxes.get('taxes'):
                    if tax.get('amount') > 0:
                        taxedAmount += tax.get('amount')
        if currency.name != 'INR':
            company_currency = invoiceObj.company_id.currency_id
            conversion = currency._get_conversion_rate(currency,company_currency,invoiceObj.company_id, invoiceObj.invoice_date)
            taxedAmount = taxedAmount *conversion
            total_excluded = total_excluded * conversion
        return [taxedAmount, total_excluded, cess_amount]

    def getGstTaxData(self, invoiceObj, invoiceLineObj, rateObjs, taxedAmount, invoiceType):
        if self.gst_type == 'gstr1':
            sign = -1 if invoiceObj.move_type in ('out_refund') else 1
        taxedAmount = sign * round(taxedAmount, 2)
        gstDict = {
            "rt": 0.0,
            "iamt": 0.0,
            "camt": 0.0,
            "samt": 0.0,
            "csamt": 0.0
        }
        if invoiceType == "export":
            gstDict = {"txval": 0.0, "rt": 0, "iamt": 0.0}
        if invoiceType in ['imps', 'impg']:
            gstDict = {
                "elg": "no",
                "txval": 0.0,
                "rt": 0,
                "iamt": 0.0,
                'tx_i': 0.0,
                'tx_cs': 0.0
            }
        if invoiceType == "b2cs":
            gstDict['sply_ty'] = 'INTRA'
            gstDict['typ'] = 'OE'
        if rateObjs:
            rateObj = rateObjs[0]
            if invoiceObj.partner_id.country_id.code == 'IN':
                if rateObj.amount_type == "group":
                    gstDict['rt'] = rateObj.children_tax_ids and rateObj.children_tax_ids[0].amount * 2 or 0
                    gstDict['samt'] = round(taxedAmount / 2, 2)
                    gstDict['camt'] = round(taxedAmount / 2, 2)
                else:
                    gstDict['rt'] = rateObj.amount
                    gstDict['iamt'] = round(taxedAmount, 2)
            elif invoiceType in ['imps', 'impg']:
                gstDict['rt'] = rateObj.amount
                gstDict['iamt'] = round(taxedAmount, 2)
        return gstDict
