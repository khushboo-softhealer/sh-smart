# Copyright (C) Softhealer Technologies.

from odoo import models, fields,api,_
from odoo.exceptions import UserError
from datetime import datetime,date

# whenever need to update any task entry value need to update following fields
# duration - microseconds
# difference_time_float - in float time
# difference_time - total time in char formate(00:00:00)

class PauseTaskEntry(models.Model):
    _name = 'sh.pause.task.entry'
    _description = 'Pause Task Timer Data'

    name=fields.Char("Name")
    user_id=fields.Many2one('res.users','User Id')
    start_date = fields.Datetime("Start Time", readonly=True)
    task_id=fields.Many2one('project.task','Task Id')
    sh_pause_time = fields.Datetime("Pause Time", readonly=True)
    is_task_running = fields.Boolean("Task Running")
    duration = fields.Float('Real Duration')
    # duration = fields.Float('Real Duration', compute='_compute_duration')
    account_analytic_id=fields.Many2one('account.analytic.line','Timesheet Id')
    difference_time=fields.Char('Actual Time')
    difference_time_float=fields.Float('Rounded Time')

    # @api.depends('start_date','sh_pause_time')
    # def _compute_duration(self):
    #     for rec in self:
    #         rec.duration = 0.0
    #         if rec.start_date and rec.sh_pause_time:
    #             diff = fields.Datetime.from_string(rec.sh_pause_time) -fields.Datetime.from_string(rec.start_date)

    #             if diff:
    #                 duration = float(diff.days) * 24 + \
    #                     (float(diff.seconds) / 3600)
                     
    #                 rec.duration=diff.total_seconds() * 1000

    @api.model
    def get_duration(self,user_id):
        if user_id:
            user = self.env['res.users'].sudo().browse(int(user_id))
            if user.task_running_ids:

                active_task=user.task_running_ids.filtered(lambda x: x.is_task_running)
                if len(active_task)>1:
                    raise UserError(_("Can't Active Two task at a time"))

                if active_task:
                    if self.env.user.start_time:
                        diff = fields.Datetime.from_string(
                            fields.Datetime.now()) - fields.Datetime.from_string(self.env.user.start_time)
                        if diff:
                            duration = float(diff.days) * 24 + \
                                (float(diff.seconds) / 3600)

                        if active_task.duration and diff:
                            return diff.total_seconds() * 1000 + active_task.duration

                        if not active_task.duration and diff:
                            return diff.total_seconds() * 1000
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

        #     if runner_id.is_task_running:
        #         if runner_id and self.env.user.start_time:
        #             diff = fields.Datetime.from_string(
        #                 fields.Datetime.now()) - fields.Datetime.from_string(self.env.user.start_time)
                
        #             if diff:
        #                 duration = float(diff.days) * 24 + \
        #                     (float(diff.seconds) / 3600)
        #             if diff and runner_id.duration:
        #                 return diff.total_seconds() * 1000 + runner_id.duration
        #             else:
        #                 return diff.total_seconds() * 1000

        #     else:        
        #         return False


    def get_task_menu_data(self, fields=[]):
        search_quick_menu = self.sudo().search([('user_id', '=', self.env.user.id),('is_task_running', '=', False) ])
        final_quick_menu_list = []
        if search_quick_menu:
            for rec in search_quick_menu:
                vals = {
                    'id': rec.id,
                    'name': rec.name,
                    'task_id': rec.task_id,
                    'duration_timer': rec.difference_time,
                }
                final_quick_menu_list.append(vals)

        return final_quick_menu_list


    def resume_task(self):

        # FIX FOR NOT GETTING sh_allow_multi_user
        # if self.task_id.task_running and not self.env.company.sh_allow_multi_user:
        #     raise UserError(
        #         " This task has been already started by another user !")

        user_id=self.env.user.id
        if user_id:
            emp_search = self.env['hr.employee'].search(
                [('user_id', '=', user_id)], limit=1)

            if emp_search:
                todays_date = date.today()
                todays_date_time = datetime.strftime(todays_date, "%Y-%m-%d 00:00:00")
                if 'is_remote_employee' in self.env['hr.employee']._fields and not emp_search.is_remote_employee:
                    attendance = self.env['hr.attendance'].sudo().search([('employee_id','=',emp_search.id),('check_in','>',todays_date_time),('check_out','=',False)])
                    if not attendance:
                        raise UserError ("You can not start task as you have not check-in !")

                    attendance = self.env['hr.attendance'].sudo().search([('employee_id','=',emp_search.id),('check_in','>',todays_date_time),('sh_break_start','!=',False),('sh_break_end','=',False)])
                    if attendance:
                        raise UserError ("You can not Resume task as you have not end break !")

        # ====================================================
        # if timer already started and you try to resume again
        # ====================================================

        if self.env.user.task_id:
            vals={
                'start_date': self.env.user.start_time,
                  'task_id': self.env.user.task_id.id  
                }
            self.env.user.task_id.paush_running_timer(vals)

        self.task_id.sudo().start_time = self.start_date

        self.env.user.write({
                    'task_id': self.task_id.id,
                    'start_time': datetime.now(),
                    'account_analytic_id':self.account_analytic_id,
                    'active_running_task_id':self.id,
                    })

        self.task_id.write({'task_running': True, 'task_runner': self.env.user.name,'task_runner_ids': [(4, self.env.user.id)]})
        self.sudo()._cr.commit()

        if self:
            json = {
                'id': self.id,
                'name': self.name,
                'task_id': self.task_id,
            }
            # self.sudo().unlink()
            self.sudo().write({'is_task_running':True})

            # reload_fix
            self.env['bus.bus']._sendone(self.env.user.partner_id, 
            'sh.timer.render', {})
            return json
        return False

    # =============================
    # for edit timesheet from tree
    # =============================
    def action_edit_timesheet(self):
        for rec in self:
            return{
                'name': "Edit Timesheet",
                'type': "ir.actions.act_window",
                'view_type': "form",
                'view_mode': "form",
                'views': [[False, "form"]],
                'res_model': "sh.edit.timesheet",
                'target': "new",
                'context': {
                'default_sh_pause_timesheet_id': rec.id,
                'default_difference_time_float': rec.difference_time_float,
                'active_id': rec.id,
            }}