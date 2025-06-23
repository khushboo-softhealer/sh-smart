# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models
from datetime import datetime, timedelta
import base64
import xlwt
from io import BytesIO
import calendar
from odoo.exceptions import UserError


class EmployeeAttendancerWizard(models.TransientModel):
    _name = "employee.attendance.wizard"
    _description = "Employee Attendancer Wizard"
    _rec_name = "print_by"

    date = fields.Date()
    print_by = fields.Selection(
        [("daily", "Daily"),
         ("weekly", "Weekly"),
         ("monthly", "Monthly")],
        default="daily")
    employee_id = fields.Many2many("hr.employee", string="Employee")

    def employee_attendance_excel(self):

        # To Check All Employee & Selected Employee
        emp_list = []

        if self.employee_id:
            employee_search = self.env["hr.employee"].sudo().search(
                [("id", "in", self.employee_id.ids)])
            if employee_search:
                employee_ids = employee_search.ids
        else:
            employee_search = self.env["hr.employee"].sudo().search([])
            if employee_search:
                employee_ids = employee_search.ids

        # Daily data Excel generate
        if self.print_by == "daily":
            if self.date:
                today = self.date
                first = datetime.strftime(today, "%Y-%m-%d 00:00:00")
                last = datetime.strftime(today, "%Y-%m-%d 23:59:59")
            else:
                today = datetime.now().date()
                first = datetime.strftime(today, "%Y-%m-%d 00:00:00")
                last = datetime.strftime(today, "%Y-%m-%d 23:59:59")

            workbook = xlwt.Workbook()
            bold = xlwt.easyxf(
                "font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz left")
            heading_format = xlwt.easyxf(
                "font:height 300,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center")
            bold_center = xlwt.easyxf(
                "font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz center")

            format3 = xlwt.easyxf("align: horiz left")

            xlwt.add_palette_colour("custom_colour_green", 0x3a)
            workbook.set_colour_RGB(0x3a, 46, 125, 50)
            format_3 = xlwt.easyxf(
                "align: horiz left;pattern: pattern solid, fore_colour custom_colour_green;")

            format_absent = xlwt.easyxf(
                "align: horiz left;pattern: pattern solid, fore_colour red;")

            xlwt.add_palette_colour("custom_colour_yellow", 0x22)
            workbook.set_colour_RGB(0x22, 255, 241, 118)
            format4 = xlwt.easyxf(
                "align: horiz left;pattern: pattern solid, fore_colour custom_colour_yellow;")

            xlwt.add_palette_colour("custom_colour_ph", 0x2a)
            workbook.set_colour_RGB(0x2a, 25, 118, 210)
            format_ph = xlwt.easyxf(
                "align: horiz left;pattern: pattern solid, fore_colour custom_colour_ph;")

            pub_holi_name = {}
            ph_list = []
            pub_holiday = self.env["resource.calendar.leaves"].sudo().search(
                [("holiday_id", "=", False),
                 ("date_from", ">=", first),
                 ("date_to", "<=", last)])
            if pub_holiday:
                for public_holiday in pub_holiday:
                    date = public_holiday.date_from.date()
                    ph_list.append(
                        public_holiday.date_from.date().strftime("%Y-%m-%d"))

                    pub_holi_name.update(
                        {public_holiday.date_from.date().strftime("%Y-%m-%d"): public_holiday.name})
            if pub_holi_name:

                worksheet = workbook.add_sheet("Employee Attendance")
                worksheet.col(0).width = int(25*260)
                worksheet.col(1).width = int(25*260)
                worksheet.write_merge(
                    1, 2, 0, 1, "Attendance Report"+" - "+str(today), heading_format)

                worksheet.write(4, 0, "HOLIDAY", bold)
                worksheet.write(4, 1, pub_holiday.name, bold)

                row = 7
            else:
                worksheet = workbook.add_sheet("Employee Attendance")
                worksheet.col(0).width = int(25*260)
                worksheet.col(1).width = int(25*260)
                worksheet.col(3).width = int(25*260)
                worksheet.col(4).width = int(25*260)

                worksheet.write_merge(
                    1, 2, 0, 4, "Attendance Report"+" - "+str(today), heading_format)
                worksheet.write_merge(4, 4, 0, 1, "PRESENT", bold_center)
                worksheet.write_merge(4, 4, 3, 4, "ABSENT", bold_center)

                worksheet.write(6, 0, "Employee", bold)
                worksheet.write(6, 1, "Duration", bold)
                worksheet.write(6, 3, "Employee", bold)
                worksheet.write(6, 4, "Reason", bold)
                row = 7
            self.env.cr.execute("""SELECT he.id,he.name,min(ha.check_in),max(ha.check_out),max(ha.check_out)::timestamp -
             min(ha.check_in)::timestamp, sum(ha.att_duration) FROM hr_attendance ha 
             INNER JOIN hr_employee he ON he.id = ha.employee_id 
             where ha.check_in >= %s and ha.check_out <= %s Group by ha.employee_id,he.id""", (str(today) + " 00:00:00", str(today) + " 23:59:59"))

            # Get Present(P) Data with duration
            for present in self.env.cr.dictfetchall():
                if present.get("id", False) in employee_ids:
                    if present.get("sum", False) and present.get("sum", False) < 8.00:
                        emp_list.append(present.get("id", False))
                        worksheet.write(
                            row, 0, (present.get("name", False)), format3)
                        worksheet.write(
                            row, 1, "PL" + " ("+str(present.get("sum", False))+")", format4)

                    else:
                        emp_list.append(present.get("id", False))
                        worksheet.write(
                            row, 0, (present.get("name", False)), format3)
                        worksheet.write(
                            row, 1, "P" + " ("+str(present.get("sum", False))+")", format_3)
                row += 1

            # Get Absent (A) Leave with reason
            row = 7
            hr_employee_leave_search = self.env["hr.leave"].search(
                [("employee_id", "in", employee_ids),
                 ("request_date_from", "<=", self.date),
                 ("request_date_to", ">=", self.date)])
            if hr_employee_leave_search:
                for hr_emp_leave in hr_employee_leave_search:
                    if hr_emp_leave:
                        emp_list.append(hr_emp_leave.employee_id.id)
                        worksheet.write(
                            row, 3, hr_emp_leave.employee_id.name, format3)
                        worksheet.write(
                            row, 4, "A" + " ("+str(hr_emp_leave.name)+")", format_absent)
                    row += 1

            # Get Absent Data which is not apply leave date and not present
            row += 0
            employee_search = self.env["hr.employee"].search(
                [("id", "not in", emp_list), ("id", "in", employee_ids)])
            if employee_search:
                for emp_leave in employee_search:
                    if emp_leave and not ph_list:
                        worksheet.write(row, 3, emp_leave.name, format3)
                        worksheet.write(row, 4, "A", format_absent)
                    row += 1

        # Weekly data excel generate
        if self.print_by == "weekly":
            if self.date:
                today = self.date
                start = today - timedelta(days=today.weekday())
                end = start + timedelta(days=6)
                delta = end - start
                first = datetime.strftime(start, "%Y-%m-%d 00:00:00")
                last = datetime.strftime(end, "%Y-%m-%d 23:59:59")
            else:
                today = datetime.now().date()
                start = today - timedelta(days=today.weekday())
                end = start + timedelta(days=6)
                delta = end - start
                first = datetime.strftime(start, "%Y-%m-%d 00:00:00")
                last = datetime.strftime(end, "%Y-%m-%d 23:59:59")
            week_date = []
            workbook = xlwt.Workbook()
            bold = xlwt.easyxf(
                "font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz left")
            heading_format = xlwt.easyxf(
                "font:height 300,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center")
            bold_center = xlwt.easyxf(
                "font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz center")

            format3 = xlwt.easyxf("align: horiz left")

            xlwt.add_palette_colour("custom_colour_green", 0x3a)
            workbook.set_colour_RGB(0x3a, 46, 125, 50)
            format_3 = xlwt.easyxf(
                "align: horiz left;pattern: pattern solid, fore_colour custom_colour_green;")

            format_absent = xlwt.easyxf(
                "align: horiz left;pattern: pattern solid, fore_colour red;")

            xlwt.add_palette_colour("custom_colour_yellow", 0x22)
            workbook.set_colour_RGB(0x22, 255, 241, 118)
            format4 = xlwt.easyxf(
                "align: horiz left;pattern: pattern solid, fore_colour custom_colour_yellow;")

            xlwt.add_palette_colour("custom_colour_ph", 0x2a)
            #workbook.set_colour_RGB(0x2a, 57, 73, 171)
            workbook.set_colour_RGB(0x2a, 25, 118, 210)
            format_ph = xlwt.easyxf(
                "align: horiz left;pattern: pattern solid, fore_colour custom_colour_ph;")

            worksheet = workbook.add_sheet("Employee Attendance weekly")
            worksheet.col(0).width = int(20*260)
            worksheet.col(1).width = int(20*260)
            worksheet.col(2).width = int(20*260)
            worksheet.col(3).width = int(20*260)
            worksheet.col(4).width = int(20*260)
            worksheet.col(5).width = int(20*260)
            worksheet.col(6).width = int(20*260)
            worksheet.col(7).width = int(20*260)
            worksheet.write_merge(1, 2, 0, 7, "Employee Attendance - weekly" +
                                  " : "+str(start)+" To " + str(end), heading_format)
            worksheet.write(6, 0, "Employee Name", bold)
            col = 0
            row = 7
            dic_date = {}
            attendance_data_list = []
            for i in range(delta.days + 1):
                col = col+1
                day = start + timedelta(days=i)
                day_name = day.strftime("%a")
                day_date = str(day)
                week_date.append(day_date)
                dic_date.update({day_date: col})
                worksheet.write(6, col, day_date+" ("+day_name+")", bold)

                self.env.cr.execute("""SELECT he.id,he.name,min(ha.check_in),max(ha.check_out),max(ha.check_out)::timestamp -
                 min(ha.check_in)::timestamp, sum(ha.att_duration) FROM hr_attendance ha 
                 INNER JOIN hr_employee he ON he.id = ha.employee_id 
                 where ha.check_in >= %s and ha.check_out <= %s Group by ha.employee_id,he.id""", (day_date + " 00:00:00", day_date + " 23:59:59"))

                for rec in self.env.cr.dictfetchall():
                    if rec.get("id", False) in employee_ids:
                        attendance_data_list.append({day_date: dict(rec)})

            row = 7
            employee_position = {}

            # Get all Employee Absent(A) and Public holiday(PH) , find Employee Position(row wise) and fill all Employee in sheet
            ph_list = []
            pub_holi_name = {}
            pub_holiday = self.env["resource.calendar.leaves"].sudo().search(
                [("holiday_id", "=", False), ("date_from", ">=", first), ("date_to", "<=", last)])
            if pub_holiday:
                for public_holiday in pub_holiday:
                    date = public_holiday.date_from.date()
                    ph_list.append(
                        public_holiday.date_from.date().strftime("%Y-%m-%d"))
                    pub_holi_name.update(
                        {public_holiday.date_from.date().strftime("%Y-%m-%d"): public_holiday.name})

            if employee_search:
                for employee in employee_search:
                    employee_position.update({employee.id: row})
                    worksheet.write(row, 0, employee.name, format3)
                    row += 1
                    for date in week_date:
                        if date in ph_list:
                            worksheet.write(employee_position.get(employee.id, False), dic_date.get(
                                date, False), "PH" + " ("+str(pub_holi_name.get(date))+")", format_ph)
                        else:
                            worksheet.write(employee_position.get(
                                employee.id, False), dic_date.get(date, False), "A", format_absent)

            # Get Present (P) Employee with Duration
            if attendance_data_list:
                for date_rec in attendance_data_list:
                    if date_rec:
                        for data_date, v in date_rec.items():
                            if data_date in week_date:
                                if v.get("sum", False) and v.get("sum", False) < 8.00:
                                    worksheet._cell_overwrite_ok = True
                                    worksheet.write(employee_position.get(v.get("id", False), False), dic_date.get(
                                        data_date, False), "PL" + " ("+str(v.get("sum", False))+" hrs)", format4)
                                else:
                                    worksheet._cell_overwrite_ok = True
                                    worksheet.write(employee_position.get(v.get("id", False), False), dic_date.get(
                                        data_date, False), "P" + " ("+str(v.get("sum", False))+" hrs)", format_3)

            # Get Leave Absent (A) (Reason) Employee with Reason
            for date in week_date:
                emp_leave = self.env["hr.leave"].sudo().search([("employee_id", "in", employee_ids), (
                    "request_date_from", "<=", date), ("request_date_to", ">=", date)], limit=1)
                if emp_leave and emp_leave.employee_id:
                    worksheet._cell_overwrite_ok = True
                    worksheet.write(employee_position.get(emp_leave.employee_id.id, False), dic_date.get(
                        date, False), "A" + " ("+str(emp_leave.name)+")", format_absent)

        # For Monthly data excel generate
        if self.print_by == "monthly":
            if self.date:
                today = self.date
                last_day = today.replace(
                    day=calendar.monthrange(today.year, today.month)[1])
                first_day = today.replace(day=1)
                delta = last_day - first_day
                first = datetime.strftime(first_day, "%Y-%m-%d 00:00:00")
                last = datetime.strftime(last_day, "%Y-%m-%d 23:59:59")
            else:
                last_day = fields.Date.today().replace(day=calendar.monthrange(
                    fields.Date.today().year, fields.Date.today().month)[1])
                first_day = fields.Date.today().replace(day=1)
                delta = last_day - first_day
                first = datetime.strftime(first_day, "%Y-%m-%d 00:00:00")
                last = datetime.strftime(last_day, "%Y-%m-%d 23:59:59")

            week_date = []
            workbook = xlwt.Workbook()
            bold = xlwt.easyxf(
                "font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz left")
            heading_format = xlwt.easyxf(
                "font:height 300,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center")
            bold_center = xlwt.easyxf(
                "font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz center")

            format3 = xlwt.easyxf("align: horiz left")

            xlwt.add_palette_colour("custom_colour_green", 0x3a)
            workbook.set_colour_RGB(0x3a, 46, 125, 50)
            format_3 = xlwt.easyxf(
                "align: horiz left;pattern: pattern solid, fore_colour custom_colour_green;")

            format_absent = xlwt.easyxf(
                "align: horiz left;pattern: pattern solid, fore_colour red;")

            xlwt.add_palette_colour("custom_colour_yellow", 0x22)
            workbook.set_colour_RGB(0x22, 255, 241, 118)
            format4 = xlwt.easyxf(
                "align: horiz left;pattern: pattern solid, fore_colour custom_colour_yellow;")

            xlwt.add_palette_colour("custom_colour_ph", 0x2a)

            workbook.set_colour_RGB(0x2a, 25, 118, 210)
            format_ph = xlwt.easyxf(
                "align: horiz left;pattern: pattern solid, fore_colour custom_colour_ph;")

            worksheet = workbook.add_sheet("Employee Attendance monthly")
            count = 0
            worksheet.col(count).width = int(25*300)

            worksheet.write_merge(1, 2, 0, 31, "Employee Attendance - monthly" +
                                  " : "+str(first_day)+" To " + str(last_day), heading_format)
            worksheet.write(6, 0, "Employee Name", bold)
            row = 7
            col = 0
            dic_date = {}
            attendance_data_list = []
            for i in range(delta.days + 1):
                col += 1
                day = first_day + timedelta(days=i)
                day_date = str(day)
                week_date.append(day_date)
                dic_date.update({day_date: col})
                worksheet.write(6, col, day_date, bold)

                self.env.cr.execute("""SELECT he.id,he.name,min(ha.check_in),max(ha.check_out),max(ha.check_out)::timestamp -
                 min(ha.check_in)::timestamp, sum(ha.att_duration) FROM hr_attendance ha 
                 INNER JOIN hr_employee he ON he.id = ha.employee_id 
                 where ha.check_in >= %s and ha.check_out <= %s Group by ha.employee_id,he.id""", (day_date + " 00:00:00", day_date + " 23:59:59"))

                for rec in self.env.cr.dictfetchall():
                    if rec.get("id", False) in employee_ids:
                        attendance_data_list.append({day_date: dict(rec)})

            # Get all Employee, find Employee Position(row wise) and fill all Employee in sheet
            row = 7
            employee_position = {}

            ph_list = []
            pub_holi_name = {}
            pub_holiday = self.env["resource.calendar.leaves"].sudo().search(
                [("holiday_id", "=", False), ("date_from", ">=", first), ("date_to", "<=", last)])
            if pub_holiday:
                for public_holiday in pub_holiday:
                    date = public_holiday.date_from.date()
                    ph_list.append(
                        public_holiday.date_from.date().strftime("%Y-%m-%d"))
                    pub_holi_name.update(
                        {public_holiday.date_from.date().strftime("%Y-%m-%d"): public_holiday.name})

            if employee_search:
                for employee in employee_search:
                    employee_position.update({employee.id: row})
                    worksheet.write(row, 0, employee.name, format3)
                    row += 1
                    for date in week_date:
                        if date in ph_list:
                            worksheet.write(employee_position.get(employee.id, False), dic_date.get(
                                date, False), "PH" + " ("+str(pub_holi_name.get(date))+")", format_ph)
                        else:
                            worksheet.write(employee_position.get(
                                employee.id, False), dic_date.get(date, False), "A", format_absent)

            # Get Present Employee with Duration
            if attendance_data_list:
                for date_rec in attendance_data_list:
                    if date_rec:
                        for data_date, v in date_rec.items():
                            if data_date in week_date:
                                if v.get("sum", False) and v.get("sum", False) < 8.00:
                                    worksheet._cell_overwrite_ok = True
                                    worksheet.write(employee_position.get(v.get("id", False), False), dic_date.get(
                                        data_date, False), "PL" + " ("+str(v.get("sum", False))+")", format4)
                                    worksheet._cell_overwrite_ok = False
                                else:
                                    worksheet._cell_overwrite_ok = True
                                    worksheet.write(employee_position.get(v.get("id", False), False), dic_date.get(
                                        data_date, False), "P" + " ("+str(v.get("sum", False))+")", format_3)
                                    worksheet._cell_overwrite_ok = False

            # Get Absent Employee with Reason
            for date in week_date:
                emp_leave = self.env["hr.leave"].sudo().search([("employee_id", "in", employee_ids), (
                    "request_date_from", "<=", date), ("request_date_to", ">=", date)], limit=1)
                if emp_leave.employee_id.id:
                    worksheet._cell_overwrite_ok = True
                    worksheet.write(employee_position.get(emp_leave.employee_id.id, False), dic_date.get(
                        date, False), "A" + " ("+str(emp_leave.name)+")", format_absent)
                    worksheet._cell_overwrite_ok = False

        filename = ("Employee Attendance Report" + ".xls")
        fp = BytesIO()
        workbook.save(fp)

        data = base64.encodestring(fp.getvalue())
        IrAttachment = self.env['ir.attachment']
        attachment_vals = {
            "name": "Employee Attendance Report",
            "res_model": "ir.ui.view",
            "type": "binary",
            "datas": data,
            "public": True,
        }
        fp.close()

        attachment = IrAttachment.search([('name', '=', 'hr_employee'),
                                          ('type', '=', 'binary'),
                                          ('res_model', '=', 'ir.ui.view')],
                                         limit=1)
        if attachment:
            attachment.write(attachment_vals)
        else:
            attachment = IrAttachment.create(attachment_vals)
        # TODO: make user error here
        if not attachment:
            raise UserError('There is no attachments...')

        url = "/web/content/" + str(attachment.id) + "?download=true"
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }
