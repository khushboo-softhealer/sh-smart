# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import http
from odoo.http import request
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class TimesheetDashboard(http.Controller):
    @http.route('/get_sh_crm_activity_done_tbl', type='http', auth="public", methods=['GET'])
    def get_sh_crm_activity_done_tbl(self, **post):
        values = {}
        values['html_tbl'] = ''
        doman = []
        if post['project_value'] != 'all':
            doman.append(('project_id', '=', int(post['project_value'])))
        if post['task_value'] != 'all':
            doman.append(('task_id', '=', int(post['task_value'])))
        if post['days_filter']:

            if post['days_filter'] == 'today':

                dt_flt1 = []
                dt_flt1.append('date')
                dt_flt1.append('>=')
                dt_flt1.append(datetime.now().date().strftime("%Y-%m-%d"))
                doman.append(tuple(dt_flt1))

                dt_flt2 = []
                dt_flt2.append('date')
                dt_flt2.append('<=')
                dt_flt2.append(datetime.now().date().strftime("%Y-%m-%d"))
                doman.append(tuple(dt_flt2))

            elif post['days_filter'] == 'yesterday':

                dt_flt1 = []
                dt_flt1.append('date')
                dt_flt1.append('>=')
                prev_day = (datetime.now().date() -
                            relativedelta(days=1)).strftime('%Y-%m-%d')
                dt_flt1.append(prev_day)
                doman.append(tuple(dt_flt1))

                dt_flt2 = []
                dt_flt2.append('date')
                dt_flt2.append('<')
                prev_day = (datetime.now().date()).strftime('%Y-%m-%d')
                dt_flt2.append(prev_day)
                doman.append(tuple(dt_flt2))

            elif post['days_filter'] == 'weekly':  # current week

                dt_flt1 = []
                dt_flt1.append('date')
                dt_flt1.append('>')
                dt_flt1.append(
                    (datetime.now().date() - relativedelta(weeks=1, weekday=0)).strftime("%Y-%m-%d"))
                doman.append(tuple(dt_flt1))

                dt_flt2 = []
                dt_flt2.append('date')
                dt_flt2.append('<=')
                dt_flt2.append(datetime.now().date().strftime("%Y-%m-%d"))
                doman.append(tuple(dt_flt2))

            elif post['days_filter'] == 'prev_week':  # Previous week

                dt_flt1 = []
                dt_flt1.append('date')
                dt_flt1.append('>')
                dt_flt1.append(
                    (datetime.now().date() - relativedelta(weeks=2, weekday=0)).strftime("%Y-%m-%d"))
                doman.append(tuple(dt_flt1))

                dt_flt2 = []
                dt_flt2.append('date')
                dt_flt2.append('<=')
                dt_flt2.append(
                    (datetime.now().date() - relativedelta(weeks=1, weekday=6)).strftime("%Y-%m-%d"))
                doman.append(tuple(dt_flt2))

            elif post['days_filter'] == 'monthly':  # Current Month

                dt_flt1 = []
                dt_flt1.append('date')
                dt_flt1.append('>')
                dt_flt1.append((datetime.now().date()).strftime("%Y-%m-01"))
                doman.append(tuple(dt_flt1))

                dt_flt2 = []
                dt_flt2.append('date')
                dt_flt2.append('<=')
                dt_flt2.append(datetime.now().date().strftime("%Y-%m-%d"))
                doman.append(tuple(dt_flt2))

            elif post['days_filter'] == 'prev_month':  # Previous Month

                dt_flt1 = []
                dt_flt1.append('date')
                dt_flt1.append('>')
                dt_flt1.append(
                    (datetime.now().date() - relativedelta(months=1)).strftime("%Y-%m-01"))
                doman.append(tuple(dt_flt1))

                dt_flt2 = []
                dt_flt2.append('date')
                dt_flt2.append('<')
                dt_flt2.append(datetime.now().date().strftime("%Y-%m-01"))
                doman.append(tuple(dt_flt2))

            elif post['days_filter'] == 'cur_year':  # Current Year

                dt_flt1 = []
                dt_flt1.append('date')
                dt_flt1.append('>')
                dt_flt1.append((datetime.now().date()).strftime("%Y-01-01"))
                doman.append(tuple(dt_flt1))

                dt_flt2 = []
                dt_flt2.append('date')
                dt_flt2.append('<=')
                dt_flt2.append(datetime.now().date().strftime("%Y-%m-%d"))
                doman.append(tuple(dt_flt2))

            elif post['days_filter'] == 'prev_year':  # Previous Year

                dt_flt1 = []
                dt_flt1.append('date')
                dt_flt1.append('>')
                dt_flt1.append(
                    (datetime.now().date() - relativedelta(years=1)).strftime("%Y-01-01"))
                doman.append(tuple(dt_flt1))

                dt_flt2 = []
                dt_flt2.append('date')
                dt_flt2.append('<')
                dt_flt2.append(datetime.now().date().strftime("%Y-01-01"))
                doman.append(tuple(dt_flt2))

            elif post['days_filter'] == 'custom':
                if post['start_date'] and post['end_date']:

                    dt_flt1 = []
                    dt_flt1.append('date')
                    dt_flt1.append('>')
                    dt_flt1.append(datetime.strptime(
                        str(post['start_date']), "%Y-%m-%d"))
                    doman.append(tuple(dt_flt1))

                    dt_flt2 = []
                    dt_flt2.append('date')
                    dt_flt2.append('<=')
                    dt_flt2.append(datetime.strptime(
                        str(post['end_date']), "%Y-%m-%d"))
                    doman.append(tuple(dt_flt2))
        if doman:
            if 'employe' in post:
                if post['employe'] != 'all':
                    employee = request.env['hr.employee'].browse(
                        int(post['employe']))
                else:
                    domains = [('user_id', '=', request.env.user.id)]
                    employee = request.env['hr.employee'].search(domains)
            else:
                domains = [('user_id', '=', request.env.user.id)]
                employee = request.env['hr.employee'].search(domains)
            doman.append(('employee_id', '=', employee.id))
            doman.append(('task_id.is_temp_task', '=', False))
            rec_limit = 10
            activities = request.env['account.analytic.line'].sudo().search(
                doman, limit=rec_limit, order='id desc')
            if activities:
                html = request.env['ir.ui.view']._render_template('sh_timesheet_dashboard.sh_timesheet_tbl', {
                    'activities': activities, 'employee': employee
                })
                values['html_tbl'] = html.encode().decode()

        return json.dumps(values)


