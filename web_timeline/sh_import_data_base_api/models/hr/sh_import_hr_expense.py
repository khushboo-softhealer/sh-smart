# -*- coding: utf-8 -*
# Part of Softhealer Technologies.

from odoo import models
import requests


class InheritImportHrContract(models.Model):
    _inherit = "sh.import.base"

    def import_hr_expense_cron(self):

        confid = self.env['sh.import.base'].search([], limit=1)
        response = requests.get(
            '''%s/api/public/hr.expense?query={tax_ids{*},currency_id{name},company_currency_id{name},*}''' % (confid.base_url))
        if response.status_code == 200:
            response_json = response.json()
            if 'count' in response_json:
                if self.records_per_page != response_json['count']:
                    self.current_import_page = 0
            count = 0
            failed = 0
            for result in response_json['result']:
                expense_vals = self.process_expense_vals(result)
                domain = [('remote_hr_expense_id', '=', result.get('id'))]
                find_expense_obj = self.env['hr.expense'].search(domain)
                try:
                    if find_expense_obj:
                        find_expense_obj.write(expense_vals)
                    else:
                        self.env['hr.expense'].create(expense_vals)
                    count += 1
                except Exception as e:
                    failed += 1
                    self.create_fail_log(
                        name=result.get('id'),
                        field_type='hr_basic',
                        error=e,
                        import_json=result,
                    )

            if count > 0:
                self.create_log(
                    field_type='hr_basic', error="%s Expense Imported Successfully" % (count), state='success')
            if failed > 0:
                self.create_log(
                    field_type='hr_basic', error="%s Expense Failed To Import" % (failed))
        else:
            self.create_log(
                field_type='hr_basic', error=response.text)

    def process_expense_vals(self, data):
        vals = {
            'name': data.get('name'),
            'date': data.get('date'),
            'unit_amount': data.get('unit_amount'),
            'quantity': data.get('quantity'),
            'untaxed_amount': data.get('untaxed_amount'),
            'total_amount': data.get('total_amount'),
            'total_amount_company': data.get('total_amount_company'),
            'company_id': 1,
            'description': data.get('description'),
            'attachment_number': data.get('attachment_number'),
            'state': data.get('state')['sh_api_current_state'],
            'reference': data.get('reference'),
            'is_refused': data.get('is_refused'),
            'payment_mode': data.get('payment_mode')['sh_api_current_state'],
            'remote_hr_expense_id': data.get('id'),
            'company_id': 1,
        }

        self.map_many2one_field(
            'hr.employee', 'remote_hr_employee_id', data, vals, 'employee_id')
        self.map_many2one_field(
            'product.product', 'remote_product_product_id', data, vals, 'product_id')
        self.map_tax_ids(data, vals)
        self.map_currency_id(data, vals)
        self.map_currency_id(data, vals, 'company_currency_id')

        # sheet_id (hr.expense.sheet)
        # if data.get('sheet_id'):
        #     if data['sheet_id'].get('id') and data['sheet_id'].get('id') != 0:
        #         domain = [('remote_hr_expense_sheet_id',
        #                    '=', data['sheet_id'].get('id'))]
        #         find_sheet_obj = self.env['hr.expense.sheet'].search(domain)
        #         if find_sheet_obj:
        #             vals['sheet_id'] = find_sheet_obj.id
        #         else:
        #             sheet_vals = {}

        return vals
