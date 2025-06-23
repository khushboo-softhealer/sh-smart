# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from datetime import date, datetime, timedelta, time
import math
import pytz
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProjectMgmtSale(models.Model):
    _inherit = 'sale.order'

    project_id = fields.Many2one(domain="[('pricing_type', '!=', 'employee_rate'), ('analytic_account_id', '!=', False)]",readonly=False,copy=False)

    sh_pricing_mode = fields.Selection([
        ('fp', 'FP - Fixed Price'),
        ('tm', 'T&M - Time and Material'),
    ], string="Pricing Model", readonly=False ,store=True)
    sh_fp_based_on = fields.Selection([
        ('no_milestone', 'No Milestone - One shot'),
        ('milestone', 'Implementation Project'),
    ], string='FP Based On', readonly=False,store=True)
    sh_tm_based_on = fields.Selection([
            ('success_pack', 'Success Packs Based'),
            ('billable', 'Billable Hours Based'),
        ], string='T&M Based On',
        help='Success Packs Based (Renewable required based on usage) - SO\nBillable Hours Based (Monthly billable invoice created) - MANUALLY', readonly=False,store=True)

    sh_project_stage_tmpl_id = fields.Many2one(
        'sh.project.project.stage.template',
        string='Project Stage Template', readonly=False,store=True
    )

    # Approx Planned Date
    sh_planned_date_from = fields.Date('Planned Date From', default=datetime.now())
    sh_planned_date_to = fields.Date('Planned Date To')
    # Total Work Duration
    sh_total_work_duration = fields.Integer('Total Work Duration (Days)', readonly=False,store=True)
    # Actual Planned Date
    # sh_actual_planned_date = fields.Date('Actual Planned Date')
    sh_actual_planned_date_from = fields.Date('Actual Planned Date From', default=datetime.now())
    sh_actual_planned_date_to = fields.Date('Actual Planned Date To')
    
    pricing_model_alert = fields.Boolean(
        string="",compute='_company_pricing_model_alert')
    
    project_manager = fields.Many2one("res.users",string="Project Manager",default=lambda self:self.env.user, required=True,domain=[('share', '=', False)], readonly=False)

    estimated_hrs = fields.Float(string="Estimated Hours", copy=False,compute='_compute_estimated_hrs')
    sh_is_sales_order_approved = fields.Boolean(string="Sales Order Approved",copy=False,readonly=True)
    sh_is_sales_order_approval_required = fields.Boolean(copy=False)
    sh_designing_head = fields.Many2one("res.users",string="Designing Head",domain=[('share', '=', False)],tracking=True)
    
    @api.depends('order_line','order_line.sale_line_estimation_template_line')
    def _compute_estimated_hrs(self):
        for rec in self:
            rec.estimated_hrs = 0.0
            if not rec.website_id:
                estimated_hrs = 0.0
                for line in rec.order_line:
                    if line.sale_line_estimation_template_line:
                        for estimation_line in line.sale_line_estimation_template_line:
                            if estimation_line:
                                estimated_hrs += estimation_line.estimated_hours
                rec.estimated_hrs = estimated_hrs

    @api.model
    def default_get(self, fields):
        res = super(ProjectMgmtSale, self).default_get(fields)
        pricing_model_alert = False
        if not self.sh_pricing_mode:
            pricing_model_alert = True
        else:
            pricing_model_alert = False
        res.update({
            'pricing_model_alert': pricing_model_alert,
        })
        return res

    def _company_pricing_model_alert(self):
        for rec in self:
            
            rec.pricing_model_alert = False
            if not rec.sh_pricing_mode:
                rec.pricing_model_alert = True
            else:
                rec.pricing_model_alert = False

    def manually_create_project(self):
        if not self.sh_pricing_mode:
            raise ValidationError("Please set Pricing mode !")
        
        if self.sh_pricing_mode == 'tm' and self.sh_tm_based_on =='billable':
            raise ValidationError("Project cannot be created for T&M billable pricing mode !")
        
        if self.sh_pricing_mode and self.estimated_hrs <= 2:
            raise ValidationError("Please set Estimated Hours !")
        
        estimation_line = False

        for line in self.order_line:
            if line.sale_line_estimation_template_line:
                estimation_line = True
                break
            
        if not estimation_line:
            raise ValidationError("Project cannot be created without Estimation !")
        
        self.update({'sh_planned_date_from':datetime.now()})
        self._onchange_total_work_duration()
        for order in self:
            if order.project_id and order.sh_task_id:
                order.sudo()._move_task_to_existing_project(order.project_id)
                order.update_project_detail(order.project_id)
            elif not order.project_id and order.sh_task_id:
                created_project = order.sudo()._create_project()
                order.sudo()._move_task_to_existing_project(created_project)
            elif order.project_id and not order.sh_task_id:
                # print("")
                order.update_project_detail(order.project_id)
                # order.sudo()._create_task_in_existing_project()
            else:
                order.sudo()._create_project()
                
    def approve_sale_order(self):
        self.sh_is_sales_order_approved = True
        self.sh_is_sales_order_approval_required = False
        self.notify_sales_person_for_approved()

    def action_quotation_send(self):
        """ Opens a wizard to compose an email, with relevant mail template loaded by default """
        self.ensure_one()

        required_fields = []       
        if not self.partner_invoice_id.phone :
            required_fields.append('Phone Number')
        if not self.partner_invoice_id.email :
            required_fields.append('Email')

        if not self.partner_invoice_id.street :
            required_fields.append('Address')
            
        if not self.partner_invoice_id.mobile :
            required_fields.append('Mobile Number')

        if not self.partner_invoice_id.country_id :
            required_fields.append('Country')
        
        if required_fields:
            fields = ', '.join(required_fields)
            raise ValidationError(f"Please set This Fields in Invoice Address Of customer '{fields}'.")

        
        if not self.website_id and not self.sh_pricing_mode:
            raise ValidationError("Please set Pricing Model !")
                
        # if self.partner_id.contact:

            
        if self.sh_pricing_mode:

            estimation_line = False

            for line in self.order_line:
                if line.sale_line_estimation_template_line:
                    estimation_line = True
                    break
                
            if not estimation_line or not self.sh_planned_date_to:
                raise ValidationError("You cannot send Quote without Estimation , Approx Plan Date & Total work duration in Project Details Tab !")

            if not self.sh_is_sales_order_approved:
                sales_total_amount = self.tax_totals.get('amount_untaxed',None)
                min_estimated_hrs_price = int(self.env['ir.config_parameter'].sudo().get_param('sh_project_mgmt.sales_estimated_hrs_price_in_usd'))

                pricelist_currency = self.pricelist_id.currency_id
                eur_currency = self.env.ref('base.EUR')
                usd_currency = self.env.ref('base.USD')
                inr_currency = self.env.ref('base.INR')
                today_date = date.today()

                self.sh_is_sales_order_approval_required = False

                if pricelist_currency == usd_currency:
                    if sales_total_amount < (self.estimated_hrs * min_estimated_hrs_price):
                        self.sh_is_sales_order_approval_required = True

                elif pricelist_currency == eur_currency:
                    # Convert USD to EUR
                    converted_amount = usd_currency._convert(from_amount=min_estimated_hrs_price,to_currency=eur_currency,company=self.env.company,date=today_date)
                    if sales_total_amount < (self.estimated_hrs * converted_amount):
                        self.sh_is_sales_order_approval_required = True

                elif pricelist_currency == inr_currency:
                    # Convert USD to INR
                    converted_amount = usd_currency._convert(from_amount=min_estimated_hrs_price,to_currency=eur_currency,company=self.env.company,date=today_date)
                    if sales_total_amount < (self.estimated_hrs * converted_amount):
                        self.sh_is_sales_order_approval_required = True

                if self.sh_is_sales_order_approval_required:
                    # Notify sales manager
                    self.notify_salesmanger_for_approval()
                    self.env.cr.commit()
                    raise ValidationError("You cannot send Mail without sales manager approval !")

        return super().action_quotation_send()

    def notify_salesmanger_for_approval(self):
        # Notify sales manager
        sales_managers = self.env['res.users'].sudo().search([('groups_id','=',self.env.ref('sales_team.group_sale_manager').id)])
        if sales_managers:
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            for user in sales_managers:
                self.env['user.push.notification'].sudo().push_notification(
                    [user],
                    'Sales Manager Approval Required','Sales Order Approval Required !',
                    f"{base_url}/mail/view?model=sale.order&res_id={self.id}",
                    'sale.order',
                    self.id,
                    'sale'
                )

            
    def notify_sales_person_for_approved(self):
        # Notify sales person
        sales_person = self.user_id
        if sales_person:
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            self.env['user.push.notification'].sudo().push_notification(
                [sales_person],
                'Sales Order Approved','Sales Order Approved !',
                f"{base_url}/mail/view?model=sale.order&res_id={self.id}",
                'sale.order',
                self.id,
                'sale'
            )

    def _create_project(self):
        '''
            Create the project based on the Pricing Model
            1) FP (NO MILESTONE): Single main project
            2) FP (MILESTONE): 1 Main project, Line wise sub projects
            3) T&M (Success Packs Based): Find Project for the customer, Create one if not find
        '''
        if not self.sh_pricing_mode:
            return
        
       

        partner = False
        sale_order_task_id = False
        if self.partner_id.parent_id:
            partner = self.partner_id.parent_id
            # project_name = self.partner_id.parent_id.name
        else:
            partner = self.partner_id
            # project_name = self.partner_id.name
        # project_name += f" {self.name}"

        user_list = []
        for user in self.sh_responsible_user_ids:
            user_list.append((4, user.id))
        if self.responsible_user_id:
            user_list.append((4, self.responsible_user_id.id))

        invoice_id_int = False
        if self.invoice_ids:
            for invoice in self.invoice_ids:
                if invoice.move_type == 'out_invoice' and invoice.state != 'cancel':
                    invoice_id_int = invoice.id
                    break

        from_date = self.sh_planned_date_from
        to_date = self.sh_planned_date_to
        print("LLLLLLLLLLLLLLLLLLLL",to_date)
        sale_order_project_id = False
        
        project_vals = {
            'name': f"{partner.name} {self.name}",
            'partner_id': partner.id,
            'date_start': from_date,
            'date': to_date,
            'allocated_hours': self.estimated_hrs,
            'sh_pricing_mode': self.sh_pricing_mode,
            'sh_fp_based_on': self.sh_fp_based_on,
            'sh_tm_based_on': self.sh_tm_based_on,
            'responsible_user_ids': user_list,
            'project_type_selection':'external',
            'odoo_version':self.odoo_version.id,
            'sh_edition_id':self.sh_edition_id.id,
            'privacy_visibility':'followers',
            'sh_technical_head':self.responsible_user_id.id,
            'sh_designing_head':self.sh_designing_head.id,
            'user_id':self.project_manager.id,

        }
        if self.project_manager:
            project_manager = self.project_manager
        else:
            project_manager = self.env['res.users'].sudo().search([('login','=','chandrika@softhealer.com')],limit=1)
        if project_manager:
            project_vals.update({'user_id':project_manager.id})
        # check new stage of project
        new_stage = self.env['project.project.stage'].sudo().search([('is_new_stage','=',True)],limit=1)
        if new_stage:
            project_vals.update({'stage_id':new_stage.id})

        if self.env.user.company_id.project_stage_template_id:
            project_vals.update({
                'sh_stage_template_id': self.env.user.company_id.project_stage_template_id.id,
                'sh_stage_ids':[(6, 0, self.env.user.company_id.project_stage_template_id.stage_ids.ids)]
            })
        if self.sh_project_stage_tmpl_id:
            project_vals.update({
                'sh_project_stage_tmpl_id': self.sh_project_stage_tmpl_id.id,
            })
            if self.sh_project_stage_tmpl_id.sh_default_stage_id:
                project_vals.update({
                    'stage_id': self.sh_project_stage_tmpl_id.sh_default_stage_id.id
                })

        # FP
        if self.sh_pricing_mode == 'fp':

            # 1) FP (NO MILESTONE): Single main project
            if self.sh_fp_based_on == 'no_milestone':
                sale_order_project_id = self.env['project.project'].sudo().create(project_vals)
                self._notify_accountable(sale_order_project_id)

                #update users from estimation
                project_description = ''
                for line in self.order_line:
                    #update analytic account at line level
                    line.sudo().write({'analytic_distribution':{sale_order_project_id.analytic_account_id.id:100}})

                    project_description += '\n' + line.name
                    if line.sale_line_estimation_template_line:
                        for estimation_line in line.sale_line_estimation_template_line:
                            if estimation_line.accountable_user_ids:
                                for accountable_user in estimation_line.accountable_user_ids:
                                    user_list.append((4, accountable_user.id))
                            if estimation_line.responsible_user_ids:
                                for responsible_user in estimation_line.responsible_user_ids:
                                    user_list.append((4, responsible_user.id))


                sale_order_project_id.sudo().write({'responsible_user_ids': user_list,
                                                    'description' : project_description})

                # link estimation lines from sale order line here
                for line in self.order_line:
                    if line.sale_line_estimation_template_line:
                        for estimation_line in line.sale_line_estimation_template_line:
                            estimation_line.project_id=sale_order_project_id.id

            # 2) FP (MILESTONE): 1 Main project, Line wise sub projects
            elif self.sh_fp_based_on == 'milestone':
                sale_order_project_id = self.env['project.project'].sudo().search([
                    ('partner_id', '=', partner.id)
                ], limit=1)
                
                if not sale_order_project_id:

                    sale_order_project_id = self.env['project.project'].sudo().create(project_vals)

                project_vals['sh_parent_id'] = sale_order_project_id.id
                for line in self.order_line:
                    project_description = line.name

                    project_vals.update({
                        'name': f"{sale_order_project_id.name} ({line.name})",
                        'allocated_hours': line.product_uom_qty
                    })

                    #update users from estimation
                    line_user_list = []
                    line_user_list.extend(user_list)
                    if line.sale_line_estimation_template_line:
                        for estimation_line in line.sale_line_estimation_template_line:
                            if estimation_line.accountable_user_ids:
                                for accountable_user in estimation_line.accountable_user_ids:
                                    line_user_list.append((4, accountable_user.id))
                            if estimation_line.responsible_user_ids:
                                for responsible_user in estimation_line.responsible_user_ids:
                                    line_user_list.append((4, responsible_user.id))
                    project_vals['responsible_user_ids'] = line_user_list


                    child_project_id = self.env['project.project'].sudo().create(project_vals)
                    self._notify_accountable(child_project_id)
                    #update analytic account at line level
                    line.sudo().write({'analytic_distribution':{child_project_id.analytic_account_id.id:100}})

                    # link estimation lines from sale order line here
                    if line.sale_line_estimation_template_line:
                        for estimation_line in line.sale_line_estimation_template_line:
                            estimation_line.project_id = child_project_id.id

        # T&M
        elif self.sh_pricing_mode == 'tm':

            # 3) T&M (Success Packs Based): Find Project for the customer, Create one if not find
            if self.sh_tm_based_on == 'success_pack':
                sale_order_project_id = self.env['project.project'].sudo().search([
                    ('partner_id', '=', partner.id)
                ], limit=1)
                allocated_hours = sale_order_project_id.allocated_hours
                if not sale_order_project_id:
                    allocated_hours = 0.0
                    project_vals['allocated_hours'] = 0.0
                    sale_order_project_id = self.env['project.project'].sudo().create(project_vals)
                
                self._notify_accountable(sale_order_project_id)
                # project_vals['sh_parent_id'] = sale_order_project_id.id
                line_user_list = []
                line_user_list.extend(user_list)
                
                for line in self.order_line[0]:
                    # project_vals.update({
                    #     'name': f"{sale_order_project_id.name} ({line.product_uom_qty} Hours) ",
                    #     'allocated_hours': line.product_uom_qty
                    # })
                    allocated_hours +=  line.product_uom_qty
                    #update users from estimation
                    
                    if line.sale_line_estimation_template_line:
                        for estimation_line in line.sale_line_estimation_template_line:
                            if estimation_line.accountable_user_ids:
                                for accountable_user in estimation_line.accountable_user_ids:
                                    line_user_list.append((4, accountable_user.id))
                            if estimation_line.responsible_user_ids:
                                for responsible_user in estimation_line.responsible_user_ids:
                                    line_user_list.append((4, responsible_user.id))
                    # project_vals['responsible_user_ids'] = line_user_list


                    # child_project_id = self.env['project.project'].sudo().create(project_vals)
                    # line.sudo().write({'project_id': child_project_id.id})
                    #update analytic account at line level
                    line.sudo().write({'analytic_distribution':{sale_order_project_id.analytic_account_id.id:100}})


                    # link estimation lines from sale order line here
                    if line.sale_line_estimation_template_line:
                        for estimation_line in line.sale_line_estimation_template_line:
                            estimation_line.project_id = sale_order_project_id.id


                sale_order_project_id.sudo().write({'allocated_hours':allocated_hours,
                                                        'date':to_date,
                                                        'responsible_user_ids':line_user_list})
                # sale_order_task_id = self.env['project.task'].sudo().create({
                #     'name': f"{partner.name} {self.name}",
                #     'project_id': sale_order_project_id.id,
                #     'partner_id': sale_order_project_id.partner_id.id,
                #     'user_ids': user_list,
                #     'account_move_id': invoice_id_int,
                #     'date_deadline': to_date,
                #     'estimated_hrs': self.estimated_hrs,
                #     'planned_hours': self.estimated_hrs,
                #     'timesheet_from_date': from_date,
                #     'timesheet_to_date': to_date,
                    
                # })
            elif self.sh_tm_based_on == 'billable':
                print("\n\n\n>>> Sale Order pack: T&M billable flow perform here ... ")

        sale_order_vals = {}
        if sale_order_project_id:
            sale_order_vals.update({'project_id': sale_order_project_id.id})
        if sale_order_task_id:
            sale_order_vals.update({'sh_task_id': sale_order_task_id.id})
        if sale_order_vals:
            self.sudo().write(sale_order_vals)

        return sale_order_project_id
    
    def _notify_accountable(self, project):
        task_notification_ids = []
        if self.responsible_user_id:
            task_notification_ids = [self.responsible_user_id]
        #notification to accoutable of all department
        for line in self.order_line:
            if line.sale_line_estimation_template_line:
                for estimation_line in line.sale_line_estimation_template_line:
                    if estimation_line.accountable_user_ids:
                        for accountable_user in estimation_line.accountable_user_ids:
                            task_notification_ids.append(accountable_user)

        if len(task_notification_ids) > 0:
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            self.env['user.push.notification'].sudo().push_notification(
                task_notification_ids,
                'Project Confirmed','Project Confirmed By client !',
                f"{base_url}/mail/view?model=project.project&res_id={project.id}",
                'project.project',
                project.id,
                'project'
            )

    def _move_task_to_existing_project(self,project):
        
        if not self.sh_pricing_mode:
            return
        
        resp_user_ids = self.sh_responsible_user_ids.ids
        task = self.sh_task_id

        if task.user_ids:
            resp_user_ids += task.user_ids.ids

        # ticket_name_list = []
        # if self.sh_sale_ticket_ids:
        #     for ticket in self.sh_sale_ticket_ids:
        #         ticket_name_list.append(ticket.name)
        # ticket_names = ''
        # if ticket_name_list:
        #     ticket_names = ', '.join(ticket_name_list)

        deliver_date = date.today()
        if self.sh_planned_date_to:
            deliver_date = deliver_date
        elif self.estimated_hrs:
            deliver_date += timedelta(math.ceil(self.estimated_hrs/8.5))

        description = ''
        for line in self.order_line:
            if not line.product_id:
                continue
            if line.product_id.sh_technical_name and line.product_id.name and line.name:
                description += f"<b>{line.product_id.name}</b> ({line.product_id.sh_technical_name})<br/>{line.name}<br/><br/>"
            elif line.product_id.name and line.name:
                description += f"<b>{line.product_id.name}</b><br/>{line.name}<br/><br/>"

        task_vals = {
            # 'name' : f"{self.partner_id.name} {self.name} {ticket_names}",
            'sh_ticket_ids':[(6,0,self.sh_sale_ticket_ids.ids)],
            'sh_sale_id':self.id,
            'date_deadline' : deliver_date,
            'user_ids' : [(6, 0, resp_user_ids)],
            "description" : description or '' + task.description or '',
            'odoo_edition':self.odoo_edition,
            'estimated_hrs' : self.estimated_hrs,
            'estimated_internal_hrs':self.estimated_hrs,
            # 'account_move_id':find_invoice.id,
            'stage_id':self.env.user.company_id.developement_project_stage_id.id,
            'project_id':project.id
        }
        if self.odoo_version:
            task_vals.update({'version_ids':[(6,0,[self.odoo_version.id])]})

        task.sudo().with_context(bypass_done_task=True).write(task_vals)

        task_notification_ids = []
        if self.responsible_user_id:
            task_notification_ids = [self.responsible_user_id]
        #notification to accoutable of all department
        for line in self.order_line:
            if line.sale_line_estimation_template_line:
                for estimation_line in line.sale_line_estimation_template_line:
                    if estimation_line.accountable_user_ids:
                        for accountable_user in estimation_line.accountable_user_ids:
                            task_notification_ids.append(accountable_user)

        if len(task_notification_ids) > 0:
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            self.env['user.push.notification'].sudo().push_notification(
                task_notification_ids,
                'Project Confirmed','Project Confirmed By client !',
                f"{base_url}/mail/view?model=project.task&res_id={task.id}",
                'project.task',
                task.id,
                'project'
            )

        self.env['mail.message'].sudo().create({
            'message_type' : 'comment',
            'model' : 'project.task',
            'res_id' : task.id,
            'author_id' : self.env.user.partner_id.id,
            'body' : description
        })

    def update_project_detail(self,project):
        to_date = project.date
        
        if self.sh_planned_date_to:
            to_date = self.sh_planned_date_to
        project.sudo().write({'allocated_hours': project.allocated_hours + self.estimated_hrs,
                        'date':to_date,
                        'sh_pricing_mode':self.sh_pricing_mode,
                        'sh_fp_based_on':self.sh_fp_based_on,
                        'sh_tm_based_on':self.sh_tm_based_on,
                            'user_id':self.project_manager.id,
                            })

        for line in self.order_line:
            #update analytic account at line level
            if not line.analytic_distribution:
                line.sudo().write({'analytic_distribution':{project.analytic_account_id.id:100}})



    def action_confirm(self):
        # status = super().action_confirm()

        if not self.website_id and not self.sh_pricing_mode:
            raise ValidationError("Please set Pricing Model !")
            
        if self.sh_pricing_mode:

            estimation_line = False

            for line in self.order_line:
                if line.sale_line_estimation_template_line:
                    estimation_line = True
                    break
                
            if not estimation_line or not self.sh_planned_date_to:
            
                raise ValidationError("You cannot send Quote without Estimation , Approx Plan Date & Total work duration in Project Details Tab !")
            

        
        self.update({'sh_planned_date_from':datetime.now()})
        self._onchange_total_work_duration()
        for order in self:
            if order.project_id and order.sh_task_id:
                order.sudo()._move_task_to_existing_project(order.project_id)
                order.update_project_detail(order.project_id)
            elif not order.project_id and order.sh_task_id:
                created_project = order.sudo()._create_project()
                order.sudo()._move_task_to_existing_project(created_project)
            elif order.project_id and not order.sh_task_id:
                # print("")
                order.update_project_detail(order.project_id)
                # order.sudo()._create_task_in_existing_project()
            else:
                order.sudo()._create_project()
        return super().action_confirm()

    def _get_holiday_count(self, from_date, to_date):
        # ==================================================
        # TODO: NEED TO ADD RESSOURCE calendar ID HERE DYNAMICALLY
        # ==================================================
        if not self.env.company.resource_calendar_id:
            return 0

        # local_tz = company_tz = pytz.timezone('Asia/Kolkata')
        # # local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
        # # Convert from_date and to_date to the company's time zone
        # from_date = company_tz.localize(datetime.combine(from_date, datetime.min.time()))
        # to_date = company_tz.localize(datetime.combine(to_date, datetime.min.time()))

        # Convert from_date and to_date to UTC for database query
        # from_date_utc = from_date.astimezone(pytz.UTC)
        # to_date_utc = to_date.astimezone(pytz.UTC)

        # from_date = datetime.combine(from_date, datetime.min.time())
        # to_date = datetime.combine(to_date, time(23, 59, 59))

        # Old Condition
        # calendar_id = %s AND holiday_id IS NULL AND date_from >= %s AND date_to <= %s
        # self.env.cr.execute(calendar_leaves_query, (self.env.company.resource_calendar_id.id, from_date, to_date))

        holidays = 0

        calendar_leaves_query = """
            SELECT *
            FROM resource_calendar_leaves
            WHERE
                calendar_id = %s AND holiday_id IS NULL AND (date_from >= %s AND (date_to <= %s OR date_from <= %s))
            """
        self.env.cr.execute(calendar_leaves_query, (self.env.company.resource_calendar_id.id, from_date, to_date, to_date))
        calendar_leaves_ids = self.env.cr.fetchall()
        calendar_leaves_record = self.env['resource.calendar.leaves'].browse(record[0] for record in calendar_leaves_ids)
        # calendar_leaves_record = self.env['resource.calendar.leaves'].search([
        #     '|',
        #     ('date_to', '<=', to_date),
        #     ('date_from', '<=', to_date),
        #     ('date_from', '>=', from_date),
        # ])

        if calendar_leaves_record:
            # for leave in calendar_leaves_record:
            #     if leave.date_from.replace(tzinfo=pytz.utc).astimezone(local_tz).date() <= to_date.replace(tzinfo=pytz.utc).astimezone(local_tz).date():
            #         holidays += (leave.date_to - leave.date_from).days + 1
            #     print(f">>> leave.name: {leave.name} | Actual: {(leave.date_to - leave.date_from).days + 1} | Consider: {(leave.date_to - leave.date_from).days + 1}")
            #     print(f">>> {leave.date_from} | {leave.date_from.replace(tzinfo=pytz.utc).astimezone(local_tz).date()}, | {to_date.replace(tzinfo=pytz.utc).astimezone(local_tz).date()} |  {to_date}, | {leave.date_from > to_date}")
            holidays = sum((leave.date_to - leave.date_from).days + 1 for leave in calendar_leaves_record)

        calendar_leaves_query = """
            SELECT *
            FROM resource_calendar_leaves
            WHERE
                calendar_id = %s AND holiday_id IS NULL AND (date_from <= %s AND (date_to >= %s AND date_to <= %s))
            """
        self.env.cr.execute(calendar_leaves_query, (self.env.company.resource_calendar_id.id, from_date, from_date, to_date))

        # If the selected from_date is between the Holiday
        calendar_leaves_ids = self.env.cr.fetchall()
        calendar_leaves_record = self.env['resource.calendar.leaves'].browse(record[0] for record in calendar_leaves_ids)
        # calendar_leaves_record = self.env['resource.calendar.leaves'].search([
        #     ('date_to', '>=', from_date),
        #     ('date_to', '<=', to_date),
        #     ('date_from', '<=', from_date),
        # ])

        if calendar_leaves_record:
            from_date = datetime.combine(from_date, datetime.min.time())
            holidays += sum((leave.date_to - from_date).days + 1 for leave in calendar_leaves_record)

        return holidays

    def _get_sunday_and_holiday_count(self, last_sunday_count=0, last_holiday_count=0):
        # count = 0
        diff_sunday_count = 0
        diff_holiday_count = 0

        new_sunday_count = self._sunday_count(self.sh_planned_date_from, self.sh_planned_date_to)
        if new_sunday_count:
            diff_sunday_count = new_sunday_count - last_sunday_count

        new_holiday_count = self._get_holiday_count(self.sh_planned_date_from, self.sh_planned_date_to)
        if new_holiday_count:
            diff_holiday_count = new_holiday_count - last_holiday_count

        if diff_sunday_count or diff_holiday_count:
            self.sh_planned_date_to += timedelta(days=diff_sunday_count+diff_holiday_count)
            self._get_sunday_and_holiday_count(new_sunday_count, new_holiday_count)
            # count += self._get_sunday_and_holiday_count(new_sunday_count, new_holiday_count)

        # return count

    @api.onchange('sh_total_work_duration', 'sh_planned_date_from')
    def _onchange_total_work_duration(self):
        self.ensure_one()
        if not (self.sh_total_work_duration and self.sh_planned_date_from):
            return
        self.sh_planned_date_to = self.sh_planned_date_from + timedelta(days=self.sh_total_work_duration-1)
        self._get_sunday_and_holiday_count()

    # ---------------------------------------------------------
    # TO SELECT PRICING MODE AND FP BASE FROM PROJECT TEMPLATE
    # ---------------------------------------------------------
    @api.onchange('sh_project_stage_tmpl_id')
    def onchange_project_stage_template(self):
        self.ensure_one()
        if self.sh_project_stage_tmpl_id:
            if self.sh_project_stage_tmpl_id.sh_pricing_mode:
                self.sh_pricing_mode=self.sh_project_stage_tmpl_id.sh_pricing_mode
            if self.sh_project_stage_tmpl_id.sh_fp_based_on:
                self.sh_fp_based_on=self.sh_project_stage_tmpl_id.sh_fp_based_on

    # --------------------------------------------------
    #  Refrence code to calcute the holidays
    # --------------------------------------------------

    def _sunday_count(self, from_date, to_date):
        # --------------- Sunday Count ----------------
        sunday = 0
        while from_date <= to_date:
            # If sunday
            if from_date.weekday() == 6:
                # if sunday_list and from_date in sunday_list:
                #     from_date += timedelta(days=1)
                #     continue
                # sunday_list.append(from_date)
                sunday += 1
            from_date += timedelta(days=1)
        return sunday

    # def _sunday_count(self, from_date, to_date, sunday_list):
    #     # --------------- Sunday Count ----------------
    #     sunday = 0
    #     while from_date <= to_date:
    #         # If sunday
    #         if from_date.weekday() == 6:
    #             if sunday_list and from_date in sunday_list:
    #                 from_date += timedelta(days=1)
    #                 continue
    #             sunday_list.append(from_date)
    #             sunday += 1
    #         from_date += timedelta(days=1)
    #     return sunday

    def _get_sunday_count(self, from_date, to_date):
        sunday_count = 0
        sunday_list = []
        while True:
            sunday = self._sunday_count(from_date, to_date, sunday_list)
            if not sunday:
                break
            from_date = to_date
            to_date += timedelta(days=sunday)
            sunday_count += sunday
        return sunday_count