class TimesheetTemporaryTask(http.Controller):
    @http.route('/get_sh_temporary_done_tbl', type='http', auth="public", methods=['GET'])
    def get_temporary_task_list(self, **post):
        values = {}
        values['html_tbl'] = ''
        doman = []
        if post['project_value'] != 'all':
            doman.append(('project_id', '=', int(post['project_value'])))
        if post['task_value'] != 'all':
            doman.append(('task_id', '=', int(post['task_value'])))
        if post['days_filter']:

            if post['days_filter'] == 'today':

                dt_flt1 = []
                dt_flt1.append('date')
                dt_flt1.append('>=')
                dt_flt1.append(datetime.now().date().strftime("%Y-%m-%d"))
                doman.append(tuple(dt_flt1))

                dt_flt2 = []
                dt_flt2.append('date')
                dt_flt2.append('<=')
                dt_flt2.append(datetime.now().date().strftime("%Y-%m-%d"))
                doman.append(tuple(dt_flt2))

            elif post['days_filter'] == 'yesterday':

                dt_flt1 = []
                dt_flt1.append('date')
                dt_flt1.append('>=')
                prev_day = (datetime.now().date() -
                            relativedelta(days=1)).strftime('%Y-%m-%d')
                dt_flt1.append(prev_day)
                doman.append(tuple(dt_flt1))

                dt_flt2 = []
                dt_flt2.append('date')
                dt_flt2.append('<')
                prev_day = (datetime.now().date()).strftime('%Y-%m-%d')
                dt_flt2.append(prev_day)
                doman.append(tuple(dt_flt2))

            elif post['days_filter'] == 'weekly':  # current week

                dt_flt1 = []
                dt_flt1.append('date')
                dt_flt1.append('>')
                dt_flt1.append(
                    (datetime.now().date() - relativedelta(weeks=1, weekday=0)).strftime("%Y-%m-%d"))
                doman.append(tuple(dt_flt1))

                dt_flt2 = []
                dt_flt2.append('date')
                dt_flt2.append('<=')
                dt_flt2.append(datetime.now().date().strftime("%Y-%m-%d"))
                doman.append(tuple(dt_flt2))

            elif post['days_filter'] == 'prev_week':  # Previous week

                dt_flt1 = []
                dt_flt1.append('date')
                dt_flt1.append('>')
                dt_flt1.append(
                    (datetime.now().date() - relativedelta(weeks=2, weekday=0)).strftime("%Y-%m-%d"))
                doman.append(tuple(dt_flt1))

                dt_flt2 = []
                dt_flt2.append('date')
                dt_flt2.append('<=')
                dt_flt2.append(
                    (datetime.now().date() - relativedelta(weeks=1, weekday=6)).strftime("%Y-%m-%d"))
                doman.append(tuple(dt_flt2))

            elif post['days_filter'] == 'monthly':  # Current Month

                dt_flt1 = []
                dt_flt1.append('date')
                dt_flt1.append('>')
                dt_flt1.append((datetime.now().date()).strftime("%Y-%m-01"))
                doman.append(tuple(dt_flt1))

                dt_flt2 = []
                dt_flt2.append('date')
                dt_flt2.append('<=')
                dt_flt2.append(datetime.now().date().strftime("%Y-%m-%d"))
                doman.append(tuple(dt_flt2))

            elif post['days_filter'] == 'prev_month':  # Previous Month

                dt_flt1 = []
                dt_flt1.append('date')
                dt_flt1.append('>')
                dt_flt1.append(
                    (datetime.now().date() - relativedelta(months=1)).strftime("%Y-%m-01"))
                doman.append(tuple(dt_flt1))

                dt_flt2 = []
                dt_flt2.append('date')
                dt_flt2.append('<')
                dt_flt2.append(datetime.now().date().strftime("%Y-%m-01"))
                doman.append(tuple(dt_flt2))

            elif post['days_filter'] == 'cur_year':  # Current Year

                dt_flt1 = []
                dt_flt1.append('date')
                dt_flt1.append('>')
                dt_flt1.append((datetime.now().date()).strftime("%Y-01-01"))
                doman.append(tuple(dt_flt1))

                dt_flt2 = []
                dt_flt2.append('date')
                dt_flt2.append('<=')
                dt_flt2.append(datetime.now().date().strftime("%Y-%m-%d"))
                doman.append(tuple(dt_flt2))

            elif post['days_filter'] == 'prev_year':  # Previous Year

                dt_flt1 = []
                dt_flt1.append('date')
                dt_flt1.append('>')
                dt_flt1.append(
                    (datetime.now().date() - relativedelta(years=1)).strftime("%Y-01-01"))
                doman.append(tuple(dt_flt1))

                dt_flt2 = []
                dt_flt2.append('date')
                dt_flt2.append('<')
                dt_flt2.append(datetime.now().date().strftime("%Y-01-01"))
                doman.append(tuple(dt_flt2))

            elif post['days_filter'] == 'custom':
                if post['start_date'] and post['end_date']:

                    dt_flt1 = []
                    dt_flt1.append('date')
                    dt_flt1.append('>')
                    dt_flt1.append(datetime.strptime(
                        str(post['start_date']), "%Y-%m-%d"))
                    doman.append(tuple(dt_flt1))

                    dt_flt2 = []
                    dt_flt2.append('date')
                    dt_flt2.append('<=')
                    dt_flt2.append(datetime.strptime(
                        str(post['end_date']), "%Y-%m-%d"))
                    doman.append(tuple(dt_flt2))
        if doman:
            if 'employe' in post:
                if post['employe'] != 'all':
                    employee = request.env['hr.employee'].browse(
                        int(post['employe']))
                else:
                    domains = [('user_id', '=', request.env.user.id)]
                    employee = request.env['hr.employee'].search(domains)
            else:
                domains = [('user_id', '=', request.env.user.id)]
                employee = request.env['hr.employee'].search(domains)
            doman.append(('employee_id', '=', employee.id))
            doman.append(('task_id.is_temp_task', '=', True))
            rec_limit = 10
            activities = request.env['account.analytic.line'].sudo().search(
                doman, limit=rec_limit, order='id desc')
            if activities:
                html = request.env['ir.ui.view']._render_template('sh_timesheet_dashboard.sh_timesheet_tbl_temporary', {
                    'activities': activities, 'employee': employee
                })
                values['html_tbl'] = html.encode().decode()
        return json.dumps(values)


