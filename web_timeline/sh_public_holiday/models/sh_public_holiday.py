# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import _, api, fields, models,tools

from odoo.exceptions import ValidationError

class ShPublicHoliday(models.Model):
    _name = "sh.public.holiday"
    _description = "Public Holiday"
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(readonly=True,default="New",copy=False)
    sh_state = fields.Selection(
        string='State',
        selection=[('draft', 'Draft'), ('approve', 'Approved'),('done','Done')],
        default='draft',copy=False,tracking=True)
    sh_from_date = fields.Date(string="From Date",tracking=True)
    sh_to_date = fields.Date(string="To Date",tracking=True)
    sh_working_schedule_ids = fields.Many2many("resource.calendar", string="Working Schedules",tracking=True)
    sh_working_hours_lines = fields.One2many("sh.public.holiday.line","sh_public_holiday_id",string="lines")
    company_id = fields.Many2one("res.company",default=lambda self: self.env.user.company_id.id,string="Company")
    employees = fields.Many2many('hr.employee',string="Employees",tracking=True) 


    def approve_stage(self):
        if self.sh_state == "draft":
            for leave in self.sh_working_hours_lines:
                if not (self.sh_from_date <= leave.sh_start_date.date() <= self.sh_to_date and 
        self.sh_from_date <= leave.sh_end_date.date() <= self.sh_to_date):
                    raise ValidationError(_(f"Choose date's between {self.sh_from_date} and {self.sh_to_date} "))

                if leave.sh_start_date > leave.sh_end_date:
                    raise ValidationError(_(f"The start leave '{leave.sh_start_date.date()}' must be smaller than the end leave date '{leave.sh_end_date.date()}'."))

        self.sh_state = 'approve'

    def create_leaves(self):
        if self.sh_state == "approve":
            for schedule in self.sh_working_schedule_ids:
                for leave in self.sh_working_hours_lines:
                    # Change date formate to string due to check leave issue
                    start_date = leave.sh_start_date.strftime('%Y-%m-%d %H:%M:%S')
                    end_date = leave.sh_end_date.strftime('%Y-%m-%d %H:%M:%S')
                    self.env['resource.calendar.leaves'].create({'name':leave.name,
                                                                 'date_from':start_date,
                                                                 'date_to':end_date,
                                                                 'calendar_id':schedule.id,})
            self.sh_state = "done"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
    
            vals['name'] = self.env['ir.sequence'].next_by_code('sh.public') or _("New")
            vals['employees'] = self.env['hr.employee'].search([('resource_calendar_id','in',vals['sh_working_schedule_ids'][0][2])])
            res = super().create(vals_list) 
        return res
    
    
    @api.onchange('sh_working_schedule_ids')
    def _onchange_sh_working_schedule_ids(self):
        if self.sh_working_schedule_ids :
            self.employees = self.env['hr.employee'].search([('resource_calendar_id','in',self.sh_working_schedule_ids.ids)])
    

    def action_send_email(self):
        email_values={}
        emails = [email for email in self.employees.mapped('personal_email') if email]
        email_values = {'email_to': ', '.join(emails)}
        template = self.env.ref("sh_public_holiday.public_holiday_mail_template")
        template.sudo().send_mail(self.id, email_values=email_values, force_send=True)

    def set_to_draft(self):
        if self.sh_state:
            self.sh_state = 'draft'
