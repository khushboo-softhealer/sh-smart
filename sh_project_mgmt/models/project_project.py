# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from datetime import datetime, timedelta, time, date
from odoo.exceptions import ValidationError
from odoo import models, fields, api, _
import calendar


class ProjectTaskInherit(models.Model):
    _inherit = "project.task"
    
    sh_pricing_mode = fields.Selection(related='project_id.sh_pricing_mode', string='Project Pricing Model', store=True,groups="sh_project_task_base.group_project_officer")
    sh_fp_based_on = fields.Selection(related='project_id.sh_fp_based_on', string='Project FP Based On', store=True,groups="sh_project_task_base.group_project_officer")
    sh_tm_based_on = fields.Selection(related='project_id.sh_tm_based_on', string='Project TM Based On', store=True,groups="sh_project_task_base.group_project_officer")
    project_stage_id = fields.Many2one('project.project.stage', related='project_id.stage_id', string='Project Stage', store=True,groups="sh_project_task_base.group_project_officer")
    project_start_date = fields.Date(related='project_id.date_start', string='Project Start Date', store=True,groups="sh_project_task_base.group_project_officer")
    project_end_date = fields.Date(related='project_id.date', string='Project End Date', store=True,groups="sh_project_task_base.group_project_officer")
    project_allocated_hours = fields.Float(related='project_id.allocated_hours', string='Project Allocated Hours', store=True,groups="sh_project_task_base.group_project_officer")
    project_total_profit = fields.Float(related='project_id.total_profit_float', string='Project Total Profit', store=True,groups="sh_project_mgmt.group_project_pl")
    
    @api.onchange('project_id')
    def onchange_project_id(self):
        if self.project_id:
            if self.project_id.default_task_users_ids:
                user_ids = []
                if self.user_ids:
                    user_ids = self.user_ids.ids
                for user in self.project_id.default_task_users_ids:
                    if user.id not in user_ids:
                        user_ids.append(user.id)
                self.user_ids = user_ids

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'project_id' in vals:
                project_id = self.env['project.project'].browse(vals.get('project_id'))
                
                if project_id.default_task_users_ids:
                    user_ids = []
                    if 'user_ids' in vals:
                        user_ids += vals.get('user_ids')[0][2]
                    for user in project_id.default_task_users_ids:
                        if user.id not in user_ids:
                            user_ids.append(user.id)
                    vals['user_ids'] = [[6, False, user_ids]]

        recs = super(ProjectTaskInherit, self).create(vals_list)
        for rec in recs:
            if rec.project_id.sh_child_ids:
                raise ValidationError(_('You cannot create task in parent project.'))        
        return recs
    

