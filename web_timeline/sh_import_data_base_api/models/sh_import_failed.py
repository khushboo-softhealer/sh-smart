# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ImportFailed(models.Model):
    _name = 'sh.import.failed'
    _description = 'Helps you to maintain the failed records track'
    _order = 'id desc'

    name = fields.Char("Name")
    error = fields.Char("Message")
    import_json = fields.Char("Import Json")
    datetime = fields.Datetime("Date & Time")
    base_config_id = fields.Many2one('sh.import.base')
    field_type = fields.Selection([
        ('customer', 'Customer'),
        ('product', 'Product'),
        ('res_users', 'Res Users'),
        ('pricelist', 'Pricelist'),
        ('partner_category', 'Partner Category'),
        ('category', 'Product Category'),
        ('auth', 'Authentication'),
        ('uom', 'Unit of Measure'),
        ('res_calendar', 'Resource Calendar'),
        ('order', 'Sale order'),
        ('location', 'Location'),
        ('warehouse', 'Warehouse'),
        ('project', 'Project'),
        ('task', 'Task'),
        ('message_subtype', 'Message Subtype'),
        ('project_basic', 'Project Basic'),
        ('lead', 'Crm Leads'),
        ('crm_tag', 'Crm Lead'),
        ('crm_basic', 'Crm Basic'),
        ('helpdesk_ticket', 'Helpdesk Ticket'),
        ('helpdesk_basic', 'Helpdesk Basic'),
        ('hr_contract', 'Hr Contract'),
        ('contract_basic', 'Contract Basic'),
        ('hr_attendance', 'Hr Attendance'),
        ('degree_basic', 'Degree Basic'),
        ('hr_payslip', 'Hr Payslip'),
        ('job_basic', 'Job Basic'),
        ('department_basic', 'Department Basic'),
        ('hr_payslip_run', 'Hr Payslip Run'),
        ('hr_payslip_work_days', 'Hr Payslip Work Days'),
        ('hr_payslip_line', 'Hr Payslip Line'),
        ('hr_contribution_register', 'Hr Contribution Register'),
        ('hr_payslip_input', 'Hr Payslip Input'),
        ('hr_payroll_structure', 'Hr Payroll Structure'),
        ('hr_applicant', 'Recruitment'),
        ('hr_applicant_basic', 'Recruitment Basic'),
        ('hr_leave', 'Time Off'),
        ('hr_leave_basic', 'Time Off Basic'),
        ('hr_basic', 'HR Basic'),
        ('hr_employee', 'Employee'),
        ('attachment', 'Attachment'),
        ('hr_employee_basic', 'Employee Basic'),
        ('blog_post', 'Blog Post'),
        ('blog_basic', 'Blog Basic'),
        ('timesheet', 'Timesheet'),
        ('blog', 'Blog'),
        ('invoice', 'Invoice'),
    ], string="Import Type")
