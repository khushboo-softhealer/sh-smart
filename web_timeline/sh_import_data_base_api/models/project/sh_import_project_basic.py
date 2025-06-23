# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
from datetime import datetime
import requests

class InheritImportBase(models.Model):
    _inherit = "sh.import.base"
    
    record_per_page_pre_define_task= fields.Integer("No of Predefine task per Page")
    current_import_page_pre_define_task = fields.Integer("Current Predefine task Page",default=0) 

    def import_basic_project_cron(self):   
        ''' ========== Connect db for import Projects basic  ==================  '''
        confid = self.env['sh.import.base'].search([],limit=1)
        response = requests.get('''%s/api/public/project.tags''' %(confid.base_url))
        response_json = response.json()
        if response.status_code==200:
            # pass
            # self.import_project_tags()
            # self.import_project_task_type()
            # self.sh_import_project_stages()
            # self.import_traning_course()
            # self.import_traning_batch()
            self.import_pre_define_task_details()
        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "project_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals) 
    
    
    def import_pre_define_task_details(self):
        ''' ============== Import Pre Define task ==============  '''
        
        confid = self.env['sh.import.base'].search([],limit=1)
        confid.current_import_page_pre_define_task += 1
        response = requests.get('''%s/api/public/pre.define.task.line?page_size=%s&page=%s''' %(confid.base_url,confid.record_per_page_pre_define_task,confid.current_import_page_pre_define_task))
        response_json = response.json()
        print("\n\n=====response_json",response_json)
        if response.status_code==200:
            count = 0
            for task in response_json['result']:
                domain = [('remote_pre_define_task_line_id', '=', task['id'])]
                find_task = self.env['pre.define.task.line'].search(domain)
                project_task_vals={
                    'remote_pre_define_task_line_id' : task['id'],
                    'description' : task['description'],
                    'display_name' : task['display_name'],
                    'name' : task['name'],
                    'sequence' : task['sequence'],
                    'tick' : task['tick'],
                }
                if task.get('sh_course_id'):
                    find_course=self.env['sh.training.course'].search([('remote_sh_traing_course_id','=',task.get('sh_course_id'))])
                    if find_course:
                        project_task_vals['sh_course_id']=find_course.id
                if find_task:
                    count += 1
                    find_task.write(project_task_vals)
                else:
                    self.env['pre.define.task.line'].create(project_task_vals)
                    count += 1
                    
            if count > 0:              
                vals = {
                    "name": confid.name,
                    "state": "success",
                    "field_type": "project_basic",
                    "error": "%s Pre Define Task Imported Successfully" %(count),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)
        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "project_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals)   

    
    def import_project_tags(self):
        ''' ============== Import Project Tags ==============  '''
        
        confid = self.env['sh.import.base'].search([],limit=1)
        response = requests.get('''%s/api/public/project.tags''' %(confid.base_url))
        response_json = response.json()
        if response.status_code==200:
            count = 0
            for tags in response_json['result']:
                domain = ['|',('remote_project_tag_id', '=', tags['id']),('name','=',tags['name'])]
                find_tag = self.env['project.tags'].search(domain)
                project_tag_vals={
                    'remote_project_tag_id' : tags['id'],
                    'color' : tags['color'],
                    'display_name':tags['display_name'],
                    'name':tags['name'],
                }
                if find_tag:
                    count += 1
                    find_tag.write(project_tag_vals)
                else:
                    self.env['project.tags'].create(project_tag_vals)
                    count += 1
                    
            if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "project_basic",
                        "error": "%s Tags Imported Successfully" %(count),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "project_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals) 


    def import_traning_course(self):
        ''' ============== Import Project Tags ==============  '''
        
        confid = self.env['sh.import.base'].search([],limit=1)
        response = requests.get('''%s/api/public/sh.training.course''' %(confid.base_url))
        response_json = response.json()
        if response.status_code==200:
            count = 0
            for data in response_json['result']:
                domain=[('remote_sh_traing_course_id','=',data.get('id'))] 
                find_course=self.env['sh.training.course'].search(domain)
               
                course_vals={
                    'remote_sh_traing_course_id':data.get('id'),
                    'display_name':data.get('display_name'),
                    'name':data.get('name'),   
                    'company_id':1                 
                }    
                if data.get('responsible_user_ids'):
                    responsible_user_list=[]
                    for user in data.get('responsible_user_ids'):
                        domain_by_id = [('remote_res_user_id','=',user)]
                        find_user_id=self.env['res.users'].search(domain_by_id)
                        if find_user_id:
                            responsible_user_list.append((4,find_user_id.id ))
                    if responsible_user_list:
                        course_vals['responsible_user_ids']= responsible_user_list

                 

                if find_course:
                    count += 1
                    find_course.write(course_vals)
                else:
                    self.env['sh.training.course'].create(course_vals)
                    count += 1
                    
            if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "project_basic",
                        "error": "%s Traning Course Imported Successfully" %(count),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "project_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals)


    def import_traning_batch(self):
        ''' ============== Import Project Tags ==============  '''
        
        confid = self.env['sh.import.base'].search([],limit=1)
        response = requests.get('''%s/api/public/sh.training.batch''' %(confid.base_url))
        response_json = response.json()
        if response.status_code==200:
            count = 0
            for batch in response_json['result']:
                domain = [('remote_sh_traing_batch_id', '=', batch['id'])]
                find_batch = self.env['sh.training.batch'].search(domain)
                traning_batch_vals={
                    'remote_sh_traing_batch_id' : batch['id'],
                    'name' : batch['name'],
                    'stage':batch.get('stage').get('sh_api_current_state'),
                }
                if batch.get('from_date'):
                    date_time=datetime.strptime(batch.get('from_date'),'%Y-%m-%d')
                    traning_batch_vals['from_date']=date_time

                if batch.get('to_date'):
                    date_time=datetime.strptime(batch.get('to_date'),'%Y-%m-%d')
                    traning_batch_vals['to_date']=date_time

                if batch.get('sh_trainee_ids'):
                    trainee_list=[]
                    for trainee in batch.get('sh_trainee_ids'):
                        domain_by_id = [('remote_res_user_id','=',trainee)]
                        find_user_id=self.env['res.users'].search(domain_by_id)
                        if find_user_id:   
                            trainee_list.append(find_user_id.id)
                    if trainee_list:
                        traning_batch_vals['sh_trainee_ids'] = [(6,0,trainee_list)]  


                if batch.get('sh_training_course_ids'):
                    course_list=[]
                    for course in batch.get('sh_training_course_ids'):
                        domain=[('remote_sh_traing_course_id','=',course)] 
                        find_course=self.env['sh.training.course'].search(domain)
                        if find_course:
                            course_list.append(find_course.id)
                    if course_list:
                        traning_batch_vals['sh_training_course_ids'] = [(6,0,course_list)]  

                if find_batch:
                    count += 1
                    find_batch.write(traning_batch_vals)
                else:
                    self.env['sh.training.batch'].create(traning_batch_vals)
                    count += 1
                    
            if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "project_basic",
                        "error": "%s Traning Batch Imported Successfully" %(count),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "project_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals) 
            
            
    def process_project_task_type(self,data):
        project_task_type_vals={
            'remote_project_task_type_id' : data['id'],
            'name' : data['name'],
            'description':data['description'],
            'sequence':data['sequence'],
            'legend_blocked':data['legend_blocked'],
            'legend_done':data['legend_done'],
            'legend_normal':data['legend_normal'],
            'fold':data['fold'],
            'auto_validation_kanban_state':data['auto_validation_kanban_state'],
            'display_name':data['display_name'],
        }   
        
        # ============== CONNECT USER IDS WITH PROJECT TASK TYPE ================
        if data.get('user_ids'):
            user_list=[]
            for user in data.get('user_ids'):
                domain_by_id = [('remote_res_user_id','=',user)]
                find_user_id=self.env['res.users'].search(domain_by_id)
                if find_user_id:
                    user_list.append((4,find_user_id.id))
            if user_list:
                project_task_type_vals['user_ids']=user_list
                
        # ============== CONNECT USER WITH PROJECT TASK TYPE ================       
        if data.get('user_id') and data['user_id']!=0:
            domain_by_id = [('remote_res_user_id','=',data['user_id'])]
            find_user_id=self.env['res.users'].search(domain_by_id)
            if find_user_id:
                project_task_type_vals['user_id']=find_user_id.id 
        
        # ============== Prepare value for stage_wize_default_employee_line  ====================        
        if data.get('stage_wize_default_employee_line'):
            stage_wize_default_employee_line=[]    
            for emp_line in data.get('stage_wize_default_employee_line'):
                emp_vals={
                    'remote_sh_stage_employee_id':emp_line.get('id'),
                    'display_name':emp_line.get('display_name'),
                    'sequence':emp_line.get('sequence'),  
                    'company_id':1,                  
                }    
                if emp_line.get('user_id') and emp_line['user_id']!=0:
                    domain_by_id = [('remote_res_user_id','=',emp_line['user_id'])]
                    find_user_id=self.env['res.users'].search(domain_by_id)
                    if find_user_id:
                        emp_vals['user_id']=find_user_id.id 
                if emp_vals:
                    stage_wize_default_employee_line.append((0,0,emp_vals))
            if stage_wize_default_employee_line:
                project_task_type_vals['stage_wize_default_employee_line']=stage_wize_default_employee_line            
        
        # ============== Prepare value for stage_wize_employee_line  ====================        
        if data.get('stage_wize_employee_line'):
            stage_wize_employee_line=[]    
            for emp_line in data.get('stage_wize_employee_line'):
                emp_vals={
                    'remote_sh_stage_employee_id':emp_line.get('id'),
                    'display_name':emp_line.get('display_name'),
                    'sequence':emp_line.get('sequence'), 
                    'company_id':1                   
                }
                if emp_line.get('user_id') and emp_line['user_id']!=0:
                    domain_by_id = [('remote_res_user_id','=',emp_line['user_id'])]
                    find_user_id=self.env['res.users'].search(domain_by_id)
                    if find_user_id:
                        emp_vals['user_id']=find_user_id.id    
                if emp_vals:
                    stage_wize_employee_line.append((0,0,emp_vals))           
            if stage_wize_employee_line:
                project_task_type_vals['stage_wize_employee_line']=stage_wize_employee_line                   
        return project_task_type_vals
            
            
    def import_project_task_type(self):
        ''' ============= Import Project Task Type ===============  '''
        
        confid = self.env['sh.import.base'].search([],limit=1)
        response = requests.get('''%s/api/public/project.task.type?query={*,stage_wize_default_employee_line{*},stage_wize_employee_line{*}}''' %(confid.base_url))
        response_json = response.json()
        
        if response.status_code==200:
            count = 0
            for task_type in response_json['result']:
                domain = ['|',('remote_project_task_type_id', '=', task_type['id']),('name','=',task_type['name'])]
                find_task_type = self.env['project.task.type'].search(domain)
                
                project_task_type_vals=self.process_project_task_type(task_type)
                if find_task_type:
                    count += 1
                    find_task_type.write(project_task_type_vals)
                else:
                    created_task_type=self.env['project.task.type'].create(project_task_type_vals)
                    count += 1
                    
            if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "project_basic",
                        "error": "%s Task Type Imported Successfully" %(count),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "project_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals) 
            

    def sh_import_project_stages(self):
        ''' ============= Import Project Stages ===============  '''
        
        confid = self.env['sh.import.base'].search([],limit=1)
        response = requests.get('''%s/api/public/project.stages''' %(confid.base_url))
        response_json = response.json()
        if response.status_code==200:
            count = 0
            for stage in response_json['result']:
                domain = ['|',('remote_project_project_stage_id', '=', stage['id']),('name','=',stage['name'])]
                find_stage = self.env['project.project.stage'].search(domain)
                project_stage_vals={
                    'remote_project_project_stage_id' : stage['id'],
                    'name' : stage['name'],
                    'display_name':stage['display_name'],
                    'sequence':stage['sequence'],
                    'fold':stage['fold'],
                }
                if find_stage:
                    count += 1
                    find_stage.write(project_stage_vals)
                else:
                    self.env['project.project.stage'].create(project_stage_vals)
                    count += 1
                    
            if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "project_basic",
                        "error": "%s Project Stage Imported Successfully" %(count),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "project_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals) 