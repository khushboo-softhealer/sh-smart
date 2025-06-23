# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models
import requests
from datetime import datetime
from datetime import timedelta
import json

class DynamicPrice(models.Model):
    _inherit = 'res.currency'

    #--------NEW METHOD-----------
    def _dynamic_currency_price(self):
        domain = [('active', '=', True)]
        all_currency = self.env['res.currency'].search(domain)
        all_company = self.env['res.company'].search([])
        
        content_url = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/eur.json"
        response = requests.get(url=content_url)
        response_json = response.json()

        if response_json.get('eur',False):
            result = response_json.get('eur')
            inr_rate = result.get('inr')
            
            if all_currency:
                for data in all_currency:
                    to_currency = '%s' % (data.name.lower())
                    for company in all_company:
                        domain = [('name', '=', response_json.get('date',False)),
                                ('currency_id', '=', data.id),('company_id','=',company.id)]
                        find_date = self.env['res.currency.rate'].search(domain)
                        vals = {'rate': result.get(to_currency)/inr_rate}
                        if find_date:
                            find_date.write(vals)
                        else:
                            vals['currency_id'] = data.id
                            vals['name'] = response_json['date']
                            vals['company_id'] = company.id
                            self.env['res.currency.rate'].create(vals)

        # Euro To Inr Rate in PRoduct/
        result = response_json.get('eur')
        inr_rate = result.get('inr')
        domain = []
        
        ### Template
        find_product = self.env['product.template'].search(domain)
        for data in find_product:
            if data.euro_price_duplicate and data.euro_price_duplicate > 0:
                data.write({'list_price': inr_rate*data.euro_price_duplicate})
                # total_price = data.sh_custom_update_price_with_depends(data)
                # print('\n\n total_price 1',total_price)
                # data.write({'sh_sales_price_with_depends': total_price})
            else:
                data.sh_custom_update_price_with_depends(data)
        
        ### Variants
        find_product_var = self.env['product.product'].search(domain)
        for rec in find_product_var:
            if rec.euro_price and rec.euro_price > 0:
                rec.write({'list_price': inr_rate*rec.euro_price})
                
                
    # def _dynamic_currency_price(self):
    #     domain = [('active', '=', True)]
    #     all_currency = self.env['res.currency'].search(domain)
    #     all_company = self.env['res.company'].search([])
    #     if all_currency:
    #         for data in all_currency:
    #             inr_currency = 'inr'
    #             to_currency = '%s' % (data.name.lower())
    #             content_url = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/%s/%s.json" % (
    #                 inr_currency, to_currency)
    #             response = requests.get(url=content_url)
    #             response_json = response.json()
    #             for company in all_company:
    #                 domain = [('name', '=', response_json['date']),
    #                         ('currency_id', '=', data.id),('company_id','=',company.id)]
    #                 find_date = self.env['res.currency.rate'].search(domain)
    #                 vals = {'rate': response_json[to_currency]}
    #                 if find_date:
    #                     find_date.write(vals)
    #                 else:
    #                     vals['currency_id'] = data.id
    #                     vals['name'] = response_json['date']
    #                     vals['company_id'] = company.id
    #                     self.env['res.currency.rate'].create(vals)

    #     # Euro To Inr Rate in PRoduct/
    #     rate_url = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/eur/inr.json"
    #     responses = requests.get(url=rate_url)
    #     responses_json = responses.json()
    #     inr_rate = responses_json['inr']
    #     domain = []
        
    #     ### Template
    #     find_product = self.env['product.template'].search(domain)
    #     for data in find_product:
    #         if data.euro_price_duplicate and data.euro_price_duplicate > 0:
    #             data.write({'list_price': inr_rate*data.euro_price_duplicate})
    #             # total_price = data.sh_custom_update_price_with_depends(data)
    #             # print('\n\n total_price 1',total_price)
    #             # data.write({'sh_sales_price_with_depends': total_price})
    #         else:
    #             data.sh_custom_update_price_with_depends(data)
        
    #     ### Variants
    #     find_product_var = self.env['product.product'].search(domain)
    #     for rec in find_product_var:
    #         if rec.euro_price and rec.euro_price > 0:
    #             rec.write({'list_price': inr_rate*rec.euro_price})

    #--------NEW METHOD-----------
    def update_past_currency_rates(self):
        date = "2021-12-31"
        date_obj = datetime.strptime(date,'%Y-%m-%d')
        today = datetime.today()
        delta = today - date_obj
        for i in range(0,delta.days):            
            date_obj = date_obj + timedelta(days=1)
            date_str = date_obj.strftime('%Y-%m-%d')
            domain = [('currency_id','=',self.id),('name','=',date_str)]
            already_created = self.env['res.currency.rate'].search(domain)
            if not already_created:
                inr_currency = 'inr'
                to_currency = '%s' % (self.name.lower())
                content_url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{date_str}/v1/currencies/eur.json"
                
                response = requests.get(url=content_url)
                if response.status_code == 200:
                    response_json = response.json()
                    if response_json.get('eur',False):
                        result = response_json.get('eur')
                        inr_rate = result.get('inr')
                        
                        vals = {'rate': result.get(to_currency)/inr_rate}
                        vals['currency_id'] = self.id
                        vals['name'] = response_json.get('date',False)
                        self.env['res.currency.rate'].create(vals)
    
    #--------OLD METHOD-----------
    # def update_past_currency_rates(self):
    #     date = "2021-12-31"
    #     date_obj = datetime.strptime(date,'%Y-%m-%d')
    #     today = datetime.today()
    #     delta = today - date_obj
    #     for i in range(0,delta.days):            
    #         date_obj = date_obj + timedelta(days=1)
    #         date_str = date_obj.strftime('%Y-%m-%d')
    #         domain = [('currency_id','=',self.id),('name','=',date_str)]
    #         already_created = self.env['res.currency.rate'].search(domain)
    #         if not already_created:
    #             inr_currency = 'inr'
    #             to_currency = '%s' % (self.name.lower())
    #             content_url = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/%s/currencies/%s/%s.json" % (
    #                 date_str,inr_currency, to_currency)
    #             response = requests.get(url=content_url)
    #             if response.status_code == 200:
    #                 response_json = response.json()
    #                 vals = {'rate': response_json[to_currency]}
    #                 vals['currency_id'] = self.id
    #                 vals['name'] = response_json['date']
    #                 self.env['res.currency.rate'].create(vals)