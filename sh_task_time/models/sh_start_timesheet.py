# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_
from datetime import datetime 
from odoo.exceptions import UserError
from datetime import datetime,timedelta, date
from odoo.http import request

class TimesheetEntry(models.Model):
    _name = 'sh.start.timesheet'
    _description = 'Timesheet Start'

    def _get_employee(self):
        employee = self.env['hr.employee'].sudo().search([('user_id','=',self.env.user.id)],limit =1)
        if employee:
            return employee
        
    project_id = fields.Many2one('project.project',string="Project")
    task_id = fields.Many2one('project.task',string="Task",domain="[('project_id','=',project_id)]")
    start_date = fields.Datetime("Start Date", default = fields.Datetime.now() , readonly=True)
    # employee_id = fields.Many2one('hr.employee',required=True)

    # new_changes
    employee_id = fields.Many2one('hr.employee',required=True,default=_get_employee)

    # NEW_CHANGES
    def button_start_task(self):
        if not self.employee_id:
            raise UserError("Only Employee can start task !")
        if not self.task_id:
            raise UserError("Please Select Task !")
        
        # ====================================================
        # VALIDATION IF YOU DON'T CHECK IN OR YOU ARE IN BREAK
        # ====================================================
    
        if self.employee_id:
            todays_date = date.today()
            todays_date_time = datetime.strftime(todays_date, "%Y-%m-%d 00:00:00")
            if 'is_remote_employee' in self.env['hr.employee']._fields and  not self.employee_id.is_remote_employee:
                attendance = self.env['hr.attendance'].sudo().search([('employee_id','=',self.employee_id.id),('check_in','>',todays_date_time),('check_in','!=',False),('check_out','=',False)])
                if not attendance:
                    raise UserError ("You can not start task as you have not check-in !")

                attendance = self.env['hr.attendance'].sudo().search([('employee_id','=',self.employee_id.id),('check_in','>',todays_date_time),('sh_break_start','!=',False),('sh_break_end','=',False)])
                if attendance:
                    raise UserError ("You can not start task as you have not end break !")
        self.task_id.action_task_start()

        # reload_fix
        self.env['bus.bus']._sendone(self.env.user.partner_id, 
            'sh.timer.render', {})

        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'reload',
        # }


    # @api.model
    # def button_start_task(self):

    #     employee = self.env['hr.employee'].sudo().search([('user_id','=',self.env.user.id)],limit =1)
    #     if employee:
    #         todays_date = date.today()
    #         todays_date_time = datetime.strftime(todays_date, "%Y-%m-%d 00:00:00")
    #         if 'is_remote_employee' in self.env['hr.employee']._fields and  not employee.is_remote_employee:
    #             attendance = self.env['hr.attendance'].sudo().search([('employee_id','=',employee.id),('check_in','>',todays_date_time),('check_in','!=',False),('check_out','=',False)])
    #             if not attendance:
    #                 raise UserError ("You can not start task as you have not check-in !")

    #             attendance = self.env['hr.attendance'].sudo().search([('employee_id','=',employee.id),('check_in','>',todays_date_time),('sh_break_start','!=',False),('sh_break_end','=',False)])
    #             if attendance:
    #                 raise UserError ("You can not start task as you have not end break !")
        
    #     responsible_users = self.get_all_responsible_users()
    #     # Create and Update Temporary Task
    #     domain = [('is_temp_task', '=', True),('name', '=', 'Temporary 1')]
    #     find_task = self.env['project.task'].sudo().search(domain)
    #     if find_task:
    #         temp_task = find_task
    #         find_task.sudo().write({
    #             'user_ids' : [(6,0,responsible_users)]
    #         })
    #     else:
    #         temp_project = self.create_temp_project(responsible_users)
    #         task_vals = {
    #             'name' : 'Temporary 1',
    #             'is_temp_task' : True,
    #             'user_ids' : [(6,0,responsible_users)],
    #             'project_id' : temp_project.id
    #         }
    #         create_temp_task = self.env['project.task'].sudo().create(task_vals)
    #         temp_task = create_temp_task
    #     temp_task.action_task_start()

    #     return {
    #         'type': 'ir.actions.client',
    #         'tag': 'reload',
    #     } 

    @api.model
    def button_pause_task(self):
        responsible_users = self.get_all_responsible_users()
        domain = [('is_temp_task', '=', True),('name', '=', 'Temporary 2')]
        find_task = self.env['project.task'].sudo().search(domain)
        if find_task:
            temp_task = find_task
            find_task.sudo().write({
                'user_ids' : [(6,0,responsible_users)]
            })
        else:
            temp_project = self.create_temp_project(responsible_users)
            task_vals = {
                'name' : 'Temporary 2',
                'is_temp_task' : True,
                'user_ids' : [(6,0,responsible_users)],
                'project_id' : temp_project.id
            }
            create_temp_task = self.env['project.task'].sudo().create(task_vals)
            temp_task = create_temp_task
        temp_task.action_task_pause()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        } 

    def get_all_responsible_users(self):        
        employees = self.env['hr.employee'].sudo().search([])
        user_list = [employee.user_id.id for employee in employees if employee.user_id]
        return user_list

    def create_temp_project(self,responsible_users):
        # Create and Update Temporary Project
        domain = [('is_temp_project', '=', True)]
        find_project = self.env['project.project'].sudo().search(domain)
        if find_project:
            temp_project = find_project
            find_project.sudo().write({
                'responsible_user_ids': [(6,0,responsible_users)],
            })
        else:
            project_vals = {
                'name' : 'Temporary',
                'responsible_user_ids': [(6,0,responsible_users)],
                'is_temp_project' : True
            }
            create_temp_project = self.env['project.project'].sudo().create(project_vals)
            temp_project = create_temp_project
        return temp_project