class Timesheet(models.Model):
    _inherit = 'account.analytic.line'

    def _domain_employee_id(self):
        # if not self.user_has_groups('hr_timesheet.group_hr_timesheet_approver'):
        #     return [('user_id', '=', self.env.user.id)]
        #modify domain to give SL to timesheet add access
        if not self.user_has_groups('sh_project_mgmt.group_project_task_create') and not self.user_has_groups('sh_project_task_base.group_project_officer'):
            return [('user_id', '=', self.env.user.id)]
        return []

    employee_id = fields.Many2one('hr.employee', "Employee", domain=_domain_employee_id, context={'active_test': False},
        help="Define an 'hourly cost' on the employee to track the cost of their time.")
    


    amount = fields.Monetary(
        'Amount',
        required=True,
        default=0.0,
        groups="analytic.group_analytic_accounting"
    )

    project_type_selection = fields.Selection(related='project_id.project_type_selection', store=True,groups="sh_project_task_base.group_project_officer")
    sh_pricing_mode = fields.Selection(related='project_id.sh_pricing_mode', string='Project Pricing Model', store=True,groups="sh_project_task_base.group_project_officer")
    sh_fp_based_on = fields.Selection(related='project_id.sh_fp_based_on', string='Project FP Based On', store=True,groups="sh_project_task_base.group_project_officer")
    sh_tm_based_on = fields.Selection(related='project_id.sh_tm_based_on', string='Project TM Based On', store=True,groups="sh_project_task_base.group_project_officer")
    project_stage_id = fields.Many2one('project.project.stage', related='project_id.stage_id', string='Project Stage', store=True,groups="sh_project_task_base.group_project_officer")
    project_start_date = fields.Date(related='project_id.date_start', string='Project Start Date', store=True,groups="sh_project_task_base.group_project_officer")
    project_end_date = fields.Date(related='project_id.date', string='Project End Date', store=True,groups="sh_project_task_base.group_project_officer")
    project_allocated_hours = fields.Float(related='project_id.allocated_hours', string='Project Allocated Hours', store=True,groups="sh_project_task_base.group_project_officer")
    project_total_profit = fields.Float(related='project_id.total_profit_float', string='Project Total Profit', store=True,groups="sh_project_mgmt.group_project_pl")

    def _hourly_cost(self):
        if self.employee_id and self.date:
            related_contract = self.env['hr.contract'].sudo().search([('employee_id','=',self.employee_id.id),
                                                                      ('date_start','<=',self.date),
                                                                      ('date_end','>=',self.date),
                                                                      ('state','!=','cancel')],limit=1)
            if related_contract:
                # compute worked days
                first_day = self.date.replace(day=1)
                last_day = self.date.replace(day=calendar.monthrange(
                    self.date.year, self.date.month)[1])

                day_from = datetime.combine(fields.Date.from_string(first_day), time.min)
                day_to = datetime.combine(fields.Date.from_string(last_day), time.max)

                work_data = related_contract.employee_id._get_work_days_data_batch(day_from, day_to, calendar=related_contract.resource_calendar_id)

                total_working_days_of_month = work_data[related_contract.employee_id.id]['days'] or 24
                perday_avg_hours = related_contract.resource_calendar_id.hours_per_day or 8.5
                
                wage =  related_contract.wage
                per_hour_rate = wage / (total_working_days_of_month * perday_avg_hours)

                return per_hour_rate
        return super()._hourly_cost()

    @api.model_create_multi
    def create(self, vals_list):
        res = super(Timesheet, self).create(vals_list)
        for rec in res:
            if rec.project_id.sh_child_ids:
                raise ValidationError(_('You cannot create timesheet in parent project.'))
        return res
    
    def action_fetch_old_timesheet_data(self):
        for timesheet in self:
            project_id = timesheet.project_id
            project_analytic_id = project_id.analytic_account_id
            timesheet_account_id = timesheet.account_id
    
            if timesheet_account_id != project_analytic_id:
                timesheet.account_id = project_analytic_id


