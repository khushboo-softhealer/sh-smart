# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api, _
from datetime import datetime,date
# from doc._extensions.pyjsparser.parser import true
from odoo.exceptions import UserError, ValidationError
from odoo.addons.resource.models.resource import float_to_time, HOURS_PER_DAY
from datetime import timedelta

class TaskTimeAccountLine(models.Model):
    _name = 'task.time.account.line'
    _description = 'Task Time Account Line'

    # @api.multi
    # @api.model
    # def _get_default_start_time(self):
    #     if self.env.user.support_task_id:
    #         return self.env.user.support_start_time
    #     elif self.env.user.task_id:            
    #         return self.env.user.start_time


    # NEW_CHANGES
    @api.model
    def _get_default_start_time(self):
        active_model = self.env.context.get('active_model')
        if active_model == 'sh.pause.task.entry':
            active_id = self.env.context.get('active_id')
            entry_search = self.env['sh.pause.task.entry'].search(
                [('id', '=', active_id)], limit=1)
            return entry_search.start_date

        if self.env.user.active_running_task_id:            
            return self.env.user.active_running_task_id.start_date

    # @api.multi
    # @api.model
    # def _get_default_end_time(self):
    #     return datetime.now()
    
    # NEW_CHANGES
    @api.model
    def _get_default_end_time(self):
        active_model = self.env.context.get('active_model')
        if active_model == 'sh.pause.task.entry':
            active_id = self.env.context.get('active_id')
            entry_search = self.env['sh.pause.task.entry'].search(
                [('id', '=', active_id)], limit=1)
            return entry_search.sh_pause_time
        else:
            return datetime.now()


    # @api.multi
#     @api.model
#     def _get_default_duration(self):
#         active_model = self.env.context.get('active_model')
#         if active_model == 'project.task':
#             active_id = self.env.context.get('active_id')
# #             if active_id:
#             if self.env.user and self.env.user.support_task_id:
#                 diff = fields.Datetime.from_string(
#                     fields.Datetime.now()) - fields.Datetime.from_string(
#                         self.env.user.support_start_time)
#                 if diff:
#                     duration = float(diff.days) * 24 + (float(diff.seconds) /
#                                                         3600)
#                     return round(duration, 2)
#             elif self.env.user and self.env.user.task_id:
#                 task_search = self.env['project.task'].search(
#                     [('id', '=', active_id)], limit=1)
#                 diff = fields.Datetime.from_string(
#                     fields.Datetime.now()) - fields.Datetime.from_string(
#                         self.env.user.start_time)
#                 if diff:
#                     duration = float(diff.days) * 24 + (float(diff.seconds) /3600)
#                     if self.env.user.support_hours:
#                         duration = duration - self.env.user.support_hours
#                     return round(duration, 2)

#         if active_model == 'sh.helpdesk.ticket':
#             active_id = self.env.context.get('active_id')
#             ticket_id = self.env[active_model].sudo().browse(active_id)

