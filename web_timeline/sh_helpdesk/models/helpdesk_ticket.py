# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from markupsafe import Markup,escape
from odoo import models, fields, tools, api, _, SUPERUSER_ID
import random
from odoo.exceptions import UserError
from odoo.tools import email_re, email_escape_char, email_split
from datetime import datetime, timedelta
from datetime import date
import uuid
import re
import logging
_logger = logging.getLogger(__name__)
from dateutil.relativedelta import relativedelta


class CRMLead(models.Model):
    _inherit = 'crm.lead'

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        ''' set sales@softhealer.com as Outgoing mail server.
            while send any message from CRM.LEAD model.
        '''
        if self.env.context.get('to_be_ignored'):
            blank_message = self.env['mail.message'].browse() 
            return blank_message
        mail_server_id = self.env['ir.mail_server'].sudo().search(
            [('smtp_user', '=', 'sales@softhealer.com')], limit=1)
        if mail_server_id:
            kwargs.update({
                'mail_server_id': mail_server_id.id
            })
        return super(CRMLead, self.with_context(mail_post_autofollow=True)).message_post(**kwargs)


class Sale(models.Model):
    _inherit = 'sale.order'

    ''' set sales@softhealer.com as Outgoing mail server.
        while send any message from SALE.ORDER model.
    '''
    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        mail_server_id = self.env['ir.mail_server'].sudo().search(
            [('smtp_user', '=', 'sales@softhealer.com')], limit=1)
        if mail_server_id:
            kwargs.update({
                'mail_server_id': mail_server_id.id
            })
        return super(Sale, self.with_context(mail_post_autofollow=True)).message_post(**kwargs)


class AccountMove(models.Model):
    _inherit = 'account.move'

    ''' set sales@softhealer.com as Outgoing mail server.
        while send any message from ACCOUNT.MOVE model.
    '''
    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        mail_server_id = self.env['ir.mail_server'].sudo().search(
            [('smtp_user', '=', 'sales@softhealer.com')], limit=1)
        if mail_server_id:
            kwargs.update({
                'mail_server_id': mail_server_id.id
            })
        return super(AccountMove, self.with_context(mail_post_autofollow=True)).message_post(**kwargs)


class Applicant(models.Model):
    _inherit = 'hr.applicant'

    ''' set career@softhealer.com as Outgoing mail server.
        while send any message from HR.APPLICANT model.
    '''

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):

        mail_server_id = self.env['ir.mail_server'].sudo().search(
            [('smtp_user', '=', 'career@softhealer.com')], limit=1)
        if mail_server_id:
            kwargs.update({
                'mail_server_id': mail_server_id.id
            })
        return super(Applicant, self.with_context(mail_post_autofollow=True)).message_post(**kwargs)


class HelpdeskSLAStatus(models.Model):
    _name = 'sh.helpdesk.sla.status'
    _description = "Helpdesk Ticket SLA Status"
    _table = 'sh_helpdesk_sla_status'
    _order = 'id ASC'
    _rec_name = 'sh_sla_id'

    sh_ticket_id = fields.Many2one(
        'sh.helpdesk.ticket', string='Ticket', required=True, ondelete='cascade', index=True)
    sh_sla_id = fields.Many2one(
        'sh.helpdesk.sla', required=True, ondelete='cascade')
    sh_status = fields.Selection([('sla_failed', 'Failed'), ('sla_passed', 'Passed'), (
        'sh_partially_passed', 'Partially Passed')], string="Status")
    color = fields.Integer("Color Index", compute='_compute_sh_color')
    sh_done_sla_date = fields.Datetime('SLA Done Date')

    @api.depends('sh_status')
    def _compute_sh_color(self):
        for rec in self:
            if rec.sh_status == 'sla_failed':
                rec.color = 1
            elif rec.sh_status == 'sla_passed':
                rec.color = 10
            elif rec.sh_status == 'sh_partially_passed':
                rec.color = 4
            else:
                rec.color = 0