class ProjectMgmtProjectProject(models.Model):
    _inherit = 'project.project'

    sh_pricing_mode = fields.Selection([
        ('fp', 'FP - Fixed Price'),
        ('tm', 'T&M - Time and Material'),
    ], string="Pricing Model", tracking=True)
    sh_fp_based_on = fields.Selection([
        ('no_milestone', 'No Milestone - One shot'),
        ('milestone', 'Implementation Project'),
    ], string='FP Based On', tracking=True)
    sh_tm_based_on = fields.Selection([
            ('success_pack', 'Success Packs Based'),
            ('billable', 'Billable Hours Based'),
        ], string='T&M Based On',tracking=True,
        help='Success Packs Based (Renewable required based on usage) - SO\nBillable Hours Based (Monthly billable invoice created) - MANUALLY'
    )
    sh_parent_id = fields.Many2one('project.project', string='Parent Project',tracking=True)
    sh_child_ids = fields.One2many('project.project', 'sh_parent_id', string='Child Projects',tracking=True)
    sh_child_project_count = fields.Integer('Child Projects Count', compute='_compute_child_project_count')
    sh_project_stage_tmpl_id = fields.Many2one(
        'sh.project.project.stage.template',
        string='Project Stage Template',tracking=True
    )
    sh_project_stage_ids = fields.Many2many(
        'project.project.stage',
        string='Project Stages',
        relation='sh_project_with_project_stages',
        # compute
        related='sh_project_stage_tmpl_id.sh_stage_ids',tracking=True
    )
    sale_line_estimation_template_line = fields.One2many(comodel_name='sh.sale.line.estimation.template.line', inverse_name='project_id', string='Estimation Template Lines')
    sh_sale_order_count = fields.Integer(compute="_compute_sh_sale_order_count")
    
    # sh_tm_based_on = fields.Selection([
    #         ('no_milestone', 'Success Packs Based'),
    #         ('milestone', 'Billable Hours Based'),
    #     ], string='T&M Based On',
    #     help='Success Packs Based (Renewable required based on usage) - SO\nBillable Hours Based (Monthly billable invoice created) - MANUALLY'
    # )
    odoo_version = fields.Many2one("sh.version",string="Version",tracking=True)
    sh_edition_id = fields.Many2one("sh.edition",string="Edition",tracking=True)
    remaining_inv_hours = fields.Float(compute='_compute_remaining_inv_hours', string='Remaining Hours', compute_sudo=True,store=True)
    default_task_users_ids = fields.Many2many('res.users', relation='project_project_default_users_rel', column1='project_id', column2='user_id',string='Default Task Users',tracking=True)
    billable_hours = fields.Float("Billable Hours",compute="_compute_billable_hours",groups="sh_project_mgmt.group_project_pl")
    total_income = fields.Float("Total Income",compute="_compute_profit",groups="sh_project_mgmt.group_project_pl")
    total_expense = fields.Float("Total Expense",compute="_compute_profit",groups="sh_project_mgmt.group_project_pl")
    total_profit = fields.Float("Profit",compute="_compute_profit",groups="sh_project_mgmt.group_project_pl")
    total_profit_percentage = fields.Float("Profit(%)",compute="_compute_profit",groups="sh_project_mgmt.group_project_pl")
    total_profit_float = fields.Float("Profit ",groups="sh_project_mgmt.group_project_pl")
    tag_ids = fields.Many2many('project.tags', relation='project_project_project_tags_rel', string='Tags',tracking=True)
    allocated_hours = fields.Float(string='Allocated Hours', tracking=True)
    project_start_date = fields.Date(string="Project Start Date",compute="_compute_project_dates") 
    project_end_date = fields.Date(string="Project End Date",compute="_compute_project_dates") 
    sh_send_timesheet = fields.Selection([('yes','Yes'),('no','No')],string="Send Timesheet",tracking=True)
    
    @api.onchange('sh_pricing_mode')
    def _onchange_sh_pricing_mode(self):
        if self.sh_pricing_mode:
            self.sh_fp_based_on = False
            self.sh_tm_based_on = False

    @api.depends('project_start_date','project_end_date')
    def _compute_project_dates(self):
        for rec in self:
            # if rec.sale_line_estimation_template_line:
            #     rec.project_start_date = min(line.from_date for line in rec.sale_line_estimation_template_line if line.from_date)
            #     rec.project_end_date = max(line.to_date for line in rec.sale_line_estimation_template_line if line.to_date)
            # else:
            #     rec.project_start_date = False
            #     rec.project_end_date = False

            from_dates = [line.from_date for line in rec.sale_line_estimation_template_line if line.from_date]
            # Get all valid to_date values
            to_dates = [line.to_date for line in rec.sale_line_estimation_template_line if line.to_date]

            # Assign the smallest from_date if available, otherwise set to False
            rec.project_start_date = min(from_dates) if from_dates else False
            # Assign the largest to_date if available, otherwise set to False
            rec.project_end_date = max(to_dates) if to_dates else False

            
    def action_open_update_project_wizard(self):
        '''Opens wizard to update stage and end date.'''
        return {
            'name': _(' Update Project'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.update.project.wizard',
            'view_id': self.env.ref('sh_project_mgmt.sh_update_project_wizard_view_form').id,
            'context' : {
                    'default_project_id' : self.id,
                    'default_stage_id' : self.stage_id.id,
                    'default_end_date' : self.date,
                    'default_sale_line_estimation_line':self.sale_line_estimation_template_line.ids
                },
            'target' : 'new',
        }
        
    def update_analytic_amount(self):
        timesheet_lines = self.env['account.analytic.line'].sudo().search([('project_id','=',self.id),('amount','=',0.0),('unit_amount','>',0.0)])
        print("timesheet_lines=========",timesheet_lines)
        for timesheet in timesheet_lines:
            print("timesheet======",timesheet)
            cost = timesheet._hourly_cost()
            amount = -timesheet.unit_amount * cost
            amount_converted = timesheet.employee_id.currency_id._convert(
                amount, timesheet.account_id.currency_id or timesheet.currency_id, self.env.company, timesheet.date)
            timesheet.sudo().update({
                'amount': amount_converted,
            })


    def _compute_profit(self):
        for project in self:
            total_income = 0.0
            total_expense = 0.0
            if project.analytic_account_id.id:
                self._cr.execute('SELECT amount  FROM account_analytic_line an LEFT JOIN product_product p ON an.product_id=p.id where account_id = %s and amount !=0.0 and an.product_id is null or account_id = %s and amount !=0.0 and p.default_code!=\'DOWN\'; ', (project.analytic_account_id.id,project.analytic_account_id.id,))
            analytic_items = self._cr.fetchall()
            for analytic_item in analytic_items:
                amount = analytic_item[0]
                if amount > 0:
                    total_income += amount
                elif amount < 0:
                    total_expense += amount
            project.total_income = total_income
            project.total_expense = total_expense * (-1)
            project.total_profit = total_income + total_expense
            project.total_profit_float = total_income + total_expense
            project.total_profit_percentage = 0.0
            if total_income > 0:
                project.total_profit_percentage = (100 * project.total_profit )/total_income
        
    def _compute_billable_hours(self):
        timesheets_read_group = self.env['account.analytic.line']._read_group(
            [('project_id', 'in', self.ids)],
            ['project_id', 'unit_amount_invoice'],
            ['project_id'],
            lazy=False)
        timesheet_time_dict = {res['project_id'][0]: res['unit_amount_invoice'] for res in timesheets_read_group}
        
        for project in self:
            project.billable_hours = 0            
            project.billable_hours = timesheet_time_dict.get(project.id, 0)

    @api.depends('allow_timesheets', 'timesheet_ids.unit_amount_invoice','timesheet_ids.unit_amount','allocated_hours')
    def _compute_remaining_inv_hours(self):
        timesheets_read_group = self.env['account.analytic.line']._read_group(
            [('project_id', 'in', self.ids)],
            ['project_id', 'unit_amount_invoice'],
            ['project_id'],
            lazy=False)
        timesheet_time_dict = {res['project_id'][0]: res['unit_amount_invoice'] for res in timesheets_read_group}
        for project in self:
            project.remaining_inv_hours = project.allocated_hours - timesheet_time_dict.get(project.id, 0)
            project.is_project_overtime = project.remaining_inv_hours < 0


    @api.depends('sh_child_ids')
    def _compute_child_project_count(self):
        for project in self:
            project.sh_child_project_count = len(project.sh_child_ids)

    def btn_show_child_projects(self):
        if not self.sh_child_ids:
            return
        return {
            'name': _('Sub Project'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'project.project',
            'target': 'current',
            'domain': [('id' ,'in', self.sh_child_ids.ids)],
            'context': {
                'create': False,
                'delete': False
            }
        }

    def btn_show_parent_project(self):
        if not self.sh_parent_id:
            return
        view = self.env.ref('project.edit_project')
        return {
            'name': _('Parent Project'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'project.project',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'current',
            'res_id': self.sh_parent_id.id,
            'context': {
                'create': False,
                'delete': False
            }
        }
    
    def _compute_sh_sale_order_count(self):
        for rec in self:
            rec.sh_sale_order_count = self.env['sale.order'].sudo().search_count([('project_id','=',rec.id)])
    
    def btn_show_sale_orders(self):
        '''Opens related sale.orders'''
        
        return {
            'name': _('Sale Order'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'views': [(False, 'tree'),(False, 'form')],
            'view_id': False,
            'domain': [('project_id','=',self.id)],
            'context': {
                'create': False,
                'delete': False
            },
            'target': 'current',
        }
    
    def action_auto_close_project(self):
        '''Cron : To Auto Close Project after 7 days from expiration date.'''
        project_ids = self.env['project.project'].sudo().search([('stage_id','!=',False),('date','!=',False)])
        if project_ids:
            for project in project_ids:
                users = [project.user_id,project.sh_technical_head,project.sh_designing_head]
                notify_user = []
                for user in users:
                    if user :
                        notify_user.append(user)

                # AUTO SEND NOTIFICATION TO PROJECT MANAGER 4 DAYS BEFORE CLOSING OF PROJECT
                if project.date and project.user_id:
                    before_days_date = project.date - timedelta(days=4)
                    if before_days_date <= date.today()  <= project.date and project.stage_id not in self.env.company.close_project_stage_ids :
                        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                        self.env['user.push.notification'].push_notification(notify_user, 'Project Expiration Reminder: Closing Soon', 'Project : %s:' % (
                            project.name), base_url+"/mail/view?model=project.project&res_id="+str(project.id), 'project.project', project.id,'project')
                
                # AUTO CLOSE PROJECT AFTER 7 DAYS FROM EXPIRATION DATE.
                if project.date and self.env.company.auto_close_project_stage_id and project.stage_id.id != self.env.company.auto_close_project_stage_id.id:
                    after_week_date = project.date + timedelta(days=7)
                    if date.today() >= after_week_date:
                        project.write({'stage_id' : self.env.company.auto_close_project_stage_id.id})
                        if project.user_id:
                            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                            self.env['user.push.notification'].push_notification(notify_user, 'Project Closed', 'Project : %s:' % (
                                project.name), base_url+"/mail/view?model=project.project&res_id="+str(project.id), 'project.project', project.id,'project')

class ProjectStages(models.Model):
    _inherit = 'project.project.stage'

    is_new_stage = fields.Boolean("Is New Stage ?",copy=False)
    is_running_stage = fields.Boolean("Is Running Stage ?",copy=False)