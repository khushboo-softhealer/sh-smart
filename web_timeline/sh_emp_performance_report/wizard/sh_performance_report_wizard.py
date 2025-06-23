# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields
from datetime import timedelta
from datetime import date
from odoo.exceptions import UserError
import calendar
import io
import base64
import xlwt


class PerformanceReportWizard(models.TransientModel):
    _name = 'sh.performance.report.wizard'
    _description = 'Performance Report Wizard'

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    employee_ids = fields.Many2many(
        'hr.employee', 'hr_employee_performance_report_table', string="Employees")

    def get_report_data(self):

        list_of_dict = []

        date_range = [self.start_date+timedelta(days=x)
                      for x in range((self.end_date-self.start_date).days + 1)]
        total_days = len(date_range)
        total_sunday = len([self.start_date+timedelta(days=x) for x in range((self.end_date -
                           self.start_date).days + 1) if (self.start_date+timedelta(days=x)).weekday() == 6])

        employees = self.employee_ids
        if not employees:
            employees = self.env['hr.employee'].search([])

        count = 0
        for employee in employees:
            count += 1

            total_global_leaves = 0
            global_leave_dates = []
            month_day_dict = {}
            allocated_leaves = 0
            allowed_late_coming = 0
            taken_leaves = 0
            office_days = 0
            leave_score = 0
            late_coming_score = 0
            timesheet_score = 0
            average_score = 0
            taken_paid_leave_count = 0
            taken_unpaid_leave_count = 0

            global_leaves = employee.resource_calendar_id.mapped(
                'global_leave_ids')
            for global_leave in global_leaves:
                global_leave_dates.extend([(global_leave.date_from+timedelta(days=x)).date(
                ) for x in range((global_leave.date_to-global_leave.date_from).days + 1)])

            global_leave_dates = list(set(global_leave_dates))

            total_global_leaves = len(
                [each_date for each_date in global_leave_dates if each_date in date_range])

            half_saturday_count = 0
            half_saturday_date_list = []

            for each_date in date_range:

                dt = date(each_date.year, each_date.month, 1)
                first_weekday = dt.isoweekday()
                first_saturday = 7 - first_weekday

                dt_of_first_saturday = date(each_date.year, each_date.month, 7)

                if first_saturday != 0:
                    dt_of_first_saturday = date(
                        each_date.year, each_date.month, first_saturday)

                third_saturday = 21 - first_weekday
                if first_saturday == 0:
                    third_saturday = 21

                dt_of_third_saturday = date(
                    each_date.year, each_date.month, third_saturday)

                half_saturday_date_list.append(dt_of_first_saturday)
                half_saturday_date_list.append(dt_of_third_saturday)

            half_saturday_date_list = list(set(half_saturday_date_list))
            for each_date in half_saturday_date_list:
                if (each_date in date_range and each_date not in global_leave_dates):
                    half_saturday_count += 1

            for each_date in date_range:

                if each_date.month in month_day_dict:
                    temp_total = month_day_dict[each_date.month]
                    month_day_dict[each_date.month] = temp_total + 1

                else:
                    month_day_dict[each_date.month] = 1

            for key, value in month_day_dict.items():

                allocated_leaves += round((value * 1.25) /
                                          calendar.mdays[key], 2)

            leaves = self.env['hr.leave'].search([('employee_id', '=', employee.id), (
                'request_date_from', '>=', self.start_date), ('request_date_to', '<=', self.end_date)])
            taken_leaves += sum(leaves.mapped('number_of_days_display'))

            for leave in leaves:
                # if leave.holiday_status_id.allocation_type == 'fixed_allocation':
                if not leave.holiday_status_id.unpaid:
                    taken_paid_leave_count += leave.number_of_days_display
                else:
                    taken_unpaid_leave_count += leave.number_of_days_display

            leaves = self.env['hr.leave'].search([('employee_id', '=', employee.id), (
                'request_date_from', '>=', self.start_date), ('request_date_to', '>', self.end_date)], limit=1)
            if leaves:
                leave_date_range = [leaves.request_date_from+timedelta(days=x) for x in range(
                    (leaves.request_date_to-leaves.request_date_from).days + 1)]
                taken_leaves += len(list(
                    set([each_date for each_date in leave_date_range if each_date in date_range])))

                #  if leaves.holiday_status_id.allocation_type == 'fixed_allocation':
                if not leaves.holiday_status_id.unpaid:
                    taken_paid_leave_count += len(list(
                        set([each_date for each_date in leave_date_range if each_date in date_range])))
                else:
                    taken_unpaid_leave_count += len(list(
                        set([each_date for each_date in leave_date_range if each_date in date_range])))

            leaves = self.env['hr.leave'].search([('employee_id', '=', employee.id), (
                'request_date_from', '<', self.start_date), ('request_date_to', '<=', self.end_date)], limit=1)
            if leaves:
                leave_date_range = [leaves.request_date_from+timedelta(days=x) for x in range(
                    (leaves.request_date_to-leaves.request_date_from).days + 1)]
                taken_leaves += len(list(
                    set([each_date for each_date in leave_date_range if each_date in date_range])))

                # if leaves.holiday_status_id.allocation_type == 'fixed_allocation':
                if not leaves.holiday_status_id.unpaid:
                    taken_paid_leave_count += len(list(
                        set([each_date for each_date in leave_date_range if each_date in date_range])))
                else:
                    taken_unpaid_leave_count += len(list(
                        set([each_date for each_date in leave_date_range if each_date in date_range])))

            office_days = total_days - total_sunday - total_global_leaves - \
                allocated_leaves - (half_saturday_count * 0.5)
            employee_present_days = office_days - taken_leaves

            domain = [('calendar_id', '=', employee.resource_calendar_id.id),
                      ('dayofweek', '=', '0'),
                      ('day_period', 'in', ['morning', 'afternoon']),
                      ('date_from', '<=', date.today()),
                      ('date_to', '>=', date.today()),
                      ]
            calendar_att_id = self.env['resource.calendar.attendance'].sudo().search(
                domain, limit=1)
            # print("\n\n\n calendar_att_id", calendar_att_id)
            worked_hrs = 0
            if calendar_att_id:
                worked_hrs = sum(calendar_att_id.mapped('sh_wroked_hours'))

            # print("\n office_days", office_days)
            # print("\n worked_hrs", worked_hrs)
            # print("\n employee_present_days", employee_present_days)
            total_worked_hrs = office_days * worked_hrs
            total_employee_present_worked_hrs = employee_present_days * worked_hrs
            # print("\n total_worked_hrs", total_worked_hrs)
            # print("\n total_employee_present_worked_hrs",
            #   total_employee_present_worked_hrs)
            # get final leave score
            leave_score = (employee_present_days * 5) / \
                office_days if office_days != 0 else 5
            if leave_score > 5:
                leave_score = 5

            late_coming_attendances = len(self.env['hr.attendance'].search([('employee_id', '=', employee.id)]).filtered(
                lambda x: x.check_in.date() in date_range and x.message_in).ids)
            late_coming_attendances_count = 0

            for key, value in month_day_dict.items():

                allowed_late_coming += round((value * 5) /
                                             calendar.mdays[key], 2)

            if late_coming_attendances == 0 or office_days == 0:
                late_coming_score = 5

            else:
                late_coming_score = (
                    ((office_days * 5)/late_coming_attendances)*5)/((office_days * 5)/allowed_late_coming)
                late_coming_attendances_count = late_coming_attendances
                if late_coming_score > 5:
                    late_coming_score = 5

            employee_timesheet_hrs = sum(self.env['account.analytic.line'].search(
                [('employee_id', '=', employee.id)]).filtered(lambda x: x.date in date_range).mapped('unit_amount'))
            total_actual_timesheet_hrs = employee.resource_calendar_id.timesheet_hrs * office_days

            if employee_timesheet_hrs == 0:
                timesheet_score = 0

            elif employee.resource_calendar_id.timesheet_hrs != 0 and office_days != 0:
                timesheet_score = (employee_timesheet_hrs * 5) / \
                    (employee.resource_calendar_id.timesheet_hrs * office_days)
                if timesheet_score > 5:
                    timesheet_score = 5

            list_of_dict.append({
                'sr_no': count,
                'emp_name': employee.name,
                'leave_score': round(leave_score, 2),
                'late_coming_score': round(late_coming_score, 2),
                'timesheet_score': round(timesheet_score, 2),
                'average_score': round((leave_score + late_coming_score + timesheet_score)/3, 2),

                'total_worked_hrs': round(total_worked_hrs, 2),
                'total_employee_present_worked_hrs': round(total_employee_present_worked_hrs, 2),
                'late_coming_attendances_count': late_coming_attendances_count,
                'employee_timesheet_hrs': round(employee_timesheet_hrs, 2),
                'total_actual_timesheet_hrs': round(total_actual_timesheet_hrs, 2),
                'taken_leaves': round(taken_leaves, 2),
                'taken_paid_leave_count': round(taken_paid_leave_count, 2),
                'taken_unpaid_leave_count': round(taken_unpaid_leave_count, 2)


            })

        return list_of_dict

    def print_xls_report(self):

        workbook = xlwt.Workbook()

        heading_format = xlwt.easyxf(
            'font:height 300,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center;align: vert center;borders: left thin, right thin, bottom thin,top thin,top_color gray40,bottom_color gray40,left_color gray40,right_color gray40'
        )
        normal_record = xlwt.easyxf('font:height 210;align: vert center')
        left_side_with_bold = xlwt.easyxf(
            'font:bold True;' 'align: horiz left;' "borders: top thin,bottom thin,right thin,left thin")

        left_side_with_bold_and_clr = xlwt.easyxf(
            'font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz left;borders: left thin, right thin, bottom thin,top thin,top_color gray40,bottom_color gray40,left_color gray40,right_color gray40')

        left_side = xlwt.easyxf(
            'align: horiz left;' "borders: top thin,bottom thin,right thin,left thin")

        left_side_with_red = xlwt.easyxf(
            'align: horiz left;' "pattern: pattern solid, fore_colour red;"  "borders: top thin,bottom thin,right thin,left thin")

        center = xlwt.easyxf(
            'font:bold True;'  'align: horiz center;align: vert center;borders: top_color black, bottom_color black, right_color black, left_color black,left thin, right thin, top thin, bottom thin')

        center_without_bold = xlwt.easyxf(
            'align: horiz center;align: vert center;' "borders: top thin,bottom thin,right thin,left thin")

        center_without_bold_with_red = xlwt.easyxf(
            'align: horiz center;align: vert center;' "pattern: pattern solid, fore_colour red;" "borders: top thin,bottom thin,right thin,left thin")

        center_with_bold_and_clr = xlwt.easyxf(
            'font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz center;align: vert center;borders: left thin, right thin, bottom thin,top thin,top_color gray40,bottom_color gray40,left_color gray40,right_color gray40')

        right_side = xlwt.easyxf(
            'align: horiz right;' "borders: top thin,bottom thin,right thin,left thin")

        currency_style_sided = xlwt.XFStyle()

        worksheet = workbook.add_sheet(u'Performance Report',
                                       cell_overwrite_ok=True)

        worksheet.col(0).width = 2000
        worksheet.col(1).width = 5000
        worksheet.col(2).width = 5000
        worksheet.col(3).width = 5000
        worksheet.col(4).width = 5000
        worksheet.col(5).width = 5000
        worksheet.col(6).width = 5000
        worksheet.col(7).width = 5000
        worksheet.col(8).width = 5000

        worksheet.write_merge(0, 1, 0, 5, "Employee Performance Report " +
                              str(self.start_date) + " To " + str(self.end_date), heading_format)

        worksheet.write(3, 0, "Sr.No.", center)
        worksheet.write(3, 1, "Name", center)
        worksheet.write(3, 2, "Leaves", center)
        worksheet.write(3, 3, "Attendance Score", center)
        worksheet.write(3, 4, "Late Coming Score", center)
        worksheet.write(3, 5, "Timesheet Score", center)
        worksheet.write(3, 6, "Average", center)

        list_of_dict = self.get_report_data()

        row = 4

        for dictt in list_of_dict:

            leaves = str(dictt.get('taken_leaves')) + ' (PL:' + str(dictt.get('taken_paid_leave_count')
                                                                    ) + ' Unpaid:' + str(dictt.get('taken_unpaid_leave_count')) + ')'
            attendance = str(dictt.get('leave_score')) + ' (' + str(dictt.get(
                'total_employee_present_worked_hrs')) + '/' + str(dictt.get('total_worked_hrs')) + ')'
            late_coming = str(dictt.get('late_coming_score')) + \
                ' (' + str(dictt.get('late_coming_attendances_count')) + ')'
            timesheet = str(dictt.get('timesheet_score')) + ' (' + str(dictt.get(
                'employee_timesheet_hrs')) + '/' + str(dictt.get('total_actual_timesheet_hrs')) + ')'

            if dictt.get('average_score') <= 3:

                worksheet.write(row, 0, dictt.get('sr_no'), left_side_with_red)
                worksheet.write(row, 1, dictt.get(
                    'emp_name'), left_side_with_red)
                worksheet.write(row, 2, leaves, left_side_with_red)
                worksheet.write(row, 3, attendance,
                                center_without_bold_with_red)
                worksheet.write(row, 4, late_coming,
                                center_without_bold_with_red)
                worksheet.write(row, 5, timesheet,
                                center_without_bold_with_red)
                worksheet.write(row, 6, str(
                    dictt.get('average_score')), center_without_bold_with_red)

            else:
                worksheet.write(row, 0, dictt.get('sr_no'), left_side)
                worksheet.write(row, 1, dictt.get('emp_name'), left_side)
                worksheet.write(row, 2, leaves, left_side)
                worksheet.write(row, 3, attendance, center_without_bold)
                worksheet.write(row, 4, late_coming, center_without_bold)
                worksheet.write(row, 5, timesheet, center_without_bold)
                worksheet.write(row, 6, str(
                    dictt.get('average_score')), center_without_bold)

            row += 1

        fp = io.BytesIO()
        workbook.save(fp)
        data = base64.encodebytes(fp.getvalue())
        ir_attachment = self.env['ir.attachment']
        attachment_vals = {
            "name": "Performance Report.xls",
            "res_model": "ir.ui.view",
            "type": "binary",
            "datas": data,
            "public": True,
        }
        fp.close()

        attachment = ir_attachment.search([('name', '=', 'XLS DATA'),
                                          ('type', '=', 'binary'),
                                          ('res_model', '=', 'ir.ui.view')],
                                          limit=1)
        if attachment:
            attachment.write(attachment_vals)
        else:
            attachment = ir_attachment.create(attachment_vals)

        # TODO: make user error here
        if not attachment:
            raise UserError('There is no attachments...')

        url = "/web/content/" + \
            str(attachment.id) + "?download=true&filename=Performance Report.xls"

        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }
