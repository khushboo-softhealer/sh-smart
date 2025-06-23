# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import api, models, fields, _
from odoo.exceptions import UserError
from odoo.fields import Command
from datetime import datetime, timedelta


class GoalSheet(models.Model):
    _name = 'sh.goal.sheet'
    _description = "Main Model for Goals"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "date_from desc"

    def sh_done_goal_sheet(self):
        for goal_sheet in self:
            goal_sheet.sudo().action_submit_employee()
            goal_sheet.sudo().action_submit_coach()
            goal_sheet.sudo().action_agree()


    name = fields.Char("Name", default="New",copy=False)
    employee_id = fields.Many2one("hr.employee", string="Employee")
    coach_id = fields.Many2one("hr.employee", string="Coach",tracking=True)
    manager_id = fields.Many2one("hr.employee", string="Manager",tracking=True)
    date_from = fields.Date("From Date")
    date_to = fields.Date("To Date")
    total_month = fields.Integer("Total Month")
    stage = fields.Selection([('draft', "Draft"), ('submitted', 'Submitted'), ('discussion', 'Discussion'), (
        'intermediate', 'Intermediate'), ('done', 'Done')], default="draft", tracking=True,copy=False)
    submitted_by_employee = fields.Boolean(
        "Submitted By Emploayee", default=False,copy=False)
    submitted_by_coach = fields.Boolean("Submitted By Coach", default=False,copy=False)
    detail_ids = fields.One2many(
        "sh.goal.sheet.line", "goal_id", string="Goal Sheet Lines")

    is_coach = fields.Boolean("IS Coach", compute="_check_login_user")
    is_manager = fields.Boolean("Is Manager", compute="_check_manager")
    coach_deadline = fields.Date("Coach Due Date")
    employee_deadline = fields.Date("Employee Due Date")
    active = fields.Boolean('Active', default=True)
    auto_submitted_employee = fields.Boolean("Auto Submitted(employee)",groups="project.group_project_manager",copy=False)
    auto_submitted_coach = fields.Boolean("Auto Submitted(Coach)",groups="project.group_project_manager",copy=False)

    message_to_manager = fields.Text("Messgae to Manager")

    creation_type = fields.Selection([('system','System Generated'),('manually','Manually Created')], default='manually',copy=False)
    contract_id= fields.Many2one('hr.contract',string="Contract")
    sh_contract_improvement_ids = fields.One2many(
        "hr.contract.improvement", 'goal_sheet_id', string="Improvements",related="contract_id.sh_contract_improvement_ids")
    sh_contract_goal_ids = fields.One2many(
        "hr.contract.goals", 'goal_sheet_id', string="Goals",related="contract_id.sh_contract_goal_ids")
    
    allocation_id = fields.Many2one("hr.leave.allocation",
                                    string="Allocation Request", copy=False, related="contract_id.allocation_id")

    leaves_count = fields.Integer(compute='_compute_leave_count',
                                  string='Leaves Count', related="contract_id.leaves_count")
    


    def action_view_allocation_leaves(self):
        in_contract_list = []
        domain = [("employee_id.id", "=", self.employee_id.id),('state','=','validate')]
        hr_leaves = self.env['hr.leave'].sudo().search(domain)
        if self.contract_id:
            for leave in hr_leaves:
                if self.contract_id.date_end and self.contract_id.date_start and leave.request_date_from and leave.request_date_to:
                    if self.contract_id.date_start <= leave.request_date_from and self.contract_id.date_end >= leave.request_date_to:
                        in_contract_list.append(leave.id)
        return {
            "type": "ir.actions.act_window",
            "name": "Leaves",
            "view_mode": "tree,form",
            "res_model": "hr.leave",
            "domain": [("id", "in", in_contract_list)]
        }

    def action_view_allocation(self):
        if self.allocation_id:
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                "res_model": "hr.leave.allocation",
                'target': 'self',
                'res_id': self.contract_id.allocation_id.id
            }
        
    def action_view_emp_timesheets(self):
        """view timesheets during contract start date and end date
        """
        check_in_date = self.contract_id.date_start
        check_out_date = self.contract_id.date_end
        timesheets = self.env['account.analytic.line'].sudo().search(
            [('employee_id', '=', self.employee_id.id)])
        if timesheets:
            timesheets = timesheets.filtered(
                lambda x: x.date >= check_in_date and x.date <= check_out_date)
            res = {
                'type': 'ir.actions.act_window',
                'name': 'Timesheets',
                'view_mode': 'tree,form',
                'view_type': 'tree,form',
                'res_model': 'account.analytic.line',
                'domain': [('id', 'in', timesheets.ids)],
            }
        return res
        
    def action_view_emp_attendance(self):
        """view attendance during contract start date and end date
        """
        curr_start_date = datetime.strftime(
            self.contract_id.date_start, "%Y/%m/%d 00:00:00")
        curr_end_date = datetime.strftime(self.contract_id.date_end, "%Y/%m/%d 23:59:59")
        attendances = self.env['hr.attendance'].search([('employee_id', '=', self.employee_id.id), (
            'check_in', '>=', curr_start_date), ('check_in', '<=', curr_end_date)])
        return {
            'type': 'ir.actions.act_window',
            'name': 'Attendances',
            'view_mode': 'tree,form',
            'res_model': 'hr.attendance',
            'domain': [('id', 'in', attendances.ids)],
        }
        
    def action_view_emp_attendance_modification_req(self):
        """view attendance modification request during contract start date and end date
        """
        check_in_date = self.contract_id.date_start
        check_out_date = self.contract_id.date_end
        attendance_modification = self.env['sh.attendance.modification.request'].search([('employee_id', '=', self.employee_id.id), ('date', '>=', check_in_date), ('date', '<=', check_out_date) ])
        return {
            'type': 'ir.actions.act_window',
            'name': 'Attendance Modification Request',
            'view_mode': 'tree,form',
            'res_model': 'sh.attendance.modification.request',
            'domain': [('id', 'in', attendance_modification.ids)],
        }
        

    def action_view_contract(self):
        if self.contract_id:
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                "res_model": "hr.contract",
                'target': 'self',
                'res_id': self.contract_id.id
            }

    # @api.model
    # def fields_get(self, allfields=None, attributes=None):
    #     fields = super().fields_get(allfields=allfields, attributes=attributes)
        
    #     if not self.env.user.has_group('project.group_project_manager'):
    #         fields_to_hide = ['submitted_by_employee','submitted_by_coach']
    #         for field in fields_to_hide:
    #             fields[field]['searchable'] = False
       
    #     return fields
    
    

    def copy_data(self, default=None):
        if default is None:
            default = {}
        if 'detail_ids' not in default:
            default['detail_ids'] = [
                Command.create(line.copy_data()[0])
                for line in self.detail_ids
            ]
        return super().copy_data(default)
    
    def _check_login_user(self):
        for rec in self:
            if self.env.user.id == self.coach_id.user_id.id:
                rec.is_coach = True
            else:
                rec.is_coach = False
            if self.coach_id.user_id.id == self.manager_id.user_id.id and self.contract_id:
                rec.is_coach = False


    def _check_manager(self):
        for rec in self:
            if self.env.user.id == self.manager_id.user_id.id:
                rec.is_manager = True
            else:
                rec.is_manager = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sh.goal.sheet.seq')
        return super(GoalSheet, self).create(vals_list)

    def action_submit_employee(self):
        self.sudo().submitted_by_employee = True
        message_vals = {
            'message_type': 'comment',
            'model': 'sh.goal.sheet',
            'res_id': self.id,
            'body': "Submitted By Employee",
        }
        self.env['mail.message'].create(message_vals)
        if self.sudo().submitted_by_coach:
            self.write({
                'stage': 'submitted'
            })

    def action_submit_coach(self):
        self.sudo().submitted_by_coach = True
        message_vals = {
            'message_type': 'comment',
            'model': 'sh.goal.sheet',
            'res_id': self.id,
            'body': "Submitted By Coach",
        }
        self.env['mail.message'].create(message_vals)
        if self.sudo().submitted_by_employee:
            self.write({
                'stage': 'submitted'
            })

    def action_agree(self):
        self.write({
            'stage': 'done'
        })

    def action_discussion(self):
        self.write({
            'stage': 'discussion'
        })

    def action_intermediate(self):
        self.write({
            'stage': 'intermediate'
        })

    def action_reset_to_draft_employee(self):
        self.write({
            'stage' : 'draft',
            'submitted_by_employee':False
        })

    def action_reset_to_draft_coach(self):
        self.write({
            'stage' : 'draft',
            'submitted_by_coach':False,
        })


    def write(self, vals):
        # for rec in self:
        if 'active' in vals and not self.user_has_groups('project.group_project_manager'):
            raise UserError(
                _("You do not have permission to perform this action"))
        
        for rec in self:
            if vals.get('detail_ids'):
                if self.env.user.id == rec.employee_id.user_id.id and rec.sudo().submitted_by_employee:
                    raise UserError(
                    _("Your goal sheet is already submitted !"))
                
                if self.env.user.id == rec.coach_id.user_id.id and rec.sudo().submitted_by_coach:
                    raise UserError(
                    _("Your goal sheet is already submitted !"))
        


        return super(GoalSheet, self).write(vals)
    
    def view_goal_sheet(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Goal Lines",
            "view_mode": "tree",
            'view_id': self.env.ref('sh_employee_goal_management.sh_goal_sheet_line_tree').id,
            "res_model": "sh.goal.sheet.line",
            "domain": [("goal_id", "=", self.id)]
        }
