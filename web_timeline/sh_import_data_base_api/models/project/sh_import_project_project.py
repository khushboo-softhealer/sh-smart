# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
from datetime import datetime
import requests
import json

class InheritImportBase(models.Model):
    _inherit = "sh.import.base"
    
    import_project=fields.Boolean("Import Project")
    records_per_page_project = fields.Integer("No of Project per page")
    current_import_page_project = fields.Integer("Current Projects Page",default=0) 

    sh_import_filter_project=fields.Boolean("Import Filtered Projects")  
    sh_from_date_project=fields.Datetime("From Date(Project)")
    sh_to_date_project=fields.Datetime("To Date(Project)") 
    sh_import_project_ids=fields.Char("Project ids")

    # subtask_project_id

    def import_project_filtered_to_queue(self):
        ''' ========== Import Filtered projects================= 
        between from date and end date ==================  ''' 

        confid = self.env['sh.import.base'].search([],limit=1)  
        if confid.sh_import_filter_project:
            response = requests.get('''%s/api/public/project.project?query={id,write_date}&filter=[["write_date",">=","%s"],["write_date","<=","%s"],["company_id","=",1]]''' 
                %(confid.base_url,str(confid.sh_from_date_project),str(confid.sh_to_date_project)))
            
            if response.status_code==200:
                response_json = response.json()
                if response_json.get('result'):
                    confid.sh_import_project_ids=[r['id'] for r in response_json.get('result')]

                else:
                    confid.sh_import_project_ids=False
        
    def import_project_from_queue(self):   
        ''' ========== Import Projects ==================  '''
        confid = self.env['sh.import.base'].search([],limit=1)
        if confid.sh_import_filter_project and confid.sh_import_project_ids:
            orders = confid.sh_import_project_ids.strip('][').split(', ')
            if len(orders) > 0 and orders[0]:   
                count=0
                failed=0  
                for project in orders[0:5]:
                    # try:
                    project_query ='''%s/api/public/project.project/%s?query=
                    {*,type_ids{*,user_ids,stage_wize_default_employee_line{*},stage_wize_employee_line{*}},resource_calendar_id{*},
                    sh_stage_ids{*,stage_wize_default_employee_line{*},stage_wize_employee_line{*}},stage_id{*}
                    }''' %(confid.base_url,project)

                    response = requests.get(project_query)
                    response_json = response.json()
                    if response.status_code==200:
                        already_added_project=False
                        for data in response_json.get('result'):
                            domain = [('remote_project_project_id', '=', data['id'])]
                            already_added_project = self.env['project.project'].search(domain)
                            project_vals=self.process_project_data(data)
                            invoice_dict={}
                            if already_added_project:
                                already_added_project.write(project_vals)
                            else:
                                created_project=self.env['project.project'].create(project_vals)

                            count += 1
                    else:
                        vals = {
                            "name": confid.name,
                            "state": "error",
                            "field_type": "order",
                            "error": response.text,
                            "datetime": datetime.now(),
                            "base_config_id": confid.id,
                            "operation": "import"
                        }
                        self.env['sh.import.base.log'].create(vals)

                if count > 0:              
                        vals = {
                            "name": confid.name,
                            "state": "success",
                            "field_type": "project",
                            "error": "%s Project Imported Successfully" %(count),
                            "datetime": datetime.now(),
                            "base_config_id": confid.id,
                            "operation": "import"
                        }
                        self.env['sh.import.base.log'].create(vals)
                    
                confid.sh_import_project_ids='['+', '.join([str(elem) for elem in orders[5:]])+']'

    def import_project_cron(self):
        ''' ========== Import Projects ============ '''

        confid = self.env['sh.import.base'].search([],limit=1)
        if confid.import_project:
            confid.current_import_page_project += 1
            response = requests.get('''%s/api/public/project.project?query=
                {*,type_ids{*,user_ids,stage_wize_default_employee_line{*},stage_wize_employee_line{*}},resource_calendar_id{*},
                sh_stage_ids{*,stage_wize_default_employee_line{*},stage_wize_employee_line{*}},stage_id{*}
                }&page_size=%s&page=%s&filter=[["company_id","=",1]]''' %(confid.base_url,confid.records_per_page_project,confid.current_import_page_project))
            response_json = response.json()
            if response.status_code==200:
                if response_json.get('count') and confid.records_per_page_project != response_json['count']:
                    confid.import_project = False
                    confid.current_import_page_project = 0
                count = 0
                failed = 0
                
                for data in response_json['result']:
                    project_vals = confid.process_project_data(data)
                    domain = [('remote_project_project_id', '=', data['id'])]
                    find_project = self.env['project.project'].search(domain)
                    try:
                        if find_project:
                            count += 1
                            find_project.write(project_vals)                            
                        else:
                            count += 1
                            create_project=self.env['project.project'].create(project_vals)    
                        
                    except Exception as e:
                        failed += 1
                        vals = {
                            "name": data['id'],
                            "error": e,
                            "import_json" : data,
                            "field_type": "project",                           
                            "datetime": datetime.now(),
                            "base_config_id": confid.id,
                        }
                        self.env['sh.import.failed'].create(vals) 
                    
                if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "project",
                        "error": "%s Project Imported Successfully" %(count - failed),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
                if failed > 0:
                    vals = {
                        "name": confid.name,
                        "state": "error",
                        "field_type": "project",
                        "error": "%s Failed To Import" %(failed),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)

            else:
                vals = {
                    "name": confid.name,
                    "state": "error",
                    "field_type": "project",
                    "error": response.text,
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)  


    def process_project_data(self,data):
        ''' ============= Prepare Data for project creation =============  '''
        project_vals={
            'name':data.get('name'),
            'remote_project_project_id':data.get('id'),
            'active':data.get('active'),
            'sequence':data.get('sequence'),
            'alias_domain':data.get('alias_domain'),
            'color':data.get('color'),
            'display_name':data.get('display_name'),
            'doc_count':data.get('doc_count'),
            'is_favorite':data.get('is_favorite'),
            'label_tasks':data.get('label_tasks'),
            'privacy_visibility':data.get('privacy_visibility').get('sh_api_current_state') if data.get('privacy_visibility') else 'portal',
            'sequence':data.get('sequence'),
            'task_count':data.get('task_count'),
            'access_token':data.get('access_token'),
            'access_url':data.get('access_url'),
            'access_warning':data.get('access_warning'),
            'alias_defaults':data.get('alias_defaults'),
            'rating_percentage_satisfaction':data.get('percentage_satisfaction_project'),
            'rating_status_period':data.get('rating_status_period').get('sh_api_current_state') if data.get('rating_status_period') and data.get('rating_status_period').get('sh_api_current_state') else 'monthly' ,           
            'allow_timesheets':data.get('allow_timesheets'),
            'is_temp_project':data.get('is_temp_project'),
            'company_id':1,
        
        }
        # ======== Get User if already created or create =========
        if data.get('user_id') and data.get('user_id')!=0:
            domain_by_id = [('remote_res_user_id','=',data['user_id'])]
            find_user_id=self.env['res.users'].search(domain_by_id)
            if find_user_id:
                project_vals['user_id']=find_user_id.id 
                                        
        # ======== Get Partner if already created or create =========
        
        if data.get('partner_id') and data['partner_id']!=0:
            domain = [('remote_res_partner_id', '=', data['partner_id'])]
            find_customer = self.env['res.partner'].search(domain)
            if find_customer:
                project_vals['partner_id'] = find_customer.id
                
        # =============== CREATE SALE ORDER IF NOT EXIST ====================================
        
        if data.get('sale_order_id') and data.get('sale_order_id')!=0:
            domain = [('remote_sale_order_id', '=', data.get('sale_order_id'))]
            find_order = self.env['sale.order'].search(domain)
            if find_order:
                project_vals['sale_order_id'] = find_order.id
        
        # ======== PREPARE SALE_LINE_ID IF EXIST THEN CONNECTED OTHER WISE CREATE ==============
        
        if data.get('sale_line_id') and data.get('sale_line_id')!=0:
            domain = [('remote_sale_order_line_id', '=', data.get('sale_line_id'))]
            find_order_line = self.env['sale.order.line'].search(domain)
            if find_order_line:
                project_vals['sale_line_id'] = find_order_line.id
            
        # ================ PREPARE VALS FOR TYPE_IDS WHICH ARE CONNECTED WITH PROJECT ========
            
        if data.get('type_ids'):
            task_type=[]
            for type in data.get('type_ids'):
                if type['id'] and type['id']!=0:
                    domain = ['|',('remote_project_task_type_id', '=', type['id']),('name', '=', type['name'])]
                    find_task_type = self.env['project.task.type'].search(domain,limit=1)
                    if find_task_type:
                        task_type.append((4,find_task_type.id))
                    else:
                        project_task_type_vals=self.process_project_task_type(type)
                        created_task_type=self.env['project.task.type'].create(project_task_type_vals)
                        task_type.append((4,created_task_type.id))
            if task_type:
                project_vals['type_ids']=task_type
        
        # ============== CONNECT RESOURCE CALENDAR WITH PROJECT =============
        if data.get('resource_calendar_id'):
            domain = [('remote_resource_calendar_id', '=', data.get('resource_calendar_id')['id'])]
            find_resource_calendar = self.env['resource.calendar'].search(domain)
            if find_resource_calendar:
                project_vals['resource_calendar_id']=find_resource_calendar.id
            # else:   
            #     resource_calendar_vals = self.process_resource_calendar_data(data.get('resource_calendar_id'))
            #     create_calendar_id=self.env['resource.calendar'].create(resource_calendar_vals) 
            #     project_vals['resource_calendar_id']=create_calendar_id.id
         
        # =============  password_o2m , project_ref  ========      
                    
        if data.get('responsible_user_ids') or data.get('sh_responsible_user_ids'):
            responsible_users=[]
            for user in data.get('responsible_user_ids'):
                if user and user!=0:
                    domain_by_id = [('remote_res_user_id','=',user)]
                    find_user_id=self.env['res.users'].search(domain_by_id)
                    
                    # ========== SEARCH USER BY ID OR BY NAME IF EXIST THEN RETURN ELSE CREATE USE AND RETURN IT =====
                    if find_user_id:
                        responsible_users.append((4,find_user_id.id ))
                            
            for user in data.get('sh_responsible_user_ids'):                
                if user and user!=0:
                    domain_by_id = [('remote_res_user_id','=',user)]
                    find_user_id=self.env['res.users'].search(domain_by_id)
                    # ========== SEARCH USER BY ID OR BY NAME IF EXIST THEN RETURN ELSE CREATE USE AND RETURN IT =====
                    
                    if find_user_id:
                        responsible_users.append((4,find_user_id.id ))             
                            
            if responsible_users:
                project_vals['responsible_user_ids']=responsible_users           
                
        # ======== Get Product if already created or create =====             
           
        if data.get('sh_product_id'):
                        
            domain=[('remote_product_product_id','=',data.get('sh_product_id'))]
            find_product=self.env['product.product'].search(domain)
            if find_product:
                project_vals['sh_product_id']=find_product.id   
    
        # ============ CONNECT STAGE WITH PROJECT ================
        
        if data.get('sh_stage_ids'):
            stage_ids=[]
            for stage in data.get('sh_stage_ids'):
                if stage['id'] and stage['id']!=0:
                    domain = ['|',('remote_project_task_type_id', '=', stage['id']),('name','=',stage['name'])]
                    find_task_type = self.env['project.task.type'].search(domain,limit=1)
                    if find_task_type:
                        stage_ids.append((4,find_task_type.id))
                    else:
                        project_task_type_vals=self.process_project_task_type(stage)             
                        created_stage=self.env['project.task.type'].create(project_task_type_vals)
                        if created_stage:
                            stage_ids.append((4,find_task_type.id))
            if stage_ids:
                project_vals['sh_stage_ids']=stage_ids
         
        # =========== CONNECT CUSTOM STAGE WITH PROJECT =================
        
        if data.get('stage_id') :
            domain = [('remote_project_project_stage_id', '=', data.get('stage_id')['id'])]
            find_stage = self.env['project.project.stage'].search(domain)
            if find_stage:
                project_vals['stage_id']=find_stage.id
            else:
                project_stage_vals={
                    'remote_project_project_stage_id' : data.get('stage_id')['id'],
                    'name' : data.get('stage_id')['name'],
                    'display_name':data.get('stage_id')['display_name'],
                    'sequence':data.get('stage_id')['sequence'],
                    'fold':data.get('stage_id')['fold'],
                }    
                create_stage=self.env['project.project.stage'].create(project_stage_vals)
                if create_stage:
                    project_vals['stage_id']=create_stage.id
            
        return project_vals       
        