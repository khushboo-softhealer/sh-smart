# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from datetime import date, datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ShEmployeeTaskAllocation(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'sh.employee.task.allocation'
    _description = 'Employee Task Allocation'
    
    name = fields.Char('Ref',default='New', tracking=True)
    sh_department_id = fields.Many2one('hr.department', string='Department',tracking=True)
    sh_employee_id = fields.Many2one('hr.employee', string='Assigned Person',tracking=True)
    sh_responsible_tl_id = fields.Many2one('hr.employee',string='Responsible TL',tracking=True)
    sh_responsible_tl_ids = fields.Many2many('hr.employee',string='All Approvers',tracking=True)
    is_lock = fields.Boolean(compute="_compute_is_lock")
    show_approval_btn = fields.Boolean(compute="_compute_show_approval_btn")
    show_cancel_btn = fields.Boolean(compute="_compute_show_cancel_btn")
    user_id = fields.Many2one('res.users',string='Create User' ,domain=[('share','=',False)], default=lambda self:self.env.user, tracking=True)
    sh_priority = fields.Selection([
                            ('very_low', 'Very Low'),
                            ('low', 'Low'),
                            ('medium', 'Medium'),
                            ('high', 'High'),
                            ('very_high', 'Very High'),
                        ], string='Priority', tracking=True)
    sh_project_id = fields.Many2one('project.project', string='Project', tracking=True)
    sh_task_id = fields.Many2one('project.task', string='Task', tracking=True)
    from_date = fields.Date('From Date', tracking=True)
    to_date = fields.Date('To Date', tracking=True)
    parent_from_date = fields.Date('Actual From Date', tracking=True)
    parent_to_date = fields.Date('Actual To Date', tracking=True)
    allocated_hours = fields.Float('Allocated Hours', tracking=True)
    existing_allocation_ids = fields.Many2many('sh.employee.task.allocation', relation="emp_task_alloc_emp_task_alloc_wizard_rel", compute="_compute_existing_allocation")
    state = fields.Selection([('draft', 'Draft'),
                              ('waiting', 'Waiting For Approval'), 
                              ('done', 'Done'), 
                              ('reject', 'Reject'), 
                              ('cancel', 'Cancel')
                            ], string="State", default='waiting', tracking=True)
    sh_remarks = fields.Text('Remarks', tracking=True)
    allocation_master_id= fields.Many2one('sh.employee.task.allocation.wizard',string="Allocation Master")
    sh_timesheet_hours = fields.Float(string="Timesheet Hours", compute="_compute_timesheet_hours")
    employee_on_leave_today = fields.Boolean(string="Employee On Leave Today",compute="_compute_check_employee_leave",)
    employee_on_half_day_leave = fields.Boolean(string="Employee On Half-Day Leave Today",compute="_compute_check_employee_leave",)
    employee_on_custom_day_leave = fields.Boolean(string="Employee On Half-Day Leave Today",compute="_compute_check_employee_leave",)

    def _compute_check_employee_leave(self):
        for rec in self:
            # Reset Fields
            rec.employee_on_leave_today = False
            rec.employee_on_half_day_leave = False
            rec.employee_on_custom_day_leave = False
    
            if rec.from_date and rec.to_date and rec.sh_employee_id:
                leave_domain = [
                    ('employee_ids', 'in', [rec.sh_employee_id.id]),
                    ('state', 'not in', ['draft', 'refused']),
                    ('date_from', '<=', rec.to_date),
                    ('date_to', '>=', rec.from_date),
                ]
    
                # Fetch all relevant leaves in a single search
                employee_leaves = self.env['hr.leave'].sudo().search(leave_domain)
    
                # Classify leave types
                for leave in employee_leaves:
                    if leave.request_unit_half:
                        rec.employee_on_half_day_leave = True
                    elif leave.request_unit_hours:
                        rec.employee_on_custom_day_leave = True
                    else:
                        rec.employee_on_leave_today = True
    
                    # Break early if a leave type is found (avoid unnecessary loops)
                    if rec.employee_on_half_day_leave or rec.employee_on_custom_day_leave or rec.employee_on_leave_today:
                        break
                    
    def _compute_timesheet_hours(self):
        for rec in self:
            hours = 0
            if rec.sh_project_id and not rec.sh_task_id:
                project_timesheets = self.env['account.analytic.line'].sudo().search([('employee_id','=',rec.sh_employee_id.id),('project_id','=',rec.sh_project_id.id),('date','>=',rec.from_date),('date','<=',rec.to_date)])
                if project_timesheets:
                    hours = sum(project_timesheets.mapped('unit_amount'))
            
            if rec.sh_project_id and rec.sh_task_id:
                task_timesheets = self.env['account.analytic.line'].sudo().search([('employee_id','=',rec.sh_employee_id.id),('project_id','=',rec.sh_project_id.id),('task_id','=',rec.sh_task_id.id),('date','>=',rec.from_date),('date','<=',rec.to_date)])
                if task_timesheets:
                    hours = sum(task_timesheets.mapped('unit_amount'))
                    
            rec.sh_timesheet_hours = hours
    
    
    def _compute_is_lock(self):
        for rec in self:
            rec.is_lock = True
            if rec.state in ['draft','waiting'] and rec.user_id.id == rec.env.uid and rec.state != 'reject':
                rec.is_lock = False
    
    # def _get_all_coach(self, coach, sh_responsible_tl_ids = []):
    #     if coach.coach_id:
    #         sh_responsible_tl_ids.append(coach.coach_id.id)
    #         self._get_all_coach(coach.coach_id,sh_responsible_tl_ids)
    #     else:
    #         sh_responsible_tl_ids.append(coach.id)
    #         return sh_responsible_tl_ids
    def _get_all_coach(self, coach, sh_responsible_tl_ids=None):
        if sh_responsible_tl_ids is None:
            sh_responsible_tl_ids = []

        # Check if the current coach has already been processed to avoid recursion
        if coach.id in sh_responsible_tl_ids:
            return sh_responsible_tl_ids

        # Add the current coach to the list
        sh_responsible_tl_ids.append(coach.id)

        # If the coach has a parent coach, recursively process the parent
        if coach.coach_id:
            self._get_all_coach(coach.coach_id, sh_responsible_tl_ids)

        return sh_responsible_tl_ids
        


    @api.onchange('sh_employee_id')
    def onchange_sh_employee_id(self):
        if self.sh_employee_id.id and self.sh_employee_id.user_id.has_group('sh_project_task_base.group_project_officer'):
            self.sh_responsible_tl_id = self.sh_employee_id.id

        else:
            self.sh_responsible_tl_id = self.sh_employee_id.coach_id.id
        
        sh_responsible_tl_ids = []
        if self.sh_employee_id.id and self.sh_employee_id.user_id.has_group('sh_project_task_base.group_project_officer') or self.sh_employee_id.user_id.has_group('sh_project_mgmt.group_project_task_create'):
            sh_responsible_tl_ids.append(self.sh_employee_id.id)
        
        if self.sh_employee_id.coach_id:
            sh_responsible_tl_ids = self._get_all_coach(self.sh_employee_id.coach_id, sh_responsible_tl_ids)

        self.sh_responsible_tl_ids = [(6,0,sh_responsible_tl_ids)]
            
    @api.depends('sh_employee_id','from_date','from_date')
    def _compute_existing_allocation(self):
        '''Computes existing allocation of employee based on from date and to date selected. '''
        for rec in self:
            rec.existing_allocation_ids = False
            domain = []
            if rec.sh_employee_id:
                domain.append(('sh_employee_id','=',rec.sh_employee_id.id))
                domain.append(('state','=','done'))
                
            if domain:
                if rec.from_date and rec.to_date:
                    existing_allocations = self.env['sh.employee.task.allocation'].sudo().search(domain)
                    if existing_allocations:
                        existing_records = []
                        for alloc in existing_allocations:
                            if alloc.from_date <= rec.from_date <= alloc.to_date or alloc.from_date <= rec.to_date <= alloc.to_date or rec.from_date <= alloc.from_date <= rec.to_date or rec.from_date <= alloc.to_date <= rec.to_date:
                                existing_records.append(alloc.id)
                        
                        if existing_records:
                            existing_ids = self.env['sh.employee.task.allocation'].browse(existing_records)
                            if existing_ids:
                                rec.existing_allocation_ids = existing_ids.ids

    @api.depends('sh_responsible_tl_ids')
    def _compute_show_approval_btn(self):
        for rec in self:
            rec.show_approval_btn = False
            if rec.sh_responsible_tl_ids:
                for sh_responsible_tl_id in rec.sh_responsible_tl_ids:
                    if sh_responsible_tl_id.user_id.id == rec.env.user.id:
                        rec.show_approval_btn = True
                    # elif rec.sh_responsible_tl_id and rec.sh_department_id:
                    #     if rec.sh_responsible_tl_id.department_id.id == rec.sh_department_id.id and rec.sh_responsible_tl_id.user_id.id == rec.env.uid:
                    #         rec.show_approval_btn = True
            # elif rec.sh_department_id and rec.sh_responsible_tl_id:
            #     dept_emp_ids = rec.env['hr.employee'].sudo().search([('department_id','=',rec.sh_department_id.id)])
            #     dept_tl_ids = []
            #     if dept_emp_ids:
            #         for emp in dept_emp_ids:
            #             if emp.user_id.has_group('sh_project_task_base.group_project_officer'):
            #                 dept_tl_ids.append(emp.id)
                
            #     if dept_tl_ids:
            #         if rec.env.uid in dept_tl_ids and rec.sh_responsible_tl_id.user_id.id == rec.env.uid:
            #             rec.show_approval_btn = True

    # @api.depends('sh_responsible_tl_id')
    # def _compute_show_approval_btn(self):
    #     for rec in self:
    #         rec.show_approval_btn = False
    #         if rec.sh_responsible_tl_id and rec.sh_responsible_tl_id.user_id:
    #             if rec.sh_responsible_tl_id.user_id.id == rec.env.user.id:
    #                 rec.show_approval_btn = True
    #             elif rec.sh_responsible_tl_id and rec.sh_department_id:
    #                 if rec.sh_responsible_tl_id.department_id.id == rec.sh_department_id.id and rec.sh_responsible_tl_id.user_id.id == rec.env.uid:
    #                     rec.show_approval_btn = True
    #         elif rec.sh_department_id and rec.sh_responsible_tl_id:
    #             dept_emp_ids = rec.env['hr.employee'].sudo().search([('department_id','=',rec.sh_department_id.id)])
    #             dept_tl_ids = []
    #             if dept_emp_ids:
    #                 for emp in dept_emp_ids:
    #                     if emp.user_id.has_group('sh_project_task_base.group_project_officer'):
    #                         dept_tl_ids.append(emp.id)
                
    #             if dept_tl_ids:
    #                 if rec.env.uid in dept_tl_ids and rec.sh_responsible_tl_id.user_id.id == rec.env.uid:
    #                     rec.show_approval_btn = True
    
    @api.depends('user_id','state')
    def _compute_show_cancel_btn(self):
        user_group = self.user_has_groups("sh_project_task_base.group_project_officer,sh_project_mgmt.group_project_task_create")
        for rec in self:
            rec.show_cancel_btn = False
            if user_group and rec.state not in ('cancel') and self.env.user.employee_id in rec.sh_responsible_tl_ids or self.env.uid == rec.user_id.id:
                rec.show_cancel_btn = True
                    
    def _add_seq(self):
        if self.name and self.name != 'New':
            return
        seq = 'ETA'
        id_len = len(str(self.id))
        if id_len == 1:
            seq += '000'
        elif id_len == 2:
            seq += '00'
        elif id_len == 3: 
            seq += '0'
        seq += str(self.id)
        self.sudo().write({'name': seq})
    
    @api.model_create_multi
    def create(self, vals_list):
        res = super(ShEmployeeTaskAllocation, self).create(vals_list)
        for rec in res:
                rec._add_seq()
        return res

    def write(self, vals):
        res = super().write(vals)
        
        if self.allocated_hours <= 0:
            raise UserError(_('Allocated hours must be greater than zero.'))
        
        # existing_allocated_hours = 0
        # if self.existing_allocation_ids:
        #     existing_allocated_hours = sum(self.existing_allocation_ids.mapped('allocated_hours'))
            
        # if self.user_id.id != self.sh_responsible_tl_id.user_id.id:
        #     total_hours = existing_allocated_hours + self.allocated_hours
        # else:
        #     total_hours = existing_allocated_hours
        
        # if total_hours > 8.5:
        #     if vals.get('state') not in ['reject','cancel']:
        #         raise UserError(_(f'{self.sh_employee_id.name} is not available for demanding hours from D. {self.from_date} to D. {self.to_date}.'))
        
        # If TL transfers allocation to another TL then notification send to new TL
        # if self.env.user.has_group('sh_project_task_base.group_project_officer') and vals.get('sh_responsible_tl_id'):
        #     base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        #     if self.sh_responsible_tl_id.user_id and self.sh_responsible_tl_id.user_id.has_group('sh_project_task_base.group_project_officer'):
        #         if self.sh_employee_id and self.sh_responsible_tl_id and self.sh_employee_id.coach_id.id == self.sh_responsible_tl_id.id and self.sh_responsible_tl_id.user_id.id != self.env.uid:
        #             self.env['user.push.notification'].push_notification(
        #                     self.sh_responsible_tl_id.user_id,
        #                     'Request For Availability of your Employee',
        #                     'Assignment request of %s for project %s is changed by %s.'% (self.sh_employee_id.name, self.sh_project_id.name, self.env.user.name),
        #                     base_url+"/mail/view?model=sh.employee.task.allocation&res_id="+str(self.id),
        #                     'sh.employee.task.allocation', 
        #                     self.id,
        #                     'assignment'
        #                 )
        #         elif not self.sh_employee_id and self.sh_responsible_tl_id and self.sh_responsible_tl_id.user_id.id != self.env.uid:
        #             self.env['user.push.notification'].push_notification(
        #                     self.sh_responsible_tl_id.user_id,
        #                     'Request For Availability of your Employee',
        #                     'Assignment request of your available employee for project %s is changed by %s.'% (self.sh_project_id.name, self.user_id.name),
        #                     base_url+"/mail/view?model=sh.employee.task.allocation&res_id="+str(self.id),
        #                     'sh.employee.task.allocation', 
        #                     self.id,
        #                     'assignment'
        #                 )
        return res
    
    def action_approve_allocation_following(self):
        '''To Approve all following allocation request'''
        for rec in self:
            allocated_hours = rec.allocated_hours
            if rec.allocation_master_id  and rec.allocation_master_id.allocation_lines:
                for each_allocation in rec.allocation_master_id.allocation_lines:
                    if each_allocation.state == 'waiting':
                        each_allocation.write({'allocated_hours':allocated_hours})
                    each_allocation.with_context({'multi_allocation_approve' : True}).action_approve_allocation()
            base_url = rec.env['ir.config_parameter'].sudo().get_param('web.base.url')

            self.env['user.push.notification'].push_notification(
                    [rec.user_id,rec.sh_employee_id.user_id],
                    'Assignment Approved',
                    'Multi Assignment of %s for project %s has been approved by %s.'% (rec.sh_employee_id.name,rec.sh_project_id.name,rec.env.user.name),
                    base_url+"/mail/view?model=sh.employee.task.allocation&res_id="+str(rec.id),
                    'sh.employee.task.allocation', 
                    rec.id,
                    'assignment'
                )
    def action_approve_allocation(self):
        '''To Approve allocation request'''
        for rec in self:
            if not rec.sh_employee_id:
                raise UserError(_('Assigned To is required in order to approve allocation.'))
            
            # if not rec.sh_responsible_tl_id:
            #     raise UserError(_('Responsible TL is required in order to reject allocation.'))
            
            if rec.state == 'waiting':
                
                # existing_allocated_hours = 0
                # if rec.existing_allocation_ids:
                #     existing_allocated_hours = sum(rec.existing_allocation_ids.mapped('allocated_hours'))
                
                # total_hours = existing_allocated_hours + rec.allocated_hours
                # if total_hours > 8.5:
                #     raise UserError(_(f'You cannot Approve because {rec.sh_employee_id.name} is not available for demanding hours from D. {rec.from_date} to D. {rec.to_date}.'))
                
                rec.state = 'done'
                if rec.state == 'done':
                    if rec.sh_employee_id:
                        # Assign employee in project and task if set while approved
                        if rec.sh_project_id:
                            rec.sh_project_id.sudo().write({'responsible_user_ids':[(4,rec.sh_employee_id.user_id.id)]})
                        if rec.sh_task_id:
                            rec.sh_task_id.sudo().write({'user_ids':[(4,rec.sh_employee_id.user_id.id)]})

                    base_url = rec.env['ir.config_parameter'].sudo().get_param('web.base.url')

                    if not self.env.context.get('multi_allocation_approve'):
                        rec.env['user.push.notification'].push_notification(
                                [rec.user_id,rec.sh_employee_id.user_id],
                                'Assignment Approved',
                                'Assignment of %s for project %s has been approved by %s.'% (rec.sh_employee_id.name,rec.sh_project_id.name,rec.env.user.name),
                                base_url+"/mail/view?model=sh.employee.task.allocation&res_id="+str(rec.id),
                                'sh.employee.task.allocation', 
                                rec.id,
                                'assignment'
                            )
            # else:
            #     raise UserError(_('You cannot approve allocation of other TL employee.'))

    def action_reject_allocation_following(self):
        '''To Reject all following allocation request'''
        for rec in self:
            if rec.allocation_master_id  and rec.allocation_master_id.allocation_lines:
                for each_allocation in rec.allocation_master_id.allocation_lines:
                    if each_allocation.from_date >= rec.from_date:
                        each_allocation.with_context({'multi_allocation_reject' : True}).action_reject_allocation()
            
            
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            self.env['user.push.notification'].push_notification(
                            [self.user_id,self.sh_employee_id.user_id],
                            'Assignment Rejected',
                            'Multi Assignment of %s for project %s has been rejected by %s.'% (self.sh_employee_id.name,self.sh_project_id.name,self.env.user.name),
                            base_url+"/mail/view?model=sh.employee.task.allocation&res_id="+str(self.id),
                            'sh.employee.task.allocation', 
                            self.id,
                            'assignment'
                        )
  

    def action_reject_allocation(self):
        '''To Reject allocation request'''
        if not self.sh_employee_id:
            raise UserError(_('Assigned To is required in order to reject allocation.'))
        
        # if not self.sh_responsible_tl_id:
        #     raise UserError(_('Responsible TL is required in order to reject allocation.'))

        # if self.sh_responsible_tl_id.user_id.id == self.env.uid or self.sh_employee_id.parent_id.user_id.id == self.env.uid or self.sh_responsible_tl_id.id == self.sh_employee_id.parent_id.id:
        if self.state == 'waiting':
            self.state = 'reject'
        

            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            if self.sh_employee_id and self.sh_responsible_tl_id and self.user_id.id != self.sh_responsible_tl_id.user_id.id:
                
                if not self.env.context.get('multi_allocation_reject'):
                    self.env['user.push.notification'].push_notification(
                            [self.user_id,self.sh_employee_id.user_id],
                            'Assignment Rejected',
                            'Assignment of %s for project %s has been rejected by %s.'% (self.sh_employee_id.name,self.sh_project_id.name,self.env.user.name),
                            base_url+"/mail/view?model=sh.employee.task.allocation&res_id="+str(self.id),
                            'sh.employee.task.allocation', 
                            self.id,
                            'assignment'
                        )
        # else:
        #     raise UserError(_('You cannot reject allocation of other TL employee.'))
    

    def action_cancel_allocation_following(self):
        '''To Cancel all following allocation request'''
        for rec in self:
            if rec.allocation_master_id  and rec.allocation_master_id.allocation_lines:
                for each_allocation in rec.allocation_master_id.allocation_lines:
                    if each_allocation.from_date >= rec.from_date:
                        each_allocation.with_context({'multi_allocation_cancel':True}).action_cancel_allocation()

            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            self.env['user.push.notification'].push_notification(
                        [rec.sh_employee_id.user_id,rec.sh_responsible_tl_id.user_id],
                        'Assignment Cancelled',
                        'Assignment of %s for project %s has been Cancelled by %s.'% (rec.sh_employee_id.name,rec.sh_project_id.name,rec.env.user.name),
                        base_url+"/mail/view?model=sh.employee.task.allocation&res_id="+str(rec.id),
                        'sh.employee.task.allocation', 
                        rec.id,
                        'assignment'
                    )

    def action_cancel_allocation(self):
        '''To Cancel allocation request'''
        self.state = 'cancel'

        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        if self.sh_employee_id and self.sh_responsible_tl_id and self.user_id.id != self.sh_responsible_tl_id.user_id.id:
            if not self.env.context.get('multi_allocation_cancel'):
                self.env['user.push.notification'].push_notification(
                        [self.sh_employee_id.user_id,self.sh_responsible_tl_id.user_id],
                        'Assignment Cancelled',
                        'Assignment of %s for project %s has been Cancelled by %s.'% (self.sh_employee_id.name,self.sh_project_id.name,self.env.user.name),
                        base_url+"/mail/view?model=sh.employee.task.allocation&res_id="+str(self.id),
                        'sh.employee.task.allocation', 
                        self.id,
                        'assignment'
                    )

    def action_reset_draft(self):
        '''To Darft allocation request'''
        self.state = 'draft'
        return{
        'type': 'ir.actions.client',
        'tag': 'reload',
        }
    
    def action_waiting(self):
        '''To confirm allocation request'''
        
        if self.sh_employee_id and self.sh_responsible_tl_id and self.user_id.id == self.sh_responsible_tl_id.user_id.id:
            self.state = 'done'
        else:
            self.state = 'waiting'

            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            if self.sh_employee_id and self.sh_responsible_tl_id and self.user_id.id != self.sh_responsible_tl_id.user_id.id:
                self.env['user.push.notification'].push_notification(
                        self.sh_responsible_tl_id.user_id,
                        'Assignment Confirmed',
                        'New Assignment request of %s for project %s is created by %s.'% (self.sh_employee_id.name, self.sh_project_id.name, self.user_id.name),
                        base_url+"/mail/view?model=sh.employee.task.allocation&res_id="+str(self.id),
                        'sh.employee.task.allocation', 
                        self.id,
                        'assignment'
                    )
                
        return{
        'type': 'ir.actions.client',
        'tag': 'reload',
        }
