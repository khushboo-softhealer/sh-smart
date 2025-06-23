# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
from datetime import datetime
import requests
import json

class ImportTask(models.Model):
    _inherit = "sh.import.base"
    

    def process_claim_data(self,data):
        claim_vals={
            'remote_sh_copyright_claim_id':data.get('id'),
            'claim_data':data.get('claim_data'),
            'claim_data_search':data.get('claim_data_search'),
            'display_name':data.get('display_name'),
            'git_hub_url':data.get('git_hub_url'),
            'git_hub_urls':data.get('git_hub_urls'),
            'is_claim':data.get('is_claim').get('sh_api_current_state'),
            'odoo_url':data.get('odoo_url'),
            'odoo_urls':data.get('odoo_urls'),
            'product_technical_name':data.get('product_technical_name'),
            'sh_technical_name':data.get('sh_technical_name'),
            'soft_url':data.get('soft_url'),    
            'company_id':1,        
        }
        
        # =============== CONNECT PRODUCT_TEMPLATE WITH COPYRIGHT CLAIM ===========
        
        if data.get('product_id'):
            domain = [('remote_product_template_id', '=', data['product_id'])]
            find_product = self.env['product.template'].search(domain,limit=1)
            if find_product:
                claim_vals['product_id'] = find_product.id
        
        # ========== CONNECT PRODUCT_IDS WITH COPYRIGHT CLAIM ===============
        if data.get('product_ids'):
            product_ids=[]
            for product in data.get('product_ids'):
                domain = [('remote_product_template_id', '=', product)]
                find_product = self.env['product.template'].search(domain,limit=1)
                if find_product:
                    product_ids.append((4,find_product.id))
            if product_ids:
                claim_vals['product_ids'] = product_ids
        if 'product_id'in claim_vals and claim_vals['product_id']:
            return claim_vals
        return False