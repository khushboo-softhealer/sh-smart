# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models


class ImportTask(models.Model):
    _inherit = "sh.import.base"
    
    
    def process_product_change_log_data(self,data):
        change_log_list=[]
        for log in data:
            product_change_log={
                'remote_product_change_log_id':log.get('id'),
                'date':log.get('date'),
                'details':log.get('details'),
                # 'display_name':log.get('display_name'),
                'log_type':log.get('log_type').get('sh_api_current_state'),           
                'company_id':1,
            }
            
            if log.get('product_id'):
            # =========== CONNECT PRODUCT TEMPLATE WITH PROJECT TASK ===============
                domain = [('remote_product_template_id', '=', log['product_id'])]
                find_product = self.env['product.template'].search(domain,limit=1)
                
                # ============== IF PRODUCT TEMPLATE IS EXIST THEN RETURN ==================
                if find_product:
                    product_change_log['product_id']=find_product.id  
                                
                # ============== ELSE CREATE PRODUCT TEMPLATE THEN RETURN ==================
                # else:
                #     product_vals=self.process_product_data(log['product_id'])
                #     product_id=self.env['product.template'].create(product_vals)
                #     if product_id:
                #         product_change_log['product_id'] = product_id.id   
        
            if product_change_log:
                find_change_log=self.env['product.change.log'].search([('remote_product_change_log_id','=',log.get('id'))])
                if not  find_change_log:

                    if product_change_log.get('date')=='':
                        del product_change_log['date']
                    change_log_list.append((0,0,product_change_log))
                else:
                    find_change_log.write(product_change_log) 
        return change_log_list
    