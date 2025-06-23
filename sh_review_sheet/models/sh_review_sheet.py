# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import _, api, fields, models
from datetime import datetime
import calendar
import calendar
from datetime import datetime
from odoo import models, fields, api

class ShReviewReport(models.Model):
    _name = "sh.review.sheet"
    _description = "Sh Review Report Model"
    _rec_name = 'project_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    project_id = fields.Many2one('project.project', string="Project",tracking=True)
    user_ids = fields.Many2many('res.users', string="Employees",tracking=True)
    from_date = fields.Date(string="Date",tracking=True)
    to_date = fields.Date(string="To Date",tracking=True)
    review_sheet_line = fields.One2many('sh.review.sheet.line', 'review_sheet_id', string="Review Sheet Line",tracking=True)

    project_manager = fields.Many2one('res.users', string="Project Head",tracking=True)
    technical_head = fields.Many2one('res.users', string="Technical Head",tracking=True)
    designing_head = fields.Many2one('res.users', string="Designing Head",tracking=True)
    state = fields.Selection([('new','New'),('close','Closed')],string="state",default='new',tracking=True)

    def close_sheet(self):
        self.sudo().write({'state':'close'})


    def time_to_float(self, time_str):
        """Convert time in HH:MM format to float."""
        try:
            hours, minutes = map(int, time_str.split(':'))
            return hours + (minutes / 60)
        except ValueError:
            raise ValueError("Invalid time format. Use HH:MM.")

    def auto_review_sheet_generation_cron(self):
        """Auto-generate review sheets based on timesheet records and project stage."""

        projects = self.env['project.project'].sudo().search([('stage_id.is_running_stage', '=', True)])
        today = datetime.today()
        first_day = today.replace(day=1)
        last_day = today.replace(day=calendar.monthrange(today.year, today.month)[1])

        review_timesheet_limit = self.env['ir.config_parameter'].sudo().get_param('sh_review_sheet.review_sheet_timesheet_limit')
        float_time_limit = self.time_to_float(review_timesheet_limit) if review_timesheet_limit else 0

        for project in projects:
            existing_review_sheet = self.env['sh.review.sheet'].sudo().search([
                ('project_id', '=', project.id),
                ('from_date', '=', first_day.date()),
                ('to_date', '=', last_day.date())
            ], limit=1)

            if existing_review_sheet:
                continue  # Skip if review sheet already exists for this project

            user_timesheet_map = {}
            users_list = []

            for user in project.responsible_user_ids:
                emp = self.env['hr.employee'].sudo().search([('user_id', '=', user.id)], limit=1)
                if not emp:
                    continue

                timesheets = self.env['account.analytic.line'].sudo().search([
                    ('date', '>=', first_day.date()),
                    ('date', '<=', last_day.date()),
                    ('project_id', '=', project.id),
                    ('employee_id', '=', emp.id)
                ])

                total_timesheet = sum(timesheets.mapped('unit_amount'))
                if total_timesheet >= float_time_limit:
                    users_list.append(user.id)
                    user_timesheet_map[user.id] = total_timesheet

            if users_list:
                review_sheet = self.env['sh.review.sheet'].sudo().create({
                    'project_id': project.id,
                    'user_ids': [(6, 0, users_list)],
                    'project_manager': project.user_id.id,
                    'technical_head': project.sh_technical_head.id,
                    'designing_head': project.sh_designing_head.id,
                    'from_date': first_day.date(),
                    'to_date': last_day.date()
                })

                self._create_review_sheet_lines(review_sheet, user_timesheet_map)

    def _create_review_sheet_lines(self, review_sheet, user_timesheet_map):
        """Helper function to create review sheet lines."""
        review_lines = []

        for user_id, total_timesheet in user_timesheet_map.items():
            for role, head in [
                ('project_manager', review_sheet.project_manager),
                ('technical_head', review_sheet.technical_head),
                ('designing_head', review_sheet.designing_head)
            ]:
                if head:
                    review_lines.append({
                        'review_sheet_id': review_sheet.id,
                        'project_id': review_sheet.project_id.id,
                        'user_id': user_id,
                        'project_responsible_type': role,
                        'project_responsible_id': head.id,
                        'timesheet': total_timesheet
                    })

        if review_lines:
            self.env['sh.review.sheet.line'].sudo().create(review_lines)


class ShReviewSheetLine(models.Model):
    _name = "sh.review.sheet.line"
    _description = "Sh Review Sheet Line"

    review_sheet_id = fields.Many2one('sh.review.sheet',string='Review Sheet ID',ondelete="cascade")
    project_id = fields.Many2one('project.project',string="Project Name")
    user_id = fields.Many2one('res.users',string="Employee Name")
    project_responsible_type = fields.Selection([
        ('project_manager','Project Manager'),
        ('technical_head','Technical Head'),
        ('designing_head','Designing Head')
    ])
    project_responsible_id = fields.Many2one('res.users',string="Project Head")
    ratings = fields.Selection([
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    ])
    review = fields.Html(string="Review")
    timesheet = fields.Float(string="Time Spent")
    state = fields.Selection(related="review_sheet_id.state",store=True)

    def open_timesheet(self):
        itemIds = []
        itemIds = self.env['account.analytic.line'].search([('employee_id.user_id','=',self.user_id.id),('project_id','=',self.project_id.id),('date','>',self.review_sheet_id.from_date),('date','<',self.review_sheet_id.to_date)]).mapped('id')
        return {
             'name': ('Timesheets'),
            'type': 'ir.actions.act_window',
            'view_id': False,
            'domain': [('id', 'in', itemIds)],
            'res_model': 'account.analytic.line',
            'view_type': 'tree',
            'view_mode': 'tree',
            'target': 'current',
        }


    def open_review_sheet(self):
        return {
            'type': 'ir.actions.act_window',
            'res_id': self.review_sheet_id.id,
            'res_model': 'sh.review.sheet',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
        }