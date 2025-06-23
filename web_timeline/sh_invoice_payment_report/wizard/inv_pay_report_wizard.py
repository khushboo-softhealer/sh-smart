# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields
from odoo.exceptions import UserError
import io
import base64
import xlwt
import xlsxwriter


class InvoicePaymentReportWizard(models.TransientModel):
    _name = 'sh.inv.pay.report.wizard'
    _description = 'Invoice Payment Report Wizard'

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)

    
    def fetch_currency_rate(self,date,currency):
        exchange_rate = 1.0
        currency_rate = currency.rate_ids.filtered(lambda x: x.name <= date)
        if currency_rate:
            currency_rate = currency_rate[-1]
            exchange_rate = (
                1/currency_rate.rate) if currency_rate and currency_rate.rate != 0 else 0
        else:
            exchange_rate = 1.0

        return exchange_rate
    
    def print_xls_report(self):
        workbook = xlwt.Workbook(encoding='utf-8')
        invoice_domain = [('move_type', '=', 'out_invoice'),('invoice_date', '>=', self.start_date),('invoice_date', '<=', self.end_date)]
        invoices = self.env['account.move'].search(invoice_domain)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("Invoices")

        bold_style = workbook.add_format({'bold': True,'align': 'center','valign': 'vcenter','border': 1})
        num_format = workbook.add_format({'num_format': '#,##0.00','align': 'right','valign': 'vcenter','border': 1})
        worksheet.merge_range('A1:R1', 'Invoice Payment Report', workbook.add_format({
            'bold': True,
            'font_size': 14,
            'align': 'center',
            'valign': 'vcenter'
        }))
        date_range = f'From: {self.start_date.strftime("%d/%m/%Y")} To: {self.end_date.strftime("%d/%m/%Y")}'
        worksheet.merge_range('A2:R2', date_range, workbook.add_format({
            'font_size': 11,
            'align': 'center',
            'valign': 'vcenter'
        }))

        header = [
            'SR. NO.', 'INVOICE NUMBER', 'DATE', 'GSTIN', 'AMOUNT', 'CURRENCY', 'EXCHANGE RATE',
            'AMOUNT (RS.)', 'NAME OF PARTY', 'CITY / COUNTRY', 'STATE', 'HSN', 'RATE',
            'IGST', 'CGST', 'SGST', 'TOTAL', 'PAID BY'
        ]
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3'})
        for col, title in enumerate(header):
            worksheet.write(2, col, title, header_format)

        row = 3
        count = 1
        col_widths = [len(title) for title in header]
        total_amount = total_amount_rs = total_igst = total_cgst = total_sgst = total_invoice_total = 0.0
        for inv in invoices:

            if inv.state == 'cancel':
                values = [
                    str(count),
                    inv.name,
                    '', '', '', '', '',
                    '-',
                    'CANCELLED INVOICE',
                    '', '', '', '', '', '', '', '-', ''
                ]
            else:
                exchange_rate = self.fetch_currency_rate(inv.invoice_date,inv.currency_id)
                hsn = inv.invoice_line_ids[0].product_id.l10n_in_hsn_code if inv.invoice_line_ids else ''
                rate = '18%' if inv.partner_id.state_id.code == 'GJ' else '0%'
                payment_jornal = self.env['account.payment'].search([('ref', '=', inv.name)], limit=1)

                country_code = inv.partner_id.country_id.code or ""
                country_name = inv.partner_id.country_id.name or ""
                state_name = inv.partner_id.state_id.name or ''
                city_name = inv.partner_id.city or ""
                city_or_country = (city_name if country_code == 'IN' else country_name)
                state = state_name if country_code and country_code == 'IN' else 'Outside Inda' if country_code else ''

                igst = cgst = sgst = 0.0

                for line in inv.tax_totals.get('groups_by_subtotal', {}).get('Untaxed Amount', []):
                    amount = line.get('tax_group_amount', 0.0)
                    group = line.get('tax_group_name', '')

                    if group == 'IGST':
                        igst += amount
                    elif group == 'CGST':
                        cgst += amount
                    elif group == 'SGST':
                        sgst += amount

                total_amount += inv.amount_total
                total_amount_rs += inv.amount_total_signed
                total_igst += igst
                total_cgst += cgst
                total_sgst += sgst
                total_invoice_total += inv.amount_tax_signed

                values = [
                    str(count),
                    inv.name,
                    inv.invoice_date.strftime('%m/%d/%Y') if inv.invoice_date else '',
                    inv.partner_id.vat or '',
                    str(inv.amount_total),
                    inv.currency_id.name,
                    round(exchange_rate,2) ,
                    str(inv.amount_total_signed),
                    inv.partner_id.name,
                    city_or_country,
                    state,
                    hsn or '',
                    rate,
                    igst, cgst, sgst, str(inv.amount_tax_signed),
                    payment_jornal.journal_id.name or 'N/A'
                ]

            # Write values and update column widths
            for col, val in enumerate(values):
                worksheet.write(row, col, val)
                col_widths[col] = max(col_widths[col], len(str(val)))

            row += 1
            count += 1

        worksheet.write(row, 3, 'TOTAL', bold_style)
        worksheet.write(row, 4, total_amount, num_format)
        worksheet.write(row, 7, total_amount_rs, num_format)
        worksheet.write(row, 13, total_igst, num_format)
        worksheet.write(row, 9, 'TOTAL', bold_style)
        worksheet.write(row, 14, total_cgst, num_format)
        worksheet.write(row, 15, total_sgst, num_format)
        worksheet.write(row, 16, total_invoice_total, num_format)

        # Apply final column widths
        for col, width in enumerate(col_widths):
            worksheet.set_column(col, col, width + 2)  # +2 for padding

        fp = io.BytesIO()
        workbook.close()
        output.seek(0)
        xlsx_data = base64.b64encode(output.read())
        IrAttachment = self.env['ir.attachment']
        attachment_vals = {
            'name': 'Invoice Payment Report.xls',
            'res_model': 'ir.ui.view',
            'type': 'binary',
            'datas': xlsx_data,
            'public': True,
            }
        fp.close()

        attachment = IrAttachment.search([('name', '=',
                'Invoice Payment Report.xls'), ('type', '=', 'binary'),
                ('res_model', '=', 'ir.ui.view')], limit=1)
        if attachment:
            attachment.write(attachment_vals)
        else:
            attachment = \
                IrAttachment.create(attachment_vals)
        if not attachment:
            raise UserError('There is no attachments...')

        url = '/web/content/' + str(attachment.id) \
            + '?download=true'
        return {'type': 'ir.actions.act_url', 'url': url,
                'target': 'new'}