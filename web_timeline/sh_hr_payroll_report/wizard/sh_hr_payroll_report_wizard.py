# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

import base64
import xlwt
from io import BytesIO
from odoo import fields, models


HEADING = xlwt.easyxf('font:height 300,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center;align: vert center;borders: left thin, right thin, bottom thin,top thin,top_color gray40,bottom_color gray40,left_color gray40,right_color gray40')
CENTER = xlwt.easyxf('font:bold True;' 'align: horiz center;align: vert center;borders: top_color black, bottom_color black, right_color black, left_color black,left thin, right thin, top thin, bottom thin')
BOX_R = xlwt.easyxf('font:bold True;' 'align: vert center;borders: top_color black, bottom_color black, right_color black, left_color black,left thin, right thin, top thin, bottom thin')
WS = 3000
WL = 5000
COL = {
    'Sr': {'col': 0, 'name': 'Sr.No.', 'width': WS},
    'EMP': {'col': 1, 'name': 'Employee Name', 'width': WL},
    'UAN': {'col': 2, 'name': 'UAN NO', 'width': WS},
    'PF_NO': {'col': 3, 'name': 'PF NO', 'width': WS},
    'ESIC': {'col': 4, 'name': 'ESIC NO', 'width': WS},
    'WORK100': {'col': 5, 'name': 'P', 'width': WS},
    'Unpaid': {'col': 6, 'name': 'LEAVE', 'width': WS},
    'GLOBAL': {'col': 7, 'name': 'GLOBAL', 'width': WS},
    'TOTAL': {'col': 8, 'name': 'TOTAL', 'width': WS},
    'BASIC': {'col': 9, 'name': 'BASIC', 'width': WS},
    'DA': {'col': 10, 'name': 'DA', 'width': WS},
    'SA': {'col': 11, 'name': 'SA', 'width': WS},
    'TA': {'col': 12, 'name': 'TA', 'width': WS},
    'HRA': {'col': 13, 'name': 'HRA', 'width': WS},
    'CA': {'col': 14, 'name': 'CA', 'width': WS},
    'OA': {'col': 15, 'name': 'OA', 'width': WS},
    'BONUS': {'col': 16, 'name': 'BONUS', 'width': WS},
    'GROSS': {'col': 17, 'name': 'GROSS', 'width': WS},
    'UNPAID': {'col': 18, 'name': 'UNPAID', 'width': WS},
    'PT': {'col': 19, 'name': 'PT', 'width': WS},
    'PF': {'col': 20, 'name': 'PF', 'width': WS},
    'TDS': {'col': 21, 'name': 'TDS', 'width': WS},
    'NET': {'col': 22, 'name': 'NET', 'width': WS}
}


class ShHrPayrollReportWizard(models.TransientModel):
    _name = "sh.hr.payroll.report.wizard"
    _description = "Hr Payroll Report Wizard"

    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    employee_ids = fields.Many2many("hr.employee", string="Employees")

    def _feed_payslip_line_data(self, line, data, worksheet, row, total_dict):
        if line.code == 'TOTAL':
            return
        col = COL.get(line.code)
        if col:
            worksheet.write(row, col['col'], float(data))
            if line.code not in total_dict:
                total_dict[line.code] = 0.0
            total_dict[line.code] += float(data)

    def _prepare_sheet(self, workbook):
        employee_list = []
        for employee in self.employee_ids:
            #check if payslip amount is greter then 0

            slip_id = self.env['hr.payslip'].sudo().search([
                ('employee_id', '=', employee.id),
                ('date_from', '>=', self.start_date),
                ('date_to', '<=', self.end_date),
            ], limit=1)
            if slip_id:

                for line in slip_id.line_ids.filtered(lambda x:x.code=='NET'):
                    if line.total > 0.0:
                        employee_list.append(employee)
                    

        worksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
        worksheet.write_merge(0, 1, 0, len(COL)-1, f"HR Payroll Report {self.start_date} To {self.end_date}", HEADING)

        # Heading Column
        for col in COL.values():
            worksheet.col(col['col']).width = col['width']
            worksheet.write(3, col['col'], col['name'], CENTER)

        # Employee Data
        row = 4
        total_dict = {
            'TOTAL': 0.0,
            'BASIC': 0.0,
            'GROSS': 0.0,
            'BONUS':0.0,
            'UNPAID': 0.0,
            'NET': 0.0,
            'WORK100': 0.0,
            'Unpaid': 0.0,
            'GLOBAL': 0.0,
            'DA': 0.0,
            'TA': 0.0,
            'SA': 0.0,
            'HRA': 0.0,
            'CA': 0.0,
            'OA': 0.0,
            'PT': 0.0,
            'TDS': 0.0,
            'PF': 0.0,
        }
        for employee in employee_list:
            for code,col in COL.items():
                if code in ['Sr', 'EMP', 'UAN', 'PF_NO', 'ESIC']:
                    continue
                worksheet.write(row, col['col'], 0)
            # # -------------------------------------
            # 1) sr no
            worksheet.write(row, 0, row-3)
            # 2) employee name
            worksheet.write(row, 1, employee.name)
            # 3) UAN NO
            # worksheet.write(row, 2, employee.name)
            # 4) PF NO
            # worksheet.write(row, 3, employee.name)
            # 5) ESIC NO
            # worksheet.write(row, 4, employee.name)
            slip_id = self.env['hr.payslip'].sudo().search([
                ('employee_id', '=', employee.id),
                ('date_from', '=', self.start_date),
                ('date_to', '=', self.end_date),
            ], limit=1)
            if slip_id:
                working_days = 0.0

                for line in slip_id.worked_days_line_ids:
                    self._feed_payslip_line_data(line, line.number_of_days, worksheet, row, total_dict)
                    if line.code in ('WORK100', 'Unpaid','GLOBAL'):
                        working_days += line.number_of_days

                for line in slip_id.line_ids:
                    self._feed_payslip_line_data(line, line.total, worksheet, row, total_dict)

                if working_days:
                    worksheet.write(row, 8, working_days)
                    total_dict['TOTAL'] += working_days
            # -------------------------------------
            row += 1
        # worksheet.write(row, 0, 'Total')
        row += 1
        for code,val in total_dict.items():
            worksheet.write(row, COL[code]['col'], val, BOX_R)
            # col = COL[code]['col']
            # worksheet.write_merge(row, row+1, col, col, val, CENTER)

    def generate_hr_payroll_report(self):
        workbook = xlwt.Workbook()
        self._prepare_sheet(workbook)
        # Save to BytesIO buffer
        buffer = BytesIO()
        workbook.save(buffer)
        # buffer.seek(0)
        ir_attachment = self.env['ir.attachment']
        attachment_vals = {
            "name": "payroll.xls",
            "res_model": "ir.ui.view",
            "type": "binary",
            "datas": base64.encodebytes(buffer.getvalue()),
            "public": True,
        }
        buffer.close()

        attachment = ir_attachment.sudo().search([
            ('name', '=', 'payroll.xls'),
            ('type', '=', 'binary'),
            ('res_model', '=', 'ir.ui.view')
        ], limit=1)
        if attachment:
            attachment.sudo().write(attachment_vals)
        else:
            attachment = ir_attachment.sudo().create(attachment_vals)
        return {
            'type': 'ir.actions.act_url',
            'url': f"/web/content/{attachment.id}?download=true&filename=Payroll Report {self.start_date} To {self.end_date}.xls",
            'target': 'new',
        }
