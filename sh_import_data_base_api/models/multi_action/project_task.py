# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
import requests
import json

class RemoteProjectTask(models.Model):
    _inherit = 'project.task'    

    def update_remote_products_with_task(self):
        confid = self.env['sh.import.base'].search([],limit=1)  
        domain = [('project_id.name', '=', 'App Store'),'|',('sh_product_id', '=', False),('product_template_id','=',False)]
        # find_task = self.env['project.task'].search(domain)
        active_id = self.env.context.get('active_id')
        task = self.env['project.task'].browse(active_id)
        # for task in find_task:
        response = requests.get('''%s/api/public/project.task/%s?query{id,product_template_id,sh_product_id}''' 
            %(confid.base_url,task.remote_project_task_id))
        response_json = response.json()
        for data in response_json['result']:
            if data['sh_product_id']:
                domain = [('remote_product_product_id','=',data['sh_product_id'])]
                find_product = self.env['product.product'].search(domain,limit=1)
                if find_product:
                    task.write({
                        'sh_product_id' : find_product.id
                    })
            if data['product_template_id']:
                domain = [('remote_product_template_id','=',data['product_template_id'])]
                find_template = self.env['product.template'].search(domain,limit=1)
                print("n\n\n",find_template)
                if find_template:
                    print("\n\n",task.product_template_id)
                    task.write({
                        'product_template_id' : find_template.id
                    })
                    print("\n\n",task.product_template_id)
            print("\n\n\n one or two")

    def find_duplicate_merge_task(self):
        all_templates = self.env['product.product'].search([])
        task_dic = {}
        for template in all_templates:
            domain = [('sh_product_id', '=', template.id),('project_id.name','=','App Store')]
            find_task = self.env['project.task'].search(domain)
            if len(find_task) > 1:
                task_dic[template.id] = find_task.ids
        print("\n\n\n",task_dic)
