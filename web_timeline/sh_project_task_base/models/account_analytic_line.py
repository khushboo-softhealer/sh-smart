# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime
import math
from odoo.exceptions import UserError


class AccountAnalyticLine(models.Model):
    _name = 'account.analytic.line'
    _inherit = ['account.analytic.line', 'mail.thread']

    start_date = fields.Datetime("Start Date", readonly=True)
    end_date = fields.Datetime("End Date", readonly=True)
    unit_amount_invoice = fields.Float("Invoice  Quantity", tracking=True)

    name = fields.Char('Description', required=True, tracking=True)
    date = fields.Date('Date', required=True, index=True, default=fields.Date.context_today, tracking=True)
    amount = fields.Monetary('Amount', required=True, default=0.0, tracking=True)
    unit_amount = fields.Float('Quantity', default=0.0, tracking=True)
    task_id = fields.Many2one('project.task', 'Task', index=True, tracking=True)
    project_id = fields.Many2one('project.project', 'Project', domain=[('allow_timesheets', '=', True)], tracking=True)
    employee_id = fields.Many2one('hr.employee', "Employee", tracking=True)
    temp_task = fields.Boolean("Temp Task",related="task_id.is_temp_task")
    
    @api.onchange('unit_amount')
    def onchange_unit_amount_timesheet(self):
        for rec in self:
            if not rec.task_id.not_billable:
                rec.unit_amount_invoice = rec.unit_amount
            else:
                rec.unit_amount_invoice = 0

    @api.model_create_multi
    def create(self, vals_list):
        # ==========================================================================
        # WRITE CODE FOR EMPLOYEE CAN NOT CREATE TIMESHEET MORE THAN WORKING HOURS
        # ==========================================================================
        
        # for vals in vals_list:
        #     if vals.get('employee_id'):
        #         find_employee=self.env['hr.employee'].browse(vals.get('employee_id'))

        #         if find_employee and not find_employee.is_remote_employee and vals.get('unit_amount'):
                    
        #             #  ---------- CALCULATE WORKING HOUR FROM CLOSE ATTENDANCE ----------

        #             if vals.get('date'):
        #                 if isinstance(vals.get('date'), str):
        #                     vals_date=datetime.strptime(vals.get('date'), '%Y-%m-%d').date()
        #                 else:
        #                     vals_date = vals.get('date')

        #             self._cr.execute('''select id,att_duration from hr_attendance where employee_id = %s and check_in :: date >= %s and check_out :: date <= %s  ''',
        #                 [vals.get('employee_id'),vals.get('date'),vals.get('date')])
        #             total_working = self._cr.dictfetchall()
        #             total_hour=sum([day.get('att_duration') for day in total_working])
        #             #  ---------- CALCULATE WORKING HOUR FROM RUNNING ATTENDANCE ----------
                    
        #             self._cr.execute('''select id,check_in from hr_attendance where employee_id = %s and check_in :: date = %s and check_out is NULL  ''',
        #                 [vals.get('employee_id'),vals.get('date')])
        #             running_attendance = self._cr.dictfetchall()
        #             running_attendance_duration=0
        #             if vals_date == datetime.now().date() and running_attendance:
        #                 running_attendance_duration=datetime.now()-running_attendance[0].get('check_in')
        #                 running_attendance_duration=math.ceil(running_attendance_duration.total_seconds()/36)/100
        #                 total_hour+=running_attendance_duration

        #             #  ---------- CALCUALATE TIMESHEET DURATION WITHOUT TEMPARARY TASK ----------
        #             current_timesheet=vals.get('unit_amount')
        #             self._cr.execute('''select id from project_task where is_temp_task=True ''')
        #             temp_task = self._cr.dictfetchall()   
        #             if temp_task:    
        #                 temp_task=self.env['project.task'].browse([r['id'] for r in temp_task])

        #                 self._cr.execute('''select id,unit_amount from account_analytic_line where employee_id = %s and date=%s and task_id not in %s ''',
        #                     [vals.get('employee_id'),vals.get('date'),tuple(temp_task.ids)])
        #                 timesheets = self._cr.dictfetchall()

        #                 # --------------- IF CURRENT TASK IS TEMP THEN NOT COUNT CURRENT TIMESHEET -------

        #                 if vals.get('task_id'):
        #                     task=self.env['project.task'].browse(vals.get('task_id'))
        #                     if task and task.id in temp_task.ids:
        #                         current_timesheet=0   

        #             else:
        #                 self._cr.execute('''select id,unit_amount from account_analytic_line where employee_id = %s and date=%s ''',
        #                     [vals.get('employee_id'),vals.get('date')])
        #                 timesheets = self._cr.dictfetchall()

        #             timesheet_amount=sum([timesheet.get('unit_amount') for timesheet in timesheets])  

                    

                    #  ---------- ADD VALIDATION FOR TIMESHEET HOUR IS NOT MORE THAN WORKING HOURS ----------
                    # if round(timesheet_amount+current_timesheet,2) > total_hour :
                    #     raise UserError("You are not allowed create timesheet more than working hours..")        
            
        
        res = super(AccountAnalyticLine, self).create(vals_list)
        
        for vals in vals_list:
            context_by_pass_done_validation = self.env.context.get('by_pass_done_validation',False)

            if not context_by_pass_done_validation and 'manual_create' in self.env.context and self.env.context.get('manual_create')==1 and res.task_id and res.project_id and not res.project_id.is_task_editable_in_done_stage and self.env.user.company_id.timesheet_restricted_task_stage_ids and res.task_id.stage_id.id in self.env.user.company_id.timesheet_restricted_task_stage_ids.ids:
                raise ValidationError(f"You can not add/edit timesheet in Task if task is in {res.task_id.stage_id.name} stage.")
        
            if res.task_id.estimated_internal_hrs > 0.0 and res.task_id.effective_hours > res.task_id.estimated_internal_hrs:
                # user_list=[]
                user_list = res.task_id.user_ids
                # user_list.append(res.task_id.user_ids.ids)
                lead_user_list = []
                for user in user_list:
                    user_obj = self.env['res.users'].sudo().browse(user.id)
                    if user_obj.has_group('sh_project_task_base.group_project_officer'):
                        lead_user_list.append(user_obj)
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                self.env['user.push.notification'].push_notification(lead_user_list,'Timesheet Hours more then Estimated hours',
                res.task_id.name,
                                                                base_url+"/mail/view?model=project.task&res_id="+str(res.task_id.id),
                                                                'project.task',res.task_id.id,'project')

        return res
    
    # ======== for sh_timesheet_custom ============
    def write(self, vals):
        # ==========================================================================
        # WRITE CODE FOR EMPLOYEE CAN NOT CREATE TIMESHEET MORE THAN WORKING HOURS
        # ==========================================================================
        # for rec in self:
            #  ---------- GET DATA FROM VALS IF EXIST OTHER WISE TAKEN FROM RECORD ----------
            
            # if 'unit_amount' in vals:
            #     unit_amount=vals.get('unit_amount')
            # else:
            #     unit_amount=rec.unit_amount

            # if 'date' in vals:
            #     vals_date=datetime.strptime(vals.get('date'), '%Y-%m-%d').date()
            #     timesheet_date=vals_date

            # if vals.get('date'):
            #     if isinstance(vals.get('date'), str):
            #         timesheet_date=datetime.strptime(vals.get('date'), '%Y-%m-%d').date()
            #     else:
            #         timesheet_date = vals.get('date')

            # else:
            #     timesheet_date=rec.date
            # if 'employee_id' in vals:
            #     find_employee=self.env['hr.employee'].browse(vals.get('employee_id'))       
            #     employee_id=find_employee.id
            # else:
            #     employee_id=rec.employee_id
            # if employee_id:
            #     if employee_id and not employee_id.is_remote_employee:
                    
            #         #  ---------- CALCULATE WORKING HOUR FROM CLOSE ATTENDANCE ----------
                    
            #         self._cr.execute('''select id,att_duration from hr_attendance where employee_id = %s and check_in :: date >= %s and check_out :: date <= %s  ''',
            #             [employee_id.id,timesheet_date,timesheet_date])
            #         total_working = self._cr.dictfetchall()
            #         total_hour=sum([day.get('att_duration') for day in total_working])
                    
            #         #  ---------- CALCULATE WORKING HOUR FROM RUNNING ATTENDANCE ----------
                    
            #         self._cr.execute('''select id,check_in from hr_attendance where employee_id = %s and check_in :: date = %s and check_out is NULL  ''',
            #             [employee_id.id,timesheet_date])
            #         running_attendance = self._cr.dictfetchall()
            #         running_attendance_duration=0
            #         if timesheet_date == datetime.now().date() and running_attendance:
            #             running_attendance_duration=datetime.now()-running_attendance[0].get('check_in')
            #             running_attendance_duration=math.ceil(running_attendance_duration.total_seconds()/36)/100
            #             total_hour+=running_attendance_duration
            #         #  ---------- CALCUALATE TIMESHEET DURATION WITHOUT TEMPARARY TASK ----------
                    
            #         self._cr.execute('''select id from project_task where is_temp_task=True ''')
            #         temp_task = self._cr.dictfetchall()   
            #         if temp_task:    
            #             temp_task=self.env['project.task'].browse([r['id'] for r in temp_task])

            #             self._cr.execute('''select id,unit_amount from account_analytic_line where employee_id = %s and date=%s and task_id not in %s  and id!=%s ''',
            #                 [employee_id.id,timesheet_date,tuple(temp_task.ids),rec.id])
            #             timesheets = self._cr.dictfetchall()


            #             # --------------- IF CURRENT TASK IS TEMP THEN NOT COUNT CURRENT TIMESHEET -------
            #             if vals.get('task_id'):
            #                 task=self.env['project.task'].browse(vals.get('task_id'))
            #                 if task and task.id in temp_task.ids:
            #                     unit_amount=0
            #             elif rec.task_id and rec.task_id.id in temp_task.ids:
            #                 unit_amount=0    

            #         else:
            #             self._cr.execute('''select id,unit_amount from account_analytic_line where employee_id = %s and date=%s and id!=%s ''',
            #                 [employee_id.id,timesheet_date,rec.id])
            #             timesheets = self._cr.dictfetchall()
                        
            #         timesheet_amount=sum([timesheet.get('unit_amount') for timesheet in timesheets]) 
                    
                    #  ---------- ADD VALIDATION FOR TIMESHEET HOUR IS NOT MORE THAN WORKING HOURS ----------
                    # if unit_amount and round(timesheet_amount+unit_amount,2) > total_hour :
                    #     raise UserError("You are not allowed create timesheet more than working hours..")                

            for rec in self:
                # Prevent timesheet on closed projects
                if rec.project_id and rec.env.user.company_id.close_project_stage_ids and rec.project_id.stage_id.id in rec.env.user.company_id.close_project_stage_ids.ids:
                    raise ValidationError("You can not add timesheet in Closed/Done Project. Please contact your project manager.")

                context_by_pass_done_validation = self.env.context.get('by_pass_done_validation',False)
                if not context_by_pass_done_validation and 'manual_create' in self.env.context and self.env.context.get('manual_create')==1 and rec.task_id and rec.project_id and not rec.project_id.is_task_editable_in_done_stage and rec.env.user.company_id.timesheet_restricted_task_stage_ids and rec.task_id.stage_id.id in rec.env.user.company_id.timesheet_restricted_task_stage_ids.ids:
                    raise ValidationError(f"You can not add/edit timesheet in Task if task is in {rec.task_id.stage_id.name} stage.")
        

                # SQL to update unit_amount_invoice if task is not billable
                if rec.task_id and rec.task_id.not_billable:
                    query = """
                        UPDATE account_analytic_line
                        SET unit_amount_invoice = %s
                        WHERE id = %s
                    """
                    self.env.cr.execute(query, (0.0, rec.id))
                    # Remove from vals so it's not written again
                    vals.pop('unit_amount_invoice', None)
                    
                return super(AccountAnalyticLine, rec).write(vals)




    def manually_transfer_timehseet(self):
        if self.date < fields.Date.today():
            raise ValidationError("You can only transfer today's timesheets.")

        ticket_id = False
        if self.ticket_id:
            ticket_id = self.ticket_id.id

        return {
            'name': 'Transfer Timesheet',
            'type': 'ir.actions.act_window',
            'res_model': 'sh.transfer.timesheet',
            'view_type': 'form',
            'view_mode': 'form',
            'domain': [('employee_id', '=', self.id)],
            'target': 'new',
            'context' : {
                'analytic_id' : self.id,
                'ticket_id': ticket_id
            }
        }
