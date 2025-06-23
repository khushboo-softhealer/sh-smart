# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, timedelta, time


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sh_sale_recurring_order_id = fields.Many2one(
        "sale.recurring",
        string="Recurring Order"
    )
    sh_recurrent_order = fields.Many2one("sale.order")
    sh_is_recurring = fields.Boolean(string="Is Recurring?")
   
    recurring_start_date = fields.Date(copy=False, tracking=True)
    recurring_end_date = fields.Date(copy=False, tracking=True)
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
    

    @api.onchange("recurring_interval", "recurring_interval_unit", "recurring_start_date")
    def _onchange_stop_recurring_interval(self):
        if self and self.recurring_start_date:
            recurring_end_date = False
            st_date = fields.Date.from_string(self.recurring_start_date)
            if self.recurring_interval_unit == "days":
                recurring_end_date = st_date + \
                    relativedelta(days=self.recurring_interval)
            elif self.recurring_interval_unit == "weeks":
                recurring_end_date = st_date + \
                    relativedelta(weeks=self.recurring_interval) - relativedelta(days=1)
            elif self.recurring_interval_unit == "months":
                recurring_end_date = st_date + \
                    relativedelta(months=self.recurring_interval) - relativedelta(days=1)
            elif self.recurring_interval_unit == "years":
                recurring_end_date = st_date + \
                    relativedelta(years=self.recurring_interval) - relativedelta(days=1)

            if recurring_end_date:
                self.recurring_end_date = recurring_end_date
            


    @api.model
    def recurring_order_cron(self):
        today = fields.Date.context_today(self)

        recurring_orders = self.env["sale.order"].search([
            ("sh_is_recurring", "=", True),
            ("sh_recurrent_order",'=',False),
            ('state','not in',['cancel','draft'])
        ])

        for rec in recurring_orders:
            # Check if today is the trigger day and not past recurring_end_date
            recurring_end_date = fields.Date.from_string(rec.recurring_end_date) if rec.recurring_end_date else None

           
            target_date = recurring_end_date
            trigger_date = recurring_end_date
            # Determine target date based on recurring interval
            if rec.recurring_interval_unit == "days":
                trigger_date = target_date
            elif rec.recurring_interval_unit == "weeks":
                trigger_date = target_date - relativedelta(days=1)
            elif rec.recurring_interval_unit == "months":
                trigger_date = target_date - relativedelta(weeks=1)
            elif rec.recurring_interval_unit == "years":
                trigger_date = target_date - relativedelta(months=1)

            if trigger_date == today and target_date >= today and not rec.sh_recurrent_order:
                # Prepare Sale Order
                # Create Sale Order
                sale_order =rec.sudo().copy()
                sale_order.sudo().write({'project_id':rec.project_id.id,'recurring_start_date':rec.recurring_end_date  + relativedelta(days=1)})
                

                if sale_order:
                    # sale_order.order_line.sale_line_estimation_template_line = rec.order_line.sale_line_estimation_template_line
                 

                    sale_manager_group_id = self.env.ref('sh_sale_order_recurring.group_recurring_sale_order_notification')
                    if sale_manager_group_id:
                        sale_manager_ids = self.env['res.users'].search([('groups_id', 'in', [sale_manager_group_id.id])])
                        for user in sale_manager_ids:
                            activity = self.env['mail.activity'].create({
                                'activity_type_id': self.env.ref('sale.mail_act_sale_upsell').id,
                                'user_id': user.id,
                                'res_id': sale_order.id,
                                'res_model_id': self.env['ir.model'].search([('model', '=', 'sale.order')], limit=1).id,
                                'summary': 'Please check and confirm it.',
                            })

                    rec.sudo().write({'sh_recurrent_order':sale_order.id})
