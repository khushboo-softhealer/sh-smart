# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ShInvoiceTimesheetWizard(models.TransientModel):
    _name = 'sh.timesheet.invoice.wizard'
    _description = 'Timesheet Invoice'

    @api.model
    def default_get(self, fields_list):
        res = super(ShInvoiceTimesheetWizard, self).default_get(fields_list)
        if self.env.user.company_id.invoice_product_id:
            res['sh_invoice_product_id'] = self.env.user.company_id.invoice_product_id.id
        return res

    sh_invoice_product_id = fields.Many2one(
        'product.product', 'Invoice Product')
    select_type = fields.Selection(
        [('timesheet', 'Timesheet'), ('task', 'Task'), ('project', 'Project')])

    def action_creating_invoice(self):
        active_ids = self.env.context.get('active_ids')
        if active_ids:
            project_list = []
            timesheet_ids = self.env['account.analytic.line'].sudo().search(
                [('id', 'in', active_ids)])
            for data in timesheet_ids:
                if data.project_id not in project_list:
                    project_list.append(data.project_id)
            if len(project_list) > 1:
                raise UserError(_("You Cannot select Multiple Project"))
            product = False
            if self.sh_invoice_product_id:
                product = self.sh_invoice_product_id
            elif project_list[0].sh_product_id:
                product = project_list[0].sh_product_id
            else:
                raise UserError(_("Please Select Product First"))
            partner = False
            if project_list[0].partner_id:
                partner = project_list[0].partner_id
            if product:
                invoice_line_list = []
                timesheet_vals = {
                    # 'partner_id' : partner.id if partner else False,
                    'user_id': self.env.user.id,
                    'date_invoice': fields.Date.today(),
                    'type': 'out_invoice',
                }
                created_invoice = self.env['account.move'].create(
                    timesheet_vals)
                accounts = product.product_tmpl_id.get_product_accounts(
                    created_invoice.fiscal_position_id)
                if self.select_type == 'timesheet':
                    tasks = []
                    for data in timesheet_ids:
                        if data.task_id not in tasks:
                            tasks.append(data.task_id)
                    for tt in tasks:
                        sec_vals = {
                            'display_type': 'line_section',
                            'name': tt.name
                        }
                        invoice_line_list.append((0, 0, sec_vals))
                        for time in tt.timesheet_ids:
                            if time in timesheet_ids:
                                line_vals = {
                                    'product_id': product.id,
                                    'name': time.name,
                                    'quantity': time.unit_amount_invoice,
                                    'price_unit': product.list_price,
                                    'account_id': accounts['income'].id
                                }
                                invoice_line_list.append((0, 0, line_vals))
                    if invoice_line_list:
                        created_invoice.write({
                            'invoice_line_ids': invoice_line_list
                        })
                    return {
                        "type": "ir.actions.act_window",
                        "name": "Invoice",
                        "views": [(self.env.ref('account.view_move_form').id, 'form')],
                        "res_model": "account.move",
                        "res_id": created_invoice.id,
                    }
                elif self.select_type == 'task':
                    tasks = []
                    for data in timesheet_ids:
                        if data.task_id not in tasks:
                            tasks.append(data.task_id)
                    for tt in tasks:
                        hours = 0.0
                        for time in tt.timesheet_ids:
                            if time in timesheet_ids:
                                hours += time.unit_amount_invoice
                        line_vals = {
                            'product_id': product.id,
                            'name': tt.name,
                            'quantity': hours,
                            'price_unit': product.list_price,
                            'account_id': accounts['income'].id
                        }
                        invoice_line_list.append((0, 0, line_vals))
                    if invoice_line_list:
                        created_invoice.write({
                            'invoice_line_ids': invoice_line_list
                        })
                    return {
                        "type": "ir.actions.act_window",
                        "name": "Invoice",
                        "views": [(self.env.ref('account.view_move_form').id, 'form')],
                        "res_model": "account.move",
                        "res_id": created_invoice.id,
                    }

                elif self.select_type == 'project':
                    hours = 0.0
                    for data in timesheet_ids:
                        hours = hours + data.unit_amount_invoice
                    line_vals = {
                        'product_id': product.id,
                        'name': project_list[0].name,
                        'quantity': hours,
                        'price_unit': product.list_price,
                        'account_id': accounts['income'].id
                    }
                    invoice_line_list.append((0, 0, line_vals))
                    if invoice_line_list:
                        created_invoice.write({
                            'invoice_line_ids': invoice_line_list
                        })
                    return {
                        "type": "ir.actions.act_window",
                        "name": "Invoice",
                        "views": [(self.env.ref('account.view_move_form').id, 'form')],
                        "res_model": "account.move",
                        "res_id": created_invoice.id,
                    }
            # else:
            #     raise UserError (_("Product OR Customer is missing"))
