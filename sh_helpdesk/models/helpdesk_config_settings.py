# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    category = fields.Boolean('Category')
    sub_category = fields.Boolean('Sub Category')
    customer_rating = fields.Boolean('Customer Rating')
    auto_close_ticket = fields.Boolean('Auto Close Ticket')
    close_days = fields.Integer('No of Days')
    new_stage_id = fields.Many2one(
        'sh.helpdesk.stages', string="Draft/New Stage")
    done_stage_id = fields.Many2one('sh.helpdesk.stages', string="Resolved Stage")
    cancel_stage_id = fields.Many2one('sh.helpdesk.stages', string="Cancel Stage")
    allocation_mail_template_id = fields.Many2one(
        'mail.template', string='Ticket Allocation To User Mail Template')
    reply_mail_template_id = fields.Many2one(
        'mail.template', string='Ticket Reply Mail Template')
    dashboard_filter = fields.Many2many(
        'sh.helpdesk.stages', 'rel_company_stage_counter', string="Dashboard Filter")
    dashboard_tables = fields.Many2many(
        'sh.helpdesk.stages', 'rel_company_stage_tables', string="Dashboard Tables")
    reopen_stage_id = fields.Many2one(
        'sh.helpdesk.stages', string="Re-Opened Stage")
    close_stage_id = fields.Many2one('sh.helpdesk.stages', string="Closed Stage")
    sh_default_team_id = fields.Many2one(
        'sh.helpdesk.team', string="Default Team")
    sh_default_user_id = fields.Many2one(
        'res.users', string="Default Assign User")
    sh_display_multi_user = fields.Boolean('Display Multi Users ?')
    sh_configure_activate = fields.Boolean(
        'Manage Products')
    sh_display_ticket_reminder = fields.Boolean('Ticket Reminder ?')
    sh_ticket_product_detail = fields.Boolean(
        "Ticket Product details in Message?", default=True)
    sh_signature = fields.Boolean("Signature?", default=True)
    sh_display_in_chatter = fields.Boolean(
        "Display in Chatter Message?", default=True)
    sh_pdf_in_message = fields.Boolean(
        "Send Report URL in Message?", default=True)
    sh_ticket_url_in_message = fields.Boolean(
        "Send Ticket URL in Message?", default=True)
    sh_customer_replied = fields.Boolean(
        'Stage change when customer replied ?')
    sh_customer_replied_stage_id = fields.Many2one(
        'sh.helpdesk.stages', string='Customer Replied Stage')
    sh_in_progress_stage_id = fields.Many2one(
        'sh.helpdesk.stages', string='In Progress Stage')
    sh_staff_replied = fields.Boolean(
        'Stage change when staff replied ?')
    sh_staff_replied_stage_id = fields.Many2one(
        'sh.helpdesk.stages', string='Staff Replied Stage')
    # done_project_stage_id = fields.Many2one(
    #     'project.task.type', string='Done Task Stage')
    sh_downgrade_task_stage_id = fields.Many2one(
        'project.task.type', string='Downgrade Task Stage')
    sh_estimation_stage_id = fields.Many2one(
        'sh.helpdesk.stages', string='Estimation Stage')
    sh_estimation_product_id = fields.Many2one(
        'product.product', string='Default Estimation Product')
    sh_estimation_pricelist_id = fields.Many2one(
        'product.pricelist', string='Default Estimation Pricelist')
    sh_follower_domain_ids = fields.Many2many(
        'sh.ticket.follower.domain', string='Follower Email Domain')

    sh_expired_demo_db = fields.Integer('Demo DB Expired (Hours)')
    sh_demo_type_id = fields.Many2one(
        'sh.helpdesk.ticket.type', string='Demo Ticket Type')
    sh_demo_db_user_ids = fields.Many2many(
        'res.users', 'rel_user_demo_ids', string='Demo Responsible Users')

    sh_stage_safe_stage_to_auto_close_ticket_ids = fields.Many2many('sh.helpdesk.stages',string="Auto close Stages")
    sh_close_ticket_limit = fields.Integer('Ticket Limit to close automatic at a time')
    sh_close_crm_stage_id = fields.Many2one('crm.stage',string='Lead/Opportunity Close Stage')
    sh_default_sale_quotation_template = fields.Many2one('sale.order.template',string="Default Quotation Template")
    # sh_enquiry_type_id = fields.Many2one('sh.helpdesk.ticket.type',string='Enquiry Ticket Type')
    sh_auto_followup_stage_id = fields.Many2one('sh.helpdesk.stages',string='Auto Followup Stage')

class HelpdeskSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    sh_default_sale_quotation_template = fields.Many2one('sale.order.template',string="Default Quotation Template",related='company_id.sh_default_sale_quotation_template',readonly=False)
    
    sh_stage_safe_stage_to_auto_close_ticket_ids = fields.Many2many('sh.helpdesk.stages',string="Auto close Stages",related='company_id.sh_stage_safe_stage_to_auto_close_ticket_ids',readonly=False)

    # company_id = fields.Many2one('res.company', string='Company', required=True,
    #                              default=lambda self: self.env.user.company_id)
    category = fields.Boolean(
        string='Category', related='company_id.category', readonly=False)
    sub_category = fields.Boolean(
        string='Sub Category', related='company_id.sub_category', readonly=False)
    customer_rating = fields.Boolean(
        string='Customer Rating', related='company_id.customer_rating', readonly=False)
    auto_close_ticket = fields.Boolean(
        string='Auto Close Ticket', related='company_id.auto_close_ticket', readonly=False)
    close_days = fields.Integer(
        string='No of Days', related='company_id.close_days', readonly=False)
    new_stage_id = fields.Many2one('sh.helpdesk.stages', string="Draft/New Stage",
                                   related='company_id.new_stage_id', readonly=False, required=True)
    done_stage_id = fields.Many2one(
        'sh.helpdesk.stages', string="Resolved Stage", related='company_id.done_stage_id', readonly=False)
    cancel_stage_id = fields.Many2one(
        'sh.helpdesk.stages', string="Cancel Stage", related='company_id.cancel_stage_id', readonly=False)
    allocation_mail_template_id = fields.Many2one(
        'mail.template', string='Ticket Allocation To User Mail Template', related='company_id.allocation_mail_template_id', readonly=False)
    reply_mail_template_id = fields.Many2one(
        'mail.template', string='Ticket Reply Mail Template', related='company_id.reply_mail_template_id', readonly=False)
    dashboard_filter = fields.Many2many('sh.helpdesk.stages', 'rel_company_stage_counter',
                                        string="Dashboard Filter", related="company_id.dashboard_filter", readonly=False, required=True)
    dashboard_tables = fields.Many2many('sh.helpdesk.stages', 'rel_company_stage_tables',
                                        string="Dashboard Tables", related="company_id.dashboard_tables", readonly=False, required=True)
    reopen_stage_id = fields.Many2one(
        'sh.helpdesk.stages', string="Re-Opened Stage", readonly=False, related='company_id.reopen_stage_id')
    close_stage_id = fields.Many2one(
        'sh.helpdesk.stages', string="Closed Stage", readonly=False, related='company_id.close_stage_id')
    sh_default_team_id = fields.Many2one(
        'sh.helpdesk.team', string="Default Team", readonly=False, related='company_id.sh_default_team_id')
    sh_default_user_id = fields.Many2one(
        'res.users', string="Default Assign User", readonly=False, related='company_id.sh_default_user_id')
    sh_display_multi_user = fields.Boolean(
        'Display Multi Users ?', related='company_id.sh_display_multi_user', readonly=False)
    sh_configure_activate = fields.Boolean(
        'Manage Products', related='company_id.sh_configure_activate', readonly=False)
    sh_display_ticket_reminder = fields.Boolean(
        'Ticket Reminder ?', related='company_id.sh_display_ticket_reminder', readonly=False)
    sh_ticket_product_detail = fields.Boolean(
        "Ticket Product details in Message?", related='company_id.sh_ticket_product_detail', readonly=False)
    sh_signature = fields.Boolean(
        "Signature?", related='company_id.sh_signature', readonly=False)
    sh_display_in_chatter = fields.Boolean(
        "Display in Chatter Message?", related='company_id.sh_display_in_chatter', readonly=False)
    sh_pdf_in_message = fields.Boolean(
        "Send Report URL in Message?", related='company_id.sh_pdf_in_message', readonly=False)
    sh_ticket_url_in_message = fields.Boolean(
        "Send Ticket URL in Message?", related='company_id.sh_ticket_url_in_message', readonly=False)
    sh_customer_replied = fields.Boolean(
        'Stage change when customer replied ?', related='company_id.sh_customer_replied', readonly=False)
    sh_customer_replied_stage_id = fields.Many2one(
        'sh.helpdesk.stages', string='Customer Replied Stage', related='company_id.sh_customer_replied_stage_id', readonly=False)
    sh_in_progress_stage_id = fields.Many2one(
        'sh.helpdesk.stages',related='company_id.sh_in_progress_stage_id', string='In Progress Stage', readonly=False)
    sh_staff_replied = fields.Boolean(
        'Stage change when staff replied ?', related='company_id.sh_staff_replied', readonly=False)
    sh_staff_replied_stage_id = fields.Many2one(
        'sh.helpdesk.stages', string='Staff Replied Stage', related='company_id.sh_staff_replied_stage_id', readonly=False)
    # done_project_stage_id = fields.Many2one(
    #     'project.task.type', string='Done Task Stage', readonly=False, related='company_id.done_project_stage_id')
    sh_downgrade_task_stage_id = fields.Many2one(
        'project.task.type', string='Downgrade Task Stage', readonly=False, related='company_id.sh_downgrade_task_stage_id')
    sh_estimation_stage_id = fields.Many2one(
        'sh.helpdesk.stages', string='Estimation Stage', related='company_id.sh_estimation_stage_id', readonly=False)
    sh_estimation_product_id = fields.Many2one(
        'product.product', string='Default Estimation Product', related='company_id.sh_estimation_product_id', readonly=False)
    sh_estimation_pricelist_id = fields.Many2one(
        'product.pricelist', string='Default Estimation Pricelist', related='company_id.sh_estimation_pricelist_id', readonly=False)
    sh_follower_domain_ids = fields.Many2many(
        'sh.ticket.follower.domain', string='Follower Email Domain', related='company_id.sh_follower_domain_ids', readonly=False)

    sh_expired_demo_db = fields.Integer(
        'Demo DB Expired (Hours)', readonly=False, related='company_id.sh_expired_demo_db')
    sh_demo_type_id = fields.Many2one(
        'sh.helpdesk.ticket.type', string='Demo Ticket Type', related='company_id.sh_demo_type_id', readonly=False)
    sh_demo_db_user_ids = fields.Many2many(
        'res.users', string='Demo Responsible Users', related='company_id.sh_demo_db_user_ids', readonly=False)
    sh_close_ticket_limit = fields.Integer('Ticket Limit to close automatic at a time', related='company_id.sh_close_ticket_limit', readonly=False)
    sh_close_crm_stage_id = fields.Many2one('crm.stage',string='Lead/Opportunity Close Stage', related='company_id.sh_close_crm_stage_id', readonly=False)
    # sh_enquiry_type_id = fields.Many2one(related='company_id.sh_enquiry_type_id', readonly=False)
    sh_auto_followup_stage_id = fields.Many2one('sh.helpdesk.stages',string='Auto Followup Stage',readonly=False,related='company_id.sh_auto_followup_stage_id')