class TimesheetProjectDashboard(http.Controller):
    @http.route('/get_project_list', type='http', auth="public", methods=['GET'])
    def get_sh_project_list(self, **post):
        projects = {}
        if 'employe' in post:
            if post['employe'] != 'all':
                employee = request.env['hr.employee'].browse(
                    int(post['employe']))
            else:
                domains = [('user_id', '=', request.env.user.id)]
                employee = request.env['hr.employee'].search(domains)
        else:
            domains = [('user_id', '=', request.env.user.id)]
            employee = request.env['hr.employee'].search(domains)
        domain = []
        project = request.env['project.project'].search(domain)
        for data in project:
            if data.id not in projects:
                projects.update({data.id: data.name})
        return json.dumps(projects)


class TimesheetTaskDashboard(http.Controller):
    @http.route('/get_project_wise_task', type='http', auth="public", methods=['GET'])
    def get_sh_project_list(self, **post):
        tasks = {}
        domain = []
        if post['type'] != 'all':
            domain.append(('project_id', '=', int(post['type'])))
        find_task = request.env['project.task'].search(domain)
        for data in find_task:
            tasks.update({data.id: data.name})
        return json.dumps(tasks)


class TimesheetTaskDashboard(http.Controller):
    @http.route('/get_employee_list', type='http', auth="public", methods=['GET'])
    def get_employee_list(self, **post):
        emps = {}
        all_employee = request.env['hr.employee'].search([])
        for data in all_employee:
            emps.update({data.id: data.name})
        return json.dumps(emps)


