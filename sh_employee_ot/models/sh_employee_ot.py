# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import _, api, fields, models
from odoo.exceptions import UserError

class Users(models.Model):
    _inherit = 'res.users'

    #temporary solution for employee not defautl set when default company is not activated in header
    @api.depends('employee_ids')
    @api.depends_context('company')
    def _compute_company_employee(self):
        employee_per_user = {
            employee.user_id: employee
            for employee in self.env['hr.employee'].search([('user_id', 'in', self.ids)])
        }
        for user in self:
            user.employee_id = employee_per_user.get(user)

class ShEmployeeOt(models.Model):

    _name = "sh.employee.ot"
    _inherit = ['mail.thread']
    _description = "Employee OT"    

    name = fields.Char(readonly=True, copy=False, default="New")
    sh_employee_id = fields.Many2one('hr.employee',string='Employee', default=lambda self: self.env.user.employee_id.id)
    sh_user_id = fields.Many2one(related="sh_employee_id.user_id",store=True)
    sh_ot_date = fields.Date(string="Overtime Date")
    sh_project_id = fields.Many2one('project.project',string="Project",tracking=True)
    sh_project_manager_id = fields.Many2one(related="sh_project_id.user_id",string="Project Manager",readonly=True)
    sh_finance_manager_ids = fields.Many2many('res.users',string="Finance Managers",readonly=True,default=lambda self: self.env.company.sh_finance_manager)
    sh_project_timesheet_ids = fields.Many2many('account.analytic.line',string="Time-Sheets")
    state = fields.Selection(selection=[('draft','Draft'),('pm', 'Waiting For Approval(PM)'), ('fm', 'Waiting For Approval(FM)'),('done','Approved'),('paid','Paid'),('cancel','Rejected'),('canceled','Canceled')], tracking=True, default="draft", string="Status")
    sh_description = fields.Html(string="Description")
    sh_total_timesheet = fields.Float(string="Total Timesheet", compute="_compute_sh_total_timehseet")

    
    @api.constrains('sh_project_timesheet_ids')
    def _check_sh_project_timesheet_ids(self):
        for rec in self:
            if not rec.sh_project_timesheet_ids:
                raise UserError("At least 1 Timesheet required to create overtime.")
    
    def _compute_sh_total_timehseet(self):  
         for rec in self:
            timesheet = sum(rec.sh_project_timesheet_ids.mapped('unit_amount'))
            rec.sh_total_timesheet = timesheet

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _("New")) == _("New"):

                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sh.employee.ot') or _("New")
                vals['state'] = "draft"
            if not vals.get('sh_finance_manager_ids',False) and self.env.company.sh_finance_manager:
                vals['sh_finance_manager_ids'] = self.env.company.sh_finance_manager.ids
        return super().create(vals_list)

    def finance_manager_notify(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        user_list = []

        for manager in self.sh_finance_manager_ids:
             user_list.append(manager)
        self.env['user.push.notification'].push_notification(
            list_of_user_ids=user_list,
            title="Overtime Request Created",
            message=f"From : {self.sh_employee_id.name}",
            link=f'{base_url}/mail/view?model=sh.employee.ot&_id={str(self.id)}',
            res_model='sh.employee.ot',
            res_id=self.id,
            type='hr')

        self.state='fm'

    def project_manager_notify(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        self.env['user.push.notification'].push_notification(
            list_of_user_ids=[self.sh_project_manager_id],
            title="Overtime Request Created",
            message=f"From : {self.sh_employee_id.name}",
            link=f'{base_url}/mail/view?model=sh.employee.ot&_id={str(self.id)}',
            res_model='sh.employee.ot',
            res_id=self.id,
            type='hr')
    
        self.state='pm'
        
    def approve_ot(self):

        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        # finance_users = []

        # for manager in self.sh_finance_manager_ids:
        #      finance_users.append(manager.name)
        self.env['user.push.notification'].push_notification(
            list_of_user_ids=[self.sh_employee_id.user_id],
            title="Overtime Request Approved",
            message=f"By : {self.env.user.name}",
            link=f'{base_url}/mail/view?model=sh.employee.ot&_id={str(self.id)}',
            res_model='sh.employee.ot',
            res_id=self.id,
            type='hr')
    
        self.state = 'done'


    def reject_ot(self):
        self.state = 'cancel'

        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        # finance_users = []

        # for manager in self.sh_finance_manager_ids:
        #      finance_users.append(manager.name)
        self.env['user.push.notification'].push_notification(
            list_of_user_ids=[self.sh_employee_id.user_id],
            title="Overtime Request Rejected",
            message=f"By : {self.env.user.name}",
            link=f'{base_url}/mail/view?model=sh.employee.ot&_id={str(self.id)}',
            res_model='sh.employee.ot',
            res_id=self.id,
            type='hr')

    def cancel_paid(self):
        if self.state == 'paid' :
            self.state = 'done'

    def write(self, vals):
        for rec in self:
            if not rec.sh_finance_manager_ids and self.env.company.sh_finance_manager:
                vals['sh_finance_manager_ids'] = self.env.company.sh_finance_manager.ids
        return super().write(vals)

    @api.onchange('sh_project_id','sh_ot_date')
    def _onchange_sh_project_id(self):
        if self.sh_project_id or self.sh_ot_date:
            self.sh_project_timesheet_ids = False

    def cancel_ot(self):
        if self.env.user.has_group('sh_project_task_base.group_project_officer') or self.env.user.has_group('hr.group_hr_manager'):
            self.state = 'canceled'
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')         
            self.env['user.push.notification'].push_notification(
            list_of_user_ids=[self.sh_employee_id.user_id],
            title="Overtime Request Rejected",
            message=f"By : {self.env.user.name}",
            link=f'{base_url}/mail/view?model=sh.employee.ot&_id={str(self.id)}',
            res_model='sh.employee.ot',
            res_id=self.id,
            type='hr')