#             if ticket_id:
#                 if self.env.user and self.env.user.support_task_id:
#                     diff = fields.Datetime.from_string(
#                         fields.Datetime.now()) - fields.Datetime.from_string(
#                             self.env.user.support_start_time)
#                     if diff:
#                         duration = float(diff.days) * 24 + (float(diff.seconds) /
#                                                             3600)
#                         return round(duration, 2)
#                 elif self.env.user and self.env.user.task_id:
#                     task_search = self.env['project.task'].search(
#                         [('id', '=', ticket_id.sh_ticket_task_id.id)], limit=1)
#                     diff = fields.Datetime.from_string(
#                         fields.Datetime.now()) - fields.Datetime.from_string(
#                             self.env.user.start_time)
#                     if diff:
#                         duration = float(diff.days) * 24 + (float(diff.seconds) /
#                                                             3600)
#                         if self.env.user.support_hours:
#                             duration = duration - self.env.user.support_hours
#                         return round(duration, 2)


    # NEW_CHANGES
    @api.model
    def _get_default_duration(self):
        active_model = self.env.context.get('active_model')

        if active_model == 'sh.pause.task.entry':
            active_id = self.env.context.get('active_id')
            entry_search = self.env['sh.pause.task.entry'].search(
                [('id', '=', active_id)], limit=1)

            if entry_search:
                if entry_search.difference_time_float:
                    return entry_search.difference_time_float

                # diff = fields.Datetime.from_string(entry_search.sh_pause_time) - fields.Datetime.from_string(entry_search.start_date)
                # if diff:
                #     duration = float(diff.days) * 24 + \
                #         (float(diff.seconds) / 3600)
                #     return round(duration, 2)

        if active_model == 'project.task':
            active_id = self.env.context.get('active_id')
            if active_id:
                task_search = self.env['project.task'].search(
                    [('id', '=', active_id)], limit=1)
                diff = fields.Datetime.from_string(fields.Datetime.now(
                )) - fields.Datetime.from_string(self.env.user.start_time)

                # ===========================================
                # if return amount from char field
                # ============================================
                # if diff:
                #     if self.env.user.active_running_task_id:
                #         if self.env.user.sudo().active_running_task_id.difference_time:
                #             old_difference_time=self.env.user.sudo().active_running_task_id.difference_time
                #             if old_difference_time:
                #                 conveted_type = datetime.strptime(old_difference_time,'%H:%M:%S')
                #                 diff=(conveted_type + diff).time()

                #     total_seconds = float(diff.hour * 3600) + float(diff.minute * 60) + float(diff.second + diff.microsecond) / 1e6
                #     return (total_seconds/ 3600.0)
                # ============================================

                if diff:
                    if self.env.user.active_running_task_id:
                        if self.env.user.sudo().active_running_task_id.difference_time_float:
                            old_difference_time=self.env.user.sudo().active_running_task_id.difference_time_float
                            return (diff.total_seconds() / 3600) + old_difference_time

                # if not old difference time
                if diff:
                    duration = float(diff.days) * 24 + \
                        (float(diff.seconds) / 3600)
                    return round(duration, 2)


        # REMAINING TO CHANGE AS PER NEW FLOW
        
        # if active_model == 'sh.helpdesk.ticket':
        #     active_id = self.env.context.get('active_id')
        #     ticket_id = self.env[active_model].sudo().browse(active_id)

        #     if ticket_id:
        #         if self.env.user and self.env.user.support_task_id:
        #             diff = fields.Datetime.from_string(
        #                 fields.Datetime.now()) - fields.Datetime.from_string(
        #                     self.env.user.support_start_time)
        #             if diff:
        #                 duration = float(diff.days) * 24 + (float(diff.seconds) /
        #                                                     3600)
        #                 return round(duration, 2)
        #         elif self.env.user and self.env.user.task_id:
        #             task_search = self.env['project.task'].search(
        #                 [('id', '=', ticket_id.sh_ticket_task_id.id)], limit=1)
        #             diff = fields.Datetime.from_string(
        #                 fields.Datetime.now()) - fields.Datetime.from_string(
        #                     self.env.user.start_time)
        #             if diff:
        #                 duration = float(diff.days) * 24 + (float(diff.seconds) /
        #                                                     3600)
        #                 if self.env.user.support_hours:
        #                     duration = duration - self.env.user.support_hours
        #                 return round(duration, 2)

    # @api.multi
    @api.model
    def _get_default_project(self):

        # when end from pause task entry
        active_model = self.env.context.get('active_model')
        if active_model == 'sh.pause.task.entry':
            active_id = self.env.context.get('active_id')
            entry_search = self.env['sh.pause.task.entry'].search(
                [('id', '=', active_id)], limit=1)

            if entry_search:
                if entry_search.task_id:
                    if entry_search.task_id.project_id:
                        return entry_search.task_id.project_id

        if self.env.user.support_task_id:
            return self.env.user.support_task_id.project_id.id
        elif self.env.user.task_id:
            return self.env.user.task_id.project_id.id
    
    # @api.multi
    @api.model
    def _get_default_task(self):

        # when end from pause task entry
        active_model = self.env.context.get('active_model')
        if active_model == 'sh.pause.task.entry':
            active_id = self.env.context.get('active_id')
            entry_search = self.env['sh.pause.task.entry'].search(
                [('id', '=', active_id)], limit=1)

            if entry_search:
                if entry_search.task_id:
                    if entry_search.task_id:
                        return entry_search.task_id

        if self.env.user.support_task_id:
            return self.env.user.support_task_id.id
        elif self.env.user.task_id:
            return self.env.user.task_id.id

      # @api.multi
    @api.model
    def _get_default_is_temporary(self):
        if self.env.user.support_task_id.is_temp_task:
            return True
        elif self.env.user.task_id.is_temp_task:
            return True
        return False
            
    name = fields.Text("Description", required=True)
    start_date = fields.Datetime("Start Date",
                                 default=_get_default_start_time,
                                 readonly=True)
    end_date = fields.Datetime("End Date",
                               default=_get_default_end_time,
                               readonly=True)
    duration = fields.Float("Duration (HH:MM)",
                            default=_get_default_duration,
                            readonly=True)
    
    project_id = fields.Many2one('project.project', 'Project',default=_get_default_project)
    task_id = fields.Many2one('project.task', 'Task',default=_get_default_task,domain=[('project_id', '=', 'project_id.id')])
    stage_id = fields.Many2one('project.task.type',related="task_id.stage_id",readonly=False)
    split_duration_1 = fields.Float("Split Duration 1",readonly=True,default=_get_default_duration)
    add_log_note = fields.Text("Log Note")
    split_add_log_note = fields.Text("Log Note")
    is_temporary = fields.Boolean("Is Temporary",default=_get_default_is_temporary)
    want_to_split = fields.Boolean("Want To Split Timesheet ?")
    split_name = fields.Text ()
    split_project_id = fields.Many2one('project.project')
    split_task_id = fields.Many2one("project.task")
    split_duration_2 = fields.Float("Split Duration 2")
    split_stage_id = fields.Many2one('project.task.type',readonly=False)

    # temporary for remove dependency helpdesk ticket

    # ticket_id = fields.Many2one('sh.helpdesk.ticket',string="Ticket No")

    # @api.onchange('split_duration_1')
    # def split_duration_1_change(self):
    #     if self.split_duration_1:
    #         self.split_duration_2 = self.duration - self.split_duration_1

    @api.onchange('split_duration_2')
    def split_duration_2_change(self):
        if self.split_duration_2:
            if self.split_duration_2 >= self.duration:
                raise UserError(_("Please Check Sum of Both Timesheet.."))
            self.split_duration_1 = self.duration - self.split_duration_2

    # @api.onchange('task_id','project_id')
    # def onchange_task_project(self):
    #     if self.project_id.is_temp_project or self.task_id.is_temp_task:
    #         self.is_temporary = True
    #     else:
    #         self.is_temporary = False


    # NEW_CHANGES
    def end_task(self):
        context = dict(self.env.context or {})
        active_model = context.get('active_model', False)
        active_id = context.get('active_id', False)
        self.duration = self._get_default_duration()
        # self.split_duration_1 = self._get_default_duration()

        vals = {'name': self.name, 'unit_amount': self.duration,
                'unit_amount_invoice' : self.duration,
                'amount': self.duration, 'date': datetime.now().date(),
                'task_id':self.task_id.id,
                'project_id':self.project_id.id,
                'ticket_id':self.ticket_id.id,
                }
        # SPLIT FLOW HERE
        # ===============
        if self.want_to_split:
            vals.update({
                'unit_amount': self.split_duration_1,
                'unit_amount_invoice': self.split_duration_1,
                'amount': self.split_duration_1,
            })

            split_vals={
                'name': self.split_name, 
                'unit_amount': self.split_duration_2,
                'unit_amount_invoice' : self.split_duration_2,
                'amount': self.split_duration_2, 
                'date': datetime.now().date(),
                'start_date':self.start_date,
                'end_date':self.end_date,
                'project_id':self.split_project_id.id,
                'task_id':self.split_task_id.id,
                # 'split_ticket_id':self.split_ticket_id.id
                }

            if self.split_project_id.analytic_account_id:
                split_vals.update({'account_id': self.split_project_id.analytic_account_id.id})

            # for split task stage change
            if self.split_task_id.stage_id != self.split_stage_id and self.split_stage_id:
                self.split_task_id.sudo().with_context(no_notification=True).write({
                    'stage_id' : self.split_stage_id.id 
                })
            
            # for split task log note
            if self.split_task_id and self.split_add_log_note :
                message_vals = {
                    'message_type' : 'comment',
                    'model' : 'project.task',
                    'res_id' : self.split_task_id.id,
                    'author_id' : self.env.user.partner_id.id,
                    'body' : self.split_add_log_note
                }
                self.env['mail.message'].sudo().create(message_vals)

            split_timesheet_id = self.env['account.analytic.line'].sudo().create(split_vals)

        if active_model == 'project.task':
            if active_id:
                task_search = self.env['project.task'].search(
                    [('id', '=', active_id)], limit=1)

                if task_search:
                    vals.update({'end_date': datetime.now()})
                    # vals.update({'task_id': task_search.id})
                    # NEW_CHANGES
                    if 'ticket_id' in self.env['task.time.account.line']._fields and self.ticket_id:
                        vals.update({'ticket_id':self.ticket_id.id})

                    # if task_search.project_id:
                    #     # vals.update({'project_id': task_search.project_id.id})
                    #     act_id = self.env['project.project'].sudo().browse(
                    #         task_search.project_id.id).analytic_account_id

                    #     if act_id:
                    #         vals.update({'account_id': act_id.id})

                    # task_search.sudo().write({'start_time': None,'task_running': False,'task_runner_ids': [(3, self.env.user.id)]})

                    task_search.sudo().write({'start_time': None, 'task_running': False})

                    # if task_search.stage_id != self.stage_id:
                    #     task_search.sudo().with_context(no_notification=True).write({
                    #         'stage_id' : self.stage_id.id 
                    #     })

                    if self.project_id:
                        act_id = self.env['project.project'].sudo().browse(
                                self.project_id.id).analytic_account_id
                        if act_id:
                            vals.update({'account_id': act_id.id})

                    if self.task_id.stage_id != self.stage_id:
                        self.task_id.sudo().with_context(no_notification=True).write({
                            'stage_id' : self.stage_id.id 
                        })
                    
                    if self.add_log_note:
                        message_vals = {
                            'message_type' : 'comment',
                            'model' : 'project.task',
                            'res_id' : self.task_id.id,
                            'author_id' : self.env.user.partner_id.id,
                            'body' : self.add_log_note
                        }
                        self.env['mail.message'].sudo().create(message_vals)


            # need to add sudo() when write timesheet 
            # customization code
            if self.env.user.account_analytic_id:
                self.env.user.account_analytic_id.sudo().write(vals)

            self.sudo()._cr.commit()

            if self.env.user.active_running_task_id:
                self.env.user.active_running_task_id.sudo().write({'is_task_running': False})
                self.env.user.active_running_task_id.sudo().unlink()

            self.env.user.write({'task_id': False,
                                'account_analytic_id':False,
                                'active_running_task_id':False
                                })

        if active_model == 'sh.pause.task.entry':
            if active_id:
                entry_search = self.env['sh.pause.task.entry'].search(
                    [('id', '=', active_id)], limit=1)

                if entry_search:
                    vals.update({'end_date': entry_search.sh_pause_time})
                    # vals.update({'task_id': entry_search.task_id.id})

                    if 'ticket_id' in self.env['task.time.account.line']._fields and self.ticket_id:
                        vals.update({'ticket_id':self.ticket_id.id})

                    # if entry_search.task_id.project_id:
                    #     vals.update({'project_id': entry_search.task_id.project_id.id})
                    #     act_id = self.env['project.project'].sudo().browse(entry_search.task_id.project_id.id).analytic_account_id
                    #     if act_id:
                    #         vals.update({'account_id': act_id.id})

                if self.project_id:
                    act_id = self.env['project.project'].sudo().browse(
                            self.project_id.id).analytic_account_id
                    if act_id:
                        vals.update({'account_id': act_id.id})

                if self.task_id.stage_id != self.stage_id:
                    self.task_id.sudo().with_context(no_notification=True).write({
                        'stage_id' : self.stage_id.id 
                    })
                
                if self.add_log_note:
                    message_vals = {
                        'message_type' : 'comment',
                        'model' : 'project.task',
                        'res_id' : self.task_id.id,
                        'author_id' : self.env.user.partner_id.id,
                        'body' : self.add_log_note
                    }
                    self.env['mail.message'].sudo().create(message_vals)
        
            if entry_search.account_analytic_id:
                entry_search.account_analytic_id.sudo().write(vals)
            entry_search.sudo().unlink()


        if active_model == 'sh.helpdesk.ticket':
            if active_id and self.env.user and self.env.user.task_id:
                ticket_id = self.env[active_model].sudo().browse(active_id)

                if ticket_id:
                    task_search = ticket_id.sh_ticket_task_id

                    if task_search:

                        vals.update({'start_date': self.start_date})
                        vals.update({'end_date': datetime.now()})
                        # vals.update({'task_id': task_search.id})

                        # if task_search.project_id:
                        #     vals.update(
                        #         {'project_id': task_search.project_id.id})
                        #     act_id = self.env['project.project'].sudo().browse(
                        #         task_search.project_id.id).analytic_account_id

                        #     if act_id:
                        #         vals.update({'account_id': act_id.id})

                        task_search.sudo().write({'start_time': None, 'task_running': False,
                                                'task_runner_ids': [(3, self.env.user.id)]})
                        if self.stage_id:
                            task_search.write({
                                'stage_id' : self.stage_id.id
                            })
        # reload_fix
        self.env['bus.bus']._sendone(self.env.user.partner_id, 
            'sh.timer.render', {})
        # return {'type': 'ir.actions.client', 'tag': 'reload'}


    # old_code here for end task
    # ==========================

    # @api.multi

    # def end_task(self):
    #     if self.want_to_split:
    #         total_duration = self.split_duration_1 + self.split_duration_2
    #         if round(total_duration,2) > round(self.duration,2):
    #             raise UserError(_("Please Check Sum of Both Timesheet.."))
    #     if self.want_to_split:
            
    #         self.process_normal_timehseet()
    #         self.process_split_timehseet()
    #     else:
    #         self.process_normal_timehseet()

    # def process_normal_timehseet(self):
    #     context = dict(self.env.context or {})
    #     task_type = context.get('task_type')
    #     active_model = context.get('active_model', False)
    #     active_id = context.get('active_id', False)
    #     task_search = False
    #     if self.want_to_split:
    #         vals = {
    #             'name': self.name,
    #             'unit_amount': self.split_duration_1,
    #             'unit_amount_invoice':self.split_duration_1,
    #             'amount': self.split_duration_1,
    #             'date': datetime.now(),
    #         }
    #     else:
    #         vals = {
    #             'name': self.name,
    #             'unit_amount': self.duration,
    #             'unit_amount_invoice':self.duration,
    #             'amount': self.duration,
    #             'date': datetime.now(),
    #         }
    #     if active_model == 'project.task':
    #         if active_id and self.env.user and self.env.user.task_id:
    #             task_search = self.env['project.task'].search(
    #                 [('id', '=', active_id)], limit=1)

    #             if task_search:

    #                 vals.update({'start_date': self.start_date})
    #                 vals.update({'end_date': datetime.now()})
    #                 if 'ticket_id' in self.env['task.time.account.line']._fields and self.ticket_id:
    #                     vals.update({'ticket_id':self.ticket_id.id})                        
    #                 vals.update({'task_id': task_search.id})

    #                 if task_search.project_id:
    #                     vals.update({'project_id': task_search.project_id.id})
    #                     act_id = self.env['project.project'].sudo().browse(
    #                         task_search.project_id.id).analytic_account_id

    #                     if act_id:
    #                         vals.update({'account_id': act_id.id})

    #                 task_search.sudo().write({'start_time': None, 'task_running': False,
    #                                         'task_runner_ids': [(3, self.env.user.id)]})
    #                 if task_search.stage_id != self.stage_id:
    #                     task_search.sudo().with_context(no_notification=True).write({
    #                         'stage_id' : self.stage_id.id 
    #                     })

    #     if active_model == 'sh.helpdesk.ticket':
    #         if active_id and self.env.user and self.env.user.task_id:
    #             ticket_id = self.env[active_model].sudo().browse(active_id)

    #             if ticket_id:
    #                 task_search = ticket_id.sh_ticket_task_id

    #                 if task_search:

    #                     vals.update({'start_date': self.start_date})
    #                     vals.update({'end_date': datetime.now()})
    #                     vals.update({'task_id': task_search.id})

    #                     if task_search.project_id:
    #                         vals.update(
    #                             {'project_id': task_search.project_id.id})
    #                         act_id = self.env['project.project'].sudo().browse(
    #                             task_search.project_id.id).analytic_account_id

    #                         if act_id:
    #                             vals.update({'account_id': act_id.id})

    #                     task_search.sudo().write({'start_time': None, 'task_running': False,
    #                                             'task_runner_ids': [(3, self.env.user.id)]})
    #                     if self.stage_id:
    #                         task_search.write({
    #                             'stage_id' : self.stage_id.id
    #                         })
    #     if task_search:
    #         timesheet_line = self.env['account.analytic.line'].sudo().search(
    #             [('task_id', '=', task_search.id), ('employee_id.user_id',
    #                                                 '=', self.env.user.id), ('end_date', '=', False)],
    #             limit=1)

    #         if timesheet_line:
    #             timesheet_line.write(vals)


    #         timesheet_line_unit_amount = timesheet_line.unit_amount

    #         if task_search.id != self.task_id.id:
    #             final_timehseet_vals = {
    #                 'name' : timesheet_line.name,
    #                 'unit_amount' : timesheet_line.unit_amount,
    #                 'unit_amount_invoice' : timesheet_line.unit_amount_invoice,
    #                 'project_id' : self.project_id.id,
    #                 'amount' : timesheet_line.amount,
    #                 'date' : timesheet_line.date,
    #                 'account_id' : timesheet_line.account_id.id,
    #                 'start_date' : timesheet_line.start_date,
    #                 'end_date' : timesheet_line.end_date,
    #                 'task_id' : self.task_id.id,
    #                 'employee_id' : timesheet_line.employee_id.id,
    #                 # 'ticket_id' : timesheet_line.ticket_id.id
    #             }

    #             if 'ticket_id' in self.env['account.analytic.line']._fields:
    #                 final_timehseet_vals['ticket_id'] = timesheet_line.ticket_id.id

    #             timesheet_id=self.env['account.analytic.line'].sudo().create(final_timehseet_vals)
    #             task_search.sudo().write({
    #                 'timesheet_ids' : [(2,timesheet_line.id)],                
    #             })
    #             if self.stage_id:
    #                 self.task_id.write({
    #                     'stage_id' : self.stage_id.id
    #                 })
    #             if self.add_log_note:
    #                 message_vals = {
    #                     'message_type' : 'comment',
    #                     'model' : 'project.task',
    #                     'res_id' : self.task_id.id,
    #                     'author_id' : self.env.user.partner_id.id,
    #                     'body' : self.add_log_note
    #                 }
    #                 self.env['mail.message'].sudo().create(message_vals)
    #         elif self.add_log_note:
    #             message_vals = {
    #                 'message_type' : 'comment',
    #                 'model' : 'project.task',
    #                 'res_id' : task_search.id,
    #                 'author_id' : self.env.user.partner_id.id,
    #                 'body' : self.add_log_note
    #             }
    #             self.env['mail.message'].sudo().create(message_vals)
    #         self.sudo()._cr.commit()
    #         if task_type == 'support':
    #             if self.env.user.support_hours:
    #                 support_hours = self.env.user.support_hours + timesheet_line_unit_amount
    #             else:
    #                 support_hours = timesheet_line_unit_amount
    #             self.env.user.write({'support_task_id': False, 'support_start_time': None, 'support_hours':support_hours})
    #         else:
    #             self.env.user.write({'task_id': False, 'start_time': None, 'support_hours':0.0})
    #         self.env['bus.bus']._sendone(self.env.user.partner_id, 
    #         'sh.timer.render', {})
    
    # def process_split_timehseet(self):
    #     context = dict(self.env.context or {})
    #     task_type = context.get('task_type')
    #     active_model = context.get('active_model', False)
    #     active_id = context.get('active_id', False)
    #     task_search = False
    #     vals = {
    #         'name': self.split_name,
    #         'unit_amount': self.split_duration_2,
    #         'unit_amount_invoice':self.split_duration_2,
    #         'amount': self.split_duration_2,
    #         'date': datetime.now(),
    #     }
    #     if active_model == 'project.task':
    #         if self.split_task_id:
    #             task_search = self.env['project.task'].search(
    #                 [('id', '=', self.split_task_id.id)], limit=1)
    #             if task_search:

    #                 vals.update({'start_date': self.start_date})
    #                 vals.update({'end_date': datetime.now()})
    #                 if 'split_ticket_id' in self.env['task.time.account.line']._fields and self.split_ticket_id:
    #                     vals.update({'ticket_id':self.split_ticket_id.id})                        
    #                 vals.update({'task_id': task_search.id})


    #                 if task_search.project_id:
    #                     vals.update({'project_id': task_search.project_id.id})
    #                     act_id = self.env['project.project'].sudo().browse(
    #                         task_search.project_id.id).analytic_account_id

    #                     if act_id:
    #                         vals.update({'account_id': act_id.id})

    #                 task_search.sudo().write({'start_time': None, 'task_running': False,
    #                                         'task_runner_ids': [(3, self.env.user.id)]})
    #                 if task_search.stage_id != self.split_stage_id:
    #                     task_search.sudo().with_context(no_notification=True).write({
    #                         'stage_id' : self.split_stage_id.id 
    #                     })

    #                 if self.split_add_log_note:
    #                     message_vals = {
    #                         'message_type' : 'comment',
    #                         'model' : 'project.task',
    #                         'res_id' : task_search.id,
    #                         'author_id' : self.env.user.partner_id.id,
    #                         'body' : self.split_add_log_note
    #                     }
    #                     self.env['mail.message'].sudo().create(message_vals)
    #             elif self.split_add_log_note:
    #                 message_vals = {
    #                     'message_type' : 'comment',
    #                     'model' : 'project.task',
    #                     'res_id' : self.split_task_id.id,
    #                     'author_id' : self.env.user.partner_id.id,
    #                     'body' : self.split_add_log_note
    #                 }
    #                 self.env['mail.message'].sudo().create(message_vals)    

    #     if active_model == 'sh.helpdesk.ticket':
    #         if active_id and self.env.user and self.env.user.task_id:
    #             ticket_id = self.env[active_model].sudo().browse(active_id)

    #             if ticket_id:
    #                 task_search = ticket_id.sh_ticket_task_id

    #                 if task_search:

    #                     vals.update({'start_date': self.start_date})
    #                     vals.update({'end_date': datetime.now()})
    #                     vals.update({'task_id': task_search.id})

    #                     if task_search.project_id:
    #                         vals.update(
    #                             {'project_id': task_search.project_id.id})
    #                         act_id = self.env['project.project'].sudo().browse(
    #                             task_search.project_id.id).analytic_account_id

    #                         if act_id:
    #                             vals.update({'account_id': act_id.id})

    #                     task_search.sudo().write({'start_time': None, 'task_running': False,
    #                                             'task_runner_ids': [(3, self.env.user.id)]})
    #                     if self.stage_id:
    #                         task_search.write({
    #                             'stage_id' : self.stage_id.id
    #                         })


    #     if task_search:
    #         self.env['account.analytic.line'].sudo().create(vals)
    #         self.sudo()._cr.commit()
    #         if task_type == 'support':
    #             self.env.user.write({'support_task_id': False, 'support_start_time': None})
    #         else:
    #             self.env.user.write({'task_id': False, 'start_time': None, 'support_hours':0.0})
    #         self.env['bus.bus']._sendone(self.env.user.partner_id, 
    #         'sh.timer.render', {})
