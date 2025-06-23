# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models


class InvoiceRecurringLine(models.Model):
    _name = "sh.invoice.recurring.line"
    _description = "Invoice Recurring Line"

    invoice_recurring_id = fields.Many2one(
        'sh.invoice.recurring', string='Order Reference', required=True, ondelete='cascade', index=True, copy=False)
    product_id = fields.Many2one(
        'product.product', string='Product', required=True)
    name = fields.Text(string='Description', required=True)
    price_unit = fields.Float(
        'Unit Price', required=True, digits='Product Price', default=0.0)
    discount = fields.Float(string='Discount (%)',
                            digits="Discount", default=0.0)
    quantity = fields.Float(
        string='Quantity', digits='Product Unit of Measure', required=True, default=1.0)
    company_id = fields.Many2one(
        "res.company", string="Company", default=lambda self: self.env.company)
    account_id = fields.Many2one(
        'account.account', string="Account", required=True)
    tax_ids = fields.Many2many('account.tax', string="Taxes")
    product_uom_category_id = fields.Many2one(
        'uom.category', related='product_id.uom_id.category_id')
    product_uom_id = fields.Many2one(
        'uom.uom', string="UoM", domain="[('category_id', '=', product_uom_category_id)]")
    journal_id = fields.Many2one(
        related='invoice_recurring_id.journal_id', store=True, index=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'account_id' not in vals and 'invoice_recurring_id' in vals:
                recurring=self.env['sh.invoice.recurring'].browse(vals.get('invoice_recurring_id'))
                vals.update({'account_id':recurring.journal_id.default_account_id.id})
        return super(InvoiceRecurringLine, self).create(vals_list)

    @api.model
    def default_get(self, default_fields):
        values = super(InvoiceRecurringLine, self).default_get(default_fields)
        if 'account_id' in default_fields and not values.get('account_id') and self._context.get('journal_id'):
            journal = self.env['account.journal'].browse(
                self._context['journal_id'])
            values.setdefault('account_id', journal.default_account_id.id)
        return values

    @api.onchange('product_id')
    def product_id_change(self):
        for rec in self:
            if rec.product_id:
                name = rec.product_id.name_get()[0][1]
                if rec.product_id.description_sale:
                    name += '\n' + rec.product_id.description_sale
                rec.name = name
                rec.price_unit = rec.product_id.lst_price
                rec.tax_ids = rec.product_id.taxes_id