class HelpdeskTicket(models.Model):
    _name = 'sh.helpdesk.ticket'
    _inherit = ['portal.mixin', 'mail.activity.mixin', 'mail.thread.cc']

    _description = "Helpdesk Ticket"
    _order = 'id DESC'
    _rec_name = 'name'
    _primary_email = 'email'
   
    def get_deafult_company(self):
        company_id = self.env.company
        return company_id

    @api.model
    def _mail_get_partner_fields(self):
        
        '''
            Purpose of using this method is we use parter_id and partner_ids field in same model
            We are facing singletone error while send email.
            We already add partner_ids in followers so alredy partner_ids record get email from odoo

        '''
        result = super(HelpdeskTicket,self)._mail_get_partner_fields()
    
        if 'partner_ids' in result:
            result.remove('partner_ids')

        return result

    @api.model
    def get_default_stage(self):
        company_id = self.env.company
        stage_id = self.env['sh.helpdesk.stages'].sudo().search(
            [('id', '=', company_id.new_stage_id.id)], limit=1)
        return stage_id.id

    name = fields.Char("Name")
    company_id = fields.Many2one(
        'res.company', string="Company", default=get_deafult_company)
    done_stage_boolean = fields.Boolean(
        'Done Stage', compute='_compute_stage_booleans', store=True)
    cancel_stage_boolean = fields.Boolean(
        'Cancel Stage', compute='_compute_stage_booleans', store=True)
    reopen_stage_boolean = fields.Boolean(
        'Reopened Stage', compute='_compute_stage_booleans', store=True)
    closed_stage_boolean = fields.Boolean(
        'Closed Stage', compute='_compute_stage_booleans', store=True)
    open_boolean = fields.Boolean(
        'Open Ticket', compute='_compute_stage_booleans', store=True)
    cancel_button_boolean = fields.Boolean(
        "Cancel Button", compute='_compute_cancel_button_boolean', search='_search_cancel_button_boolean')
    done_button_boolean = fields.Boolean(
        "Done Button", compute='_compute_done_button_boolean', search='_search_done_button_boolean')
    state = fields.Selection([('customer_replied', 'Customer Replied'), ('staff_replied', 'Staff Replied')],
                             string="Replied Status", default='customer_replied', required=True, readonly=True)
    active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the product without removing it.")
    ticket_from_website = fields.Boolean('Ticket From Website')
    cancel_reason = fields.Char("Cancel Reason", tracking=True)
    tag_ids = fields.Many2many('sh.helpdesk.tags', string="Tags")
    priority = fields.Many2one(
        'helpdesk.priority', string='Priority', tracking=True)
    stage_id = fields.Many2one('sh.helpdesk.stages', string="Stage",
                               default=get_default_stage, tracking=True, index=True, group_expand='_read_group_stage_ids')
    ticket_type = fields.Many2one(
        'sh.helpdesk.ticket.type', string='Ticket Type', tracking=True)
    team_id = fields.Many2one(
        'sh.helpdesk.team', string='Team', tracking=True)
    team_head = fields.Many2one(
        'res.users', "Team Head", tracking=True, readonly=True, domain=[('share', '=', False)])
    user_id = fields.Many2one(
        'res.users', string="Assigned User", tracking=True, domain=[('share', '=', False)])
    subject_id = fields.Many2one(
        'sh.helpdesk.sub.type', string='Ticket Subject Type', tracking=True)
    category_id = fields.Many2one(
        'sh.helpdesk.category', string="Category", tracking=True)
    sub_category_id = fields.Many2one(
        'helpdesk.subcategory', string="Sub Category")
    partner_id = fields.Many2one(
        'res.partner', string='Partner', tracking=True, required=True)
    partner_category_id = fields.Many2one('partner.category', string='Partner Category')
    person_name = fields.Char(string='Person Name',
                              tracking=True)
    email = fields.Char(string='Email', tracking=True)
    close_date = fields.Datetime(
        string='Close Date', tracking=True)
    close_by = fields.Many2one(
        'res.users', string='Closed By', tracking=True)
    cancel_date = fields.Datetime(
        string='Cancelled Date', tracking=True)
    cancel_by = fields.Many2one(
        'res.users', string='Cancelled By', tracking=True)
    replied_date = fields.Datetime('Replied Date')
    product_ids = fields.Many2many('product.product', string='Products',tracking=True)
    comment = fields.Text(string="Comment", tracking=True)
    description = fields.Html('Description ', tracking=True)
    color = fields.Integer(string='Color Index')
    priority_new = fields.Selection([('1', 'Very Low'), ('2', 'Low'), ('3', 'Normal'), ('4', 'High'), (
        '5', 'Very High'), ('6', 'Excellent')], string="Customer Rating", tracking=True)
    customer_comment = fields.Text(
        "Customer Comment", tracking=True)
    new_stage_boolean = fields.Boolean()
    attachment_ids = fields.Many2many('ir.attachment',
                                      string="Attachments")
    form_url = fields.Char('Form Url', compute='get_form_url')
    category_bool = fields.Boolean(
        string='Category Setting', related='company_id.category', store=True)
    sub_category_bool = fields.Boolean(
        string='Sub Category Setting', related='company_id.sub_category', store=True)
    rating_bool = fields.Boolean(
        string='Rating Setting', related='company_id.customer_rating', store=True)
    ticket_allocated = fields.Boolean("Allocated")
    sh_user_ids = fields.Many2many(
        'res.users', string="Responsible Users ", domain=[('share', '=', False)])
    sh_display_multi_user = fields.Boolean(
        compute='_compute_sh_display_multi_user')    
    product_technical_name = fields.Char("Product Technical Names",compute="_compute_product_technical_name", tracking=True)
    sh_default_sale_quotation_template = fields.Many2one('sale.order.template',string="Default Quotation Template",default=lambda self: self.env.company.sh_default_sale_quotation_template.id)
  
    website_id = fields.Many2one(
        string='Website',
        comodel_name='website',
        ondelete='restrict',
    )
    

    def _compute_product_technical_name(self):
        for rec in self:
            tech_name = ''
            if rec.product_ids:
                for product in rec.product_ids:
                    if product.sh_technical_name:
                        tech_name += product.sh_technical_name + ' | '
            rec.product_technical_name = tech_name

    @api.model
    def _default_sh_display_product(self):

        if self.env.company and self.env.company.sh_configure_activate:
            return True
        else:
            return False

    sh_display_product = fields.Boolean(
        compute='_compute_sh_display_product', compute_sudo=True, default="_default_sh_display_product")
    sh_edition_id = fields.Many2one('sh.edition', 'Edition')
    sh_odoo_hosted_id = fields.Many2one(
        'sh.odoo.hosted.on', string='Hosted On')
    sh_version_id = fields.Many2one('sh.version', 'Version',tracking=True)
    sh_ticket_alarm_ids = fields.Many2many(
        'sh.ticket.alarm', string='Ticket Reminders')
    sh_status = fields.Selection([('sla_failed', 'Failed'), ('sla_passed', 'Passed'), (
        'sh_partially_passed', 'Partially Passed')], string="Status")
    sh_sla_policy_ids = fields.Many2many('sh.helpdesk.sla', 'sh_helpdesk_sla_status',
                                         'sh_ticket_id', 'sh_sla_id', string="Helpdesk SLA Policies", copy=False)
    sh_sla_status_ids = fields.One2many(
        'sh.helpdesk.sla.status', 'sh_ticket_id', string="Helpdesk SLA Status")
    sh_sla_deadline = fields.Datetime(
        'SLA Deadline', compute='_compute_sh_sla_deadline')
    sh_status_boolean = fields.Boolean()
    sh_days_to_reach = fields.Float(
        string='SLA reached duration')
    sh_days_to_late = fields.Float(
        string='SLA late duration')
    sh_ticket_report_url = fields.Char()
    report_token = fields.Char("Access Token")
    portal_ticket_url_wp = fields.Char(compute='_compute_ticket_portal_url_wp')
    mobile_no = fields.Char('Mobile')
    sh_ticket_vals = fields.Text('Ticket Vals')
    email_subject = fields.Char('Email Subject', tracking=True)
    odoo_store_ticket = fields.Boolean('Odoo Store Ticket ?')
    store_reference = fields.Char('Order Reference')
    sh_odoo_end_ticket_id = fields.Many2one(
        'sh.odoo.end.ticket', string='Odoo End Ticket')
    odoo_end_ticket_count = fields.Integer()
    sh_feedback_link = fields.Char(
        'Feedback')
    sh_order_date = fields.Datetime(
        'Order Date')
    sh_days_left = fields.Integer(
        'Days left ?')
    sh_total_order_qty = fields.Float(
        'Total Ordered QTY')
    sh_total_order_price_unit = fields.Float(
        'Total Price')
    sh_close_ticket = fields.Boolean('Closed Ticket ?')
    sh_store_link = fields.Char('Store URL')
    sh_check_downgrade = fields.Boolean('Check Downgrade Versions?')
    sh_click_downgrade = fields.Boolean('Click Downgrade')
    sh_ticket_replied_status = fields.Selection(
        [('staff', 'Staff Replied'), ('customer', 'Customer Replied')], string='Ticket Replied Status')
    partner_ids = fields.Many2many('res.partner', string='Partners')
    followers_added = fields.Boolean()
    sh_same_ticket_count = fields.Integer(readonly=True)
    sh_common_compute_form = fields.Boolean(
        compute='_compute_sh_common_compute_form', compute_sudo=True)

    sh_special = fields.Boolean('Special Ticket')
    sh_competitors_added = fields.Char(
        'Competitors Followers added', compute='_compute_followers_message')

    task_count = fields.Integer('Tasks', compute='_compute_task_count')
    task_ids = fields.Many2many('project.task', string='Task')

    sh_invoice_ids = fields.Many2many("account.move", string=" Invoice")
    sh_sale_order_ids = fields.Many2many("sale.order", string="Order ")
    
    task_id = fields.Many2one('project.task.type', 'Status of Task', compute='_compute_last_task_status')

    #ticket auto followup start
    sh_auto_followup = fields.Boolean('Auto Follow-up')
    sh_number_of_followup_taken = fields.Integer('Number of Followup Taken')
    sh_followup_template_id = fields.Many2one('sh.ticket.followup.configuration',string='Followup Template')
    sh_followup_history_ids = fields.One2many('sh.followup.history','sh_followup_ticket_id',string='Followup history')
    #ticket auto followup end

    def _compute_last_task_status(self):
        for ticket in self:
            ticket.task_id = False
            task_ids = self.env['project.task'].sudo().search([('sh_ticket_ids', 'in', [ticket.id])])
            # Sorting tasks by creation date in descending order
            if task_ids:
                sorted_tasks = task_ids.sudo().sorted(key=lambda r: r.create_date, reverse=True)
                if sorted_tasks and sorted_tasks[0].sudo().stage_id:
                    ticket.task_id = sorted_tasks[0].sudo().stage_id.id                

    @api.model
    def default_due_date(self):
        return fields.Datetime.now()

    sh_due_date = fields.Datetime('Reminder Due Date',
                                  default=default_due_date)

    def _message_get_suggested_recipients(self):
        recipients = super(
            HelpdeskTicket, self)._message_get_suggested_recipients()

        # if recipients:
        #     exclude_email = ['catchall@softhealer.com','sales@softhealer.com','info@softhealer.com','angeltest7890@gmail.com']
        #     include_recipients = []
        #     recipients_list = recipients.get(self.id)
        #     for each_element in recipients_list:
        #         for each_tuple in tools.email_split_tuples(each_element[1]):
        #             if each_tuple[1] not in exclude_email:
        #                 include_recipients.append(each_element)
        # recipients.update({self.id:include_recipients})

        # --------------------------------------------------------------------------------------------------------------------
        # REMOVE recipients RECORD WHICH CONTAIN exclude_email
        # --------------------------------------------------------------------------------------------------------------------
        # try:
        #     if recipients:                                
        #         exclude_email = ['catchall@softhealer.com','sales@softhealer.com','info@softhealer.com','angeltest7890@gmail.com']
        #         recipients_list = recipients.get(self.id)
        #         updated_recipients_list = []               
                
        #         for each_element in recipients_list:
        #             email = tools.email_split_tuples(each_element[1])[0][1]
        #             if email not in exclude_email:
        #                 updated_recipients_list.append(each_element)

        #         recipients.update({self.id:updated_recipients_list})

        #         return recipients

        # except Exception as e:
        #     return recipients

        exclude_email = ['catchall@softhealer.com', 'sales@softhealer.com', 'info@softhealer.com', 'angeltest7890@gmail.com', 'softhealersolutions@gmail.com']

        try:
            if recipients:
                
                recipients_list = recipients.get(self.id, [])
                
                updated_recipients_list = [element for element in recipients_list if tools.email_split_tuples(element[1])[0][1] not in exclude_email]

                recipients.update({self.id: updated_recipients_list})

            return recipients

        except Exception as e:
            
            return recipients

        
        # --------------------------------------------------------------------------------------------------------------------
        # REMOVE recipients RECORD WHICH CONTAIN exclude_email
        # --------------------------------------------------------------------------------------------------------------------

    def action_log_note(self):
        self.ensure_one()
        return{
            'name':'Add a log note',
            'type':'ir.actions.act_window',
            'res_model':'sh.log.note',
            'view_mode':'form',
            'target':'new'
        }

    #Ticket Auto Followup History lines added 
    @api.constrains('sh_followup_template_id')
    def _check_sh_followup_template_id(self):
        for record in self:
            # Ensure only runs when record is saved or has an ID
            if record.stage_id and record.sh_followup_template_id and record.env.company.sh_auto_followup_stage_id:
                if record.stage_id.id == record.env.company.sh_auto_followup_stage_id.id:
                    # clear old pending
                    pending_lines = record.sh_followup_history_ids.filtered(lambda l: l.sh_status == 'pending')
                    pending_lines.unlink()
                    
                    followup_history = []
                    schedule_date = fields.Date.today()
                    for line in record.sh_followup_template_id.sh_ticket_followup_line_ids:
                        schedule_date += timedelta(days=line.sh_interval)
                        followup_history.append((0, 0, {
                            'sh_schedule_date': schedule_date,
                            'sh_email_template_id': line.sh_email_template_id.id,
                            'sh_status': 'pending'
                        }))
                    record.sh_followup_history_ids = followup_history

    @api.onchange('sh_edition_id')
    def _onchange_sh_edition_id_odoo_hosted(self):
        domain = {}
        odoo_hosted_list = []
        if self.sh_edition_id:
            odoo_hosted_obj = self.env['sh.odoo.hosted.on'].search(
                [('sh_edtion_id', '=', self.sh_edition_id.id)])
            if odoo_hosted_obj:
                for odoo_hosted in odoo_hosted_obj:
                    odoo_hosted_list.append(odoo_hosted.id)
                domain = {'sh_odoo_hosted_id': [
                    ('id', 'in', odoo_hosted_list)]}
            else:
                domain = {'sh_odoo_hosted_id': [('id', 'in', [])]}
        return {'domain': domain}

    def _compute_followers_message(self):

        for rec in self:
            rec.sh_competitors_added = False
            if rec.message_follower_ids:
                followers = []
                for follower in rec.message_follower_ids:
                    followers.append(follower.partner_id.id)
                competitors_partner = []
                if followers:
                    if self.env.company.sh_follower_domain_ids:
                        for follower_domain in self.env.company.sh_follower_domain_ids:
                            partners = self.env['res.partner'].sudo().search(
                                [('id', 'in', followers), ('email', 'ilike', follower_domain.name)])
                            if partners:
                                for partner in partners:
                                    competitors_partner.append(partner.id)
                if competitors_partner:
                    rec.sh_competitors_added = 'Competitors added as followers...'

  
    def _compute_sh_common_compute_form(self):
        '''
        Common compute funcation for compute data while form view open
        '''
        for record in self:
            record.sh_common_compute_form = True

            # -----------------------------------------------------------------------------
            # GET NUMBER OF TICKETS WITH SAME PARTNER
            # -----------------------------------------------------------------------------
            tickets = self.env['sh.helpdesk.ticket'].sudo().search_count(
                [('id', '!=', record.id), ('partner_id', '=', record.partner_id.id)])
            if tickets:
                record.sh_same_ticket_count = tickets
            # -----------------------------------------------------------------------------
            # GET NUMBER OF TICKETS WITH SAME PARTNER
            # -----------------------------------------------------------------------------

            # -----------------------------------------------------
            # SET REPLIE STATUS BASED ON CHATTER MESSAGE
            # -----------------------------------------------------
            if record.partner_id.name != 'unknown customer':
                status = 'customer'
                message_id = self.env['mail.message'].sudo().search([('subtype_id', '!=', self.env.ref(
                    'mail.mt_note').id), ('res_id', '=', record.id), ('model', '=', 'sh.helpdesk.ticket')], limit=1)
                if message_id:
                    if message_id.author_id:
                        user_id = self.env['res.users'].sudo().search(
                            [('partner_id', '=', message_id.author_id.id)], limit=1)
                        if user_id and user_id.has_group('base.group_portal'):
                            status = 'customer'
                        elif user_id and not user_id.has_group('base.group_portal'):
                            status = 'staff'
                        elif not user_id:
                            status = 'customer'
                record.sh_ticket_replied_status = status
            else:
                record.sh_ticket_replied_status = False
            # -----------------------------------------------------
            # SET REPLIE STATUS BASED ON CHATTER MESSAGE
            # -----------------------------------------------------

            # -----------------------------------------------------
            # SET ORDER QTY/TOTAL ORDER PRICE DETAILS
            # -----------------------------------------------------
            record.sh_order_date = False
            record.sh_days_left = 0
            record.sh_total_order_qty = 0.0
            record.sh_total_order_price_unit = 0.0
            # if record.store_reference:
            #     order_line = self.env['sale.order.line'].sudo().search(
            #         [('origin', '=', record.store_reference)], limit=1)
            #     if order_line:
            #         record.sh_order_date = order_line.order_id.date_order
            #         support_end_date = order_line.order_id.date_order + \
            #             timedelta(days=60)
            #         sh_order_date = support_end_date - fields.Datetime.now()
            #         record.sh_days_left = int(sh_order_date.days)
            #     order_lines = self.env['sale.order.line'].sudo().search(
            #         [('origin', '=', record.store_reference)])
            #     if order_lines:
            #         sh_total_order_qty = 0.0
            #         sh_total_order_price_unit = 0.0
            #         for line in order_lines:
            #             sh_total_order_qty += line.product_uom_qty
            #             sh_total_order_price_unit += line.price_unit
            #         record.sh_total_order_qty = sh_total_order_qty
            #         record.sh_total_order_price_unit = sh_total_order_price_unit
            # -----------------------------------------------------
            # SET ORDER QTY/TOTAL ORDER PRICE DETAILS
            # -----------------------------------------------------

            # -----------------------------------------------------
            # GENERATE FEEDBACK URL
            # -----------------------------------------------------
            # record.sh_feedback_link = ''
            # if not record.product_ids and not record.sh_version_id:
            #     record.sh_feedback_link = '/ticket/feedback/' + str(record.id)
            # elif record.product_ids and record.sh_version_id:
            #     version = record.sh_version_id.name.split('Odoo ')
            #     if version:
            #         record.sh_feedback_link = 'https://apps.odoo.com/apps/modules/' + \
            #             str(version[1])+'.0/' + \
            #             str(record.product_ids[0].sh_technical_name) + \
            #             '#loempia-comments'
            # -----------------------------------------------------
            # GENERATE FEEDBACK URL
            # -----------------------------------------------------

            # -----------------------------------------------------
            # ODOO TICKET COUNTER
            # -----------------------------------------------------
            odoo_end_ticket_count = self.env['sh.odoo.end.ticket'].sudo().search_count(
                [('email_subject', 'ilike', record.store_reference)])
            record.odoo_end_ticket_count = odoo_end_ticket_count
            # -----------------------------------------------------
            # ODOO TICKET COUNTER
            # -----------------------------------------------------

            # ----------------------------------------
            # GENERATE TICKET REPORT URL
            # ----------------------------------------
            record.sh_ticket_report_url = False
            if record.company_id.sh_pdf_in_message:
                base_url = self.env['ir.config_parameter'].sudo(
                ).get_param('web.base.url')
                ticket_url = "%0A%0A Click here to download Ticket Document : %0A" + \
                    base_url+record.get_download_report_url()
                record.sh_ticket_report_url = base_url+record.get_download_report_url()
            # ----------------------------------------
            # GENERATE TICKET REPORT URL
            # ----------------------------------------

            # ---------------------------------------
            # DAY TO REACH
            # ---------------------------------------
            sh_days_to_reach = 0.0
            if record.sh_sla_status_ids:
                for line in record.sh_sla_status_ids:
                    if line.sh_done_sla_date:
                        sla_deadline = record.create_date
                        if line.sh_sla_id.sh_days > 0:
                            deadline = record.team_id.sh_resource_calendar_id.plan_days(
                                line.sh_sla_id.sh_days+1,
                                record.create_date,
                                compute_leaves=True)
                            sla_deadline = deadline.replace(
                                hour=record.create_date.hour, minute=record.create_date.minute, second=record.create_date.second, microsecond=record.create_date.microsecond)
                        else:
                            sla_deadline = record.create_date
                        deadline = record.team_id.sh_resource_calendar_id.plan_hours(
                            line.sh_sla_id.sh_hours, sla_deadline, compute_leaves=True)
                        delta = line.sh_done_sla_date - deadline
                        sh_days_to_reach += delta.days
            record.sh_days_to_reach = sh_days_to_reach
            # ---------------------------------------
            # DAYS TO REACH
            # ---------------------------------------

            # ---------------------------------------
            # DAYS TO LATE
            # ---------------------------------------
            sh_days_to_late = 0.0
            if record.sh_sla_status_ids:
                for line in record.sh_sla_status_ids:
                    if line.sh_done_sla_date:
                        sla_deadline = record.create_date
                        if line.sh_sla_id.sh_days > 0:
                            deadline = record.team_id.sh_resource_calendar_id.plan_days(
                                line.sh_sla_id.sh_days+1,
                                record.create_date,
                                compute_leaves=True)
                            sla_deadline = deadline.replace(
                                hour=record.create_date.hour, minute=record.create_date.minute, second=record.create_date.second, microsecond=record.create_date.microsecond)
                        else:
                            sla_deadline = record.create_date
                        deadline = record.team_id.sh_resource_calendar_id.plan_hours(
                            line.sh_sla_id.sh_hours, sla_deadline, compute_leaves=True)
                        delta = line.sh_done_sla_date - deadline
                        sh_days_to_late += delta.days
            record.sh_days_to_late = sh_days_to_late
            # ---------------------------------------
            # DAY TO LATE
            # ---------------------------------------
            record.sh_common_compute_form = True
            record.sh_status_boolean = False
            sla_passed = record.sh_sla_status_ids.filtered(
                lambda x: x.sh_status == 'sla_passed')
            sla_failed = record.sh_sla_status_ids.filtered(
                lambda x: x.sh_status == 'sla_failed')
            if sla_passed and sla_failed:
                record.sh_status = 'sh_partially_passed'

            record.new_stage_boolean = False
            if record.create_date.date() == fields.Date.today() and record.stage_id.id == self.env.user.company_id.new_stage_id.id:
                record.new_stage_boolean = True

            record.sh_common_compute_form = True

    def action_view_old_tickets_of_customer(self):
        self.ensure_one()
        domain = [('id', '!=', self.id),
                  ('partner_id', '=', self.partner_id.id)]
        find_ticket = self.sudo().search(domain)
        return{
            'name': 'Related Tickets',
            'res_model': 'sh.helpdesk.ticket',
            'type': 'ir.actions.act_window',
            'view_mode': 'kanban,tree,form',
            'domain': [('id', 'in', find_ticket.ids)],
            'target': 'current',
        }

    def preview_ticket(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': self.get_portal_url(),
        }

    def _compute_access_url(self):
        super(HelpdeskTicket, self)._compute_access_url()
        for ticket in self:
            ticket.access_url = '/my/sh_tickets/%s' % (ticket.id)

    def action_assign_to_me(self):
        self.ensure_one()
        self.sh_user_ids = [(4, self.env.user.id)]

    @api.model
    def refresh_ticket(self):
        fetchmail_cron_id = self.env.ref(
            'fetchmail.ir_cron_mail_gateway_action')
        if fetchmail_cron_id:
            fetchmail_cron_id.sudo().method_direct_trigger()
        return True

    def action_give_feedback(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        template_id = self.env.ref(
            'sh_helpdesk.sh_send_feedback_email_template').id
        try:
            compose_form_id = ir_model_data.check_object_reference(
                'mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'sh.helpdesk.ticket',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'force_email': True
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    def action_view_odoo_end_tickets(self):
        self.ensure_one()
        return{
            'name': 'Odoo End Tickets',
            'res_model': 'sh.odoo.end.ticket',
            'type': 'ir.actions.act_window',
            'view_mode': 'kanban,tree,form',
            'domain': [('email_subject', 'ilike', self.store_reference)],
            'target': 'current',
        }

    @api.onchange('product_ids')
    def onchange_product_ids(self):
        self.ensure_one()
        if self.product_ids:
            # responsible_user = []
            for product in self.product_ids:
                # == for responsible users =====

                # if product.resposible_user_id:
                #     responsible_user.append(product.resposible_user_id.id)

                # == For Version id =======
                if product.product_template_attribute_value_ids:
                    version_attribute_id = product.product_template_attribute_value_ids.sudo().filtered(
                        lambda x: x.attribute_id.name == 'Version')
                    if version_attribute_id:
                        version_id = self.env['sh.version'].sudo().search(
                            [('name', '=', version_attribute_id.name)], limit=1)
                        if version_id:
                            self.sh_version_id = version_id.id
            # if responsible_user:
            #     self.sh_user_ids = [(6, 0, responsible_user)]
        else:
            self.sh_version_id = False

    @api.onchange('odoo_store_ticket')
    def onchange_odoo_store_ticket(self):
        self.ensure_one()
        if not self.odoo_store_ticket:
            if not self.partner_id:
                self.store_reference = False
                self.partner_id = False
        else:
            if not self.partner_id:
                unknown_customer = self.env['res.partner'].search(
                    [('name', '=', 'unknown customer')], limit=1)
                if unknown_customer:
                    self.partner_id = unknown_customer.id

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        all_stages = self.env['sh.helpdesk.stages'].sudo().search([])
        search_domain = [('id', 'in', all_stages.ids)]

        # perform search
        stage_ids = stages._search(
            search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    def _search_done_button_boolean(self, operator, value):
        not_done_ids = []
        done_ids = []
        for record in self.search([]):
            if record.stage_id.is_done_button_visible:
                done_ids.append(record.id)
            else:
                not_done_ids.append(record.id)
        if operator == '=':
            return [('id', 'in', done_ids)]
        elif operator == '!=':
            return [('id', 'in', not_done_ids)]
        else:
            return []

    def _search_cancel_button_boolean(self, operator, value):
        not_cancel_ids = []
        cancel_ids = []
        for record in self.search([]):
            if record.stage_id.is_cancel_button_visible:
                cancel_ids.append(record.id)
            else:
                not_cancel_ids.append(record.id)
        if operator == '=':
            return [('id', 'in', cancel_ids)]
        elif operator == '!=':
            return [('id', 'in', not_cancel_ids)]
        else:
            return []

    def _compute_ticket_portal_url_wp(self):
        for rec in self:
            rec.portal_ticket_url_wp = False
            if rec.company_id.sh_pdf_in_message:
                base_url = self.env['ir.config_parameter'].sudo(
                ).get_param('web.base.url')
                ticket_url = base_url+rec.get_portal_url()
                rec.portal_ticket_url_wp = ticket_url

    def _get_token(self):
        """ Get the current record access token """
        if self.report_token:
            return self.report_token
        else:
            report_token = str(uuid.uuid4())
            self.write({'report_token': report_token})
            return report_token

    def get_download_report_url(self):
        url = ''
        if self.id:
            self.ensure_one()
            url = '/download/ht/' + '%s?access_token=%s' % (
                self.id,
                self._get_token()
            )
        return url

    def action_send_whatsapp(self):
        self.ensure_one()
        if not self.partner_id.mobile:
            raise UserError(_("Partner Mobile Number Not Exist !"))
        template = self.env.ref(
            'sh_helpdesk.sh_send_whatsapp_email_template')

        ctx = {

            'default_model': 'sh.helpdesk.ticket',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template.id),
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': True,
            'default_is_wp': True,
        }
        attachment_ids = self.env['ir.attachment'].sudo().search(
            [('res_model', '=', 'sh.helpdesk.ticket'), ('res_id', '=', str(self.id))])
        if attachment_ids:
            ctx.update({
                'attachment_ids': [(6, 0, attachment_ids.ids)]
            })
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    def _compute_sh_sla_deadline(self):
        for rec in self:
            rec.sh_sla_deadline = date.today()
            status_ids = rec.sh_sla_status_ids.filtered(
                lambda x: x.sh_status == False)
            ticket_create_date = fields.Datetime.from_string(rec.create_date)
            sla_deadline = rec.create_date
            working_schedule = rec.team_id.sh_resource_calendar_id
            if status_ids:
                sla_deadline_list = []
                for line in status_ids:
                    if line.sh_sla_id.sh_days > 0:
                        deadline = working_schedule.plan_days(
                            line.sh_sla_id.sh_days+1,
                            ticket_create_date,
                            compute_leaves=True)
                        sla_deadline = deadline.replace(hour=ticket_create_date.hour, minute=ticket_create_date.minute,
                                                        second=ticket_create_date.second, microsecond=ticket_create_date.microsecond)
                    else:
                        sla_deadline = ticket_create_date
                    sla_deadline_list.append(working_schedule.plan_hours(
                        line.sh_sla_id.sh_hours, sla_deadline, compute_leaves=True))
                if sla_deadline_list:
                    rec.sh_sla_deadline = min(sla_deadline_list)

    @api.model
    def change_sh_status(self):
        self.ensure_one()
        if self.sh_sla_status_ids:
            for line in self.sh_sla_status_ids:
                sla_deadline = self.create_date
                if line.sh_sla_id.sh_days > 0:
                    deadline = self.team_id.sh_resource_calendar_id.plan_days(
                        line.sh_sla_id.sh_days+1,
                        self.create_date,
                        compute_leaves=True)
                    sla_deadline = deadline.replace(hour=self.create_date.hour, minute=self.create_date.minute,
                                                    second=self.create_date.second, microsecond=self.create_date.microsecond)
                else:
                    sla_deadline = self.create_date
                sh_deadline = self.team_id.sh_resource_calendar_id.plan_hours(
                    line.sh_sla_id.sh_hours, sla_deadline, compute_leaves=True)
                if line.sh_sla_id and line.sh_sla_id.sh_sla_target_type == 'reaching_stage':
                    if line.sh_sla_id.sh_stage_id.id == self.stage_id.id:
                        line.sh_done_sla_date = fields.Datetime.now()
                        line.sh_status = False
                        self.sh_status = False
                        if line.sh_done_sla_date and sh_deadline:
                            line.sh_status = 'sla_passed' if line.sh_done_sla_date < sh_deadline else 'sla_failed'
                            self.sh_status = 'sla_passed' if line.sh_done_sla_date < sh_deadline else 'sla_failed'
                        else:
                            line.sh_status = False if (
                                not sh_deadline or sh_deadline > fields.Datetime.now()) else 'sla_failed'
                            self.sh_status = False if (
                                not sh_deadline or sh_deadline > fields.Datetime.now()) else 'sla_failed'
                elif line.sh_sla_id and line.sh_sla_id.sh_sla_target_type == 'assign_to':
                    if not self.user_id or not self.sh_user_ids:
                        line.sh_done_sla_date = fields.Datetime.now()
                        line.sh_status = False
                        self.sh_status = False
                        if line.sh_done_sla_date and sh_deadline:
                            line.sh_status = 'sla_passed' if line.sh_done_sla_date < sh_deadline else 'sla_failed'
                            self.sh_status = 'sla_passed' if line.sh_done_sla_date < sh_deadline else 'sla_failed'
                        else:
                            line.sh_status = False if (
                                not sh_deadline or sh_deadline > fields.Datetime.now()) else 'sla_failed'
                            self.sh_status = False if (
                                not sh_deadline or sh_deadline > fields.Datetime.now()) else 'sla_failed'

    @api.onchange('team_id', 'ticket_type')
    def _onchange_sh_helpdesk_policy_ids(self):
        if self:
            for rec in self:
                rec.sh_sla_policy_ids = [
                    (6, 0, rec.helpdesk_sla_create(rec.team_id.id, rec.ticket_type.id))]

    @api.depends('company_id')
    def _compute_sh_display_multi_user(self):
        if self:
            for rec in self:
                rec.sh_display_multi_user = False
                if rec.company_id and rec.company_id.sh_display_multi_user:
                    rec.sh_display_multi_user = True

    @api.model
    def helpdesk_sla_create(self, team_id, ticket_type):
        self.ensure_one()
        sla_policy_ids_list = []
        if self.sh_sla_status_ids:
            self.sh_sla_status_ids.unlink()
        if team_id:
            sla_policy_ids = self.env['sh.helpdesk.sla'].sudo().search(
                [('sh_team_id', '=', team_id)])
            if sla_policy_ids:
                for policy_id in sla_policy_ids:
                    if policy_id.id not in sla_policy_ids_list:
                        sla_policy_ids_list.append(policy_id.id)
        if ticket_type:
            if team_id:
                sla_policy_ids = self.env['sh.helpdesk.sla'].sudo().search(
                    [('sh_ticket_type_id', '=', ticket_type), ('sh_team_id', '=', team_id)])
                if sla_policy_ids:
                    for policy_id in sla_policy_ids:
                        if policy_id.id not in sla_policy_ids_list:
                            sla_policy_ids_list.append(policy_id.id)
            elif not team_id:
                sla_policy_ids = self.env['sh.helpdesk.sla'].sudo().search(
                    [('sh_ticket_type_id', '=', ticket_type)])
                if sla_policy_ids:
                    for policy_id in sla_policy_ids:
                        if policy_id.id not in sla_policy_ids_list:
                            sla_policy_ids_list.append(policy_id.id)
        return sla_policy_ids_list

    # @api.depends('company_id')
    def _compute_sh_display_product(self):
        if self:
            for rec in self:
                rec.sh_display_product = False
                if rec.company_id and rec.company_id.sh_configure_activate:
                    rec.sh_display_product = True

    @api.model
    def message_new(self, msg_dict, custom_values=None):
        defaults = {}
        email_from = email_escape_char(email_split(msg_dict.get('from'))[0])
        email_to = email_escape_char(email_split(msg_dict.get('to'))[0])
        if email_to.lower() == 'softhealersolutions@gmail.com':
            if email_from == 'apps@odoo.com':
                email_subject = msg_dict.get('subject')
                if email_subject:
                    email_subject = email_subject.split(" ")
                    length = len(email_subject)
                    email_subject_str = email_subject[length - 1]
                    body = msg_dict.get('body')
                    if body:
                        subject = ''
                        if 'SO' in email_subject_str:
                            subject = email_subject_str
                        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
                        url = re.findall(regex, msg_dict.get('body'))
                        if url:
                            store_url = [x[0] for x in url]
                            for x_url in store_url:
                                if 'https://apps.odoo.com/web/login?redirect=/apps/modules/' or 'https://apps.odoo.com/web/login?redirect=/apps/support/' in x_url:
                                    ticket_url = ''
                                    if '#' in x_url:
                                        split_t_url = x_url.split('#')
                                        ticket_url = split_t_url[0]
                                    else:
                                        if 'redirect=/apps/dashboard/preferences' not in x_url and ticket_url == '':
                                            ticket_url = x_url
                                    url_split = re.compile(
                                        r'[\:/?=\-&]+', re.UNICODE).split(ticket_url)
                                    if url_split:
                                        for tech_name in url_split:
                                            if 'sh_' in tech_name:
                                                if tech_name:
                                                    product_id = self.env['product.product'].sudo().search(
                                                        [('sh_technical_name', '=', tech_name)], limit=1)
                                                    if product_id:
                                                        ticket_id = self.env['sh.helpdesk.ticket'].sudo().search([('odoo_store_ticket', '=', True), (
                                                            'product_ids.sh_technical_name', '=', tech_name), ('store_reference', '=', subject)], limit=1)
                                                        if ticket_id:
                                                            ticket_vals = {
                                                                'state': 'customer_replied'}
                                                            if ticket_id.sh_store_link:
                                                                ticket_vals.update({
                                                                    'sh_store_link': ticket_url
                                                                })
                                                            ticket_id.sudo().write(ticket_vals)
                                                            subtype_id = self.env['mail.message.subtype'].sudo().search(
                                                                [('name', '=', 'Note')], limit=1)
                                                            message_id = self.env['mail.message'].with_context(new_message_ticket=True).sudo().create({
                                                                'subject': 'Customer Replied',
                                                                'date': msg_dict.get('date'),
                                                                'author_id': 2,
                                                                'message_type': 'notification',
                                                                'subtype_id': self.env.ref('mail.mt_note').id,
                                                                'model': 'sh.helpdesk.ticket',
                                                                'res_id': ticket_id.id,
                                                                'body': body,
                                                            })
                                                        else:
                                                            unknown_customer = self.env['res.partner'].sudo().search(
                                                                [('name', '=', 'unknown customer')], limit=1)
                                                            if unknown_customer:
                                                                defaults.update({
                                                                    'email_subject':  msg_dict.get('subject') or _("No Subject"),
                                                                    'person_name': unknown_customer.name,
                                                                    'partner_id': unknown_customer.id or False,
                                                                    'description': msg_dict.get('body'),
                                                                    'state': 'customer_replied',
                                                                    'replied_date': msg_dict.get('date'),
                                                                    'odoo_store_ticket': True,
                                                                    'store_reference': subject,
                                                                    'sh_store_link': ticket_url,
                                                                    'product_ids': [(6, 0, product_id.ids)],
                                                                    # 'sh_user_ids': [(6, 0, product_id.product_tmpl_id.resposible_user_id.ids)],
                                                                })
                                elif 'https://apps.openerp.com' in x_url:
                                    ticket_url = ''
                                    if '#' in x_url:
                                        split_t_url = x_url.split('#')
                                        ticket_url = split_t_url[0]
                                    else:
                                        ticket_url = x_url
                                    url_split = re.compile(
                                        r'[\:/?=\-&]+', re.UNICODE).split(x_url)
                                    if url_split:
                                        for tech_name in url_split:
                                            if 'sh_' in tech_name:
                                                if tech_name:
                                                    product_id = self.env['product.product'].sudo().search(
                                                        [('sh_technical_name', '=', tech_name)], limit=1)
                                                    if product_id:
                                                        ticket_id = self.env['sh.helpdesk.ticket'].sudo().search([('odoo_store_ticket', '=', True), (
                                                            'product_ids', 'in', [product_id.id]), ('store_reference', '=', subject)], limit=1)
                                                        if ticket_id:
                                                            ticket_vals = {
                                                                'state': 'customer_replied'}
                                                            if ticket_id.sh_store_link:
                                                                ticket_vals.update({
                                                                    'sh_store_link': ticket_url
                                                                })
                                                            ticket_id.sudo().write(ticket_vals)
                                                            subtype_id = self.env['mail.message.subtype'].sudo().search(
                                                                [('name', '=', 'Note')], limit=1)
                                                            message_id = self.env['mail.message'].sudo().with_context(new_message_ticket=True).create({
                                                                'subject': 'Customer Replied',
                                                                'date': msg_dict.get('date'),
                                                                'message_type': 'comment',
                                                                'subtype_id': subtype_id.id,
                                                                'model': 'sh.helpdesk.ticket',
                                                                'res_id': ticket_id.id,
                                                                'body': body,
                                                            })
                                                        else:
                                                            unknown_customer = self.env['res.partner'].sudo().search(
                                                                [('name', '=', 'unknown customer')], limit=1)
                                                            if unknown_customer:
                                                                defaults.update({
                                                                    'email_subject':  msg_dict.get('subject') or _("No Subject"),
                                                                    'partner_id': unknown_customer.id or False,
                                                                    'person_name': unknown_customer.name,
                                                                    'description': msg_dict.get('body'),
                                                                    'state': 'customer_replied',
                                                                    'replied_date': msg_dict.get('date'),
                                                                    'odoo_store_ticket': True,
                                                                    'store_reference': subject,
                                                                    'sh_store_link': ticket_url,
                                                                    'product_ids': [(6, 0, product_id.ids)],
                                                                    # 'sh_user_ids': [(6, 0, product_id.product_tmpl_id.resposible_user_id.ids)],
                                                                })

                if defaults:
                    return super(HelpdeskTicket, self).message_new(msg_dict, custom_values=defaults)
            else:
                # Messate To Be Ingnored
                self = self.with_context(to_be_ignored = True)
                return super(HelpdeskTicket, self).message_new(msg_dict, custom_values=defaults)
                
        elif email_from.lower() == 'softhealersolutions@gmail.com':
            # Messate To Be Ingnored
            self = self.with_context(to_be_ignored = True)
            return super(HelpdeskTicket, self).message_new(msg_dict, custom_values=defaults)
            
        else:
            email = msg_dict.get('from') or ''

            name, email = '', ''

            split_results = tools.email_split_tuples(msg_dict.get('from'))

            if split_results:
                name, email = split_results[0]
            
            spam_email_ids = self.env.user.company_id.sh_skip_crm_lead_ids
            spam_emails = []
            if spam_email_ids:
                for spam_email in spam_email_ids:
                    if spam_email.name not in spam_emails:
                        spam_emails.append(spam_email.name)

            # ====================================================            
            # Check Spam Email List             
            # ====================================================            
            if email in spam_emails:
                self = self.with_context(to_be_ignored = True)
                return super(HelpdeskTicket, self).message_new(msg_dict, custom_values=defaults)
            # ====================================================            
            # Check Spam Email List             
            # ====================================================

            if email != 'noreply@youtube.com' and email != 'no-reply@youtube.com' and email not in spam_emails:
                # val = msg_dict.get('from').split('<')[0]
                defaults.update({
                    'person_name': name,
                    'email_subject':  msg_dict.get('subject') or _("No Subject"),
                    'email': email,
                    'partner_id': msg_dict.get('author_id', False),
                    'description': msg_dict.get('body'),
                    'state': 'customer_replied',
                    'replied_date': msg_dict.get('date')
                })
                partner_ids = []
                if msg_dict.get('author_id', False):
                    partner_ids.append(msg_dict.get('author_id', False))
                
                # ======================================================
                # IN V16 ME MANAGED BY SUGGEST RECEIPTNS METHOD
                # ======================================================
                # if 'Fwd' in msg_dict.get('subject'):
                #     original_body = msg_dict.get('body')
                #     soup = BeautifulSoup(original_body)
                #     a_tag = soup.find_all('a')
                #     if a_tag:
                #         for tag in a_tag:
                #             split_1 = str(tag).split('mailto:')
                #             if len(split_1) > 1:
                #                 split_2 = split_1[1].split('>')
                #                 if len(split_2) > 0:
                #                     tag_split_1 = split_2[0].split('"')
                #                     if len(tag_split_1) > 0:
                #                         email_address = tag_split_1[0].strip()
                #                         if email_address.lower() != 'info_softhealer.com' and email_address.lower() != 'sales@softhealer.com' and email_address.lower() != 'angeltest7890@gmail.com' and email_address.lower() != 'catchall@softhealer.com':
                #                             partner_id = self.env['res.partner'].search([
                #                                 ('email', '=', email_address.lower())
                #                             ], limit=1)
                #                             if partner_id:
                #                                 partner_ids.append(
                #                                     partner_id.id)
                #                             else:
                #                                 partner_id = self.env['res.partner'].sudo().create({
                #                                     'name': email_address.lower(),
                #                                     'email': email_address.lower(),
                #                                 })
                #                                 partner_ids.append(
                #                                     partner_id.id)
                # if 'to' in msg_dict:
                #     if ',' in msg_dict.get('to'):
                #         email_to = msg_dict.get('to').split(",")
                #         if email_to:
                #             for to_email in email_to:
                #                 email_address = to_email.strip()
                #                 email_address = email_escape_char(
                #                     email_split(email_address)[0])
                #                 if email_address.lower() != 'info@softhealer.com' and email_address.lower() != 'sales@softhealer.com' and email_address.lower() != 'angeltest7890@gmail.com' and email_address.lower() != 'catchall@softhealer.com':
                #                     partner_id = self.env['res.partner'].search([
                #                         ('email', '=', email_address)
                #                     ], limit=1)
                #                     if partner_id:
                #                         partner_ids.append(partner_id.id)
                #                     else:
                #                         p_name = self.env['res.partner']._parse_partner_name(
                #                             to_email)[0] if to_email else email_address
                #                         partner_id = self.env['res.partner'].sudo().create({
                #                             'name': p_name or email_address,
                #                             'email': email_address,
                #                         })
                #                         partner_ids.append(partner_id.id)
                #     else:
                #         email_address = email_escape_char(
                #             email_split(msg_dict.get('to'))[0])
                #         if email_address.lower() != 'info@softhealer.com' and email_address.lower() != 'sales@softhealer.com' and email_address.lower() != 'angeltest7890@gmail.com' and email_address.lower() != 'catchall@softhealer.com':
                #             partner_id = self.env['res.partner'].search([
                #                 ('email', '=', email_address)
                #             ], limit=1)
                #             if partner_id:
                #                 partner_ids.append(partner_id.id)
                #             else:
                #                 p_name = self.env['res.partner']._parse_partner_name(
                #                     msg_dict.get('to'))[0] if msg_dict.get('to') else email_address
                #                 partner_id = self.env['res.partner'].sudo().create({
                #                     'name': p_name or email_address,
                #                     'email': email_address,
                #                 })
                #                 partner_ids.append(partner_id.id)
                # if 'cc' in msg_dict and msg_dict.get('cc') != '':
                #     if ',' in msg_dict.get('cc'):
                #         email_cc = msg_dict.get('cc').split(",")
                #         if email_cc:
                #             for cc_email in email_cc:
                #                 email_address = cc_email.strip()
                #                 email_address = email_escape_char(
                #                     email_split(email_address)[0])
                #                 p_name = self.env['res.partner']._parse_partner_name(
                #                     cc_email)[0] if cc_email else email_address
                #                 if email_address.lower() != 'info@softhealer.com' and email_address.lower() != 'sales@softhealer.com' and email_address.lower() != 'angeltest7890@gmail.com' and email_address.lower() != 'catchall@softhealer.com':
                #                     partner_id = self.env['res.partner'].search([
                #                         ('email', '=', email_address)
                #                     ], limit=1)
                #                     if partner_id:
                #                         partner_ids.append(partner_id.id)
                #                     else:
                #                         partner_id = self.env['res.partner'].sudo().create({
                #                             'name': p_name or email_address,
                #                             'email': email_address,
                #                         })
                #                         partner_ids.append(partner_id.id)
                #     else:
                #         email_address = email_escape_char(
                #             email_split(msg_dict.get('cc'))[0])
                #         if email_address.lower() != 'info@softhealer.com' and email_address.lower() != 'sales@softhealer.com' and email_address.lower() != 'angeltest7890@gmail.com' and email_address.lower() != 'catchall@softhealer.com':
                #             partner_id = self.env['res.partner'].search([
                #                 ('email', '=', email_address)
                #             ], limit=1)
                #             if partner_id:
                #                 partner_ids.append(partner_id.id)
                #             else:
                #                 p_name = self.env['res.partner']._parse_partner_name(
                #                     msg_dict.get('cc'))[0] if msg_dict.get('cc') else email_address
                #                 partner_id = self.env['res.partner'].sudo().create({
                #                     'name': p_name or email_address,
                #                     'email': email_address,
                #                 })
                #                 partner_ids.append(partner_id.id)

                # if partner_ids:
                #     defaults.update({
                #         'message_partner_ids':[(6,0,partner_ids)],
                #     })

                # ======================================================
                # IN V16 ME MANAGED BY SUGGEST RECEIPTNS METHOD
                # ======================================================
                if partner_ids:
                    defaults.update({
                        'partner_ids': [(6, 0, partner_ids)],
                    })
                return super(HelpdeskTicket, self).message_new(msg_dict, custom_values=defaults)

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        if self.env.context.get('to_be_ignored'):
            blank_message = self.env['mail.message'].browse() 
            return blank_message

        # WHILE SEND MAIL FROM CHATTER'S SEND MESSAGE BUTTON ADD PARTNER IN FOLLOWERS IF NOT.
        if 'fetchmail_cron_running' not in self.env.context and self.partner_id and self.partner_id.id not in self.message_follower_ids.mapped('partner_id').ids:
            self.message_subscribe(partner_ids=self.partner_id.ids)

        mail_server_id = self.env['ir.mail_server'].sudo().search(
            [('smtp_user', '=', 'angeltest7890@gmail.com')], limit=1)
        if mail_server_id:
            kwargs.update({
                'mail_server_id': mail_server_id.id
            })        

        self.replied_date = fields.Datetime.now()

        domain = [('model', '=', 'sh.helpdesk.ticket'),('res_id', '=', self.id),('subtype_id.name', '=', 'Discussions')]
        find_message = self.env['mail.message'].search(domain)   
        if find_message and not self.env.context.get('fetchmail_cron_running'):

            if len(find_message) == 1 and find_message.author_id.email and find_message.author_id.email != 'mailto:angeltest7890@gmail.com':
                final_message = ''
                
                final_message+= Markup(kwargs['body']) + Markup('<br/>')
                final_message+= Markup('_________Original__________')+Markup(find_message.body)+Markup('<br/>')
                                
                kwargs.update({
                    'body' : final_message
                }) 
        elif not find_message and not self.env.context.get('fetchmail_cron_running'):
            if 'subtype_id' in kwargs:
                if kwargs.get('subtype_id') != self.env.ref('mail.mt_note').id:
                    final_message = ''
                        
                    final_message+= Markup(kwargs['body']) + Markup('<br/>')
                    final_message+= Markup('_________Original__________')+Markup(self.description)+Markup('<br/>')

                    kwargs.update({
                        'body' : final_message
                    })
            if 'subtype_xmlid' in kwargs:
                if kwargs.get('subtype_xmlid')!='mail.mt_note':
                    final_message = ''
                        
                    final_message+= Markup(kwargs['body']) + Markup('<br/>')
                    final_message+= Markup('_________Original__________')+Markup(self.description)+Markup('<br/>')

                    kwargs.update({
                        'body' : final_message
                    })

        
        if not self.env.context.get('fetchmail_cron_running'):
            
            # Should Not add Support User While Send Message From Portal Chatter
            if not kwargs.get('from_portal_chatter'):

                if kwargs.get('subtype_xmlid'):
                    if not kwargs.get('subtype_xmlid') == 'mail.mt_note':
                        find_support_user = self.env['res.partner'].search([('email','=','angeltest7890@gmail.com')],limit=1)

                        if find_support_user:
                            kwargs.update({
                                    'author_id' : find_support_user.id
                                })                    
                else:
                    find_support_user = self.env['res.partner'].search([('email','=','angeltest7890@gmail.com')],limit=1)

                    if find_support_user:
                        kwargs.update({
                                'author_id' : find_support_user.id
                            })
        if kwargs.get('from_portal_chatter'):

            self = self.with_context(form_portal_chatter = True)

        return super(HelpdeskTicket, self).message_post(**kwargs)

    def _message_post_after_hook(self, message, *args, **kwargs):
        if message.author_id.name == 'unknown customer':
            message.partner_ids = [(6, 0, [])] or False
        if self.email and not self.partner_id:
            new_partner = message.partner_ids.filtered(
                lambda partner: partner.email == self.email)
            if new_partner:
                self.search([
                    ('partner_id', '=', False),
                    ('email', '=', new_partner.email),
                ]).write({'partner_id': new_partner.id})
        return super(HelpdeskTicket, self)._message_post_after_hook(message, *args, **kwargs)

    def get_form_url(self):
        if self:
            base_url = self.env['ir.config_parameter'].sudo(
            ).get_param('web.base.url')
            url_str = ''
            action = self.env.ref('sh_helpdesk.helpdesk_ticket_action').id
            if base_url:
                url_str += str(base_url)+'/web#'
            for rec in self:
                url_str += 'id='+str(rec.id)+'&action='+str(action) + \
                    '&model=sh.helpdesk.ticket&view_type=form'
                rec.form_url = url_str

    def _get_report_base_filename(self):
        self.ensure_one()
        return '%s %s' % ('Ticket', self.name)

    @api.model_create_multi
    def create(self, values):
        for vals in values:
            if not vals.get('partner_id') and self.env.context.get('to_be_ignored'):                                               
                blank_helpdesk_records = self.env['sh.helpdesk.ticket'].browse() 
                return blank_helpdesk_records

        res = False
        for vals in values:
            partners = []
            if vals.get('partner_ids') and len(vals.get('partner_ids')[0][2]) > 0:
                for pid in vals.get('partner_ids')[0][2]:
                    partners.append(pid)
            vals.update({
                'sh_ticket_vals': str(vals)
            })
            # if vals.get('product_ids') and len(vals.get('product_ids')[0][2]) > 0:
            #     users = []
            #     if vals.get('sh_user_ids'):
            #         added_users = vals.get('sh_user_ids')[0][1]
            #         for u in added_users:
            #             users.append(u)
            #     products = vals.get('product_ids')[0][2]
            #     if products:
            #         for product in products:
            #             product_id = self.env['product.product'].sudo().browse(
            #                 product)
            #             if product_id and product_id.resposible_user_id and product_id.resposible_user_id.id not in users:
            #                 users.append(product_id.resposible_user_id.id)
            #             if product_id and product_id.other_responsible_users and product_id.other_responsible_users.ids not in users:
            #                 for o_u in product_id.other_responsible_users:
            #                     users.append(o_u.id)
            #     if users:
            #         vals.update({
            #             'sh_user_ids': [(6, 0, users)]
            #         })
            
            if not vals.get('partner_id') and self.env.context.get('to_be_ignored'):                                               
                blank_helpdesk_records = self.env['sh.helpdesk.ticket'].browse() 
                return blank_helpdesk_records

            if vals.get('partner_id') == False and vals.get('email'):

                # res = super(HelpdeskTicket, self).create(values)

                # if company_id.sh_demo_stage_id.id == res.stage_id.id:
                #     demo_tag_id = self.env['helpdesk.tags'].sudo().search(
                #         [('name', '=', 'Demo')], limit=1)
                #     if demo_tag_id:
                #         res.tag_ids = [(4, demo_tag_id.id)]
                # if res.sh_lead_ids:
                #     res.message_subscribe(
                #         partner_ids=res.sh_lead_ids[0].message_partner_ids.ids)
                # support_user_id = self.env['res.users'].sudo().search(
                #     [('login', '=', 'angeltest7890@gmail.com')], limit=1)

                # if support_user_id:
                #     if support_user_id.partner_id.name != 'unknown customer':
                #         res.message_subscribe(
                #             partner_ids=support_user_id.partner_id.ids)


                for (name, email) in tools.email_split_tuples(vals.get('email')):

                    if email and email != 'noreply@youtube.com' and email != 'no-reply@youtube.com':

                        partner_id = self.env['res.partner'].sudo().search(
                            [('email', '=', email)], limit=1)

                        if not partner_id:

                            partner_id = self.env['res.partner'].create({
                                'name': name,
                                'email': email,
                                'company_type': 'person',
                            })
                                                
                        partners.append(partner_id.id)
                        
                        vals.update({'partner_id': partner_id.id,'email': email,'person_name': partner_id.name})
                    
                
            
            if self.env.user.company_id.sh_default_team_id and not vals.get('team_id') and not vals.get('user_id'):
                vals.update({
                    'team_id': self.env.user.company_id.sh_default_team_id.id,
                    'team_head': self.env.user.company_id.sh_default_team_id.team_head.id,
                    'user_id': self.env.user.company_id.sh_default_user_id.id,
                })
            number = random.randrange(1, 10)
            company_id = self.env.user.company_id
            if company_id:
                vals['name'] = self.env['ir.sequence'].with_context(
                    check_company=company_id.id).next_by_code('sh.helpdesk.ticket')
                if company_id.new_stage_id:
                    vals['stage_id'] = company_id.new_stage_id.id
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sh.helpdesk.ticket')
            vals['color'] = number
            if partners:
                vals.update({
                    'partner_ids': [(6, 0, partners)]
                })
            # if res:
            #     for rec in res:
            #         if rec.stage_id and rec.stage_id.id == self.env.company.new_stage_id.id:
            #             stage_id = self.env['sh.helpdesk.stages'].browse(vals.get('stage_id'))
            #             if stage_id and stage_id.mail_template_ids:
            #                 for template in stage_id.mail_template_ids:
            #                     email_values = {'subject':'Re: '+rec.name}
            #                     template.send_mail(rec.id,force_send=True,email_values=email_values)
        if res:
            listt = []
            if res.team_head:
                listt.append(res.team_head.id)

            if res.sh_user_ids:
                listt.extend(res.sh_user_ids.ids)

            # if res.user_id:
            #     listt.append(res.user_id.id)
            # else:
            #     if res.team_id.team_members:
            #         listt.extend(res.team_id.team_members.ids)

            base_url = self.env['ir.config_parameter'].sudo(
            ).get_param('web.base.url')
            if len(listt) == 0:
                users = self.env['res.users'].search([])
                for user in users:
                    if user.has_group('sh_helpdesk.helpdesk_group_manager'):
                        if user.sh_new_notification_on_off:
                            listt.append(user.id)
            product_name = ''
            if res.product_ids:
                product_name = ' ('+str(res.product_ids[0].sh_technical_name)+')'

            self.env['user.push.notification'].push_notification(list(set(listt)), 'New Ticket Created', '%s:' % (
                res.name+product_name), base_url+"/mail/view?model=helpdesk.ticket&res_id="+str(res.id), 'sh.helpdesk.ticket', res.id, 'support')
            return res
        else:
            res=super(HelpdeskTicket, self).create(values)
            listt = []
            if res.team_head:
                listt.append(res.team_head)

            if res.sh_user_ids:
                listt.extend(res.sh_user_ids)

            # if res.user_id:
            #     listt.append(res.user_id)
            # else:
            #     if res.team_id.team_members:
            #         listt.extend(res.team_id.team_members)

            base_url = self.env['ir.config_parameter'].sudo(
            ).get_param('web.base.url')
            if len(listt) == 0:
                users = self.env['res.users'].search([])
                for user in users:
                    if user.has_group('sh_helpdesk.helpdesk_group_manager'):
                        if user.sh_new_notification_on_off:
                            listt.append(user)
            product_name = ''
            if res.product_ids:
                product_name = ' ('+str(res.product_ids[0].sh_technical_name)+')'
                
            if res.partner_id and res.partner_id.partner_category_id.id :
                res.partner_category_id = res.partner_id.partner_category_id.id

            self.env['user.push.notification'].push_notification(list(set(listt)), 'New Ticket Created', '%s:' % (
                res.name+product_name), base_url+"/mail/view?model=helpdesk.ticket&res_id="+str(res.id), 'sh.helpdesk.ticket', res.id, 'support')
            return res
        
    def write(self, vals):
        for record in self:
            if 'sh_auto_followup' in vals and vals.get('sh_auto_followup'):
                if record.stage_id.id != self.env.company.sh_auto_followup_stage_id.id:
                    vals.update({
                        'stage_id':self.env.company.sh_auto_followup_stage_id.id,
                        'sh_number_of_followup_taken': 0,
                    })
        if vals.get('partner_id'):
            partner_id = self.env['res.partner'].sudo().browse(
                vals.get('partner_id'))
            if partner_id:
                vals.update({
                    'partner_ids': [(4, partner_id.id)]
                })
        if vals.get('state'):
            if vals.get('state') == 'customer_replied':
                if self.env.user.company_id.sh_customer_replied:
                    for rec in self:
                        if rec.stage_id.id != self.env.user.company_id.new_stage_id.id:
                            vals.update({
                                'stage_id': self.env.user.company_id.sh_customer_replied_stage_id.id
                            })
            elif vals.get('state') == 'staff_replied':
                if self.env.user.company_id.sh_staff_replied:
                    for rec in self:
                        if rec.sh_auto_followup:
                            if self.env.user.company_id.sh_auto_followup_stage_id:
                                vals.update({
                                    'stage_id': self.env.user.company_id.sh_auto_followup_stage_id.id
                                })
                        else: 
                            if rec.stage_id.id != self.env.user.company_id.new_stage_id.id:
                                vals.update({
                                    'stage_id': self.env.user.company_id.sh_staff_replied_stage_id.id
                                })
        user_groups = self.env.user.groups_id.ids
        if vals.get('stage_id'):
            if vals.get('stage_id') == self.env.company.sh_auto_followup_stage_id.id:
                vals.update({
                    'sh_auto_followup':True,
                    'sh_number_of_followup_taken': 0,
                })
            if self.env['ir.module.module'].sudo().search([('name', '=', 'sh_demo_db')], limit=1).state == 'installed' and self.env.user.company_id.sh_demo_stage_id.id == vals.get('stage_id'):
                demo_tag_id = self.env['sh.helpdesk.tags'].sudo().search(
                    [('name', '=', 'Demo')], limit=1)
                if demo_tag_id:
                    vals.update({
                        'tag_ids': [(4, demo_tag_id.id)]
                    })
 
            stage_id = self.env['sh.helpdesk.stages'].sudo().search(
                [('id', '=', vals.get('stage_id'))], limit=1)
            if stage_id and stage_id.sh_group_ids:
                is_group_exist = False
                list_user_groups = user_groups
                list_stage_groups = stage_id.sh_group_ids.ids
                for item in list_stage_groups:
                    if item in list_user_groups:
                        is_group_exist = True
                        break
                if not is_group_exist:
                    raise UserError(
                        _('You have not access to edit this support request.'))
            
            # --------------------------------------------------------------
            
            # When ticket manually goes to done stage, Move related task of inquiry project to done stage
            if stage_id.id == self.company_id.done_stage_id.id:
                if self.company_id.project_id_created_from_so:
                    task_ids = self.env['project.task'].sudo().search(
                                [('sh_ticket_ids', 'in', [self.id])])
                    if task_ids:
                        for task in task_ids:
                            if task.project_id.id == self.company_id.project_id_created_from_so.id:
                                task.stage_id = task.company_id.done_project_stage_id.id
            # --------------------------------------------------------------

        
        if vals.get('stage_id') and not self.env.user.has_group('sh_helpdesk.helpdesk_group_team_leader') and self.env.user.share == False:
            raise UserError(_('You have not access to change stage.'))


        # if vals.get('product_ids') and len(vals.get('product_ids')[0][2]) > 0:
        #     users = []
        #     if vals.get('sh_user_ids'):
        #         added_users = vals.get('sh_user_ids')[0][1]
        #         for u in added_users:
        #             users.append(u)
        #     products = vals.get('product_ids')[0][2]
        #     if products:
        #         for product in products:
        #             product_id = self.env['product.product'].sudo().browse(
        #                 product)
        #             if product_id and product_id.resposible_user_id:
        #                 users.append(product_id.resposible_user_id.id)
        #             if product_id and product_id.other_responsible_users:
        #                 for o_u in product_id.other_responsible_users:
        #                     users.append(o_u.id)
        #     if users:
        #         vals.update({
        #             'sh_user_ids': [(6, 0, users)]
        #         })
        if vals.get('partner_id') and self.company_id.new_stage_id.mail_template_ids:
            for template in self.company_id.new_stage_id.mail_template_ids:
                template.sudo().send_mail(self.id, force_send=True)
        new_added_user=False
        if vals.get('sh_user_ids'):
            vals_users=vals.get('sh_user_ids')
            if len(vals_users[0])==3:
                vals_users=[x for x in vals_users[0][2]]
            elif len(vals_users[0])==2:
                vals_users=[x[1] for x in vals_users if len(x) == 2]
            if self.sh_user_ids:
                new_added_user=list(set(vals_users).difference(self.sh_user_ids.ids))
            else:
                new_added_user=vals_users
            new_added_user = self.env['res.users'].sudo().browse(new_added_user)
        res = super(HelpdeskTicket, self).write(vals)
        if vals.get('team_id') and vals.get('team_head') and vals.get('user_id') and vals.get('sh_user_ids') and not vals.get('ticket_allocated'):
            allocation_template = self.company_id.allocation_mail_template_id
            team_head = self.env['res.users'].sudo().browse(
                vals.get('team_head'))
            user_id = self.env['res.users'].sudo().browse(vals.get('user_id'))
            email_formatted = []
            if team_head.partner_id.email_formatted not in email_formatted:
                email_formatted.append(team_head.partner_id.email_formatted)
            if user_id.partner_id.email_formatted:
                email_formatted.append(user_id.partner_id.email_formatted)
            users = vals.get('sh_user_ids')[0][1]
            user_ids = self.env['res.users'].sudo().browse(users)
            for user in user_ids:
                if user.id != user_id.id:
                    if user.partner_id.email_formatted not in email_formatted:
                        email_formatted.append(user.partner_id.email_formatted)
            email_formatted_str = ','.join(email_formatted)
            email_values = {'email_to': email_formatted_str}
            if allocation_template:
                allocation_template.sudo().send_mail(self.id, force_send=True,
                                                     email_values=email_values)
            if self:
                for rec in self:
                    rec.ticket_allocated = True
        elif vals.get('team_id') and vals.get('team_head') and vals.get('user_id') and not vals.get('sh_user_ids') and not vals.get('ticket_allocated'):
            allocation_template = self.company_id.allocation_mail_template_id
            team_head = self.env['res.users'].sudo().browse(
                vals.get('team_head'))
            user_id = self.env['res.users'].sudo().browse(vals.get('user_id'))
            email_formatted = []
            if team_head.partner_id.email_formatted not in email_formatted:
                email_formatted.append(team_head.partner_id.email_formatted)
            if user_id.partner_id.email_formatted not in email_formatted:
                email_formatted.append(user_id.partner_id.email_formatted)
            email_formatted_str = ','.join(email_formatted)
            email_values = {'email_to': email_formatted_str}
            if allocation_template:
                allocation_template.sudo().send_mail(self.id, force_send=True,
                                                     email_values=email_values)
            if self:
                for rec in self:
                    rec.ticket_allocated = True
        elif vals.get('team_id') and vals.get('team_head') and not vals.get('user_id') and vals.get('sh_user_ids') and not vals.get('ticket_allocated'):
            allocation_template = self.company_id.allocation_mail_template_id
            email_formatted = []
            users = vals.get('sh_user_ids')[0][1]
            user_ids = self.env['res.users'].sudo().browse(users)
            team_head = self.env['res.users'].sudo().browse(
                vals.get('team_head'))
            if team_head.partner_id.email_formatted not in email_formatted:
                email_formatted.append(team_head.partner_id.email_formatted)
            for user in user_ids:
                if user.partner_id.email_formatted:
                    email_formatted.append(user.partner_id.email_formatted)
            email_formatted_str = ','.join(email_formatted)
            email_values = {'email_to': email_formatted_str}
            if allocation_template:
                allocation_template.sudo().send_mail(self.id, force_send=True,
                                                     email_values=email_values)
            if self:
                for rec in self:
                    rec.ticket_allocated = True

        elif not vals.get('team_id') and not vals.get('team_head') and vals.get('user_id') and vals.get('sh_user_ids') and not vals.get('ticket_allocated'):
            allocation_template = self.company_id.allocation_mail_template_id
            email_formatted = []
            user_id = self.env['res.users'].sudo().browse(vals.get('user_id'))
            users = vals.get('sh_user_ids')[0][1]
            user_ids = self.env['res.users'].sudo().browse(users)
            if user_id.partner_id.email_formatted not in email_formatted:
                email_formatted.append(user_id.partner_id.email_formatted)
            for user in user_ids:
                if user.id != user_id.id:
                    if user.partner_id.email_formatted not in email_formatted:
                        email_formatted.append(user.partner_id.email_formatted)
            email_formatted_str = ','.join(email_formatted)
            email_values = {'email_to': email_formatted_str}
            if allocation_template:
                allocation_template.sudo().send_mail(self.id, force_send=True,
                                                     email_values=email_values)
            if self:
                for rec in self:
                    rec.ticket_allocated = True
        elif not vals.get('team_id') and not vals.get('team_head') and vals.get('user_id') and not vals.get('sh_user_ids') and not vals.get('ticket_allocated'):
            allocation_template = self.company_id.allocation_mail_template_id
            user_id = self.env['res.users'].sudo().browse(vals.get('user_id'))
            email_values = {'email_to': str(
                user_id.partner_id.email_formatted)}
            if allocation_template:
                allocation_template.sudo().send_mail(self.id, force_send=True,
                                                     email_values=email_values)
            if self:
                for rec in self:
                    rec.ticket_allocated = True
        elif not vals.get('team_id') and not vals.get('team_head') and not vals.get('user_id') and vals.get('sh_user_ids') and not vals.get('ticket_allocated'):
            allocation_template = self.company_id.allocation_mail_template_id
            user_ids = False
            if vals.get('sh_user_ids') and len(vals.get('sh_user_ids')) == 1:
                users = vals.get('sh_user_ids')[0][1]
                user_ids = self.env['res.users'].sudo().browse(users)
            elif vals.get('sh_user_ids') and len(vals.get('sh_user_ids')) > 1:
                users = vals.get('sh_user_ids')[0][1]
                user_ids = self.env['res.users'].sudo().browse(users)
            email_formatted = []
            if user_ids:
                for user in user_ids:
                    if user.partner_id.email_formatted not in email_formatted:
                        email_formatted.append(user.partner_id.email_formatted)
                email_formatted_str = ','.join(email_formatted)
                email_values = {'email_to': email_formatted_str}
                if allocation_template:
                    allocation_template.sudo().send_mail(self.id, force_send=True,
                                                         email_values=email_values)
                if self:
                    for rec in self:
                        rec.ticket_allocated = True
        listt = []
        customer_replied_notif_users = []
        ticket_assigned_notif_users = []
        if self:
            for rec in self:
                # if rec.product_ids:
                #     if rec.product_ids[0].other_responsible_users:
                #         for responsible in rec.product_ids[0].other_responsible_users:
                #             if responsible not in customer_replied_notif_users:
                #                 customer_replied_notif_users.append(
                #                     responsible)
                #     if rec.product_ids[0].resposible_user_id:
                #         if rec.product_ids[0].resposible_user_id not in customer_replied_notif_users:
                #             customer_replied_notif_users.append(
                #                 rec.product_ids[0].resposible_user_id)
                if rec.team_head:
                    listt.append(rec.team_head.id)
                    if rec.team_head.sh_customer_reply_notification_on_off:
                        customer_replied_notif_users.append(rec.team_head)
                    if rec.team_head.sh_ticket_assigned_notification_on_off and vals.get('team_head'):
                        ticket_assigned_notif_users.append(rec.team_head)
                if rec.sh_user_ids:
                    listt.extend(rec.sh_user_ids.ids)
                    for u in rec.sh_user_ids:
                        if u.sh_customer_reply_notification_on_off:
                            customer_replied_notif_users.append(u)
                if rec.sh_user_ids and new_added_user:
                    for new_u in new_added_user:
                        if new_u.sh_ticket_assigned_notification_on_off:
                            ticket_assigned_notif_users.append(new_u)
                # if rec.user_id:
                #     listt.append(rec.user_id.id)
                #     if rec.user_id.sh_customer_reply_notification_on_off:
                #         customer_replied_notif_users.append(rec.user_id)
                #     if rec.user_id.sh_ticket_assigned_notification_on_off and vals.get('user_id'):
                #         ticket_assigned_notif_users.append(rec.user_id)
                # else:
                #     if rec.team_id.team_members:
                #         listt.extend(rec.team_id.team_members.ids)
                #         for m in rec.team_id.team_members:
                #             if m.sh_customer_reply_notification_on_off:
                #                 customer_replied_notif_users.append(m)
                #             if m.sh_ticket_assigned_notification_on_off:
                #                 ticket_assigned_notif_users.append(m)
                rec.message_unsubscribe(
                    partner_ids=self.env.user.partner_id.ids)
        

        if vals.get('team_head') or vals.get('user_id') or vals.get('sh_user_ids'):
            base_url = self.env['ir.config_parameter'].sudo(
            ).get_param('web.base.url')
            if self:
                for rec in self:
                    product_name = ''
                    if rec.product_ids:
                        product_name = ' (' + str(rec.product_ids[0].sh_technical_name)+')'
                    self.env['user.push.notification'].push_notification(list(set(ticket_assigned_notif_users)), 'Ticket Assigned', 'Ticket Ref %s:' % (
                        rec.name+product_name), base_url+"/mail/view?model=helpdesk.ticket&res_id="+str(rec.id), 'sh.helpdesk.ticket', rec.id,'support')

        if vals.get('state') == 'customer_replied':

            base_url = self.env['ir.config_parameter'].sudo(
            ).get_param('web.base.url')
            if self:
                for rec in self:
                    product_name = ''
                    if rec.product_ids:
                        product_name = ' (' + str(rec.product_ids[0].sh_technical_name)+')'
                    self.env['user.push.notification'].push_notification(list(set(customer_replied_notif_users)), 'Customer Replied ', 'Ticket Ref %s:' % (
                        rec.name+product_name), base_url+"/mail/view?model=helpdesk.ticket&res_id="+str(rec.id), 'sh.helpdesk.ticket', rec.id,'support')
        return res

    @api.depends('stage_id')
    def _compute_stage_booleans(self):
        if self:
            for rec in self:
                rec.cancel_stage_boolean = False
                rec.done_stage_boolean = False
                rec.reopen_stage_boolean = False
                rec.closed_stage_boolean = False
                rec.open_boolean = False
                if rec.stage_id.id == rec.company_id.cancel_stage_id.id:
                    rec.cancel_stage_boolean = True
                    rec.open_boolean = True
                elif rec.stage_id.id == rec.company_id.done_stage_id.id:
                    rec.done_stage_boolean = True
                    rec.open_boolean = True
                elif rec.stage_id.id == rec.company_id.reopen_stage_id.id:
                    rec.reopen_stage_boolean = True
                    rec.open_boolean = False
                elif rec.stage_id.id == rec.company_id.close_stage_id.id:
                    rec.closed_stage_boolean = True
                    rec.open_boolean = True

    @api.depends('stage_id')
    def _compute_cancel_button_boolean(self):
        if self:
            for rec in self:
                rec.cancel_button_boolean = False
                if rec.stage_id.is_cancel_button_visible:
                    rec.cancel_button_boolean = True

    @api.depends('stage_id')
    def _compute_done_button_boolean(self):
        if self:
            for rec in self:
                rec.done_button_boolean = False
                if rec.stage_id.is_done_button_visible:
                    rec.done_button_boolean = True

    def action_approve(self):
        self.ensure_one()
        if self.stage_id.sh_next_stage:
            self.stage_id = self.stage_id.sh_next_stage.id
            self.change_sh_status()
            self._compute_sh_sla_deadline()
            if self.stage_id.mail_template_ids:
                for template in self.stage_id.mail_template_ids:
                    template.sudo().send_mail(self.id, force_send=True)

    def aciton_draft(self):
        self.ensure_one()
        if self.company_id and self.company_id.new_stage_id:
            self.stage_id = self.company_id.new_stage_id.id

    def action_done(self):
        self.ensure_one()
        if self.company_id and self.company_id.done_stage_id and self.company_id.done_stage_id.mail_template_ids:
            for template in self.company_id.done_stage_id.mail_template_ids:
                template.sudo().send_mail(self.id, force_send=True)
            self.stage_id = self.company_id.done_stage_id.id

    def action_reply(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        template_id = self.company_id.reply_mail_template_id.id
        try:
            compose_form_id = ir_model_data.check_object_reference(
                'mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'sh.helpdesk.ticket',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'force_email': True
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    def action_closed(self):
        self.ensure_one()
        if self.company_id and self.company_id.close_stage_id and self.company_id.close_stage_id.mail_template_ids:
            for template in self.company_id.close_stage_id.mail_template_ids:
                template.sudo().send_mail(self.id, force_send=True)
        self.write({'close_date': fields.Datetime.now(), 'close_by': self.env.user.id,
                    'closed_stage_boolean': True, 'stage_id': self.company_id.close_stage_id.id})

    def action_cancel(self):
        self.ensure_one()
        if self.company_id and self.company_id.cancel_stage_id and self.company_id.cancel_stage_id.mail_template_ids:
            for template in self.company_id.cancel_stage_id.mail_template_ids:
                template.sudo().send_mail(self.id, force_send=True)
        stage_id = self.company_id.cancel_stage_id
        self.stage_id = stage_id.id
        self.cancel_date = fields.Datetime.now()
        self.cancel_by = self.env.user.id
        self.cancel_stage_boolean = True

    def action_open(self):
        if self.company_id and self.company_id.reopen_stage_id and self.company_id.reopen_stage_id.mail_template_ids:
            for template in self.company_id.reopen_stage_id.mail_template_ids:
                template.sudo().send_mail(self.id, force_send=True)
        self.write({
            'stage_id': self.company_id.reopen_stage_id.id,
            'open_boolean': True,
        })

    @api.onchange('team_id')
    def onchange_team(self):
        if self.team_id:
            self.team_head = self.team_id.team_head
            user_ids = self.env['sh.helpdesk.team'].sudo().search(
                [('id', '=', self.team_id.id)])
            return {'domain': {'user_id': [('id', 'in', user_ids.team_members.ids)], 'sh_user_ids': [('id', 'in', user_ids.team_members.ids)]}}
        else:
            self.team_head = False

    @api.onchange('category_id')
    def onchange_category(self):
        if self.category_id:
            sub_category_ids = self.env['helpdesk.subcategory'].sudo().search(
                [('parent_category_id', '=', self.category_id.id)]).ids
            products = []
            product_ids = self.env['product.product'].sudo().search(
                [('categ_id', '=', self.category_id.category_id.id)])
            if product_ids:
                for product in product_ids:
                    if product.id not in products:
                        products.append(product.id)
            return {'domain': {'sub_category_id': [('id', 'in', sub_category_ids)], 'product_ids': [('id', 'in', products)]}}
        else:
            self.sub_category_id = False

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id:
            self.person_name = self.partner_id.name
            self.email = self.partner_id.email
            self.mobile_no = self.partner_id.mobile
            self.partner_category_id = self.partner_id.partner_category_id.id
        else:
            self.person_name = False
            self.email = False
            self.mobile_no = False
            self.partner_category_id = False

    # def message_subscribe(
    #     self,
    #     partner_ids=None,
    #     channel_ids=None,
    #     subtype_ids=None
    # ):
    #     if self:
    #         if self.partner_id.name == 'unknown customer':
    #             return False
    #     return super(HelpdeskTicket, self).message_subscribe(partner_ids, subtype_ids)

    def action_stop_spaming_ticket(self):
        for rec in self:
            if rec.email:
                sh_email = email_split(rec.email)
                spam_lead_id = self.env['sh.skip.crm.lead'].sudo().create({
                    'name': sh_email[0]
                })
                if spam_lead_id:
                    self.env.user.company_id.sh_skip_crm_lead_ids = [
                        (4, spam_lead_id.id)]

    @api.model
    def _run_auto_close_ticket(self):
        company_ids = self.env['res.company'].sudo().search([])
        if company_ids:
            for company in company_ids:
                if company.auto_close_ticket:
                    # ticket_limit = 5
                    # if company.sh_close_ticket_limit > 0:
                    #     ticket_limit = company.sh_close_ticket_limit
                    tikcet_ids = self.env['sh.helpdesk.ticket'].sudo().search([
                        ('stage_id', 'in', company.sh_stage_safe_stage_to_auto_close_ticket_ids.ids),
                        ('sh_close_ticket','=',False)
                    ])
                    if tikcet_ids:
                        for ticket in tikcet_ids:
                            if ticket.partner_id.name == 'unknown customer':
                                replied_date = ticket.replied_date
                                if replied_date:
                                    no_of_days = company.close_days
                                    end_date = replied_date + \
                                        timedelta(days=no_of_days)
                                    if end_date < fields.Datetime.now():
                                        ticket.sudo().write({
                                            'close_date': fields.Datetime.now(),
                                            'closed_stage_boolean': True,
                                            'stage_id': company.close_stage_id.id,
                                            'sh_close_ticket': True
                                        })
                                        ticket._compute_stage_booleans()
                                        # Closes all tasks of ticket
                                        if ticket.task_ids and company.done_project_stage_id:
                                            for task in ticket.task_ids:
                                                if task.stage_id.id != company.done_project_stage_id.id:
                                                    task.write({'stage_id': company.done_project_stage_id.id, 'is_closed':True})
                            else:
                                replied_date = ticket.replied_date
                                if replied_date:
                                    no_of_days = company.close_days
                                    end_date = replied_date + \
                                        timedelta(days=no_of_days)
                                    if end_date < fields.Datetime.now():
                                        ticket.sudo().write({
                                            'close_date': fields.Datetime.now(),
                                            'closed_stage_boolean': True,
                                            'stage_id': company.close_stage_id.id,
                                            'sh_close_ticket': True
                                        })
                                        ticket._compute_stage_booleans()
                                        # Closes all tasks of ticket
                                        if ticket.task_ids and company.done_project_stage_id:
                                            for task in ticket.task_ids:
                                                if task.stage_id.id != company.done_project_stage_id.id:
                                                    task.write({'stage_id': company.done_project_stage_id.id, 'is_closed':True})

    # === For Helpdesk Task ====
    def _compute_task_count(self):
        if self:
            for rec in self:
                rec.task_count = 0
                task_ids = self.env['project.task'].sudo().search(
                    [('sh_ticket_ids', 'in', [rec.id])])
                if task_ids:
                    rec.task_count = len(task_ids.ids)

    def view_task(self):
        task_ids = self.env['project.task'].sudo().search(
            [('sh_ticket_ids', 'in', [self.id])])
        return{
            'name': 'Tasks',
            'res_model': 'project.task',
            'view_mode': 'kanban,tree,form',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', task_ids.ids)],
            'target': 'current',
        }

    #Ticket Auto Followup
    @api.model
    def _run_auto_followup(self):
        followup_stage_id = self.env['res.company'].search([]).mapped('sh_auto_followup_stage_id')
        followup_line_ids = self.env['sh.followup.history'].search([('sh_followup_ticket_id.ticket_type.sh_followup','=',True),('sh_followup_ticket_id.ticket_type.sh_followup_config_id','!=',False),('sh_followup_ticket_id.stage_id','=',followup_stage_id.id),('sh_status','=','pending')])
        if followup_line_ids:
            for followup_line in followup_line_ids:
                recipient_ids = []
                if followup_line.sh_followup_ticket_id.message_partner_ids:
                    for recepient in followup_line.sh_followup_ticket_id.message_partner_ids:
                        if recepient.email != 'angeltest7890@gmail.com':
                            recipient_ids.append(recepient.id)
                if followup_line.sh_schedule_date and followup_line.sh_schedule_date == fields.Date.today():
                    mail_compose_message_id=self.env['mail.compose.message'].create({'model':'sh.helpdesk.ticket',
                                                     'res_id':followup_line.sh_followup_ticket_id.id,
                                                     'partner_ids':[(6, 0, recipient_ids)],
                                                     'template_id':followup_line.sh_email_template_id.id,
                                                     'composition_mode':'comment',
                                                     'email_from':'angeltest7890@gmail.com',
                                                     'email_layout_xmlid':'mail.mail_notification_layout_with_responsible_signature',
                                                     })
                    mail_compose_message_id._compute_can_edit_body()
                    mail_compose_message_id._onchange_template_id_wrapper()
                    mail = mail_compose_message_id.with_context(auto_followup_email = True).action_send_mail()
                    print("\n\n\nmail",mail)

                    # email_values = {'subject':'Re: '+followup_line.sh_followup_ticket_id.name,'recipient_ids':[(6,0,recipient_ids)]}
                    # mail_id = followup_line.sh_email_template_id.sudo().send_mail(followup_line.sh_followup_ticket_id.id, force_send=True,email_values=email_values)
                    # mail = self.env['mail.mail'].sudo().search([('id','=',int(mail_id))])
                    # followup_line.sh_date_of_followup = fields.Date.today()
                    # if mail and mail.state in ['sent']:
                    #     followup_line.sh_status = 'success'
                    #     followup_line.sh_failure_reason = mail.failure_reason
                    # elif mail and mail.state not in ['sent']:
                    #     followup_line.sh_status = 'failure'
                        
                # ticket.sh_number_of_followup_taken = ticket.sh_number_of_followup_taken + 1
        # ticket_type_ids = self.env['sh.helpdesk.ticket.type'].search([('sh_followup','=',True),('sh_followup_config_id','!=',False)])
        # if ticket_type_ids:
        #     for ticket_type in ticket_type_ids:
        #         ticket_ids = self.env['sh.helpdesk.ticket'].search([('ticket_type','=',ticket_type.id),('sh_auto_followup','=',True),('stage_id','not in',ticket_type.sh_exclude_stage_ids.ids)])
        #         if ticket_ids:
        #             for ticket in ticket_ids:
        #                 recipient_ids = []
        #                 if ticket.message_partner_ids:
        #                     for recepient in ticket.message_partner_ids:
        #                         if recepient.email != 'angeltest7890@gmail.com':
        #                             recipient_ids.append(recepient.id)
        #                 if ticket.replied_date and ticket_type.sh_followup_inverval_selection == 'days':
        #                     followup_date = ticket.replied_date + timedelta(days=ticket_type.sh_followup_interval)
        #                     if followup_date <= fields.Datetime.now() and ticket.sh_number_of_followup_taken < ticket_type.sh_number_of_followup and ticket_type.sh_followup_template_id:
        #                         email_values = {'subject':'Re: '+ticket.name,'recipient_ids':[(6,0,recipient_ids)]}
        #                         ticket_type.sh_followup_template_id.sudo().send_mail(ticket.id, force_send=True,email_values=email_values)
        #                         ticket.sh_number_of_followup_taken = ticket.sh_number_of_followup_taken + 1
        #                 elif ticket.replied_date and ticket_type.sh_followup_inverval_selection == 'weeks':
        #                     followup_date = ticket.replied_date + timedelta(weeks=ticket_type.sh_followup_interval)
        #                     if followup_date <= fields.Datetime.now() and ticket.sh_number_of_followup_taken < ticket_type.sh_number_of_followup and ticket_type.sh_followup_template_id:
        #                         email_values = {'subject':'Re: '+ticket.name,'recipient_ids':[(6,0,recipient_ids)]}
        #                         ticket_type.sh_followup_template_id.sudo().send_mail(ticket.id, force_send=True,email_values=email_values)
        #                         ticket.sh_number_of_followup_taken = ticket.sh_number_of_followup_taken + 1
        #                 elif ticket.replied_date and ticket_type.sh_followup_inverval_selection == 'months':
        #                     followup_date = ticket.replied_date + relativedelta(months=ticket_type.sh_followup_interval)
        #                     if followup_date <= fields.Datetime.now() and ticket.sh_number_of_followup_taken < ticket_type.sh_number_of_followup and ticket_type.sh_followup_template_id:
        #                         email_values = {'subject':'Re: '+ticket.name,'recipient_ids':[(6,0,recipient_ids)]}
        #                         ticket_type.sh_followup_template_id.sudo().send_mail(ticket.id, force_send=True,email_values=email_values)
        #                         ticket.sh_number_of_followup_taken = ticket.sh_number_of_followup_taken + 1
        #                 elif ticket.replied_date and ticket_type.sh_followup_inverval_selection == 'year':
        #                     followup_date = ticket.replied_date + relativedelta(years=ticket_type.sh_followup_interval)
        #                     if followup_date <= fields.Datetime.now() and ticket.sh_number_of_followup_taken < ticket_type.sh_number_of_followup and ticket_type.sh_followup_template_id:
        #                         email_values = {'subject':'Re: '+ticket.name,'recipient_ids':[(6,0,recipient_ids)]}
        #                         ticket_type.sh_followup_template_id.sudo().send_mail(ticket.id, force_send=True,email_values=email_values)
        #                         ticket.sh_number_of_followup_taken = ticket.sh_number_of_followup_taken + 1

class FollowupHistory(models.Model):
    _name = 'sh.followup.history'
    _description = 'Followup History'

    sh_schedule_date = fields.Date('Schedule Date')
    sh_date_of_followup = fields.Date('Date of followup')
    sh_email_template_id = fields.Many2one('mail.template',string='Email Template')
    sh_status = fields.Selection([('pending','Pending'),('failure','Failure'),('success','Success')],string='Status')
    sh_followup_ticket_id = fields.Many2one('sh.helpdesk.ticket',string='Followup Ticket')
    sh_failure_reason = fields.Text('Failure Reason')