class TimesheetTaskDashboard(http.Controller):
    @http.route('/get_sh_emplooyee_tbl', type='http', auth="public", methods=['GET'])
    def get_sh_project_list(self, **post):
        tasks = {}
        domain = []
        if post['days_filter']:

            if post['days_filter'] == 'today':

                dt_flt1 = []
                dt_flt1.append('date')
                dt_flt1.append('>=')
                dt_flt1.append(datetime.now().date().strftime("%Y-%m-%d"))
                domain.append(tuple(dt_flt1))

                dt_flt2 = []
                dt_flt2.append('date')
                dt_flt2.append('<=')
                dt_flt2.append(datetime.now().date().strftime("%Y-%m-%d"))
                domain.append(tuple(dt_flt2))

            elif post['days_filter'] == 'yesterday':

                dt_flt1 = []
                dt_flt1.append('date')
                dt_flt1.append('>=')
                prev_day = (datetime.now().date() -
                            relativedelta(days=1)).strftime('%Y-%m-%d')
                dt_flt1.append(prev_day)
                domain.append(tuple(dt_flt1))

                dt_flt2 = []
                dt_flt2.append('date')
                dt_flt2.append('<')
                prev_day = (datetime.now().date()).strftime('%Y-%m-%d')
                dt_flt2.append(prev_day)
                domain.append(tuple(dt_flt2))

            elif post['days_filter'] == 'weekly':  # current week

                dt_flt1 = []
                dt_flt1.append('date')
                dt_flt1.append('>')
                dt_flt1.append(
                    (datetime.now().date() - relativedelta(weeks=1, weekday=0)).strftime("%Y-%m-%d"))
                domain.append(tuple(dt_flt1))

                dt_flt2 = []
                dt_flt2.append('date')
                dt_flt2.append('<=')
                dt_flt2.append(datetime.now().date().strftime("%Y-%m-%d"))
                domain.append(tuple(dt_flt2))

            elif post['days_filter'] == 'prev_week':  # Previous week

                dt_flt1 = []
                dt_flt1.append('date')
                dt_flt1.append('>')
                dt_flt1.append(
                    (datetime.now().date() - relativedelta(weeks=2, weekday=0)).strftime("%Y-%m-%d"))
                domain.append(tuple(dt_flt1))

                dt_flt2 = []
                dt_flt2.append('date')
                dt_flt2.append('<=')
                dt_flt2.append(
                    (datetime.now().date() - relativedelta(weeks=1, weekday=6)).strftime("%Y-%m-%d"))
                domain.append(tuple(dt_flt2))

            elif post['days_filter'] == 'monthly':  # Current Month

                dt_flt1 = []
                dt_flt1.append('date')
                dt_flt1.append('>')
                dt_flt1.append((datetime.now().date()).strftime("%Y-%m-01"))
                domain.append(tuple(dt_flt1))

                dt_flt2 = []
                dt_flt2.append('date')
                dt_flt2.append('<=')
                dt_flt2.append(datetime.now().date().strftime("%Y-%m-%d"))
                domain.append(tuple(dt_flt2))

            elif post['days_filter'] == 'prev_month':  # Previous Month

                dt_flt1 = []
                dt_flt1.append('date')
                dt_flt1.append('>')
                dt_flt1.append(
                    (datetime.now().date() - relativedelta(months=1)).strftime("%Y-%m-01"))
                domain.append(tuple(dt_flt1))

                dt_flt2 = []
                dt_flt2.append('date')
                dt_flt2.append('<')
                dt_flt2.append(datetime.now().date().strftime("%Y-%m-01"))
                domain.append(tuple(dt_flt2))

            elif post['days_filter'] == 'cur_year':  # Current Year

                dt_flt1 = []
                dt_flt1.append('date')
                dt_flt1.append('>')
                dt_flt1.append((datetime.now().date()).strftime("%Y-01-01"))
                domain.append(tuple(dt_flt1))

                dt_flt2 = []
                dt_flt2.append('date')
                dt_flt2.append('<=')
                dt_flt2.append(datetime.now().date().strftime("%Y-%m-%d"))
                domain.append(tuple(dt_flt2))

            elif post['days_filter'] == 'prev_year':  # Previous Year

                dt_flt1 = []
                dt_flt1.append('date')
                dt_flt1.append('>')
                dt_flt1.append(
                    (datetime.now().date() - relativedelta(years=1)).strftime("%Y-01-01"))
                domain.append(tuple(dt_flt1))

                dt_flt2 = []
                dt_flt2.append('date')
                dt_flt2.append('<')
                dt_flt2.append(datetime.now().date().strftime("%Y-01-01"))
                domain.append(tuple(dt_flt2))

            elif post['days_filter'] == 'custom':
                if post['start_date'] and post['end_date']:

                    dt_flt1 = []
                    dt_flt1.append('date')
                    dt_flt1.append('>')
                    dt_flt1.append(datetime.strptime(
                        str(post['start_date']), "%Y-%m-%d"))
                    domain.append(tuple(dt_flt1))

                    dt_flt2 = []
                    dt_flt2.append('date')
                    dt_flt2.append('<=')
                    dt_flt2.append(datetime.strptime(
                        str(post['end_date']), "%Y-%m-%d"))
                    domain.append(tuple(dt_flt2))
        if domain:
            master_employee = {}
            domains = [('user_id', '=', request.env.user.id)]
            employee = request.env['hr.employee'].search(domains)
            all_employee = request.env['hr.employee'].search(
                [('coach_id', '=', employee.id)])
            employee_list = [emp.id for emp in all_employee]
            domain.append(('employee_id', 'in', employee_list))
            domain.append(('task_id.is_temp_task', '=', True))
            if post['project_value'] != 'all':
                domain.append(('project_id', '=', int(post['project_value'])))
            final_all_employee = request.env['account.analytic.line'].sudo().search(
                domain, order='id desc')
            for data in final_all_employee:
                if data.employee_id.name not in master_employee:
                    master_employee.update(
                        {data.employee_id.name: data.unit_amount})
                else:
                    pund = master_employee.get(data.employee_id.name)
                    master_employee.update(
                        {data.employee_id.name: data.unit_amount+pund})
            if master_employee:
                html = request.env['ir.ui.view']._render_template('sh_timesheet_dashboard.sh_timesheet_employee_tbl', {
                    'activities': master_employee
                })
                master_employee = html.encode().decode()
        return json.dumps(master_employee)
