# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

from datetime import  datetime, timedelta



class ProjectTask(models.Model):
    _inherit = 'project.task'

    _rec_names_search = ['name', 'sh_technical_name','sh_product_id.sh_technical_name']

    product_template_id = fields.Many2one('product.template','Product Template Id', tracking=True)

    project_type_selection = fields.Selection(related='project_id.project_type_selection', store=True)

    # task time fields
    partner_id = fields.Many2one("res.partner",string="Customer")
    sale_product_id = fields.Many2one("product.product", string="Sale Product")
    pylint_score = fields.Float("Pylint Score", tracking=True)
    sh_last_update_date = fields.Date('Last Updated Date',compute='_compute_sh_last_update_date')
    sh_no_of_days = fields.Integer('No of Days',compute='_compute_sh_no_of_days')
    allow_timesheet_edit = fields.Boolean("Allow Edit Timesheet")
    odoo_edition = fields.Selection([('community','Community'),('enterprise','Enterprise')], string="Edition ")

    task_type = fields.Selection([
                ('customisation','Customisation/Improvement/Enhancement'),
                ('bug','Bug'),
                ('support','Support'),
            ], string="Task Type")
    bug_root_cause = fields.Text("Root Cause")
    corrective_action_for_bug = fields.Text("Corrective Action Taken")
    preventive_action_for_bug = fields.Text("Preventive Action")
    sh_deadline_n_estimated_hours_mendatory = fields.Boolean(related='project_id.sh_deadline_n_estimated_hours_mendatory')

    def _compute_sh_last_update_date(self):
        for rec in self:
            rec.sh_last_update_date = False
            if rec.parent_id:
                if rec.sh_product_id and rec.sh_product_id.last_updated_date:
                    rec.sh_last_update_date = rec.sh_product_id.last_updated_date
            else:
                if rec.product_template_id and rec.product_template_id.module_last_updated_date:
                    rec.sh_last_update_date = rec.product_template_id.module_last_updated_date

    def _compute_sh_no_of_days(self):
        for rec in self:
            rec.sh_no_of_days = 0
            if rec.parent_id:
                if rec.sh_product_id and rec.sh_product_id.last_updated_date:
                    rec.sh_no_of_days = (fields.Date.today() - rec.sh_product_id.last_updated_date).days
            else:
                if rec.product_template_id and rec.product_template_id.module_last_updated_date:
                    rec.sh_no_of_days = (fields.Date.today() - rec.product_template_id.module_last_updated_date).days


    sh_product_id = fields.Many2one('product.product', string="Product Variant", tracking=True)
    sh_technical_name = fields.Char(string="Technical Name", tracking=True)
    depends = fields.Many2many('sh.depends', string="Depends",)
    license = fields.Many2one('sh.license', string="License",)
    product_version = fields.Char(string="Product Version",)
    supported_browsers = fields.Many2many(
        'product.browsers', string="Supported Browsers", )
    released_date = fields.Date(string="Released",)
    last_updated_date = fields.Date(string="Last Updated",)
    live_demo = fields.Char(string="Live Demo", )
    user_guide = fields.Char(string="User Guide",)
    related_video = fields.Many2many('blog.post.video', string="Video",)
    sh_tag_ids = fields.Many2many('product.tags', string=" Tags",)
    sh_edition_ids = fields.Many2many('sh.edition', string="Edition",)
    sh_scale_ids = fields.Many2one('sh.scale', string="Product Scale",related="product_template_id.sh_scale_ids")
    sh_blog_post_ids = fields.Many2many('blog.post', string="Blogs")
    banner = fields.Binary("Banner")
    sh_product_counter = fields.Integer("Product Downloads", related="product_template_id.sh_product_counter")

    task_running = fields.Boolean("Task Running")
    task_runner = fields.Char(string="Task Runner",)
    start_time = fields.Datetime("Start Time", copy=False)
    end_time = fields.Datetime("End Time", copy=False)
    total_time = fields.Char("Total Time", copy=False)
    duration = fields.Float('Real Duration',
                            compute='_compute_duration',
                            tracking=True)
    is_user_working = fields.Boolean("Is User working ?",
                                     compute='_compute_is_user_working')

    coach_ids = fields.Many2many("res.users",string="Coaches",domain=[('share', '=', False)])
    is_appstore_project = fields.Boolean("Is AppStore Project", compute="_compute_app_store_project", store=True)

    def _compute_app_store_project(self):
        for rec in self:
            rec.is_appstore_project = False
            if self.env.company.appstore_project_id.id == rec.project_id.id:
                rec.is_appstore_project = True

    def _populate_missing_personal_stages(self):
        """
            Here we don't want to generate any personal stage
            especailly for intelliwaves project
            ['Inbox', 'Today', 'This Week', 'This Month', 'Later', 'Done', 'Canceled']
            for intelliwaves technologies this method do nothing
            that's why we commented this method and just return nothing

        """
        return
        # Assign the default personal stage for those that are missing

    @api.onchange('user_ids')
    def _onchange_user_coach(self):

        if self._origin.id:
            if self._origin.user_ids:
                self.coach_ids = False
                for user in self._origin.user_ids:
                    domain = [('user_id', '=', user._origin.id)]
                    find_employee = self.env['hr.employee'].sudo().search(domain,limit=1)
                    if find_employee.sudo().coach_id.user_id.id:
                        self.coach_ids = [(4,find_employee.sudo().coach_id.user_id.id)]
        else:
            if self.user_ids._origin:
                self.coach_ids = False
                for user in self.user_ids._origin:
                    domain = [('user_id', '=', user.id)]
                    find_employee = self.env['hr.employee'].sudo().search(domain,limit=1)
                    if find_employee.sudo().coach_id.user_id.id:
                        self.coach_ids = [(4,find_employee.sudo().coach_id.user_id.id)]

        
    @api.model
    def _compute_is_user_working(self):
        for rec in self:
            rec.is_user_working = True
            if rec and rec.timesheet_ids:
                timesheet_line = rec.timesheet_ids.filtered(
                    lambda x: x.task_id.id == rec.id and x.end_date == False
                    and x.start_date != False)
                if timesheet_line:
                    rec.is_user_working = True
                else:
                    rec.is_user_working = False
    @api.model
    @api.depends('timesheet_ids.unit_amount')
    def _compute_duration(self):
        for rec in self:
            if rec and rec.timesheet_ids:
                timesheet_line = rec.timesheet_ids.filtered(
                    lambda x: x.task_id.id == rec.id and x.end_date == False
                    and x.start_date != False)
                if timesheet_line:
                    rec.duration = timesheet_line[0].unit_amount
                else:
                    rec.duration=False
            else:
                rec.duration=False
    version_ids = fields.Many2many('sh.version', string="Version")
    is_need_integrate = fields.Boolean("Need to integrate with appstore")
    related_task = fields.Many2one(
        'project.task',
        string=" Related Task"
    )
    related_task_state = fields.Many2one('project.task.type',
                                         string=" Status",
                                         related="related_task.stage_id",)
    existing_related_task = fields.Many2one(
        'project.task',
        string="Related Task"
    )
    existing_related_task_state = fields.Many2one('project.task.type',
                                         string="Status ",
                                         related="existing_related_task.stage_id",)

    feature_expansion = fields.Selection([('existing', 'Feature Expansion - Existing Task'), ('new', 'Separate Expansion'), ('cancel', 'Not useful')], default='cancel')

    sh_is_issue = fields.Boolean(string="Is Issue",)
    end_task_bool = fields.Boolean("End Task",
                                   default=False,
                                   compute='_compute_end_task_bool')
    start_task_bool = fields.Boolean("Start Task",
                                     compute='_compute_start_task_bool')

    start_id = fields.Integer()
    project_task_change_log_ids = fields.One2many(
        'product.change.log', 'project_task_id', 'Task Change Log')

    task_runner_ids = fields.Many2many(
        'res.users', 'runner_user_rel', 'user_id', 'runner_id', string="Runner")

    responsible_user_names = fields.Char(compute='onchange_task_runner_ids')
    already_add_exist = fields.Boolean("Already Add in Exist Task")

    # git_repo = fields.Many2one('sh.git.repo',related="sh_product_id.git_repo",string="Git Repo",store=True)
    git_repo = fields.Many2one('sh.git.repo', string="Git Repo")

    def _add_sh_product_variant(self):
        for task in self:
            if not task.sh_product_id and task.parent_id:
                task_product_obj = self.env['product.product'].search([
                    ('related_sub_task', '=', task.id)
                ])
                if task_product_obj and len(task_product_obj) == 1:
                    task.sh_product_id = task_product_obj.id

    def _multi_action_add_git_repo(self):
        failed_list = []
        added_count = 0
        self._add_sh_product_variant()
        for task in self:
            if task.git_repo:
                continue
            if task.sh_product_id:
                if task.sh_product_id.git_repo:
                    task.write({'git_repo': task.sh_product_id.git_repo.id})
                    added_count += 1
                    continue
            if task.product_template_id:
                if task.product_template_id.git_repo:
                    task.write({'git_repo': task.sh_product_id.git_repo.id})
                    added_count += 1
                    continue

            failed_list.append(task.sh_technical_name or task.name)
        message = ''
        if added_count:
            message += f"Git repo added in the {added_count} task(s)\n"
        if failed_list:
            message += f"Failed to add the git repo in the {len(failed_list)} task(s):\n" + '\n'.join(failed_list)
        if not message:
            message = 'Task(s) alredy have the git repo'
        return self.popup_message(message)

    is_manager_temp = fields.Boolean(
        'Is manager Temp', default=False, tracking=True)
    is_manager = fields.Boolean(
        'Is manager', default=True, compute='get_manager', readonly=False, tracking=True)

    check_config_setting_bool = fields.Boolean(default=True,
                                               compute="_compute_project_id_check_config_setting_bool")

    upcoming_feature_ids = fields.One2many("sh.task.upcoming.feature",
                                           "task_id")
    is_temp_task = fields.Boolean(string="Temporary Task")

    account_move_id = fields.Many2one('account.move',string='Invoice Id')

    @api.depends('task_runner_ids')
    def onchange_task_runner_ids(self):
        for rec in self:

            rec.responsible_user_names = False
            names = ''
            count = 0
            for user in rec.task_runner_ids:
                if count == 0:
                    names = user.name
                    count = 1
                else:
                    names += ',' + user.name

            rec.responsible_user_names = names

    @api.model
    def get_manager(self):
        for data in self:
            if self.env.user.has_group('sh_project_task_base.group_project_officer') or self.env.user.has_group('sh_project_mgmt.group_project_task_create'):
                data.is_manager = True
            else:
                data.is_manager = False


    def _compute_start_task_bool(self):
        for rec in self:
            rec.start_task_bool = True

            if self.env.user.task_id.id == rec.id:
                rec.start_task_bool = False

    def _compute_end_task_bool(self):
        for rec in self:
            rec.end_task_bool = False
            timesheet_line = self.env['account.analytic.line'].sudo().search(
                [('task_id', '=', rec.id), ('employee_id.user_id',
                                            '=', self.env.uid), ('end_date', '=', False)],
                limit=1)
            if timesheet_line and self.env.user.task_id:
                rec.end_task_bool = True

    @api.depends("project_id")
    def _compute_project_id_check_config_setting_bool(self):
        config_appstore_id = self.env['res.config.settings'].search([])
        for rec in self:
            rec.check_config_setting_bool = True
            if self.env.user.company_id and self.env.user.company_id.appstore_project_id:
                if rec.project_id.id == self.env.user.company_id.appstore_project_id.id:
                    rec.check_config_setting_bool = False


    def create_task(self):

        if self.feature_expansion == 'existing' and self.existing_related_task :
            self.existing_related_task.write({
                'upcoming_feature_ids' :[( 0, 0, {'description' : self.name,
                                        'ref_task_id' : self.id,} )] or False,
                'stage_id': self.company_id.to_be_project_stage_id.id or False,
            })
            self.already_add_exist = True

        if self.feature_expansion == 'new' :
            task_copy_model = self.copy(default={
                'project_id': self.company_id.preappstore_project_id.id,
                'name': self.name,
                'upcoming_feature_ids' :[( 0, 0, {'description' : self.name,
                                        'ref_task_id' : self.id,} )] or False,
                'stage_id': self.company_id.feature_project_stage_id.id or False,
            })
            self.write({
                'related_task': task_copy_model.id
            })

    
    # ======= sh_task_estimation module fields ===============

    estimated_hrs = fields.Float(string="Estimated Hours(External)",tracking=True)
    estimated_internal_hrs = fields.Float(string="Estimated Hours(Internal)",tracking=True)

    is_beyond_estimation = fields.Boolean(
        "Timesheet more then Estimated Hours", compute="_is_beyond_estimation", search="_search_is_beyond")

    is_deadline_n_estimated_hrs_mendatory = fields.Boolean(compute="_compute_is_deadline_n_estimated_hrs_mendatory", store=True)
    
    created_from_alias = fields.Boolean(string="Created From Alias", default=False)

    @api.depends('project_id.sh_deadline_n_estimated_hours_mendatory')
    def _compute_is_deadline_n_estimated_hrs_mendatory(self):
        for rec in self:
            rec.is_deadline_n_estimated_hrs_mendatory = False
            if rec.project_id.sh_deadline_n_estimated_hours_mendatory and not (self.env.user.share or rec.created_from_alias):
                rec.is_deadline_n_estimated_hrs_mendatory = True
      
    @api.onchange('estimated_hrs')
    def _onchange_estimated_hrs(self):
        if self.estimated_internal_hrs == 0:
                self.estimated_internal_hrs = self.estimated_hrs

    def _search_is_beyond(self, operator, value):
        task_list = []
        if operator == '=' and value == True:
            task_ids = self.env['project.task'].sudo().search([])
            for task in task_ids:
                if task.estimated_internal_hrs > 0.0 and task.effective_hours > task.estimated_internal_hrs:
                    task_list.append(task.id)
        return [('id', 'in', task_list)]

    def _is_beyond_estimation(self):
        for task in self:
            if task.estimated_internal_hrs > 0.0 and task.effective_hours > task.estimated_internal_hrs:
                task.is_beyond_estimation = True
            else:
                task.is_beyond_estimation = False

    # def write(self, vals):
    #     if not self.env.user.has_group('sh_project_task_base.group_project_officer'):
    #         vals_list=list(vals.keys())
    #         if 'stage_id' in vals_list:
    #             vals_list.remove('stage_id')
    #         if 'sequence' in vals_list:
    #             vals_list.remove('sequence')
    #         if 'timesheet_count' in vals_list:
    #             vals_list.remove('timesheet_count')
    #         if vals_list:
    #             raise UserError("You are not Allowed Change ..")

    #     record = super(ProjectTask, self).write(vals)
    #     return record


    @api.onchange('sh_technical_name')
    def _onchange_sh_technical_name(self):
        self.ensure_one()
        if self.project_id.id != self.env.user.company_id.appstore_project_id.id:
            return
        if self._origin.parent_id:
            if self._origin.parent_id.sh_technical_name:
                self.sh_technical_name = self._origin.parent_id.sh_technical_name
            else:
                self._origin.parent_id.sh_technical_name = self.sh_technical_name
        elif self._origin.child_ids:
            if self.sh_technical_name:
                for child_task in self._origin.child_ids:
                    child_task.sh_technical_name = self.sh_technical_name

    # ========== Pop-Up Message ==========
    def popup_message(self, message):
        view = self.env.ref('sh_message.sh_message_wizard')
        context = dict(self._context or {})
        context['message'] = message
        return {
            'name': 'Task',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context
        }

    # -----------------------------------------
    #  Multi action: Add Technical Name
    # -----------------------------------------

    # def multi_action_add_tech_name(self):
    #     message = ''
    #     counter = already_has = 0
    #     product_not_found_list = []
    #     for task in self:

    #         if task.sh_technical_name:
    #             already_has += 1
    #             continue

    #         has_parent_task_without_tech_name = False
    #         if task.parent_id:
    #             if task.parent_id.sh_technical_name:
    #                 task.sh_technical_name = task.parent_id.sh_technical_name
    #                 counter += 1
    #                 continue
    #             has_parent_task_without_tech_name = True

    #         check_product_tmpl = True
    #         search_in_product = True
    #         message2 = ''

    #         # If Child Task
    #         if task.sh_product_id:
    #             search_in_product = False
    #             if task.sh_product_id.sh_technical_name:
    #                 # If product variant has tech name
    #                 task.sh_technical_name = task.sh_product_id.sh_technical_name
    #                 counter += 1
    #                 check_product_tmpl = False
    #             else:
    #                 if task.sh_product_id.product_tmpl_id:
    #                     # If product tmpl has tech name
    #                     if task.sh_product_id.product_tmpl_id.sh_technical_name:
    #                         task.sh_product_id.sh_technical_name = task.sh_product_id.product_tmpl_id.sh_technical_name
    #                         task.sh_technical_name = task.sh_product_id.product_tmpl_id.sh_technical_name
    #                         counter += 1
    #                         check_product_tmpl = False
    #                     else:
    #                         message2 = f'\nTask: {task.name}\nLinked product or its tmpl not have tech name !'
    #                 else:
    #                     message2 = f'\nTask: {task.name}\nLinked product not have tech name nor tmpl !'

    #         # If Parent Task
    #         if task.product_template_id:
    #             search_in_product = False
    #             if check_product_tmpl:
    #                 if task.product_template_id.sh_technical_name:
    #                     task.sh_technical_name = task.product_template_id.sh_technical_name
    #                     counter += 1
    #                 else:
    #                     message += f'\nTask: {task.name}\nError: Product tmpl without tech name !\n'
    #         elif not search_in_product and check_product_tmpl and message2:
    #             message += message2

    #         if search_in_product:
    #             product = self.env['product.product'].sudo().search([
    #                 ('related_sub_task', '=', task.id)
    #             ])
    #             if product:
    #                 if len(product) == 1:
    #                     task.sudo().write({
    #                         'sh_product_id': product.id,
    #                         'sh_technical_name': product.sh_technical_name
    #                     })
    #                     if not product.sh_technical_name:
    #                         message += f'\nTask: {task.name}\nError: Product without tech name !\n'
    #                     else:
    #                         counter += 1
    #                 else:
    #                     message += f'\nTask: {task.name}\nError: Multiple product found with the same task !\n'
    #             else:
    #                 product_tmpl = self.env['product.template'].sudo().search([
    #                     ('related_task', '=', task.id)
    #                 ])
    #                 if product_tmpl:
    #                     if len(product_tmpl) == 1:
    #                         task.sudo().write({
    #                             'product_template_id': product_tmpl.id,
    #                             'sh_technical_name': product_tmpl.sh_technical_name
    #                         })
    #                         if not product_tmpl.sh_technical_name:
    #                             message += f'\nTask: {task.name}\nError: Product tmpl without tech name !\n'
    #                         else:
    #                             counter += 1
    #                     else:
    #                         message += f'\nTask: {task.name}\nError: Multiple product tmpl found with the same task !\n'
    #                 else:
    #                     product_not_found_list.append(task.name)

    #         if has_parent_task_without_tech_name and task.sh_technical_name:
    #             task.parent_id.sh_technical_name = task.sh_technical_name

    #     if counter:
    #         message = f'Technical name write in the {counter} tasks.\n{message}'
    #     if already_has:
    #         message = f'\nTechnical name already has in the {already_has} tasks.'
    #     if product_not_found_list:
    #         product_not_found_str = "\n".join(product_not_found_list)
    #         message += f'\nError: Product not found for the following {len(product_not_found_list)} tasks:\n{product_not_found_str}'

    #     if message:
    #         return self.popup_message(message)
    #     else:
    #         return self.popup_message('Something went wrong !')

    def _get_responsible_user(self):
        # If child task created
        responsible_user = False
        if self.parent_id:
            if self.parent_id.product_template_id:
                if self.parent_id.product_template_id.git_repo:
                    if self.parent_id.product_template_id.git_repo.responsible_user:
                        responsible_user = self.parent_id.product_template_id.git_repo.responsible_user
        # If child task created
        elif self.product_template_id:
            if self.product_template_id.git_repo:
                if self.product_template_id.git_repo.responsible_user:
                    responsible_user = self.product_template_id.git_repo.responsible_user
        if responsible_user:
            self.sudo().write({
                'sh_project_task_base_responsible_tl_id': responsible_user.id
            })

    # --------------------------------------------

    def _tech_name_and_version_req_stage(self, vals):
        '''
            If technical name and version required at this stage,
            and if not provided, then raise an error
        '''
        if not vals.get('stage_id'):
            return
        if not self.project_id:
            return
        if self.project_id.id != self.env.user.company_id.appstore_project_id.id:
            return
        if not self.env.user.company_id.sh_tech_name_and_version_req_stage_ids:
            return
        if vals['stage_id'] not in self.env.user.company_id.sh_tech_name_and_version_req_stage_ids.ids:
            return
        if not self.sh_technical_name:
            raise UserError(_('Required the technical name at this stage !'))
        if not self.version_ids:
            raise UserError(_('Required the version at this stage !'))

    # ------------------------------------------------
    #  Technical name must be unique
    # ------------------------------------------------

    # @api.constrains('sh_technical_name', 'project_id')
    # def _sh_technical_name_constrain(self):
    #     for task in self.filtered(lambda t: t.project_id.id == t.env.user.company_id.appstore_project_id.id):
    #         if not task.sh_technical_name:
    #             continue
    #         find_tasks = self.sudo().search([
    #             ('id', '!=', task.id),
    #             ('sh_technical_name', '=', task.sh_technical_name)
    #         ])
    #         product_dict = {
    #             'templates': [],
    #             'variants': []
    #         }
    #         if find_tasks:
    #             for find_task in find_tasks:
    #                 if find_task.product_template_id:
    #                     product_dict['templates'].append(find_task.product_template_id.id)
    #                 elif find_task.sh_product_id:
    #                     product_dict['variants'].append(find_task.sh_product_id.id)
    #                 if find_task.parent_id:
    #                     # If sibling tasks
    #                     if task.parent_id:
    #                         if find_task.parent_id.id == task.parent_id.id:
    #                             continue
    #                     # parent task
    #                     if find_task.parent_id.id == task.id:
    #                         continue
    #                 # child task
    #                 if task.parent_id:
    #                     if task.parent_id.id == find_task.id:
    #                         continue
    #                 raise ValidationError(_('Technical name must be unique !'))

    #         domain = [('sh_technical_name', '=', task.sh_technical_name)]
    #         tmpls = self.env['product.template'].sudo().search(domain)
    #         if tmpls:
    #             if not product_dict['templates']:
    #                 raise ValidationError(_("Technical name must be unique !\nAlready used in product templates."))
    #             for tmpl in tmpls:
    #                 if tmpl.id not in product_dict['templates']:
    #                     raise ValidationError(_(f"Technical name must be unique !\nAlready used in product template '{tmpl.name}'"))
    #                 if tmpl.product_variant_ids:
    #                     for variant in tmpl.product_variant_ids:
    #                         if variant.sh_technical_name == task.sh_technical_name:
    #                             if not product_dict['variants']:
    #                                 raise ValidationError(_(f"Technical name must be unique !\nAlready used in product variant '{variant.name}'"))
    #                         if variant.id not in product_dict['variants']:
    #                             raise ValidationError(_(f"Technical name must be unique !\nAlready used in product variant '{variant.name}'"))
    #         variants = self.env['product.product'].sudo().search(domain)
    #         if variants:
    #             if not product_dict['variants']:
    #                 raise ValidationError(_('Technical name must be unique !\nAlready used in product variants.'))
    #             for variant in variants:
    #                 if variant.id not in product_dict['variants']:
    #                     raise ValidationError(_(f'Technical name must be unique !\nAlready used in product variant {variant.name}'))

    # ------------------------------------------------
    #  Auto tick the pending ss bool if config
    # ------------------------------------------------

    def _is_auto_tick_pending_ss_stage(self, vals):
        if not vals.get('stage_id'):
            return
        if not self.env.user.company_id.sh_pending_ss_id:
            return
        if vals['stage_id'] == self.env.user.company_id.sh_pending_ss_id.id:
            if not self.sh_pending_ss:
                self.write({
                    'sh_pending_ss': True
                })
        


    def _add_git_repo(self):
        if self.git_repo:
            return
        if self.sh_product_id:
            if self.sh_product_id.git_repo:
                self.write({'git_repo': self.sh_product_id.git_repo.id})
                return
        if self.product_template_id:
            if self.product_template_id.git_repo:
                self.write({'git_repo': self.product_template_id.git_repo.id})
                return

    # ------------------------------------------------
    #  Override methods
    # ------------------------------------------------

    def write(self, vals):
        # check validation of deadline
        for rec in self:
            # if rec.stage_id.id == rec.project_id.company_id.done_project_stage_id.id and not rec.project_id.is_task_editable_in_done_stage:
            #     if not (vals.get('stage_id') is None and vals.get('stage_history_line', False)):
            #         raise ValidationError("You cannot edit a task or add a timesheet if the task is in the Done stage.")
            
            if vals.get('stage_id') and not vals.get('date_deadline') and not rec.date_deadline and rec.is_deadline_n_estimated_hrs_mendatory:
                raise UserError("Please set Deadline of task !")
                        
            # if vals.get('date_deadline',False) and vals.get('date_deadline',False) < str(fields.Date.today()):
            #     raise UserError("You can not set past deadline ! ")
            
            if 'project_id' in vals:
                new_project_id = vals.get('project_id')
                    # Move subtasks to the new project
                rec.child_ids.write({'project_id': new_project_id})

                # Move timesheets to the new project
                rec.timesheet_ids.write({'project_id': new_project_id})
        
        status = super(ProjectTask,self).write(vals)
        if vals.get('sh_product_id') or vals.get('product_template_id'):
            self._add_git_repo()
        if 'project_id' in vals:
            self._compute_app_store_project()
        if 'product_template_id' in vals:
            self._get_responsible_user()
        if 'stage_id' in vals or 'project_id' in vals:
            self._tech_name_and_version_req_stage(vals)
        if 'stage_id' in vals:
            self._is_auto_tick_pending_ss_stage(vals)

        if 'user_ids' in vals:
            # AUTO ADD USERS IN PROJECT WHEN ADDED IN TASK
            for user in self.user_ids:
                project_user_ids = self.project_id.responsible_user_ids.ids 
                if user.id not in project_user_ids:
                    project_user_ids.append(user.id)
                self.project_id.sudo().responsible_user_ids = project_user_ids
        
        return status

    @api.model_create_multi
    def create(self, vals_list):
        # Iterate through each task data in vals_list
        # for vals in vals_list:
        #     # Set 'date_deadline' to one week from now if it is not provided
        #     if not vals.get('date_deadline'):
        #         vals['date_deadline'] = (datetime.now() + timedelta(weeks=1)).date()
        tasks = super(ProjectTask, self).create(vals_list)

        for task in tasks:
            # Add Default Assignees from Project to Tasks
            if 'default_project_id' in self.env.context:
                project_id = self.env.context.get('default_project_id')
                project = self.env['project.project'].sudo().browse(project_id)
                if project.default_task_users_ids.ids:
                    task['user_ids'] = [(6,0,list(set(project.default_task_users_ids.ids + task.user_ids.ids)))]

            if task.is_deadline_n_estimated_hrs_mendatory and task.estimated_hrs <= 0:
                raise UserError("Estimated Hours must be positive.")
            task._compute_app_store_project()
            task._get_responsible_user()
            task._add_git_repo()

            # Adds Log note when task is created.
            task._message_log(body="Task Created")
        return tasks

    # ------------------------------------------------
    #  Fields
    # ------------------------------------------------

    sh_project_task_base_responsible_tl_id = fields.Many2one(
        'res.users', string='Responsible TL', tracking=True, domain=[('share', '=', False)])
    sh_project_task_base_dev_id = fields.Many2one(
        'res.users', string='Developer 1', tracking=True, domain=[('share', '=', False)])
    sh_project_task_base_dev2_id = fields.Many2one(
        'res.users', string='Developer 2', tracking=True, domain=[('share', '=', False)])
    sh_project_task_base_functional_id = fields.Many2one(
        'res.users', string='Functional', tracking=True, domain=[('share', '=', False)])

    sh_project_task_base_support_dev_id = fields.Many2one(
        'res.users', string='Supporting Developer', tracking=True, domain=[('share', '=', False)])
    sh_project_task_base_tester_id = fields.Many2one(
        'res.users', string='Tester', tracking=True, domain=[('share', '=', False)])
    sh_project_task_base_designer_id = fields.Many2one(
        'res.users', string='Designer', tracking=True, domain=[('share', '=', False)])
    sh_project_task_base_index_by_id = fields.Many2one(
        'res.users', string='Index By', tracking=True, domain=[('share', '=', False)])
    sh_project_task_base_marketed_by_id = fields.Many2one(
        'res.users', string='Marketed By', tracking=True, domain=[('share', '=', False)])

    # pylint_score alread has
    sh_project_task_base_multi_comapy = fields.Boolean(
        'Multi Company', tracking=True)
    sh_project_task_base_multi_website = fields.Boolean(
        'Multi Website', tracking=True)
    sh_project_task_base_check_downgrade = fields.Boolean(
        'Check Downgrade', tracking=True)
    sh_project_task_base_cr_count = fields.Integer(
        'CR', compute='_compute_cr_count')
    sh_migration_need_functional_support = fields.Boolean(
        'Need Functional Support', tracking=True)
    sh_need_testing = fields.Boolean('Need Testing ?', tracking=True)
    sh_pending_ss = fields.Boolean('Pending Screenshot', tracking=True)
    sh_targeted_app = fields.Boolean('Targeted App', tracking=True)
    not_billable = fields.Boolean("Not Billable", tracking=True)
    timesheet_zero_for_not_billable_task = fields.Boolean(compute="_compute_timesheet_zero_for_not_billable_task")

    # ------------------------------------------------
    #  Other Methods
    # ------------------------------------------------

    @api.depends('not_billable')
    def _compute_timesheet_zero_for_not_billable_task(self):
        for rec in self:
            rec.timesheet_zero_for_not_billable_task = False
            if rec.not_billable:
                timesheet_ids = rec.env['account.analytic.line'].sudo().search([('task_id','=',rec.id)])

                if timesheet_ids:

                    for t in timesheet_ids:
                        t.with_context(by_pass_timesheet_lock_validation = True).write({'unit_amount_invoice' : 0})

                    rec.timesheet_zero_for_not_billable_task = True

    def _compute_cr_count(self):
        for task in self:
            task.sh_project_task_base_cr_count = self.env['sh.task.upcoming.feature'].search_count([
                ('task_id', '=', task.id)
            ])
           
    def un_tick_not_billable(self):
        self.write({'not_billable':False})
    
    def smart_btn_open_cr(self):
        view = {
            'name': 'CR',
            'type': 'ir.actions.act_window',
            'res_model': 'sh.task.upcoming.feature',
            'domain': [('task_id', '=', self.id)],
            'context': {
                'default_task_id': self.id,
                'create': False
            },
            'target': 'current',
        }
        if self.sh_project_task_base_cr_count == 0:
            view.update({
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': self.env.ref('sh_project_task_base.sh_task_upcoming_feature_view_form').id
            })
            return view
        view.update({
            'view_type': 'form',
            'view_mode': 'tree,form',
        })
        return view

    def multi_action_mass_update_task(self):
        # if self.env.user.has_group('sh_task_time.group_project_officer'):
        return {
            'name': 'Mass Update',
            'res_model': 'sh.mass.update.task.wizard',
            'view_mode': 'form',
            'context': {
                'default_task_ids': [(6, 0, self.env.context.get('active_ids'))]
            },
            'view_id': self.env.ref('sh_project_task_base.sh_mass_update_task_wizard_form_view').id,
            'target': 'new',
            'type': 'ir.actions.act_window'
        }
        # else:
        #     raise ValidationError("You are not authorized to perform this !")

    # Send Notification and create log when task has the bug and cr while moving task to the UAT or Main stage
    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        if self.stage_id.sh_is_uat or self.stage_id.sh_is_push_to_main:
            bugs = self.env['sh.module.bug'].sudo().search([('task_id', '=', self._origin.id)])
            titles = []
            for bug in bugs:
                if bug.state_id not in self.env.company.sh_migration_bug_complete_state_ids: 
                    titles.append(bug.title)

            if titles:  # Only raise error if there are unresolved bugs
                raise ValidationError(
                    _(f"Bug Found in Task: {self.name}\nBugs: {', '.join(titles)}"))
            