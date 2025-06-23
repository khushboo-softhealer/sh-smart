# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime,date, timedelta

class ShEmployeeTaskAllocationWizard(models.Model):
    _name = 'sh.employee.task.allocation.wizard'
    _description = 'Employee Task Allocation Wizard'

    sh_department_id = fields.Many2one('hr.department', string='Department',)
    sh_employee_id = fields.Many2one('hr.employee', string='Assigned To',)
    sh_responsible_tl_id = fields.Many2one('hr.employee',string='Responsible TL',readonly=True)
    sh_responsible_tl_ids = fields.Many2many('hr.employee',string='All Approvers',tracking=True)
    user_id = fields.Many2one('res.users',string='Requested User' ,domain=[('share','=',False)], default=lambda self:self.env.user)
    sh_priority = fields.Selection([
                            ('very_low', 'Very Low'),
                            ('low', 'Low'),
                            ('medium', 'Medium'),
                            ('high', 'High'),
                            ('very_high', 'Very High'),
                        ], string='Priority', default="medium")
    
    sh_project_id = fields.Many2one('project.project', string='Project')
    sh_task_id = fields.Many2one('project.task', string='Task',)
    from_date = fields.Date('From Date',default=lambda self: fields.Date.context_today(self))
    to_date = fields.Date('To Date',default=lambda self: fields.Date.context_today(self))
    allocated_hours = fields.Float('Allocated Hours')
    existing_allocation_ids = fields.Many2many('sh.employee.task.allocation', relation="emp_task_alloc_emp_task_alloc_wizard_rel", compute="_compute_existing_allocation")
    sh_remarks = fields.Text('Remarks')
    allocation_lines = fields.One2many('sh.employee.task.allocation','allocation_master_id',string="Allcation Lines")

    def _get_all_coach(self, coach, sh_responsible_tl_ids =[]):
        sh_responsible_tl_ids.append(coach.id)
        if coach.coach_id and coach != coach.coach_id:
            sh_responsible_tl_ids = self._get_all_coach(coach.coach_id,sh_responsible_tl_ids)

    def _valid_field_parameter(self, field, name):
        # allow tracking on models inheriting from 'mail.thread'
        return name == 'tracking' or super()._valid_field_parameter(field, name)

    @api.onchange('sh_employee_id','from_date')
    def onchange_sh_employee_id(self):
        '''Sets Responsible TL of employee.'''
        self.sh_responsible_tl_id = False
        if self.sh_employee_id and self.sh_employee_id.user_id and self.sh_employee_id.user_id.has_group('sh_project_task_base.group_project_officer'):
            self.sh_department_id = False
            self.sh_responsible_tl_id = self.sh_employee_id.id
        elif self.sh_employee_id:
            self.sh_responsible_tl_id = self.sh_employee_id.coach_id.id
            self.sh_department_id = False

        sh_responsible_tl_ids = []
        if self.sh_employee_id.id and self.sh_employee_id.user_id.has_group('sh_project_task_base.group_project_officer') or self.sh_employee_id.user_id.has_group('sh_project_mgmt.group_project_task_create'):
            sh_responsible_tl_ids.append(self.sh_employee_id.id)
        
        if self.sh_employee_id.coach_id:
            self._get_all_coach(self.sh_employee_id.coach_id, sh_responsible_tl_ids)
            self.sh_responsible_tl_ids = [(6,0,sh_responsible_tl_ids)]
        
        
        if self.from_date and self.to_date and self.sh_employee_id:
            leave_domain = [
                ('employee_ids', 'in', [self.sh_employee_id.id]),
                ('state', 'not in', ['draft', 'refuse']),
                # ('request_date_from', '<=', self.from_date),
                # ('request_date_to', '>=', self.to_date),
                ('request_date_to', '>=', self.from_date),
                ('request_date_from', '<=', self.to_date),
            ]

            # Fetch all relevant leaves in a single search
            employee_leaves = self.env['hr.leave'].sudo().search(leave_domain)
            # Classify leave types
            for leave in employee_leaves:
                if leave.request_unit_half:
                    time = dict(leave._fields['request_date_from_period'].selection)
                    self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
                        'title': _("Warning"),
                        'sticky' : True,
                        'message': _(f'{self.sh_employee_id.name} is on Half Day Leave in {time.get(leave.request_date_from_period)}',)})
                elif leave.request_unit_hours:
                    from_time = dict(leave._fields['request_hour_from'].selection)
                    to_time = dict(leave._fields['request_hour_to'].selection)
                    self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
                        'title': _("Warning"),
                        'sticky' : True,
                        'message': _(f'{self.sh_employee_id.name} is on Leave From {from_time.get(leave.request_hour_from)} To {to_time.get(leave.request_hour_to)} ',)})
                else:
                    self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
                        'title': _("Warning"),
                        'sticky' : True,
                        'message': _(f'{self.sh_employee_id.name} is on Full Day Leave on {leave.request_date_from} to {leave.request_date_to}')})
        
    @api.onchange('sh_responsible_tl_id')
    def onchange_responsible_tl_id(self):
        if self.sh_responsible_tl_id or self.sh_employee_id:
            self.sh_department_id = False
    
    @api.onchange('sh_project_id')
    def onchange_project_id(self):
        '''Adds domain of selected project in sh_task_id m2o.'''
        if self.sh_project_id:
            domain = [('project_id', '=', self.sh_project_id.id)]
            if self.sh_task_id.project_id.id != self.sh_project_id.id:
                self.sh_task_id = False
        else:
            domain = []
        return {'domain': {'sh_task_id': domain}}

    @api.onchange('sh_task_id')
    def onchange_sh_task_id(self):
        '''Sets sh_project_id of task when sh_task_id is selected.'''
        if self.sh_task_id and self.sh_task_id.project_id:
            self.sh_project_id = self.sh_task_id.project_id.id
    
    @api.depends('sh_employee_id','from_date','from_date')
    def _compute_existing_allocation(self):
        '''Computes existing allocations of employee based on from date and to date selected.'''
        
        for rec in self:
            rec.existing_allocation_ids = False
            domain = []
            if rec.sh_employee_id:
                domain.append(('sh_employee_id','=',rec.sh_employee_id.id))
                domain.append(('state','in',['done','waiting']))
                
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

    def create_emp_task_allocation(self):
        '''Create Employee Task Allocation record.'''
        
        if not any(self.sh_department_id or self.sh_employee_id or self.sh_responsible_tl_id):
            raise UserError(_('You must have to select either Assigned To or Responsible TL or Depratment.'))
        
        if self.from_date < date.today() or self.to_date < date.today():
            raise UserError(_('You cannot allocate task for back date.'))
        
        # if self.allocated_hours <= 0 or self.allocated_hours > 8.5:
        #     raise UserError(_('Allocated hours must be greater than zero and less than 8.5 hours.'))
        
        # if self.sh_employee_id:
        #     existing_allocated_hours = 0
        #     if self.existing_allocation_ids:
        #         existing_allocated_hours = sum(self.existing_allocation_ids.mapped('allocated_hours'))
            
        #     total_hours = existing_allocated_hours + self.allocated_hours

        #     if total_hours > 8.5:
        #         raise UserError(_(f'{self.sh_employee_id.name} is not available for demanding hours from D. {self.from_date} to D. {self.to_date}.'))

        start_dt = self.from_date
        end_dt = self.to_date
        # difference between current and previous date
        delta = timedelta(days=1)

        # store the dates between two dates in a list
        dates = []

        while start_dt <= end_dt:
            # add current date to list by converting  it to iso format
            dates.append(start_dt.isoformat())
            # increment start date by timedelta
            start_dt += delta

        print('Dates between', start_dt, 'and', end_dt)
        print(dates)

        allocation_id = False
        for allocation_date in dates:
            vals = {
                'user_id' : self.user_id.id,
                'sh_project_id' : self.sh_project_id.id,
                'sh_task_id' : self.sh_task_id.id,
                'sh_priority' : self.sh_priority or 'medium',
                'from_date' :allocation_date,
                'to_date' :allocation_date,
                'allocated_hours' : self.allocated_hours,
                'sh_remarks' : self.sh_remarks,
                'allocation_master_id':self.id,
                'parent_from_date':self.from_date,
                'parent_to_date':self.to_date
            }
            
            if self.sh_employee_id :
                vals.update({
                    'sh_employee_id' : self.sh_employee_id.id,
                })
            if self.sh_responsible_tl_id:
                vals.update({
                    'sh_responsible_tl_id' : self.sh_responsible_tl_id.id,
                })
            if self.sh_responsible_tl_ids:
                vals.update({
                    'sh_responsible_tl_ids' : [(6,0,self.sh_responsible_tl_ids.ids)],
                })
                
            # if self.sh_employee_id and self.sh_responsible_tl_id and self.sh_responsible_tl_ids:
            #     vals.update({
                    
            #         'sh_responsible_tl_id' : self.sh_responsible_tl_id.id,
            #         'sh_responsible_tl_ids':[(6,0,self.sh_responsible_tl_ids.ids)],
            #         'sh_department_id' : False,
            #     })
            # elif not self.sh_employee_id and self.sh_responsible_tl_id:
            #     vals.update({
            #         'sh_employee_id' : False,
            #         'sh_responsible_tl_id' : self.sh_responsible_tl_id.id or False,
            #         'sh_responsible_tl_ids':[(6,0,self.sh_responsible_tl_ids.ids)],
            #         'sh_department_id' : False,
            #     })
            # elif self.sh_department_id:
            #     vals.update({
            #         'sh_department_id' : self.sh_department_id.id,
            #     })
            
            # when responsible create allocation for their team member
            if self.sh_employee_id and self.sh_responsible_tl_id and self.user_id.id == self.sh_responsible_tl_id.user_id.id:
                vals.update({'state' : 'done'})

                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                self.env['user.push.notification'].push_notification(
                        [self.sh_employee_id.user_id],
                        'New Assignment Created',
                        'New Assignment request of %s for project %s is created and approved by %s.'% (self.sh_employee_id.name, self.sh_project_id.name, self.user_id.name),
                        base_url+"/mail/view?model=sh.employee.task.allocation&res_id="+str(self.id),
                        'sh.employee.task.allocation', 
                        self.id,
                        'assignment'
                    )
            
            if not allocation_id:
                allocation_id = self.env['sh.employee.task.allocation'].sudo().create(vals)
            else:
                self.env['sh.employee.task.allocation'].sudo().create(vals)
        
        if allocation_id:
            if allocation_id.sh_employee_id and allocation_id.state == 'done':
                # Add employee in project and task if set while approved
                if allocation_id.sh_employee_id:
                    if allocation_id.sh_project_id:
                        allocation_id.sh_project_id.sudo().write({'responsible_user_ids':[(4,allocation_id.sh_employee_id.user_id.id)]})
                    if allocation_id.sh_task_id:
                        allocation_id.sh_task_id.sudo().write({'user_ids':[(4,allocation_id.sh_employee_id.user_id.id)]})


            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            if self.sh_employee_id and self.sh_responsible_tl_id and self.user_id.id != self.sh_responsible_tl_id.user_id.id:
                self.env['user.push.notification'].push_notification(
                        [allocation_id.sh_employee_id.user_id,allocation_id.sh_responsible_tl_id.user_id],
                        'New Assignment Created',
                        'New Assignment request of %s for project %s is created by %s.'% (allocation_id.sh_employee_id.name, allocation_id.sh_project_id.name, allocation_id.user_id.name),
                        base_url+"/mail/view?model=sh.employee.task.allocation&res_id="+str(allocation_id.id),
                        'sh.employee.task.allocation', 
                        allocation_id.id,
                        'assignment'
                    )
        
            # elif not self.sh_employee_id and self.sh_responsible_tl_id:
            #     self.env['user.push.notification'].push_notification(
            #             allocation_id.sh_responsible_tl_id.user_id,
            #             'Request For Availability of your Employee',
            #             'Assignment request of your available employee for project %s is created by %s.'% (allocation_id.sh_project_id.name, allocation_id.user_id.name),
            #             base_url+"/mail/view?model=sh.employee.task.allocation&res_id="+str(allocation_id.id),
            #             'sh.employee.task.allocation', 
            #             allocation_id.id,
            #             'assignment'
            #         )
            # elif self.sh_department_id and not self.sh_employee_id and not self.sh_responsible_tl_id:
            #     dept_emp_ids = self.env['hr.employee'].sudo().search([('department_id','=',self.sh_department_id.id)])
            #     dept_tl_ids = []
            #     if dept_emp_ids:
            #         for emp in dept_emp_ids:
            #             if emp.user_id.has_group('sh_project_task_base.group_project_officer'):
            #                 dept_tl_ids.append(emp.user_id)
                    
            #         if dept_tl_ids:
            #             self.env['user.push.notification'].push_notification(
            #                     dept_tl_ids,
            #                     'Request For Availability of your Employee',
            #                     'Assignment request of your available employee for project %s is created by %s.'% (allocation_id.sh_project_id.name, allocation_id.user_id.name),
            #                     base_url+"/mail/view?model=sh.employee.task.allocation&res_id="+str(allocation_id.id),
            #                     'sh.employee.task.allocation', 
            #                     allocation_id.id,
            #                     'assignment'
            #                 )
