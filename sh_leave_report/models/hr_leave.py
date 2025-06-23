# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models
import xlwt
import base64
from io import BytesIO
import html2text


class Leave(models.Model):
    _inherit = "hr.leave"

    def action_leave_xls(self):
        workbook = xlwt.Workbook()
        heading_format = xlwt.easyxf(
            'font:height 300,bold True;pattern: pattern solid, fore_colour white;align: horiz center,vertical center;borders:top thick;borders:bottom thick;')
        bold = xlwt.easyxf(
            'font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz left,vertical center;borders:top thick;borders:bottom thick;')
        color = xlwt.easyxf(
            'font:height 250, bold True, colour blue; align: horiz left,vertical center;borders:top thick;borders:bottom thick;')
        all_center = xlwt.easyxf('align: horiz left,vertical center;')
        format1 = xlwt.easyxf('align: horiz left;')
        format2 = xlwt.easyxf(
            'font:bold True;align: horiz center,vertical center;')
        format3 = xlwt.easyxf(
            'align: horiz center,vertical center;')
        sign_border = xlwt.easyxf('font:bold True;borders:bottom thick;')

        data = {}
        data = dict(data or {})
        active_ids = self.env.context.get('active_ids')

        Leaves = self.env['hr.leave'].search(
            [('id', 'in', active_ids)])

        handle = html2text.HTML2Text()
        count = len(Leaves)
        if count == 1:
            final_value = {}
            worksheet = workbook.add_sheet(
                Leaves.name, cell_overwrite_ok=True)

            worksheet.write_merge(
                0, 1, 0, 2, 'Leave Request', heading_format)
            worksheet.write_merge(
                3, 4, 0, 2, 'Employee Information :', color)

            worksheet.col(0).width = int(50 * 260)
            worksheet.col(1).width = int(50 * 260)
            worksheet.col(2).width = int(50 * 260)

            final_value['employee_id'] = Leaves.employee_id.name
            if Leaves.employee_id.job_id:
                final_value['job_id'] = Leaves.employee_id.job_id.name
            if Leaves.employee_id.department_id:
                final_value['department_id'] = Leaves.employee_id.department_id.name
            if Leaves.employee_id.work_email:
                final_value['work_email'] = Leaves.employee_id.work_email
            if Leaves.employee_id.mobile_phone:
                final_value['mobile_phone'] = Leaves.employee_id.mobile_phone

            final_value['holiday_status_id'] = Leaves.holiday_status_id.name
            final_value['name'] = Leaves.name
            if Leaves.request_date_from:
                final_value['request_date_from'] = Leaves.request_date_from
            else:
                final_value['request_date_from'] = ''

            if Leaves.request_date_to:
                final_value['request_date_to'] = Leaves.request_date_to
            else:
                final_value['request_date_to'] = ''

            final_value['number_of_days'] = Leaves.number_of_days
            final_value['create_date'] = Leaves.create_date
            final_value['state'] = Leaves.state
            final_value['parent_id'] = Leaves.parent_id.name
            final_value['report_note'] = ''
            if Leaves.report_note:
                final_value['report_note'] = handle.handle(Leaves.report_note)

            if Leaves.employee_id:
                worksheet.write_merge(
                    6, 6, 0, 0, final_value['employee_id'], format1)
            else:
                worksheet.write_merge(
                    6, 6, 0, 0, '', format1)

            if Leaves.employee_id.job_id:
                worksheet.write_merge(
                    7, 7, 0, 0, final_value['job_id'], format1)
            else:
                worksheet.write_merge(
                    7, 7, 0, 0, '', format1)
            if Leaves.employee_id.department_id:
                worksheet.write_merge(
                    8, 8, 0, 0, final_value['department_id'], format1)
            else:
                worksheet.write_merge(
                    8, 8, 0, 0, '', format1)

            if Leaves.employee_id.work_email:
                worksheet.write_merge(
                    9, 9, 0, 0, final_value['work_email'], format1)
            else:
                worksheet.write_merge(
                    9, 9, 0, 0, '', format1)

            if Leaves.employee_id.mobile_phone:
                worksheet.write_merge(
                    10, 10, 0, 0, final_value['mobile_phone'], format1)
            else:
                worksheet.write_merge(
                    10, 10, 0, 0, '', format1)

            worksheet.write_merge(
                13, 14, 0, 0, 'Leave Type', bold)
            worksheet.write_merge(
                13, 14, 1, 1, final_value['holiday_status_id'], all_center)

            worksheet.write_merge(
                15, 16, 0, 0, 'About Leave ', bold)
            worksheet.write_merge(
                15, 16, 1, 1, final_value['name'], all_center)

            worksheet.write_merge(
                17, 18, 0, 0, 'Duration ', bold)
            Duration = str(final_value['request_date_from']) + \
                ' To ' + str(final_value['request_date_to'])
            worksheet.write_merge(
                17, 18, 1, 1, Duration, all_center)

            worksheet.write_merge(
                19, 20, 0, 0, 'Days', bold)
            worksheet.write_merge(
                19, 20, 1, 1, final_value['number_of_days'], all_center)

            worksheet.write_merge(
                21, 22, 0, 0, 'Date', bold)
            worksheet.write_merge(
                21, 22, 1, 1, str(final_value['create_date'].strftime("%Y-%m-%d")), all_center)

            worksheet.write_merge(
                23, 24, 0, 0, 'Status', bold)
            worksheet.write_merge(
                23, 24, 1, 1, final_value['state'], all_center)

            worksheet.write_merge(
                26, 27, 0, 2, 'Comment by Manager :', color)
            worksheet.write_merge(
                28, 30, 0, 2, final_value['report_note'], format1)

            worksheet.write_merge(
                34, 34, 0, 0, '', sign_border)

            worksheet.write_merge(
                35, 35, 0, 0, 'Manager', format2)

            worksheet.write_merge(
                34, 34, 2, 2, '', sign_border)

            worksheet.write_merge(
                35, 35, 2, 2, final_value['employee_id'], format3)
            if Leaves.employee_id.job_id:

                worksheet.write_merge(
                    36, 36, 2, 2, final_value['job_id'], format2)
            else:
                worksheet.write_merge(
                    36, 36, 2, 2, '', format2)

        else:
            final_value = {}
            leave_lines = []
            worksheet = workbook.add_sheet(
                'Leave Report', cell_overwrite_ok=True)
            for record in Leaves:

                product = {
                    'employee_id': record.employee_id.name,
                    'holiday_status_id': record.holiday_status_id.name,
                    'name': record.name,
                    'request_date_from': record.request_date_from,
                    'request_date_to': record.request_date_to,
                    'number_of_days': record.number_of_days,
                    'create_date': record.create_date,
                    'state': record.state,
                }
                leave_lines.append(product)

            worksheet.write_merge(
                0, 1, 0, 6, 'Leave Request', heading_format)

            worksheet.col(0).width = int(20 * 260)
            worksheet.col(1).width = int(20 * 260)
            worksheet.col(2).width = int(20 * 260)
            worksheet.col(3).width = int(30 * 260)
            worksheet.col(4).width = int(15 * 260)
            worksheet.col(5).width = int(25 * 260)
            worksheet.col(6).width = int(15 * 260)

            worksheet.write_merge(3, 4, 0, 0, "Employee", bold)
            worksheet.write_merge(3, 4, 1, 1, "Leave Type", bold)
            worksheet.write_merge(3, 4, 2, 2, "About Leave", bold)
            worksheet.write_merge(3, 4, 3, 3, "Duration", bold)
            worksheet.write_merge(3, 4, 4, 4, "Days", bold)
            worksheet.write_merge(3, 4, 5, 5, "Date", bold)
            worksheet.write_merge(3, 4, 6, 6, "Status", bold)

            row = 5

            for rec in leave_lines:

                if rec.get('employee_id'):
                    worksheet.write(row, 0, rec.get('employee_id'))
                if rec.get('holiday_status_id'):
                    worksheet.write(row, 1, rec.get('holiday_status_id'))
                else:
                    worksheet.write(row, 1, '')
                if rec.get('name'):
                    worksheet.write(row, 2, str(rec.get('name')))
                request_date_from = ''
                request_date_to = ''
                if rec.get('request_date_from'):
                    request_date_from = str(rec.get('request_date_from'))
                if rec.get('request_date_to'):
                    request_date_to = str(rec.get('request_date_to'))

                date = str(request_date_from + ' TO ' + request_date_to)
                if date:
                    worksheet.write(row, 3, date)
                else:
                    worksheet.write(row, 3, '')
                if rec.get('number_of_days'):
                    worksheet.write(row, 4, str(rec.get('number_of_days')))
                else:
                    worksheet.write(row, 4, '')
                if rec.get('create_date'):
                    worksheet.write(row, 5, str(
                        rec.get('create_date').strftime("%Y-%m-%d")))
                else:
                    worksheet.write(row, 5, '')
                if rec.get('state'):
                    worksheet.write(row, 6, rec.get('state'))
                else:
                    worksheet.write(row, 6, '')

                row += 1

        filename = ('About Leave Xls Report' + '.xls')
        fp = BytesIO()
        workbook.save(fp)
        export_id = self.env['leave.excel.extended'].sudo().create({
            'excel_file': base64.encodebytes(fp.getvalue()),
            'file_name': filename,
        })

        return{
            'type': 'ir.actions.act_url',
            'url': 'web/content/?model=leave.excel.extended&field=excel_file&download=true&id=%s&filename=%s' % (export_id.id, export_id.file_name),
            'target': 'new',
        }
