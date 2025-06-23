# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import api, fields, models, Command
from odoo.tools.safe_eval import safe_eval as eval
from odoo.exceptions import ValidationError

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    def _compute_fees(self, amount, currency, country):
        """ Compute the transaction fees.

        The computation is based on the fields `fees_dom_fixed`, `fees_dom_var`, `fees_int_fixed`
        and `fees_int_var`, and is performed with the formula
        :code:`fees = (amount * variable / 100.0 + fixed) / (1 - variable / 100.0)` where the values
        of `fixed` and `variable` are taken from either the domestic (`dom`) or international
        (`int`) fields, depending on whether the country matches the company's country.

        For a provider to base the computation on different variables, or to use a different
        formula, it must override this method and return the resulting fees.

        :param float amount: The amount to pay for the transaction.
        :param recordset currency: The currency of the transaction, as a `res.currency` record.
        :param recordset country: The customer country, as a `res.country` record.
        :return: The computed fees.
        :rtype: float
        """
        self.ensure_one()

        fees = 0.0
        if self.fees_active:
            if country == self.company_id.country_id:
                fixed = self.fees_dom_fixed
                variable = self.fees_dom_var
            else:
                fixed = self.fees_int_fixed
                variable = self.fees_int_var
            # fees = (amount * variable / 100.0 + fixed) / (1 - variable / 100.0)
            fees = (amount * variable / 100.0 + fixed) # Changed by softhealer 
        return fees


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _create_payment(self, **extra_create_values):
        """Create an `account.payment` record for the current transaction.

        If the transaction is linked to some invoices, their reconciliation is done automatically.

        Note: self.ensure_one()

        :param dict extra_create_values: Optional extra create values
        :return: The created payment
        :rtype: recordset of `account.payment`
        """
        self.ensure_one()

        payment_method_line = self.provider_id.journal_id.inbound_payment_method_line_ids\
            .filtered(lambda l: l.code == self.provider_code)
        total_payment_amount = round(self.amount,2) + round(self.fees,2)
        payment_values = {
            #amount updated ---Code added by softhealer to add fees in amount
            'amount': abs(total_payment_amount),  # A tx may have a negative amount, but a payment must >= 0
            #=========code end ---softhealer---
            # 'amount': abs(self.amount),  # A tx may have a negative amount, but a payment must >= 0
            'payment_type': 'inbound' if self.amount > 0 else 'outbound',
            'currency_id': self.currency_id.id,
            'partner_id': self.partner_id.commercial_partner_id.id,
            'partner_type': 'customer',
            'journal_id': self.provider_id.journal_id.id,
            'company_id': self.provider_id.company_id.id,
            'payment_method_line_id': payment_method_line.id,
            'payment_token_id': self.token_id.id,
            'payment_transaction_id': self.id,
            'ref': f'{self.reference} - {self.partner_id.name} - {self.provider_reference or ""}',
            **extra_create_values,
        }
        payment = self.env['account.payment'].create(payment_values)
        payment.action_post()

        # Track the payment to make a one2one.
        self.payment_id = payment

        if self.invoice_ids:
            self.invoice_ids.filtered(lambda inv: inv.state == 'draft').action_post()

            (payment.line_ids + self.invoice_ids.line_ids).filtered(
                lambda line: line.account_id == payment.destination_account_id
                and not line.reconciled
            ).reconcile()

        return payment

    def _invoice_sale_orders(self):
        for tx in self.filtered(lambda tx: tx.sale_order_ids):
            # Create invoices
            tx = tx.with_company(tx.company_id).with_context(company_id=tx.company_id.id)
            confirmed_orders = tx.sale_order_ids.filtered(lambda so: so.state in ('sale', 'done'))
            if confirmed_orders:
                confirmed_orders._force_lines_to_invoice_policy_order()
                
                invoices = confirmed_orders.with_context(
                    raise_if_nothing_to_invoice=False
                )._create_invoices()

                # Setup access token in advance to avoid serialization failure between
                # edi postprocessing of invoice and displaying the sale order on the portal
                for invoice in invoices:
                    invoice._portal_ensure_token()
                    #Code by softhealer to add paypal fee product in invoice
                    if tx.provider_id.code == 'paypal' and tx.fees > 0.0:
                    # if tx.provider_id.code == 'stripe':
                        paypal_product = self.env.ref('sh_paypal_fee_mgmt.paypal_fee_product')
                        if not paypal_product:
                            raise ValidationError("Paypal Fee product not found !")
                        
                        # accounts = paypal_product.product_tmpl_id.get_product_accounts(
                        # invoice.fiscal_position_id)
                        paypal_product = paypal_product.with_company(5)

                        invoice_line_vals = {
                            'product_id': paypal_product.id,
                            'product_uom_id' : paypal_product.uom_id.id,
                            'name': "Paypal Fees",
                            'quantity': 1.0,
                            'price_unit': tx.fees,
                            'move_id': invoice.id,
                            'account_id': paypal_product.property_account_income_id.id or paypal_product.categ_id.property_account_income_categ_id.id,
                            'tax_ids':[(6,0,[])]
                        }
                        print("\n\n\ninvoice_line_vals",invoice_line_vals)
                        line = self.env['account.move.line'].with_context(
                            check_move_validity=False).sudo().create(invoice_line_vals)

                    #=code end=======================softhealer
                tx.invoice_ids = [Command.set(invoices.ids)]