# Part of Softhealer Technologies.

import json
import odoo.http as http
from odoo.http import request
from datetime import datetime

class PartnerRead(http.Controller):

    @http.route(['''/get_json_data'''], type='http', auth="public", website=True, csrf=False, sitemap=False)
    def get_json_data(self):
        attendance_detail = {}
        geolocation_data = request.env['attendance.geolocation'].sudo().search([
        ], limit=1)
        lat = -25.363
        long = 131.044
        attendances = False
        if geolocation_data and geolocation_data.from_date and geolocation_data.to_date:
            domain = []
            if geolocation_data.department_id:
                domain.append(('employee_id.department_id', '=',
                               geolocation_data.department_id.id))

            if geolocation_data.job_id:
                domain.append(('employee_id.job_id', '=',
                               geolocation_data.job_id.id))

            if geolocation_data.employee_ids:
                attendances = request.env['hr.attendance'].sudo().search([('employee_id', 'in', geolocation_data.employee_ids.ids), (
                    'check_in', '>=', geolocation_data.from_date), ('check_out', '<=', geolocation_data.to_date)])
            elif geolocation_data.department_id or geolocation_data.job_id:
                domain.append(('check_in', '>=', geolocation_data.from_date))
                domain.append(('check_out', '<=', geolocation_data.to_date))
                attendances = request.env['hr.attendance'].sudo().search(
                    domain)

            if attendances:
                count = 1
                for attendance in attendances:
                    if attendance.in_latitude and attendance.in_longitude:
                        attendance_detail[attendance.id] = [attendance.in_latitude, attendance.in_longitude,
                                                            attendance.employee_id.name, int(attendance.employee_id.id), attendance.id]
                        if count == 1:
                            lat = attendance.in_latitude
                            long = attendance.in_longitude
                            count = 0
                    elif attendance.out_latitude and attendance.out_longitude:
                        attendance_detail[attendance.id] = [attendance.out_latitude, attendance.out_longitude,
                                                            attendance.employee_id.name,  int(attendance.employee_id.id), attendance.id]
                        if count == 1:
                            lat = attendance.in_latitude
                            long = attendance.in_longitude
                            count = 0

        bigData = {
            'attendance_detail': attendance_detail,
            'lat': lat,
            'long': long
        }
        return json.dumps(bigData)

class PartneBreakrRead(http.Controller):

    @http.route('/get_break_start_time', type='http', auth="public",methods=['GET'])
    def get_break_start(self):
        today = datetime.now().date()
        domains = [('user_id', '=', request.env.user.id)]
        employee = request.env['hr.employee'].search(domains)
        domain = [('employee_id', '=', employee.id),('sh_break_start_date', '=', today)]
        attend = request.env['hr.attendance'].search(domain,order='id desc',limit=1)
        data = {}
        if attend.sh_break_start:
            between = datetime.now() - attend.sh_break_start
            sec = int(round(between.total_seconds() * 1e3))
            end = True
            if attend.sh_break_end:
                end = False
            data = {
                'b_start' : sec,
                'end' : end
            }
        return json.dumps(data)
