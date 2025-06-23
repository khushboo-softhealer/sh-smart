# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, timedelta, time
from odoo.addons.sale.models.sale_order import READONLY_FIELD_STATES
LOCKED_FIELD_STATES = {
    state: [('readonly', True)]
    for state in {'done', 'cancel'}
}

class SaleRecurring(models.Model):
    _name = "sale.recurring"
    _inherit = ['portal.mixin', 'mail.thread','mail.activity.mixin', 'utm.mixin']
    _description = "Sale Order Recurring"
    _order = "id desc"

    name = fields.Char(
        string="Sale Recurring Reference",
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _("New"),
        tracking=True
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Customer",
        required=True,
        tracking=True
    )
    start_date = fields.Date(
        index=True,
        copy=False,
        required=True,
        default=fields.Date.context_today,
        store=True,
        tracking=True
    )
    active = fields.Boolean(default=True, tracking=True)
    title = fields.Char(tracking=True)
    note = fields.Text(tracking=True)
    order_line = fields.One2many(
        "sale.recurring.line",
        "sale_recurring_id",
        string="Order Lines",
        copy=True,
        auto_join=True
    )
    last_generated_date = fields.Date(
        string="Last date",
        index=True,
        copy=False,
        tracking=True
    )
    end_date = fields.Date(copy=False, tracking=True)

    state = fields.Selection([
        ("draft", "New"),
        ("confirm", "Running"),
        ("pending", "To Renew"),
        ("done", "Expired"),
        ("cancel", "Cancelled"),
    ],
        string="Status",
        required=True,
        copy=False,
        default="draft",
        tracking=True
    )

    # main recurring part
    recurring_interval = fields.Integer(
        string="Interval",
        default=1,
        required=True,
        tracking=True
    )
    recurring_interval_unit = fields.Selection([
        ("days", "Days"),
        ("weeks", "Weeks"),
        ("months", "Months"),
        ("years", "Years"),
    ],
        string="Interval Unit",
        default="years",
        required=True,
        tracking=True
    )

    stop_recurring_interval = fields.Integer(
        string="Stop after", tracking=True)
    stop_recurring_interval_unit = fields.Selection(
        related="recurring_interval_unit",
        string="Stop Interval Unit", required=True, tracking=True)

    signature = fields.Image(help='Signature received through the portal.',
                             copy=False, attachment=True, max_width=1024, max_height=1024)
    signed_by = fields.Char(
        help='Name of the person that signed the SO.', copy=False)
    signed_on = fields.Datetime(help='Date of the signature.', copy=False)

    online_signature = fields.Boolean(
        related='company_id.sh_sale_online_signature')
    company_id = fields.Many2one("res.company",
                                 string="Company",
                                 default=lambda self: self.env.company)

    partner_invoice_id = fields.Many2one(
        comodel_name='res.partner',
        string="Invoice Address",
        compute='_compute_partner_invoice_id',
        store=True, readonly=False, required=True, precompute=True,
        states=LOCKED_FIELD_STATES,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    partner_shipping_id = fields.Many2one(
        comodel_name='res.partner',
        string="Delivery Address",
        compute='_compute_partner_shipping_id',
        store=True, readonly=False, required=True, precompute=True,
        states=LOCKED_FIELD_STATES,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", )

    sale_order_template_id = fields.Many2one(
        comodel_name='sale.order.template',
        string="Quotation Template",
        compute='_compute_sale_order_template_id',
        store=True, readonly=False, check_company=True, precompute=True,
        states=READONLY_FIELD_STATES,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    odoo_version = fields.Many2one('sh.version', string="Version", required=True)

    pricelist_id = fields.Many2one(
        comodel_name='product.pricelist',
        string="Pricelist",
        compute='_compute_pricelist_id',
        store=True, readonly=False, precompute=True, check_company=True, required=True,  # Unrequired company
        states=READONLY_FIELD_STATES,
        tracking=1,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="If you change the pricelist, only newly added lines will be affected.")

    payment_term_id = fields.Many2one(
        comodel_name='account.payment.term',
        string="Payment Terms",
        compute='_compute_payment_term_id',
        store=True, readonly=False, precompute=True, check_company=True,  # Unrequired company
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",required=True)



    # project_id = fields.Many2one(domain="[('pricing_type', '!=', 'employee_rate'), ('analytic_account_id', '!=', False)]", readonly=False)

    project_manager = fields.Many2one("res.users", string="Project Manager", default=lambda self: self.env.user,required=True)

    po_ref = fields.Char("PO Reference")

    timeline = fields.Char(string="Timeline",required=True)

    estimated_hrs = fields.Float(string="Estimated Hours", copy=False, compute='_compute_estimated_hrs')

    sh_edition_id = fields.Many2one('sh.edition', string='Edition',required=True)

    is_sh_confirm_sale = fields.Boolean(string="Is Confirm Sale", default=False, copy=False)

    sh_is_download_module_mail_sent = fields.Boolean(string="Is Download Module Mail Sent", default=False, copy=False)

    sh_move_task_to_preapp_store = fields.Boolean('Create Task To PreApp Store')

    sh_replied_status_id = fields.Many2one('sh.replied.status', string='Replied Status ', index=True,group_expand='_read_group_replied_stage_ids', tracking=True)

    sh_sale_ticket_ids = fields.Many2many("sh.helpdesk.ticket", string="Tickets")

    responsible_user_id = fields.Many2one("res.users", string="Technical Head")

    sh_task_id = fields.Many2one("project.task", string="Task")

    website_id = fields.Many2one('website', string='Website',help='Website through which this order was placed for eCommerce orders.')

    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Salesperson",
        compute='_compute_user_id',
        store=True, readonly=False, precompute=True, index=True,
        tracking=2,
        domain=lambda self: "[('groups_id', '=', {}), ('share', '=', False), ('company_ids', '=', company_id)]".format(
            self.env.ref("sales_team.group_sale_salesman").id
        ))

    team_id = fields.Many2one(
        comodel_name='crm.team',
        compute='_compute_team_id',
        store=True, readonly=False, precompute=True, ondelete="set null",
        change_default=True, check_company=True,  # Unrequired company
        tracking=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    require_signature = fields.Boolean(
        string="Online Signature",
        compute='_compute_require_signature',
        store=True, readonly=False, precompute=True,
        states=READONLY_FIELD_STATES,
        help="Request a online signature and/or payment to the customer in order to confirm orders automatically.")


    require_payment = fields.Boolean(
        string="Online Payment",
        compute='_compute_require_payment',
        store=True, readonly=False, precompute=True,
        states=READONLY_FIELD_STATES)

    # Approx Planned Date
    sh_planned_date_from = fields.Date('Planned Date From', default=datetime.now(), required=True)
    sh_planned_date_to = fields.Date('Planned Date To', required=True)
    # Total Work Duration
    sh_total_work_duration = fields.Integer('Total Work Duration (Days)', required=True)
    sh_project_stage_tmpl_id = fields.Many2one(
        'sh.project.project.stage.template',
        string='Project Stage Template',required=True)
    sh_pricing_mode = fields.Selection([
        ('fp', 'FP - Fixed Price'),
        ('tm', 'T&M - Time and Material'),
    ], string="Pricing Model", required=True)
    sh_fp_based_on = fields.Selection([
        ('no_milestone', 'No Milestone - One shot'),
        ('milestone', 'Milestone Based'),
    ], string='FP Based On', required=True)
    sh_tm_based_on = fields.Selection([
        ('success_pack', 'Success Packs Based'),
        ('billable', 'Billable Hours Based'),
    ], string='T&M Based On',
        help='Success Packs Based (Renewable required based on usage) - SO\nBillable Hours Based (Monthly billable invoice created) - MANUALLY'
    )

    def write(self, vals):
        if 'sh_total_work_duration' in vals and vals['sh_total_work_duration']:
            if vals['sh_total_work_duration'] <= 0:
                raise ValidationError(_("Total Work Duration must be greater then zero."))
        return super(SaleRecurring, self).write(vals)


    def has_to_be_signed(self, include_draft=False):
        return True

    @api.depends('product_id')
    def _compute_product_uom(self):
        for line in self:
            if not line.product_uom or (line.product_id.uom_id.id != line.product_uom.id):
                line.product_uom = line.product_id.uom_id

    @api.onchange('sale_order_template_id')
    def _onchange_sale_order_template_id(self):
        if not self.sale_order_template_id:
            return

        sale_order_template = self.sale_order_template_id.with_context(lang=self.partner_id.lang)

        order_lines_data = [fields.Command.clear()]
        order_lines_data += [
            fields.Command.create(line._prepare_order_line_values())
            for line in sale_order_template.sale_order_template_line_ids
        ]

        # Rename 'product_uom' to 'product_uom_id'
        updated_order_lines_data = []
        for command in order_lines_data:
            if isinstance(command, tuple) and len(command) == 3 and isinstance(command[2], dict):
                values = command[2].copy()
                if 'product_uom' in values:
                    values['product_uom_id'] = values.pop('product_uom')
                updated_order_lines_data.append((command[0], command[1], values))
            else:
                updated_order_lines_data.append(command)

        # set first line to sequence -99, so a resequence on first page doesn't cause following page
        # lines (that all have sequence 10 by default) to get mixed in the first page
        if len(updated_order_lines_data) >= 2:
            updated_order_lines_data[1][2]['sequence'] = -99

        self.order_line = updated_order_lines_data


    @api.depends('company_id')
    def _compute_require_payment(self):
        for order in self:
            order.require_payment = order.company_id.portal_confirmation_pay

    @api.depends('company_id')
    def _compute_require_signature(self):
        for order in self:
            order.require_signature = order.company_id.portal_confirmation_sign

    @api.depends('partner_id', 'user_id')
    def _compute_team_id(self):
        cached_teams = {}
        for order in self:
            default_team_id = self.env.context.get('default_team_id',
                                                   False) or order.partner_id.team_id.id or order.team_id.id
            user_id = order.user_id.id
            company_id = order.company_id.id
            key = (default_team_id, user_id, company_id)
            if key not in cached_teams:
                cached_teams[key] = self.env['crm.team'].with_context(
                    default_team_id=default_team_id
                )._get_default_team_id(
                    user_id=user_id, domain=[('company_id', 'in', [company_id, False])])
            order.team_id = cached_teams[key]

    @api.depends('partner_id')
    def _compute_user_id(self):
        for order in self:
            if order.partner_id and not (order._origin.id and order.user_id):
                # Recompute the salesman on partner change
                #   * if partner is set (is required anyway, so it will be set sooner or later)
                #   * if the order is not saved or has no salesman already
                order.user_id = (
                        order.partner_id.user_id
                        or order.partner_id.commercial_partner_id.user_id
                        or (self.user_has_groups('sales_team.group_sale_salesman') and self.env.user)
                )

    @api.depends('order_line', 'order_line.sale_line_estimation_template_line')
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

    @api.depends('partner_id')
    def _compute_payment_term_id(self):
        for order in self:
            order = order.with_company(order.company_id)
            order.payment_term_id = order.partner_id.property_payment_term_id

    @api.depends('partner_id')
    def _compute_pricelist_id(self):
        for order in self:
            if not order.partner_id:
                order.pricelist_id = False
                continue
            order = order.with_company(order.company_id)
            order.pricelist_id = order.partner_id.property_product_pricelist

    # Do not make it depend on `company_id` field
    # It is triggered manually by the _onchange_company_id below iff the SO has not been saved.
    def _compute_sale_order_template_id(self):
        for order in self:
            company_template = order.company_id.sale_order_template_id
            if company_template and order.sale_order_template_id != company_template:
                if 'website_id' in self._fields and order.website_id:
                    # don't apply quotation template for order created via eCommerce
                    continue
                order.sale_order_template_id = order.company_id.sale_order_template_id.id

    @api.onchange('company_id')
    def _onchange_company_id(self):
        """Trigger quotation template recomputation on unsaved records company change"""
        if self._origin.id:
            return
        self._compute_sale_order_template_id()

    @api.depends('partner_id')
    def _compute_partner_invoice_id(self):
        for order in self:
            order.partner_invoice_id = order.partner_id.address_get(['invoice'])['invoice'] if order.partner_id else False

    @api.depends('partner_id')
    def _compute_partner_shipping_id(self):
        for order in self:
            order.partner_shipping_id = order.partner_id.address_get(['delivery'])['delivery'] if order.partner_id else False


    def active_sr(self):
        if self:
            for rec in self:
                if not rec.active:
                    rec.active = True

    def archive_sr(self):
        if self:
            for rec in self:
                if rec.active:
                    rec.active = False

    @api.onchange("stop_recurring_interval", "recurring_interval_unit", "start_date")
    def _onchange_stop_recurring_interval(self):
        if self and self.start_date:
            if self.stop_recurring_interval > 0:
                end_date = False
                st_date = fields.Date.from_string(self.start_date)
                if self.recurring_interval_unit == "days":
                    end_date = st_date + \
                        relativedelta(days=self.stop_recurring_interval - 1)
                elif self.recurring_interval_unit == "weeks":
                    end_date = st_date + \
                        relativedelta(weeks=self.stop_recurring_interval - 1)
                elif self.recurring_interval_unit == "months":
                    end_date = st_date + \
                        relativedelta(months=self.stop_recurring_interval - 1)
                elif self.recurring_interval_unit == "years":
                    end_date = st_date + \
                        relativedelta(years=self.stop_recurring_interval - 1)

                if end_date:
                    self.end_date = end_date
            else:
                self.end_date = False

    # compute no of sale order in this recuring
    sh_sale_recurring_count = fields.Integer(
        string="# of Sales Orders",
        compute="_compute_sh_sale_recurring_order_compute"
    )
    sh_quote_recurring_count = fields.Integer(
        string="# of Quotations",
        compute="_compute_sh_quote_recurring_compute"
    )
    sh_invoice_count = fields.Integer(
        string="# of Invoices",
        compute="_compute_sh_invoices_recurring_compute"
    )

    def _compute_access_url(self):
        super(SaleRecurring, self)._compute_access_url()
        for order in self:
            order.access_url = '/my/recurring_orders/%s' % (order.id)

    def _compute_sh_sale_recurring_order_compute(self):
        sale_order_obj = self.env["sale.order"]
        if self:
            for rec in self:
                rec.sh_sale_recurring_count = 0
                so_count = sale_order_obj.sudo().search_count([
                    ("sh_sale_recurring_order_id", "=", rec.id),
                    ("state", "in", ['sale', 'done'])
                ])
                rec.sh_sale_recurring_count = so_count

    def _compute_sh_quote_recurring_compute(self):
        sale_order_obj = self.env["sale.order"]
        if self:
            for rec in self:
                rec.sh_quote_recurring_count = 0
                quote_count = sale_order_obj.sudo().search_count([
                    ("sh_sale_recurring_order_id", "=", rec.id),
                    ("state", "in", ['draft', 'sent'])
                ])
                rec.sh_quote_recurring_count = quote_count

    def _compute_sh_invoices_recurring_compute(self):
        if self:
            for rec in self:
                rec.sh_invoice_count = 0
                orders = self.env['sale.order'].sudo().search(
                    [('sh_sale_recurring_order_id', '=', rec.id), ('state', 'in', ['sale', 'done'])])
                if orders:
                    invoices = []
                    for sale_order in orders:
                        if sale_order.invoice_ids:
                            for invoice in sale_order.invoice_ids:
                                if invoice.id not in invoices:
                                    invoices.append(invoice.id)
                    rec.sh_invoice_count = len(invoices)

    def action_view_recurring_order(self):
        if self:
            sale_order_obj = self.env["sale.order"]
            search_recurring_orders = sale_order_obj.sudo().search([
                ("sh_sale_recurring_order_id", "=", self.id),
                ('state', 'in', ['sale', 'done'])
            ])
            if search_recurring_orders:
                view = self.env.ref("sale.view_quotation_tree")
                _ = view and view.id or False
                return {
                    "name":   "Recurring Orders",
                    "type":   "ir.actions.act_window",
                    "view_type":   "form",
                    "view_mode":   "tree,form",
                    "target":   "self",
                    "res_model":   "sale.order",
                    "view_id":   False,
                    "domain":   [("id", "in", search_recurring_orders.ids)]
                }

    def action_view_invoices(self):
        if self:
            orders = self.env['sale.order'].sudo().search(
                [('sh_sale_recurring_order_id', '=', self.id), ('state', 'in', ['sale', 'done'])])
            invoices = []
            if orders:
                for sale_order in orders:
                    if sale_order.invoice_ids:
                        for invoice in sale_order.invoice_ids:
                            if invoice.id not in invoices:
                                invoices.append(invoice.id)
            action = self.env["ir.actions.actions"]._for_xml_id(
                "account.action_move_out_invoice_type")
            if len(invoices) > 1:
                action['domain'] = [('id', 'in', invoices)]
            elif len(invoices) == 1:
                form_view = [
                    (self.env.ref('account.view_move_form').id, 'form')]
                if 'views' in action:
                    action['views'] = form_view + \
                        [(state, view)
                         for state, view in action['views'] if view != 'form']
                else:
                    action['views'] = form_view
                action['res_id'] = invoices[0]
            else:
                action = {'type': 'ir.actions.act_window_close'}
            return action

    def action_view_recurring_quote(self):
        if self:
            sale_order_obj = self.env["sale.order"]
            search_recurring_orders = sale_order_obj.sudo().search([
                ("sh_sale_recurring_order_id", "=", self.id),
                ('state', 'in', ['draft', 'sent'])
            ])
            if search_recurring_orders:
                view = self.env.ref("sale.view_quotation_tree")
                _ = view and view.id or False
                return {
                    "name":   "Recurring Quotations",
                    "type":   "ir.actions.act_window",
                    "view_type":   "form",
                    "view_mode":   "tree,form",
                    "target":   "self",
                    "res_model":   "sale.order",
                    "view_id":   False,
                    "domain":   [("id", "in", search_recurring_orders.ids)]
                }

    @api.constrains("start_date", "end_date")
    def _check_dates(self):
        if self.filtered(lambda c: c.end_date and c.start_date > c.end_date):
            raise ValidationError(_("start date must be less than end date."))

    @api.constrains("stop_recurring_interval")
    def _check_stop_recurring_interval(self):
        if self.filtered(lambda c: c.stop_recurring_interval < 0):
            raise ValidationError(_("Stop after must be positive."))

    @api.constrains("recurring_interval")
    def _check_recurring_interval(self):
        if self.filtered(lambda c: c.recurring_interval < 0):
            raise ValidationError(_("Interval must be positive."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            recurring_seq = self.env["ir.sequence"].next_by_code(
                "sh.sale.recurring.sequence")
            vals.update({"name": recurring_seq})

        res = super(SaleRecurring, self).create(vals_list)
        res.message_subscribe(partner_ids=res.partner_id.ids)
        return res

    @api.model
    def recurring_order_cron(self):
        today = fields.Date.context_today(self)

        active_orders = self.env["sale.recurring"].search([
            ("state", "=", "confirm"),
            ("active", "=", True),
        ])

        for rec in active_orders:
            last_date = fields.Date.from_string(
                rec.last_generated_date) if rec.last_generated_date else fields.Date.from_string(rec.start_date)
            interval = rec.recurring_interval or 1

            # Determine target date based on recurring interval
            if rec.recurring_interval_unit == "days":
                target_date = last_date + relativedelta(days=interval)
                trigger_date = target_date
            elif rec.recurring_interval_unit == "weeks":
                target_date = last_date + relativedelta(weeks=interval)
                trigger_date = target_date - timedelta(days=1)
            elif rec.recurring_interval_unit == "months":
                target_date = last_date + relativedelta(months=interval)
                trigger_date = target_date - timedelta(days=7)
            elif rec.recurring_interval_unit == "years":
                target_date = last_date + relativedelta(years=interval)
                trigger_date = target_date - timedelta(days=7)

            # Check if today is the trigger day and not past end_date
            end_date = fields.Date.from_string(rec.end_date) if rec.end_date else None

            if trigger_date <= today and (not end_date or target_date <= end_date):
                # Prepare Sale Order
                sale_order_vals = {
                    "partner_id": rec.partner_id.id,
                    "date_order": target_date,
                    "sh_sale_recurring_order_id": rec.id,
                    "origin": rec.name,
                    "order_line": [],

                    'odoo_version': rec.odoo_version.id,
                    'project_manager': rec.project_manager.id,
                    'po_ref': rec.po_ref,
                    'timeline': rec.timeline,
                    'sh_edition_id': rec.sh_edition_id.id,
                    'is_sh_confirm_sale': rec.is_sh_confirm_sale,
                    'sh_is_download_module_mail_sent': rec.sh_is_download_module_mail_sent,
                    'sh_move_task_to_preapp_store': rec.sh_move_task_to_preapp_store,
                    'sh_replied_status_id': rec.sh_replied_status_id.id,
                    'sh_sale_ticket_ids': [(6, 0, rec.sh_sale_ticket_ids.ids)],
                    'responsible_user_id': rec.responsible_user_id.id,
                    'sh_task_id': rec.sh_task_id.id,
                    'website_id': rec.website_id.id,
                    'sh_planned_date_from': rec.sh_planned_date_from,
                    'sh_planned_date_to': rec.sh_planned_date_to,
                    'sh_total_work_duration': rec.sh_total_work_duration,
                    'sh_project_stage_tmpl_id': rec.sh_project_stage_tmpl_id.id,
                    'sh_pricing_mode': rec.sh_pricing_mode,
                    'sh_fp_based_on': rec.sh_fp_based_on,
                    'sh_tm_based_on': rec.sh_tm_based_on,
                    'sh_is_recurring': True,
                    'pricelist_id': rec.pricelist_id.id,
                }

                for line in rec.order_line:
                    if line.product_id and line.product_id.uom_id:
                        sale_order_vals["order_line"].append((0, 0, {
                            "product_id": line.product_id.id,
                            "price_unit": line.price_unit,
                            "product_uom_qty": line.product_uom_qty,
                            "discount": line.discount,
                            "product_uom": line.product_id.uom_id.id,
                            "name": line.name,
                            "analytic_distribution": line.analytic_distribution,
                        }))

                # Create Sale Order
                sale_order = self.env["sale.order"].create(sale_order_vals)

                if sale_order:
                    sale_order.order_line.sale_line_estimation_template_line = rec.order_line.sale_line_estimation_template_line
                    rec.last_generated_date = target_date

                    sale_manager_group_id = self.env.ref('sh_sale_order_recurring.group_recurring_sale_order_notification')
                    if sale_manager_group_id:
                        sale_manager_ids = self.env['res.users'].search([('groups_id', 'in', [sale_manager_group_id.id])])
                        for user in sale_manager_ids:
                            activity = self.env['mail.activity'].create({
                                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                                'user_id': user.id,
                                'res_id': sale_order.id,
                                'res_model_id': self.env['ir.model'].search([('model', '=', 'sale.order')], limit=1).id,
                                'summary': 'Please check and confirm it.',
                            })

            # If the recurring has reached the end, close it
            if end_date and target_date >= end_date:
                rec.state = "done"

    def create_order_manually(self):
        self.ensure_one()
        today = fields.Date.context_today(self)

        # Calculate last and next recurring dates
        last_date = fields.Date.from_string(self.last_generated_date) if self.last_generated_date else fields.Date.from_string(self.start_date)
        interval = self.recurring_interval or 1

        if self.recurring_interval_unit == "days":
            target_date = last_date + relativedelta(days=interval)
            trigger_date = target_date
        elif self.recurring_interval_unit == "weeks":
            target_date = last_date + relativedelta(weeks=interval)
            trigger_date = target_date - timedelta(days=1)
        elif self.recurring_interval_unit == "months":
            target_date = last_date + relativedelta(months=interval)
            trigger_date = target_date - timedelta(days=7)
        elif self.recurring_interval_unit == "years":
            target_date = last_date + relativedelta(years=interval)
            trigger_date = target_date - timedelta(days=7)

        # Handle end date check
        end_date = fields.Date.from_string(self.end_date) if self.end_date else None
        if end_date and target_date > end_date:
            self.state = "done"
            return

        # Only create if today >= trigger_date
        if today >= trigger_date:
            sale_order_vals = {
                "partner_id": self.partner_id.id,
                "date_order": target_date,
                "sh_sale_recurring_order_id": self.id,
                "origin": self.name,
                "order_line": [],

                'pricelist_id': self.pricelist_id.id,
                'odoo_version': self.odoo_version.id,
                'project_manager': self.project_manager.id,
                'po_ref': self.po_ref,
                'timeline': self.timeline,
                'sh_edition_id': self.sh_edition_id.id,
                'is_sh_confirm_sale': self.is_sh_confirm_sale,
                'sh_is_download_module_mail_sent': self.sh_is_download_module_mail_sent,
                'sh_move_task_to_preapp_store': self.sh_move_task_to_preapp_store,
                'sh_replied_status_id': self.sh_replied_status_id.id,
                'sh_sale_ticket_ids': [(6, 0, self.sh_sale_ticket_ids.ids)],
                'responsible_user_id': self.responsible_user_id.id,
                'sh_task_id': self.sh_task_id.id,
                'website_id': self.website_id.id,
                'sh_planned_date_from': self.sh_planned_date_from,
                'sh_planned_date_to': self.sh_planned_date_to,
                'sh_total_work_duration': self.sh_total_work_duration,
                'sh_project_stage_tmpl_id': self.sh_project_stage_tmpl_id.id,
                'sh_pricing_mode': self.sh_pricing_mode,
                'sh_fp_based_on': self.sh_fp_based_on,
                'sh_tm_based_on': self.sh_tm_based_on,
                'sh_is_recurring':True,
            }

            for line in self.order_line:
                if line.product_id and line.product_id.uom_id:
                    sale_order_vals["order_line"].append((0, 0, {
                        "product_id": line.product_id.id,
                        "price_unit": line.price_unit,
                        "product_uom_qty": line.product_uom_qty,
                        "discount": line.discount,
                        "product_uom": line.product_id.uom_id.id,
                        "name": line.name,
                        "analytic_distribution": line.analytic_distribution,
                    }))

            created_so = self.env["sale.order"].create(sale_order_vals)
            if created_so:
                created_so.order_line.sale_line_estimation_template_line = self.order_line.sale_line_estimation_template_line

                self.last_generated_date = target_date

                sale_manager_group_id = self.env.ref('sh_sale_order_recurring.group_recurring_sale_order_notification')
                if sale_manager_group_id:
                    sale_manager_ids = self.env['res.users'].search([('groups_id', 'in', [sale_manager_group_id.id])])
                    for user in sale_manager_ids:
                        activity = self.env['mail.activity'].create({
                            'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                            'user_id': user.id,
                            'res_id': created_so.id,
                            'res_model_id': self.env['ir.model'].search([('model', '=', 'sale.order')], limit=1).id,
                            'summary': 'Please check and confirm it.',
                        })

            if end_date and target_date >= end_date:
                self.state = "done"

    # action to change muti recode in action

    def action_to_renew(self):
        print("\n\n\n>>>> self", self)

        for recode in self:
            print("\n\n\n>>>muti ", recode.state)
            recode.write({'state': "pending"})

    def action_in_process(self):
        print("\n\n\n>>>> self", self)

        for recode in self:
            print("\n\n\n>>>muti ", recode.state)
            recode.write({'state': "confirm"})

    def action_expired(self):
        print("\n\n\n>>>> self", self)

        for recode in self:
            print("\n\n\n>>>muti ", recode.state)
            recode.write({'state': "done"})


class SaleRecurringLine(models.Model):
    _name = "sale.recurring.line"
    _description = "Sale Order Recurring Line"
    _inherit = ['analytic.mixin']

    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False)

    sale_recurring_id = fields.Many2one(
        "sale.recurring",
        string="Order Reference",
        ondelete="cascade",
        index=True,
        copy=False
    )
    product_id = fields.Many2one(
        "product.product",
        string="Product",
        domain=[("sale_ok", "=", True)],
        change_default=True,
        ondelete="restrict"
    )
    name = fields.Text(string="Description", required=True)
    price_unit = fields.Float(
        "Unit Price",
        digits="Product Price",
        default=0.0
    )
    discount = fields.Float(
        string="Discount (%)",
        digits="Discount",
        default=0.0
    )
    product_uom_qty = fields.Float(
        string="Quantity",
        digits="Product Unit of Measure",
        required=True,
        default=1.0
    )
    company_id = fields.Many2one("res.company",string="Company",default=lambda self: self.env.company)

    sale_line_estimation_template_line = fields.One2many('sh.sale.line.estimation.template.line', 'sale_recurring_line_id',string='Estimation Template Lines')
    estimation_template_id = fields.Many2one('sh.estimation.template', 'Estimation Template Id')
    website_description = fields.Char()
    sequence = fields.Integer(string="Sequence")

    @api.onchange("product_id")
    def product_id_change(self):
        if self:
            for rec in self:
                if rec.product_id:
                    name = rec.product_id.name_get()[0][1]
                    if rec.product_id.description_sale:
                        name += "\n" + rec.product_id.description_sale
                    rec.name = name
                    rec.price_unit = rec.product_id.lst_price

    product_uom_id = fields.Many2one(
        comodel_name='uom.uom',
        string="Unit of Measure",
        compute='_compute_product_uom_id',
        store=True, readonly=False, precompute=True,
        domain="[('category_id', '=', product_uom_category_id)]")


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('display_type', self.default_get(['display_type'])['display_type']):
                vals.update(product_id=False, product_uom_qty=0, product_uom_id=False)
        return super().create(vals_list)

    def write(self, values):

        res = super(SaleRecurringLine, self).write(values)

        if 'display_type' in values and self.filtered(lambda line: line.display_type != values.get('display_type')):
            raise UserError(_("You cannot change the type of a sale quote line. Instead you should delete the current line and create a new line of the proper type."))

        for vals in values:

            # TO ADD ESTIMATION LINE TOTAL HOURS AS A SALE ORDER QUANTITY
            # ===========================================================
            total_hours = 0
            if 'sale_line_estimation_template_line' in vals:
                if self.sale_line_estimation_template_line:
                    total_hours = 0
                    for line in self.sale_line_estimation_template_line:
                        total_hours += line.estimated_hours

                if self.product_uom_qty < total_hours:
                    raise ValidationError(
                        "You cannot add more quantity in Estimation then defined in sale order line !")

        return res


    @api.depends('product_id')
    def _compute_product_uom_id(self):
        for option in self:
            option.product_uom_id = option.product_id.uom_id

    @api.onchange('estimation_template_id')
    def onchange_estimation_template_id(self):
        for order_line in self:

            # Remove the Already existing lines from the one2many
            if order_line.sale_line_estimation_template_line:
                order_line.sale_line_estimation_template_line = False

            # Add the lines of template in one2many
            if order_line.estimation_template_id and order_line.estimation_template_id.estimation_template_line:
                for line in order_line.estimation_template_id.estimation_template_line:
                    estimation_template_line = self.env['sh.sale.line.estimation.template.line'].sudo().create({
                        'department_id': line.department_id.id,
                        'estimated_hours': line.estimated_hours,
                        'accountable_user_ids': line.accountable_user_ids,
                        'responsible_user_ids': line.responsible_user_ids,
                        'other_details': line.other_details,
                        'sale_recurring_line_id': order_line.id,
                    })


    def btn_add_detail_estimation(self):
        self.ensure_one()
        view = self.env.ref('sh_sale_order_recurring.sale_recurring_line_form_view')
        return {
            'name': _('Estimation Templates'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'sale.recurring.line',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': self.id,
        }