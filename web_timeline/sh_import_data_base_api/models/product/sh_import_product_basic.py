# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
import requests
import json
from datetime import datetime

class InheritImportBase(models.Model):
    _inherit = "sh.import.base"
    

    def import_product_public_category(self):
        response = requests.get('%s/api/public/product.public.category?query={*,parent_id{*}}' %(self.base_url))
        if response.status_code == 200:
            response_json = response.json()
            total_count = response_json['count']
            count = 0
            for categ in response_json['result']:
                print("................categ...........",categ)
                domain = [('name', '=', categ['name'])]
                find_category = self.env['product.public.category'].search(domain)
                if find_category:
                    count += 1
                    find_category.write({
                        'remote_product_public_categ_id' : categ['id'],
                    })
                else:
                    categ_vals = {
                        'name' : categ['name'],
                        'remote_product_public_categ_id' : categ['id'],
                        'show_category':categ['show_category'],
                    }
                    if categ['parent_id']['name'] != '':
                        domain = [('name', '=', categ['parent_id']['name'])]
                        find_parent_id = self.env['product.public.category'].search(domain,limit=1)
                        if find_parent_id:
                            categ_vals['parent_id'] = find_parent_id.id
                    

                    created_category =self.env['product.public.category'].create(categ_vals)
                    count += 1
                    if categ['child_id']:
                       find_categ = self.env['product.public.category'].search([('remote_product_public_categ_id','in',categ['child_id'])]) 
                       if find_categ:
                           for categ in find_categ:
                               categ.write({'parent_id':created_category.id})
            if count == total_count:
                vals = {
                    "name": self.name,
                    "state": "success",
                    "field_type": "category",
                    "error": "All Ecommerce Category Imported Successfully",
                    "datetime": datetime.now(),
                    "base_config_id": self.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)
        else:
            vals = {
                "name": self.name,
                "state": "error",
                "field_type": "category",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": self.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals)
    def import_product_category(self):
        response = requests.get('%s/api/public/product.category?query={*,parent_id{*}}' %(self.base_url))
        if response.status_code == 200:
            response_json = response.json()
            total_count = response_json['count']
            count = 0
            for categ in response_json['result']:
                domain = [('name', '=', categ['name'])]
                find_category = self.env['product.category'].search(domain)
                if find_category:
                    count += 1
                    find_category.write({
                        'remote_product_category_id' : categ['id'],
                    })
                else:
                    categ_vals = {
                        'name' : categ['name'],
                        'remote_product_category_id' : categ['id'],
                    }
                    if categ['parent_id']['name'] != '':
                        domain = [('name', '=', categ['parent_id']['name'])]
                        find_parent_id = self.env['product.category'].search(domain,limit=1)
                        if find_parent_id:
                            categ_vals['parent_id'] = find_parent_id.id                       
                    created_category =self.env['product.category'].create(categ_vals)
                    count += 1
                    count += 1
                    if categ['child_id']:
                       find_categ = self.env['product.category'].search([('remote_product_category_id','in',categ['child_id'])]) 
                       if find_categ:
                           for categ in find_categ:
                               categ.write({'parent_id':created_category.id})
            if count == total_count:
                vals = {
                    "name": self.name,
                    "state": "success",
                    "field_type": "category",
                    "error": "All Category Imported Successfully",
                    "datetime": datetime.now(),
                    "base_config_id": self.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)
        else:
            vals = {
                "name": self.name,
                "state": "error",
                "field_type": "category",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": self.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals)
            
    def process_category(self,category):
        domain = ['|',('name', '=', category['name']),('remote_uom_category_id', '=', category['id'])]
        find_category = self.env['uom.category'].search(domain,limit=1)
        if find_category:
            find_category.write({
                'remote_uom_category_id' : category['id']
            })
            return find_category
        else:
            categ_vals = {
                'name' : category['name'],
                'measure_type' : category['measure_type']['sh_api_current_state'],
                'remote_uom_category_id' : category['id']
            }
            created_category = self.env['uom.category'].create(categ_vals)
            return created_category  
    
    def process_pricelist(self,data):
        pricelist_vals={
            'remote_product_pricelist_id':data.get('id'),
            'active':data.get('active'),
            'selectable':data.get('selectable'),
            'sh_show_in_offer_page':data.get('sh_show_in_offer_page'),
            'code':data.get('code'),
            'display_name':data.get('display_name'),
            'name':data.get('name'),
            'sh_description':data.get('sh_description'),
            'sequence':data.get('sequence'),
            'discount_policy':data.get('discount_policy').get('sh_api_current_state'),
            'company_id':1
        }
        
        # ============ CONNECT WITH COUNTRY GROUP ======================
        if data.get('country_group_ids'):
            country_group_list=[]
            for country_group in data.get('country_group_ids'):
                domain=[('name','=',country_group.get('name'))]
                find_country_group=self.env['res.country.group'].search(domain,limit=1)
                if find_country_group:
                    country_group_list.append((4,find_country_group.id))
                else:
                    country_group_vals={
                        'name':country_group.get('name'),
                        'display_name':country_group.get('display_name'),
                    }
                    if country_group.get('country_ids'):
                        country_list=[]
                        for country in country_group.get('country_ids'):
                            find_contry=self.env['res.country'].search([('name','=',country.get('name'))],limit=1)
                            if find_contry:
                                country_list.append((4,find_contry.id)) 
                    if country_list:
                        country_group_vals['country_ids']=country_list
                    if country_group_vals:
                        created_country_group=self.env['res.country.group'].create(country_group_vals)
                        if created_country_group:
                            country_group_list.append((4,created_country_group.id))
            if country_group_list:
                pricelist_vals['country_group_ids']=country_group_list
        
        if data.get('currency_id'):
            domain=[('name','=',data.get('currency_id').get('name'))]
            find_currency_id=self.env['res.currency'].search(domain,limit=1)
            if find_currency_id:
                pricelist_vals['currency_id']=find_currency_id.id   
                
        if data.get('item_ids'):
            item_list=[]
            for item in data.get('item_ids'):
                item_vals={
                    'display_name':item.get('display_name'),
                    'name':item.get('name'),
                    'price':item.get('price'),
                    'fixed_price':item.get('fixed_price'),
                    'percent_price':item.get('percent_price'),
                    'price_discount':item.get('price_discount'),
                    'price_max_margin':item.get('price_max_margin'),
                    'price_min_margin':item.get('price_min_margin'),
                    'price_round':item.get('price_round'),
                    'price_surcharge':item.get('price_surcharge'),
                    'min_quantity':item.get('min_quantity'),
                    'applied_on':item.get('applied_on').get('sh_api_current_state'),
                    'base':item.get('base').get('sh_api_current_state'),
                    'compute_price':item.get('compute_price').get('sh_api_current_state'),
                    'company_id':1
                }  
                if item.get('date_end'):
                    date_time=datetime.strptime(item.get('date_end'),'%Y-%m-%d')
                    item_vals['date_end']=date_time
                if item.get('date_start'):
                    date_time=datetime.strptime(item.get('date_start'),'%Y-%m-%d')
                    item_vals['date_start']=date_time  
             
                if item.get('base_pricelist_id'):
                    find_base_pricelist=self.env['product.pricelist'].search([('remote_product_pricelist_id','=',item.get('base_pricelist_id'))])
                    if find_base_pricelist:
                        item_vals['base_pricelist_id']=find_base_pricelist.id
                        
                if item.get('categ_id'):
                    domain = [('name', '=', item.get('categ_id')['name'])]
                    find_category = self.env['product.category'].search(domain)
                    if find_category:
                        item_vals['categ_id']=find_category.id
                    else:
                        categ_vals = {
                        'name' : item.get('categ_id')['name'],
                        'remote_product_category_id' : item.get('categ_id')['id'],
                        }
                        if item.get('categ_id')['parent_id']['name'] != '':
                            domain = [('name', '=', item.get('categ_id')['parent_id']['name'])]
                            find_parent_id = self.env['product.category'].search(domain)
                            if find_parent_id:
                                categ_vals['parent_id'] = find_parent_id.id
                        created_category=self.env['product.category'].create(categ_vals)  
                        if created_category:
                            item_vals['categ_id']=created_category.id          
                if item.get('currency_id'):   
                    domain=[('name','=',item.get('currency_id').get('name'))]
                    find_currency_id=self.env['res.currency'].search(domain,limit=1)
                    if find_currency_id:
                        item_vals['currency_id']=find_currency_id.id
                        
                if item.get('product_id') and item.get('product_id')!=0:
                    domain=[('remote_product_product_id','=',item.get('product_id').get('id'))]
                    find_product=self.env['product.product'].search(domain)
                    if find_product:
                        item_vals['product_id']=find_product.id   
                            
                if item.get('product_tmpl_id') and item.get('product_tmpl_id').get('id') and item.get('product_tmpl_id').get('id')!=0:                
                    domain=[('remote_product_template_id','=',item.get('product_tmpl_id').get('id'))]
                    find_product=self.env['product.template'].search(domain)
                    if find_product:
                        item_vals['product_tmpl_id']=find_product.id   
                    else:
                        product_vals=self.process_product_data(item.get('product_tmpl_id'))
                        if product_vals:
                            created_product=self.env['product.template'].create(product_vals)
                            if created_product:
                                if created_product:
                                    item_vals['product_tmpl_id']=created_product.id                
                               
                if item_vals:
                    item_list.append((0,0,item_vals))  
            if item_list:
                pricelist_vals['item_ids']=item_list
                                       
        return pricelist_vals    
        
    def import_product_pricelist(self):
        response = requests.get('%s/api/public/product.pricelist?query={*,country_group_ids{*,country_ids{name}},currency_id{*},item_ids{*,categ_id{id,name, parent_id{name}},currency_id{*},product_id{*,taxes_id{name,amount,type_tax_use},supplier_taxes_id{name,amount,type_tax_use},seller_ids{*,name{name,title,ref,type,website,supplier,street,email,is_company,phone,mobile,id,company_type}}},product_tmpl_id{*,taxes_id{name,amount,type_tax_use},supplier_taxes_id{name,amount,type_tax_use},seller_ids{*,name{name,title,ref,type,website,supplier,street,email,is_company,phone,mobile,id,company_type}}}}}' %(self.base_url))
        if response.status_code == 200:
            response_json = response.json()
            total_count = response_json['count']
            count = 0
            for pricelist in response_json['result']:
                domain = [('remote_product_pricelist_id', '=', pricelist['id'])]
                find_pricelist = self.env['product.pricelist'].search(domain)
                pricelist_vals=self.process_pricelist(pricelist)
                if find_pricelist:
                    count += 1
                    find_pricelist.write(pricelist_vals)
                else:
                    self.env['product.pricelist'].create(pricelist_vals)
                    count += 1
            if count == total_count:
                vals = {
                    "name": self.name,
                    "state": "success",
                    "field_type": "pricelist",
                    "error": "Pricelist Imported Successfully",
                    "datetime": datetime.now(),
                    "base_config_id": self.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)
        else:
            vals = {
                "name": self.name,
                "state": "error",
                "field_type": "pricelist",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": self.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals) 