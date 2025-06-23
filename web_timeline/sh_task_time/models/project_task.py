# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api, _
from datetime import datetime,date
# from doc._extensions.pyjsparser.parser import true
from odoo.exceptions import UserError, ValidationError
from odoo.addons.resource.models.resource import float_to_time, HOURS_PER_DAY
from datetime import timedelta

class ProjectTask(models.Model):
    _inherit = 'project.task'

    sh_is_preappstore_task = fields.Boolean(
        "Is Preappstore Task", compute="_compute_sh_is_preappstore_task",
        default=False)
    sh_ticket_ids = fields.Many2many('sh.helpdesk.ticket', string='Tickets ')
    def _compute_sh_is_preappstore_task(self):
        for rec in self:
            if rec.project_id.id and rec.project_id.id == rec.company_id.preappstore_project_id.id:
                rec.sh_is_preappstore_task=True
            else:
                rec.sh_is_preappstore_task=False

    def action_sale_create_order(self):
        context = {}
        if not self.partner_id:
            raise UserError("Please Select Customer !")
        if self.partner_id:
            context.update({
                'default_partner_id': self.partner_id.id,
            })
        if self.env.user.id:
            context.update({
                'default_user_id': self.env.user.id,
                'default_responsible_user_id': self.env.user.id,
            })
        if self:
            context.update({
                'default_sh_task_id': self.id,
            })
        # if self.user_id:
            
        #     context.update({
        #         'default_responsible_user_id': self.user_id.id,
        #     })

        if self.user_ids:
           
            context.update({
                'default_sh_responsible_user_ids': [(6, 0, self.user_ids.ids)],
            })
        if self.odoo_edition:
            edition = self.odoo_edition
            # if self.sh_edition_id.name == 'Community':
            #     edition = 'community'
            # if self.sh_edition_id.name == 'Enterprise':
            #     edition = 'enterprise'
            context.update({
                'default_odoo_edition': edition,
            })
        if self.version_ids:
            context.update({
                'default_odoo_version': self.version_ids[0].id,
            })
        # if self.sh_user_ids:
        #     context.update({
        #         'default_responsible_user_id': self.sh_user_ids[0].id,
        #     })
        if not self.sale_product_id:
            raise UserError("Please select Sale Product !")

        if self.sale_product_id:
            line_list = []
            
            line_vals = {
                'product_id': self.sale_product_id.id,
                'name': self.sale_product_id.name_get()[0][1],
                'product_uom_qty': 1.0,
                'price_unit': self.sale_product_id.list_price,
                'product_uom': self.sale_product_id.uom_id.id,
            }
            if self.sale_product_id.taxes_id:
                line_vals.update({
                    'tax_id': [(6, 0, self.sale_product_id.taxes_id.ids)]
                })
            line_list.append((0, 0, line_vals))
            context.update({
                'default_order_line': line_list
            })
        return{
            'name': 'Sale Order',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'context': context,
            'target': 'current'
        }


    # partner_id = fields.Many2one("res.partner",string="Customer")
    # sale_product_id = fields.Many2one("product.product", string="Sale Product")
    # pylint_score = fields.Float("Pylint Score")
    # sh_last_update_date = fields.Date('Last Updated Date',compute='_compute_sh_last_update_date')
    # sh_no_of_days = fields.Integer('No of Days',compute='_compute_sh_no_of_days')
    # allow_timesheet_edit = fields.Boolean("Allow Edit Timesheet")
    # odoo_edition = fields.Selection([('community','Community'),('enterprise','Enterprise')], string="Edition")
    
    def assign_user_to_current_task(self):
        popup_view_id = self.env.ref('sh_task_time.sh_add_user_task_wizard_view').id
        return {
            'name': _('Add Users'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'sh.add.users',                
            'view_id': popup_view_id,
            'target': 'new',
        }


    def action_edit_my_timesheet(self):
        if self.env.user not in self.user_ids and self.env.user not in self.user_id:
            raise UserError(_("You are not allowed to update Timesheet, Ask your senior to Update"))
        popup_view_id = self.env.ref('sh_task_time.sh_update_timesheet_task_wizard_view').id
        return {
            'name': _('Add Timesheet'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'sh.update.timesheet',                
            'view_id': popup_view_id,
            'target': 'new',
        }

    # @api.multi
    @api.model
    def _message_auto_subscribe_notify(self, partner_ids, template):
        if not self or self.env.context.get('mail_auto_subscribe_no_notify'):
            return
        if not self.env.registry.ready:  # Don't send notification during install
            return

        view = self.env['ir.ui.view'].browse(self.env['ir.model.data'].xmlid_to_res_id(template))

    # -------- Duplicate create method in same file so merge both code in one method ----------

    # @api.model_create_multi
    # def create(self, vals_list):
    #     records  = super(ProjectTask, self).create(vals_list)
    #     for res in records:
    #         if res.user_ids:
    #             if self.env.user.id not in res.user_ids.ids:
    #                 base_url = self.env['ir.config_parameter'].sudo(
    #                 ).get_param('web.base.url')
    #                 self.env['user.push.notification'].push_notification([res.user_id], 'New Task Created', 'Task : %s:' % (
    #                     res.name), base_url+"/mail/view?model=project.task&res_id="+str(res.id), 'project.task', res.id,'project')
             
    #     return records


    def write(self, vals):
        if vals.get('user_ids'):
            self = self.with_context(stop_sent_notify=True)
        for rec in self:
            if vals.get('stage_id') and rec.stage_id.id==vals.get('stage_id'):
                del vals['stage_id']

        # new_added_user=False
        # if vals.get('user_ids'):
        #     vals_users=vals.get('user_ids')
        #     if len(vals_users[0])==3:
        #         vals_users=vals_users[0][2]
        #     elif len(vals_users[0])==2:
        #         vals_users=[vals_users[0][1]]
        #     if self.user_ids:
        #         new_added_user=list(set(vals_users).difference(self.user_ids.ids))
        #     else:
        #         new_added_user=vals_users
        #     new_added_user = self.env['res.users'].sudo().browse(new_added_user)
        res  = super(ProjectTask, self).write(vals)
        for rec in self:
            base_url = self.env['ir.config_parameter'].sudo(
                ).get_param('web.base.url')
            # if new_added_user:
            #     for user in new_added_user:
            #         self.env['user.push.notification'].push_notification([user], 'Task Assigned', 'Task : %s:' % (
            #             rec.name), base_url+"/mail/view?model=project.task&res_id="+str(rec.id), 'project.task', rec.id,'project')   

            previous_stage = rec.stage_id.id
            if vals.get('stage_id'):
                print()
                default_employees = rec.stage_id.stage_wize_default_employee_line.sorted(
                lambda x: x.sequence).mapped('user_id')
                for default_employee in default_employees:
                    if default_employee.id not in rec.sudo().user_ids.sudo().ids:
                        rec.sudo().user_ids = [(4, default_employee.id)]
                        self.env['user.push.notification'].push_notification([default_employee], 'Task Assigned', 'Task : %s:' % (
                            rec.name), base_url+"/mail/view?model=project.task&res_id="+str(rec.id), 'project.task', rec.id,'project')
                
                if 'no_notification' not in self.env.context:
                    state_user_list = rec.stage_id.stage_wize_employee_line.sorted(
                        lambda x: x.sequence).mapped('user_id')
                    task_user_list = rec.user_ids.ids
                    # Developer
                    if rec.sh_project_task_base_dev_id:
                        if rec.sh_project_task_base_dev_id.id not in task_user_list:
                            task_user_list.append(rec.sh_project_task_base_dev_id.id)
                    # Tester
                    if rec.sh_project_task_base_tester_id:
                        if rec.sh_project_task_base_tester_id.id not in task_user_list:
                            task_user_list.append(rec.sh_project_task_base_tester_id.id)
                    # Designer
                    if rec.sh_project_task_base_designer_id:
                        if rec.sh_project_task_base_designer_id.id not in task_user_list:
                            task_user_list.append(rec.sh_project_task_base_designer_id.id)
                    # Index By
                    if rec.sh_project_task_base_index_by_id:
                        if rec.sh_project_task_base_index_by_id.id not in task_user_list:
                            task_user_list.append(rec.sh_project_task_base_index_by_id.id)
                    # Marketed By
                    if rec.sh_project_task_base_marketed_by_id:
                        if rec.sh_project_task_base_marketed_by_id.id not in task_user_list:
                            task_user_list.append(rec.sh_project_task_base_marketed_by_id.id)
                    for state_user in state_user_list:
                        if state_user and state_user.id in task_user_list:
                            self.env['user.push.notification'].push_notification([state_user], 'Task Stage Changed', 'Task : %s:' % (
                                rec.name), base_url+"/mail/view?model=project.task&res_id="+str(rec.id), 'project.task', rec.id,'project')
                            task_user_list.remove(state_user.id)

        return res



    sh_sale_id = fields.Many2one("sale.order",string="Sale Reference", compute="_get_sale_reference")

    # @api.multi
    @api.model
    def _get_sale_reference(self):
        for rec in self:
            rec.sh_sale_id = False
            if 'sh_task_id' in self.env['sale.order']._fields:
                sale_id = self.env['sale.order'].sudo().search([('sh_task_id','=',rec.id)],limit=1, order="id desc")
                if sale_id:
                    rec.sh_sale_id = sale_id.id

    def get_invoices(self):
        if self.env.user.has_group('account.group_account_manager'):
            invoices = self.env['account.move'].search([("project_task_id", "=", self.id)])

            if len(invoices.ids) == 1:
                return {
                    "type": "ir.actions.act_window",
                    "name": "Invoices",
                    "views": [(self.env.ref('account.view_move_form').id, 'form')],
                    "res_model": "account.move",
                    "res_id": invoices.id,      
                }
            
            else:
                return {
                    "type": "ir.actions.act_window",
                    "name": "Invoices",
                    "view_mode": "tree,form",
                    "res_model": "account.move",  
                    "domain": [("project_task_id", "=", self.id)],
                }


        else:
            raise ValidationError("You are not authorized to perform this !")
        
        
    def version_wise_subtask(self):
        new_created_child_task = self.env["project.task"]
        for rec in self:
            for version_id in rec.version_ids:
                find_version_task=self.env['project.task'].search([('version_ids','in',version_id.id),('parent_id','=',rec.id)])
                if not find_version_task:
                    find_first_verison_task=self.env['project.task'].search([('parent_id','=',rec.id)],limit=1)
                    if new_created_child_task or find_first_verison_task:
                        if new_created_child_task:
                            child_task=new_created_child_task[0].copy(default={
                            'name': rec.name,
                            'parent_id': rec.id,
                            'version_ids': [(6, 0, version_id.ids)]
                            })
                        else:
                            child_task=find_first_verison_task[0].copy(default={
                                'name': rec.name,
                                'parent_id': rec.id,
                                'version_ids': [(6, 0, version_id.ids)]
                            })
                    else:
                        child_task=rec.copy(default={
                            'name': rec.name,
                            'parent_id': rec.id,
                            'version_ids': [(6, 0, version_id.ids)]
                        })
                    new_created_child_task|=child_task


    def action_subtask(self):
        action = self.env.ref('project.project_task_action_sub_task').read()[0]
        ctx = self.env.context.copy()
        ctx.update({
            'default_parent_id': self.id,
            'default_project_id': self.env.context.get('project_id', self.project_id.id),
            'default_name': self.env.context.get('name', self.name) + ':',
            'default_partner_id': self.env.context.get('partner_id', self.partner_id.id),
            'search_default_project_id': self.env.context.get('project_id', self.project_id.id),
            'search_default_parent_only': 0,
            'default_date_deadline': self.date_deadline,
            'default_description': self.description,

            'default_user_ids': [(6, 0, self.user_ids.ids)],
            'default_tag_ids': [(6, 0, self.tag_ids.ids)],
        })
        action['context'] = ctx
        action['domain'] = [('id', 'child_of', self.id), ('id', '!=', self.id)]
        return action

    @api.model
    def get_duration(self, task):
        if self.env.user and self.env.user.task_id:
            if self.env.user.start_time:
                if self.env.user.support_task_id or self.env.user.support_hours:
                    diff = fields.Datetime.from_string(
                        fields.Datetime.now()) - fields.Datetime.from_string(
                            self.env.user.start_time)
                    if diff:
                        float_time = self.env.user.support_hours
                        float_time = float_to_time(self.env.user.support_hours)
                        seconds = (float_time.hour * 60 + float_time.minute) * 60 + float_time.second
                        if self.env.user.support_task_id:
                            support_diff = fields.Datetime.from_string(
                                fields.Datetime.now()) - fields.Datetime.from_string(
                                self.env.user.support_start_time)
                            return (diff.total_seconds()- seconds - support_diff.total_seconds())* 1000
                        else:
                            return (diff.total_seconds()-seconds )* 1000
                else:
                    diff = fields.Datetime.from_string(
                        fields.Datetime.now()) - fields.Datetime.from_string(
                            self.env.user.start_time)
                    return diff.total_seconds() * 1000

    # OLD_START_TASK_METHOD_HERE

    # def action_task_start(self):

    #     if self.project_id.sudo().stage_id.id in self.company_id.close_project_stage_ids.ids:
    #         raise UserError("You can not start Task ! Project is already in done/close stage.")

    #     self.start_id = 0

    #     if self.env.user.task_id:
    #         raise UserError("You can not start 2 tasks at same time !")

        
    #     self.sudo().start_time = datetime.now()

    #     # add entry in line

    #     vals = {'name': '/', 'date': datetime.now()}
    #     if self.env.context.get('active_model') == 'sh.helpdesk.ticket' and self.env.context.get('active_id'):
    #         vals.update({
    #             'ticket_id': self.env.context.get('active_id')
    #         })
    #     if self:
    #         vals.update({'start_date': datetime.now()})
    #         vals.update({'task_id': self.id})

    #         if self.project_id:
    #             vals.update({'project_id': self.project_id.id})
    #             act_id = self.env['project.project'].sudo().browse(
    #                 self.project_id.id).analytic_account_id

    #             if act_id:
    #                 vals.update({'account_id': act_id.id})

    #     usr_id = self.env.user.id
    #     if usr_id:
    #         emp_search = self.env['hr.employee'].search(
    #             [('user_id', '=', usr_id)], limit=1)

    #         if emp_search:
    #             vals.update({'employee_id': emp_search.id})

    #             todays_date = date.today()
    #             todays_date_time = datetime.strftime(todays_date, "%Y-%m-%d 00:00:00")
    #             if 'is_remote_employee' in self.env['hr.employee']._fields and not emp_search.is_remote_employee:
    #                 attendance = self.env['hr.attendance'].sudo().search([('employee_id','=',emp_search.id),('check_in','>',todays_date_time),('check_out','=',False)])
    #                 if not attendance:
    #                     raise UserError ("You can not start task as you have not check-in !")

    #                 attendance = self.env['hr.attendance'].sudo().search([('employee_id','=',emp_search.id),('check_in','>',todays_date_time),('sh_break_start','!=',False),('sh_break_end','=',False)])
    #                 if attendance:
    #                     raise UserError ("You can not start task as you have not end break !")
        

    #     self.env['account.analytic.line'].sudo().create(vals)
    #     self.env.user.write({'task_id': self.id, 'start_time': datetime.now()})
    #     self.write({'task_running': True, 'task_runner': self.env.user.name,
    #                 'task_runner_ids': [(4, self.env.user.id)]})
    #     self.sudo()._cr.commit()
    #     self.env['bus.bus']._sendone(self.env.user.partner_id, 
    #         'sh.timer.render', {})
        

    def action_task_start(self):

        context_by_pass_done_validation = self.env.context.get('by_pass_done_validation',False)
        if self.project_id.sudo().stage_id.id in self.company_id.close_project_stage_ids.ids:
            raise UserError("You can not start Task ! Project is already in done/close stage.")
        

        if not context_by_pass_done_validation and self.project_id and not self.project_id.is_task_editable_in_done_stage and self.env.user.company_id.timesheet_restricted_task_stage_ids and self.stage_id.id in self.env.user.company_id.timesheet_restricted_task_stage_ids.ids:
                raise ValidationError(f"You can not add/edit timesheet in Task if task is in {self.stage_id.name} stage.")
        
        
        # if not context_by_pass_done_validation and self.project_id and self.env.user.company_id.done_project_stage_id and not self.project_id.is_task_editable_in_done_stage and self.env.user.company_id.done_project_stage_id.id == self.stage_id.id :

        #     raise ValidationError("You can not start Done Task.")
    
        self.start_id = 0

        if self.env.user.task_id:
            raise UserError("You can not start 2 tasks at same time !")
        

        search_pause_entry=self.env['sh.pause.task.entry'].search([('task_id','=',self.id),('user_id','=',self.env.user.id)])
        if search_pause_entry:
            raise UserError("You can not start same task twice, you can resume it again !")

        self.sudo().start_time = datetime.now()

        # add entry in line
        vals = {'name': '/', 'date': datetime.now().date()}

        if self.env.context.get('active_model') == 'sh.helpdesk.ticket' and self.env.context.get('active_id'):
            vals.update({
                'ticket_id': self.env.context.get('active_id')
            })
        if self:
            vals.update({'start_date': datetime.now()})
            vals.update({'task_id': self.id})

            if self.project_id:
                vals.update({'project_id': self.project_id.id})
                act_id = self.env['project.project'].sudo().browse(
                    self.project_id.id).analytic_account_id

                if act_id:
                    vals.update({'account_id': act_id.id})

        usr_id = self.env.user.id
        if usr_id:
            emp_search = self.env['hr.employee'].search(
                [('user_id', '=', usr_id)], limit=1)

            if emp_search:
                vals.update({'employee_id': emp_search.id})

                todays_date = date.today()
                todays_date_time = datetime.strftime(todays_date, "%Y-%m-%d 00:00:00")
                if 'is_remote_employee' in self.env['hr.employee']._fields and not emp_search.is_remote_employee:
                    attendance = self.env['hr.attendance'].sudo().search([('employee_id','=',emp_search.id),('check_in','>',todays_date_time),('check_out','=',False)])
                    if not attendance:
                        raise UserError ("You can not start task as you have not check-in !")

                    attendance = self.env['hr.attendance'].sudo().search([('employee_id','=',emp_search.id),('check_in','>',todays_date_time),('sh_break_start','!=',False),('sh_break_end','=',False)])
                    if attendance:
                        raise UserError ("You can not start task as you have not end break !")
        

        account_analytic_id=self.env['account.analytic.line'].sudo().create(vals)

        # customization code
        if account_analytic_id:
            self.env.user.write({'account_analytic_id': account_analytic_id.id})


        self.env.user.write({'task_id': self.id, 'start_time': datetime.now()})
        self.write({'task_running': True, 'task_runner': self.env.user.name,
                    'task_runner_ids': [(4, self.env.user.id)]})
        self.sudo()._cr.commit()
        self.env['bus.bus']._sendone(self.env.user.partner_id, 
            'sh.timer.render', {})

        # new_changes
        # user wise customization
        pause_entry_vals={
            'start_date': datetime.now(),
            'user_id': self.env.user.id,
            'task_id': self.id,
            # 'name': self.name,
            'name': f"{self.project_id.name} : {self.name}",
            'account_analytic_id': account_analytic_id.id,
            'is_task_running': True,
            }

        pause_id=self.env['sh.pause.task.entry'].create(pause_entry_vals)
        if pause_id:
            self.env.user.write({'active_running_task_id': pause_id.id})

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }


    # new_changes
    def paush_running_timer(self,vals):
        usr_id = self.env.user
        push_entry_vals={}

        if not usr_id.active_running_task_id and usr_id.account_analytic_id:
            if usr_id:
                push_entry_vals={
                    'user_id':usr_id.id,
                    'task_id':self.id,
                    # 'name':self.name,
                    'name': f"{self.project_id.name} : {self.name}",
                }
            if usr_id.account_analytic_id:
                push_entry_vals.update({
                    'account_analytic_id':usr_id.account_analytic_id.id,
                })

            if vals.get('start_date'):
                diff = fields.Datetime.from_string(datetime.now()) -fields.Datetime.from_string(vals.get('start_date'))
                if diff:
                    duration=diff.total_seconds() * 1000

                push_entry_vals.update({
                    'start_date':vals.get('start_date'),
                    'sh_pause_time':datetime.now(),
                    'duration':duration,
                    'difference_time':str(diff).split(".")[0] if diff else False,
                    'difference_time_float':diff.total_seconds()/3600,
                })

            ative_task_entry=self.env['sh.pause.task.entry'].create(push_entry_vals)

            usr_id.write({'active_running_task_id':ative_task_entry.id})

        else:
            # for add duration if already have old duration
            if usr_id.start_time:
                diff = fields.Datetime.from_string(datetime.now()) -fields.Datetime.from_string(usr_id.start_time)

                if diff:
                    duration=diff.total_seconds() * 1000
                    usr_id.sudo().active_running_task_id.duration=usr_id.sudo().active_running_task_id.duration+duration

                    if usr_id.sudo().active_running_task_id.difference_time:
                        old_difference_time=usr_id.sudo().active_running_task_id.difference_time
                        if old_difference_time:

                            # IF PAUSE TIMER IS IN DAYS(GREATER THAN 24 HOURS)
                            if 'day' in old_difference_time or 'days' in old_difference_time:
                                days,old_difference_time = old_difference_time.split(',')
                                old_difference_time=old_difference_time.strip()

                            conveted_type = datetime.strptime(old_difference_time,'%H:%M:%S')
                            total_time_task=conveted_type + diff
                            if total_time_task:
                                usr_id.sudo().active_running_task_id.difference_time=str(total_time_task.time()).split(".")[0]
                    else:
                        usr_id.sudo().active_running_task_id.difference_time=str(diff).split(".")[0]


                    if usr_id.sudo().active_running_task_id.difference_time_float:
                        old_difference_time=usr_id.sudo().active_running_task_id.difference_time_float
                        usr_id.sudo().active_running_task_id.difference_time_float=(diff.total_seconds() / 3600) + old_difference_time

                    else:
                        usr_id.sudo().active_running_task_id.difference_time_float=diff.total_seconds() / 3600

                # if diff:
                #     duration=diff.total_seconds() * 1000
                #     usr_id.sudo().active_running_task_id.duration=usr_id.sudo().active_running_task_id.duration+duration

                #     if usr_id.sudo().active_running_task_id.difference_time_float:
                #         old_difference_time=usr_id.sudo().active_running_task_id.difference_time_float
                #         usr_id.sudo().active_running_task_id.difference_time_float=(diff.total_seconds() / 3600) + old_difference_time

                #     else:
                #         usr_id.sudo().active_running_task_id.difference_time_float=diff.total_seconds() / 3600


            usr_id.sudo().active_running_task_id.write({'sh_pause_time':datetime.now(),'is_task_running':False})

        # ======= remove user data from task
        self.sudo().write({'start_time': None,'task_running': False, 'task_runner':False,
                           'task_runner_ids': [(3, self.env.user.id)]})

        self.env.user.write({
            'task_id': False,
            'account_analytic_id':False,
            'start_time':False,
            'active_running_task_id':False,
            })

        self.sudo()._cr.commit()
        # reload_fix
        self.env['bus.bus']._sendone(self.env.user.partner_id, 
            'sh.timer.render', {})
        
        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'reload',
        # }


     # @api.multi
    @api.model
    def action_task_pause(self):
        self.start_id = 0

        if self.env.user.support_task_id:
            raise UserError("You can not start 2 support tasks at same time !")

        self.sudo().start_time = datetime.now()

        # add entry in line

        vals = {'name': '/', 'date': datetime.now().date()}
        if self.env.context.get('active_model') == 'sh.helpdesk.ticket' and self.env.context.get('active_id'):
            vals.update({
                'ticket_id': self.env.context.get('active_id')
            })
        if self:
            vals.update({'start_date': datetime.now()})
            vals.update({'task_id': self.id})

            if self.project_id:
                vals.update({'project_id': self.project_id.id})
                act_id = self.env['project.project'].sudo().browse(
                    self.project_id.id).analytic_account_id

                if act_id:
                    vals.update({'account_id': act_id.id})

        usr_id = self.env.user.id
        if usr_id:
            emp_search = self.env['hr.employee'].search(
                [('user_id', '=', usr_id)], limit=1)

            if emp_search:
                vals.update({'employee_id': emp_search.id})

                todays_date = date.today()
                todays_date_time = datetime.strftime(todays_date, "%Y-%m-%d 00:00:00")
                if'is_remote_employee' in self.env['hr.employee']._fields and not emp_search.is_remote_employee:
                    attendance = self.env['hr.attendance'].sudo().search([('employee_id','=',emp_search.id),('check_in','>',todays_date_time),('check_out','=',False)])
                    if not attendance:
                        raise UserError ("You can not start task as you have not check-in !")

                    attendance = self.env['hr.attendance'].sudo().search([('employee_id','=',emp_search.id),('check_in','>',todays_date_time),('sh_break_start','!=',False),('sh_break_end','=',False)])
                    if attendance:
                        raise UserError ("You can not start task as you have not end break !")
        

        self.env['account.analytic.line'].sudo().create(vals)
        self.env.user.write({'support_task_id': self.id, 'support_start_time': datetime.now()})
        self.write({'task_running': True, 'task_runner': self.env.user.name,
                    'task_runner_ids': [(4, self.env.user.id)]})
        self.sudo()._cr.commit()
        self.env['bus.bus']._sendone(self.env.user.partner_id, 
            'sh.timer.render', {})

    @api.model
    def action_user_task_end(self):
        usr_id = self.env.user
        if usr_id and usr_id.task_id:
            usr_id.task_id.action_task_end()
        return {}

    def action_task_end(self):
        self.sudo().end_time = datetime.now()
        self.sudo().start_time = self.env.user.start_time
        if self.env.user and self.env.user.task_id:
            tot_sec = (self.end_time -
                       self.env.user.start_time).total_seconds()
            tot_hours = round((tot_sec / 3600.0), 2)

            self.sudo().total_time = tot_hours

            return {
                'name': "End Task Timesheet",
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'task.time.account.line',
                'context': {
                    'end_time': datetime.now(),
                    'start_time': self.env.user.start_time
                },
                'target': 'new',
            }

    # @api.multi
    @api.model
    def create_product(self):

        for rec in self:
            if not rec.sh_product_id and not rec.product_template_id:

                version_attribute = self.env['product.attribute'].search(
                    [('name', 'ilike', 'Version')], limit=1)

                if not version_attribute:
                    version_attribute = self.env['product.attribute'].create({
                        'name': 'Version'
                    })

                model_product_template = self.env['product.template'].create({
                    'name': rec.name,
                })

                # if rec.project_task_change_log_ids:
                #     for log in rec.project_task_change_log_ids:
                #         self.env['product.change.log'].sudo().create({
                #                     'product_id': model_product_template.id,
                #                     'version':log.version,
                #                     'date':log.date,
                #                     'log_type':log.log_type,
                #                     'details':log.details
                #                     })
                rec.write({
                    'product_template_id': model_product_template.id
                })

                if rec.subtask_count != 0:
                    subtasks = self.search([('parent_id', '=', rec.id)])

                    version_value_list = []
                    dictt = []
                    for subtask in subtasks:
                        if subtask.version_ids:
                            attr_value = self.env['product.attribute.value'].search(
                                [('name', 'ilike', subtask.version_ids[0].name)], limit=1)

                            if attr_value:
                                version_value_list.append(attr_value.id)
                            else:
                                version_attr_value = self.env['product.attribute.value'].create({
                                    'name': subtask.version_ids[0].name,
                                    'attribute_id': version_attribute.id
                                })
                                version_value_list.append(
                                    version_attr_value.id)

                    dictt.append((0, 0, {
                        'attribute_id': version_attribute.id,
                        'value_ids': [(6, 0, version_value_list)]
                    }))

                    model_product_template.update({
                        'attribute_line_ids': dictt
                    })

                    product_product = self.env['product.product'].search(
                        [('product_tmpl_id', '=', model_product_template.id)])

                    for subtask in subtasks:
                        if subtask.version_ids:
                            subtask_rel_product = product_product.filtered(
                                lambda x: x.attribute_value_ids.name == subtask.version_ids[0].name)
                            if subtask_rel_product:
                                subtask_rel_product[0].write({
                                    'resposible_user_id': subtask.user_id.id,
                                    'sh_technical_name': subtask.sh_technical_name,
                                    'depends': [(6, 0, subtask.depends.ids)],
                                    'license': subtask.license.id,
                                    'product_version': subtask.product_version,
                                    'supported_browsers': [(6, 0, subtask.supported_browsers.ids)],
                                    'released_date': subtask.released_date,
                                    'last_updated_date': subtask.last_updated_date,
                                    'live_demo': subtask.live_demo,
                                    'user_guide': subtask.user_guide,
                                    'tag_ids': [(6, 0, subtask.sh_tag_ids.ids)],
                                    'sh_edition_ids': [(6, 0, subtask.sh_edition_ids.ids)],
                                    'related_video': [(6, 0, subtask.related_video.ids)],
                                    'banner': subtask.banner,
                                    'sh_blog_post_ids': [(6, 0, subtask.sh_blog_post_ids.ids)],
                                    'sh_scale_ids': subtask.sh_scale_ids.id,

                                })
                                if subtask.project_task_change_log_ids:
                                    for log in subtask.project_task_change_log_ids:
                                        self.env['product.change.log'].sudo().create({
                                            'product_variant_id': subtask_rel_product.id,
                                            'version': log.version,
                                            'date': log.date,
                                            'log_type': log.log_type,
                                            'details': log.details
                                        })

                                subtask.write({
                                    'sh_product_id': subtask_rel_product.id
                                })

                model_product_template.write({
                    'resposible_user_id': rec.user_id.id,
                    'sh_technical_name': rec.sh_technical_name,
                    'depends': [(6, 0, rec.depends.ids)],
                    'license': rec.license.id,
                    'product_version': rec.product_version,
                    'supported_browsers': [(6, 0, rec.supported_browsers.ids)],
                    'released_date': rec.released_date,
                    'last_updated_date': rec.last_updated_date,
                    'live_demo': rec.live_demo,
                    'user_guide': rec.user_guide,
                    'related_video': [(6, 0, rec.related_video.ids)],
                    'banner': rec.banner,
                    'sh_blog_post_ids': [(6, 0, rec.sh_blog_post_ids.ids)],
                    'tag_ids': [(6, 0, rec.sh_tag_ids.ids)],
                    'sh_edition_ids': [(6, 0, rec.sh_edition_ids.ids)],
                    'sh_scale_ids': rec.sh_scale_ids.id,
                    'versions': [(6, 0, rec.version_ids.ids)],
                })

    def name_get(self):
        result = []
        for task in self:
            name = task.name
            if len(task.version_ids) == 1 and task.project_id.id != self.env.user.company_id.appstore_project_id.id:
                name = task.version_ids.name + '/' + name
            result.append((task.id, name))
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        if args is None:
            args = []
        domain = args + ['|','|', ('name', 'ilike', name), ('sh_technical_name', 'ilike', name),('odoo_edition', 'ilike', name)]   
        return super(ProjectTask, self)._search(domain, limit=limit)

    @api.model
    def _task_message_auto_subscribe_notify(self, users_per_task):
        
        # Stop Sent Emails While Assined User Set Fron Project Task
        if self.env.context.get('stop_sent_notify'):
            return True
        
        return super(ProjectTask,self)._task_message_auto_subscribe_notify(users_per_task=users_per_task)


    @api.model_create_multi
    def create(self, vals_list):

        # Check if 'user_ids' key exists in the dictionary
        if 'user_ids' in vals_list[0]:
            self = self.with_context(stop_sent_notify=True)

        rec = super(ProjectTask, self).create(vals_list)
        for res in rec:
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            if res.user_ids:
                for user in list(set(res.user_ids)):
                    if self.env.user.id != user.id:
                        self.env['user.push.notification'].push_notification([user], 'New Task Created', 'Task : %s:' % (
                            res.name), base_url+"/mail/view?model=project.task&res_id="+str(res.id), 'project.task', res.id,'project')
            elif res.partner_id and not res.user_ids or res.project_id.user_id:
                self.env['user.push.notification'].push_notification([res.project_id.user_id], 'New Task Created', 'Task : %s:' % (
                        res.name), base_url+"/mail/view?model=project.task&res_id="+str(res.id), 'project.task', res.id,'project')

            if res.parent_id:
                res.sh_product_id = res.parent_id.sh_product_id.id
                res.sh_technical_name = res.parent_id.sh_technical_name
                res.depends = [(6,0,res.parent_id.depends.ids)]
                res.banner = res.parent_id.banner
                res.sh_edition_ids = [(6,0,res.parent_id.sh_edition_ids.ids)]
                res.license = res.parent_id.license.id
                res.product_version = res.parent_id.product_version
                res.supported_browsers = [(6,0,res.parent_id.supported_browsers.ids)]
                res.released_date = res.parent_id.released_date
                res.last_updated_date = res.parent_id.last_updated_date
                res.live_demo = res.parent_id.live_demo
                res.user_guide = res.parent_id.user_guide
                res.related_video = [(6,0,res.parent_id.related_video.ids)]
                res.sh_blog_post_ids = [(6,0,res.parent_id.sh_blog_post_ids.ids)]
                res.sh_tag_ids = [(6,0,res.parent_id.sh_tag_ids.ids)]
                res.sh_scale_ids = res.parent_id.sh_scale_ids.id            
        return res
