# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
from datetime import datetime
import requests
import json

class ImportTask(models.Model):
    _inherit = "sh.import.base"
    
    import_task=fields.Boolean("Import Task")
    records_per_page_task = fields.Integer("No of Task per page")
    current_import_page_task = fields.Integer("Current Task Page",default=0) 

    sh_import_filter_task=fields.Boolean("Import Filtered Tasks")  
    sh_from_date_task=fields.Datetime("From Date(Task)")
    sh_to_date_task=fields.Datetime("To Date(Task)") 
    sh_import_task_ids=fields.Char("Task ids")
    
    def import_task_filtered_to_queue(self):
        ''' ========== Import Filtered tasks ================= 
        between from date and end date ==================  ''' 

        confid = self.env['sh.import.base'].search([],limit=1)  
        if confid.sh_import_filter_task:
            # response = requests.get('''%s/api/public/project.task?query={id,write_date}&filter=[["write_date",">=","%s"],["write_date","<=","%s"],["company_id","=",1]]''' 
            #     %(confid.base_url,str(confid.sh_from_date_task),str(confid.sh_to_date_task)))
            query='%s/api/public/mail.message?query={id,write_date}&order="id asc"&filter=[["write_date",">=","%s"],["write_date","<=","%s"],["model","=","project.task"]]' %(confid.base_url,str(confid.sh_from_date_task),str(confid.sh_to_date_task))
            response = requests.get(query)
            if response.status_code==200:
                response_json = response.json()
                if response_json.get('result'):
                    confid.message_ids=[r['id'] for r in response_json.get('result')]
                else:
                    confid.message_ids=False

    def import_task_from_queue(self):   
        ''' ========== Import Task ==================  '''
        confid = self.env['sh.import.base'].search([],limit=1)
        if confid.sh_import_filter_task and confid.sh_import_task_ids:
            tasks = confid.sh_import_task_ids.strip('][').split(', ')
            if len(tasks) > 0 and tasks[0]:   
                count=0
                failed=0  
                for task_id in tasks[0:100]:
                    # try:
                    # task_query ='''%s/api/public/project.task/%s''' %(confid.base_url,task_id)
                    task_query ='''%s/api/public/project.task/%s?query={*,-banner,-rating_last_image,batch_id{*},check_list{*,checklist_ids{*}},depends{*},sh_edition_ids{*},sh_tag_ids{*},supported_browsers{*},tag_ids{*},version_ids{*},course_id{*},displayed_image_id{*},
                    existing_related_task_state{*,stage_wize_default_employee_line{*},stage_wize_employee_line{*}},git_repo{*},hr_applicant_id{id,name,partner_name,email_from,email_cc,partner_phone,partner_mobile,salary_expected,salary_proposed,description,
                    active,color,day_close,day_open,delay_close,display_name,employee_name,probability,salary_proposed_extra,salary_expected_extra,user_email,legend_blocked,legend_done,legend_normal,availability,date_closed,date_last_stage_update,
                    date_open,priority,kanban_state,attachment_number,sh_hr_placement_is_confirm,hide_button_bool,interview_type,sh_hr_placement_schedule_datetime,placement_id,college_id,interview_ids,reject_reason_id,medium_id{id,name,display_name,active},
                    categ_ids{id,name,color,display_name},type_id{id,name,sequence,display_name},source_id{id,name,display_name},
                    partner_id,department_id{id,name},last_stage_id,stage_id,user_id},license{*},related_task_state{*,stage_wize_default_employee_line{*},stage_wize_employee_line{*}},sh_scale_ids{*},stage_id{*,stage_wize_default_employee_line{*},stage_wize_employee_line{*}},claim_ids{*},custom_checklist_ids{*,name{*}},
                    project_task_change_log_ids{*},rating_ids{*,parent_res_model_id{name},res_model_id{name}},
                    upcoming_feature_ids{*}}&filter=['|',["active", "=", False],["active", "=", True]]''' %(confid.base_url,task_id)

                    response = requests.get(task_query)

                    # print("\n\n\n\n\n responceee",response.text)
                    if response.status_code==200:
                        response_json = response.json()
                        already_added_task=False
                        for data in response_json.get('result'):
                            print("\n=========== data['id']", data['id'])
                            domain = [('remote_project_task_id', '=', data['id'])]
                            already_added_task = self.env['project.task'].search(domain)
                            task_vals=self.process_task_data(data)
                            if already_added_task:
                                already_added_task.write(task_vals)
                            else:
                                created_task=self.env['project.task'].create(task_vals)

                            count += 1
                    else:
                        vals = {
                            "name": confid.name,
                            "state": "error",
                            "field_type": "task",
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
                            "field_type": "task",
                            "error": "%s Task Imported Successfully" %(count),
                            "datetime": datetime.now(),
                            "base_config_id": confid.id,
                            "operation": "import"
                        }
                        self.env['sh.import.base.log'].create(vals)
                    
                confid.sh_import_task_ids='['+', '.join([str(elem) for elem in tasks[100:]])+']'


    
    def import_task_cron(self):
        ''' ========== Import Projects Task ============ '''
        
        confid = self.env['sh.import.base'].search([],limit=1)
        # confid.import_task_from_queue()
        if confid.import_task:
            confid.current_import_page_task += 1
            response = requests.get('''%s/api/public/project.task?query={*,-banner,-rating_last_image,batch_id{*},check_list{*,checklist_ids{*}},depends{*},sh_edition_ids{*},sh_tag_ids{*},supported_browsers{*},tag_ids{*},version_ids{*},course_id{*},displayed_image_id{*},
            existing_related_task_state{*,stage_wize_default_employee_line{*},stage_wize_employee_line{*}},git_repo{*},hr_applicant_id{id,name,partner_name,email_from,email_cc,partner_phone,partner_mobile,salary_expected,salary_proposed,description,
            active,color,day_close,day_open,delay_close,display_name,employee_name,probability,salary_proposed_extra,salary_expected_extra,user_email,legend_blocked,legend_done,legend_normal,availability,date_closed,date_last_stage_update,
            date_open,priority,kanban_state,attachment_number,sh_hr_placement_is_confirm,hide_button_bool,interview_type,sh_hr_placement_schedule_datetime,placement_id,college_id,interview_ids,reject_reason_id,medium_id{id,name,display_name,active},
            categ_ids{id,name,color,display_name},type_id{id,name,sequence,display_name},source_id{id,name,display_name},
            partner_id,department_id{id,name},last_stage_id,stage_id,user_id},license{*},related_task_state{*,stage_wize_default_employee_line{*},stage_wize_employee_line{*}},sh_scale_ids{*},stage_id{*,stage_wize_default_employee_line{*},stage_wize_employee_line{*}},claim_ids{*},custom_checklist_ids{*,name{*}},
            message_ids{id,subtype_id{*},author_id,body,channel_ids{*},date,display_name,email_from,has_error,layout,mail_activity_type_id{*},message_id,message_type,model,moderation_status,moderator_id,need_moderation,needaction,no_auto_thread,notification_ids,
            rating_value,record_name,reply_to,res_id,starred,subject},project_task_change_log_ids{*},rating_ids{*,parent_res_model_id{name},res_model_id{name}},timesheet_ids{*,general_account_id{*,tax_ids{*},currency_id{name}}},
            upcoming_feature_ids{*}}&page_size=%s&page=%s&filter=[["company_id","=",1],["project_id","=",221]]''' %(confid.base_url,confid.records_per_page_task,confid.current_import_page_task))
            response_json = response.json()
            if response.status_code==200:
                if 'count' in response_json and confid.records_per_page_task != response_json['count'] : 
                    confid.import_task = False
                    confid.current_import_page_task = 0
                count = 0
                failed = 0
                
                for data in response_json['result']:
                    task_vals = confid.process_task_data(data)
                    domain = [('remote_project_task_id', '=', data['id'])]
                    find_task = self.env['project.task'].search(domain)
                    try:
                        if find_task:
                            count += 1
                            find_task.write(task_vals)                           
                        else:
                            count += 1
                            # print("\n\n\n",task_vals)
                            create_task=self.env['project.task'].create(task_vals)  
                        
                    except Exception as e:
                        failed += 1
                        vals = {
                            "name": data['id'],
                            "error": e,
                            "import_json" : data,
                            "field_type": "task",                           
                            "datetime": datetime.now(),
                            "base_config_id": confid.id,
                        }
                        self.env['sh.import.failed'].create(vals) 
                    
                if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "task",
                        "error": "%s Task Imported Successfully" %(count - failed),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
                if failed > 0:
                    vals = {
                        "name": confid.name,
                        "state": "error",
                        "field_type": "task",
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
                    "field_type": "task",
                    "error": response.text,
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)  
                

    def import_one_task(self,task_id):
        ''' ========== Import Projects Task ============ '''
        if task_id:
            confid = self.env['sh.import.base'].search([],limit=1)
            url = '''%s/api/public/project.task/%s?query={*,-banner,-rating_last_image,batch_id{*},check_list{*,checklist_ids{*}},depends{*},sh_edition_ids{*},sh_tag_ids{*},supported_browsers{*},tag_ids{*},version_ids{*},course_id{*},displayed_image_id{*},
            existing_related_task_state{*,stage_wize_default_employee_line{*},stage_wize_employee_line{*}},git_repo{*},hr_applicant_id{id,name,partner_name,email_from,email_cc,partner_phone,partner_mobile,salary_expected,salary_proposed,description,
            active,color,day_close,day_open,delay_close,display_name,employee_name,probability,salary_proposed_extra,salary_expected_extra,user_email,legend_blocked,legend_done,legend_normal,availability,date_closed,date_last_stage_update,
            date_open,priority,kanban_state,attachment_number,sh_hr_placement_is_confirm,hide_button_bool,interview_type,sh_hr_placement_schedule_datetime,placement_id,college_id,interview_ids,reject_reason_id,medium_id{id,name,display_name,active},
            categ_ids{id,name,color,display_name},type_id{id,name,sequence,display_name},source_id{id,name,display_name},
            partner_id,department_id{id,name},last_stage_id,stage_id,user_id},license{*},related_task_state{*,stage_wize_default_employee_line{*},stage_wize_employee_line{*}},sh_scale_ids{*},stage_id{*,stage_wize_default_employee_line{*},stage_wize_employee_line{*}},claim_ids{*},custom_checklist_ids{*,name{*}},
            message_ids{id,subtype_id{*},author_id,body,channel_ids{*},date,display_name,email_from,has_error,layout,mail_activity_type_id{*},message_id,message_type,model,moderation_status,moderator_id,need_moderation,needaction,no_auto_thread,notification_ids,
            rating_value,record_name,reply_to,res_id,starred,subject},project_task_change_log_ids{*},rating_ids{*,parent_res_model_id{name},res_model_id{name}},timesheet_ids{*,general_account_id{*,tax_ids{*},currency_id{name}}},
            upcoming_feature_ids{*}}''' %(confid.base_url,task_id)
                                    
            response = requests.get(url)
            response_json = response.json()
            if response.status_code==200:                
                for data in response_json['result']:
                    task_vals = confid.process_task_data(data)
                    return task_vals
        else:
            return False
        
    def process_task_data(self,data):
        ''' ============= Prepare Project related task list =============  '''
        task_vals={
            'remote_project_task_id':data.get('id'),
            'active':data.get('active'),         
            'color':data.get('color'),
            'allow_timesheets':data.get('allow_timesheets'),
            'description':data.get('description'),
            'display_name':data.get('display_name'),
            'email_cc':data.get('email_cc'),
            'email_from':data.get('email_from'),
            'kanban_state':data.get('kanban_state').get('sh_api_current_state'),
            'kanban_state_label':data.get('kanban_state_label'),
            'legend_blocked':data.get('legend_blocked'),
            'legend_done':data.get('legend_done'),
            'legend_normal':data.get('legend_normal'),
            'message_has_error':data.get('message_has_error'),
            'message_has_error_counter':data.get('message_has_error_counter'),
            'message_is_follower':data.get('message_is_follower'),
            'message_needaction':data.get('message_needaction'),
            'message_needaction_counter':data.get('message_needaction_counter'),
            'name':data.get('name'),
            'planned_hours':data.get('planned_hours'),
            'priority':data.get('priority').get('sh_api_current_state'),
            'rating_count':data.get('rating_count'),
            'rating_last_feedback':data.get('rating_last_feedback'),
            'rating_last_value':data.get('rating_last_value'),
            'sequence':data.get('sequence'),
            'subtask_planned_hours':data.get('subtask_planned_hours'),
            'working_days_close':data.get('working_days_close'),
            'working_days_open':data.get('working_days_open'),
            'working_hours_close':data.get('working_hours_close'),
            'working_hours_open':data.get('working_hours_open'),
            'access_token':data.get('access_token'),
            'access_url':data.get('access_url'),         
            'access_warning':data.get('access_warning'),
            'analytic_account_active':data.get('analytic_account_active'),
            'effective_hours':data.get('effective_hours'),
            'is_project_map_empty':data.get('is_project_map_empty'),
            'progress':data.get('progress'),
            'remaining_hours':data.get('remaining_hours'),
            'subtask_effective_hours':data.get('subtask_effective_hours'),
            'total_hours_spent':data.get('total_hours_spent'),    
            'allow_timesheet_edit':data.get('allow_timesheet_edit'),
            'already_add_exist':data.get('already_add_exist'),
            'changed_effective_hours':data.get('changed_effective_hours'),
            'check_bool_int_sch_time':data.get('check_bool_int_sch_time'),
            'check_config_setting_bool':data.get('check_config_setting_bool'),
            'claim':data.get('claim'),
            'custom_checklist':data.get('custom_checklist'),
            'duration':data.get('duration'),
            'end_task_bool':data.get('end_task_bool'),
            'estimated_hrs':data.get('estimated_hrs'),
            'feature_expansion':data.get('feature_expansion').get('sh_api_current_state'),
            'is_beyond_estimation':data.get('is_beyond_estimation'),
            'is_manager':data.get('is_manager'),
            'is_manager_temp':data.get('is_manager_temp'),
            'is_need_integrate':data.get('is_need_integrate'),
            'is_temp_task':data.get('is_temp_task'),
            'is_user_working':data.get('is_user_working'),
            'live_demo':data.get('live_demo'),
            'odoo_edition':data.get('odoo_edition').get('sh_api_current_state'),
            'product_version':data.get('product_version'),
            'pylint_score':data.get('pylint_score'),
            'responsible_user_names':data.get('responsible_user_names'),
            'sh_is_issue':data.get('sh_is_issue'),
            'sh_no_of_days':data.get('sh_no_of_days'),
            'sh_product_counter':data.get('sh_product_counter'),
            'sh_technical_name':data.get('sh_technical_name'),
            'sh_training_comment':data.get('sh_training_comment'),
            'sh_training_rating':data.get('sh_training_rating').get('sh_api_current_state'),
            'stage_cancel':data.get('stage_cancel'),
            'stage_done':data.get('stage_done'),
            'stage_draft':data.get('stage_draft'),
            'start_id':data.get('start_id'),
            'start_task_bool':data.get('start_task_bool'),
            'task_runner':data.get('task_runner'),
            'task_running':data.get('task_running'),
            'ticket_count':data.get('ticket_count'),
            'timesheet_count':data.get('timesheet_count'),
            'trainee':data.get('trainee'),
            'total_time':data.get('total_time'),
            'user_guide':data.get('user_guide'), 
            'company_id':1,           
        }
        
        # =========== CONNECT CUSTOM STAGE WITH PROJECT =================
        if data.get('stage_id') and data.get('stage_id').get('id') and data.get('stage_id').get('id')!=0:
            domain = [('remote_project_task_type_id', '=', data.get('stage_id')['id'])]
            find_task_type = self.env['project.task.type'].search(domain,limit=1)
            if find_task_type:
                task_vals['stage_id']=find_task_type.id
            else:
                project_task_type_vals=self.process_project_task_type(data.get('stage_id'))   
                create_task_type=self.env['project.task.type'].create(project_task_type_vals)    
                if create_task_type:
                    task_vals['stage_id']=create_task_type.id
        
        # print("\n\n\===========data.get('sh_product_id')",data.get('sh_product_id'))
        if data.get('sh_product_id') and data.get('sh_product_id')!=0:
            domain = [('remote_product_product_id', '=', data.get('sh_product_id'))]
            find_product = self.env['product.product'].search(domain)
            if find_product:
                task_vals['sh_product_id'] = find_product[0].id    

        print("\n\n============data.get('batch_id')",data.get('batch_id'))
        if data.get('batch_id'):
            batch_list=[]
            for batch in data.get('batch_id'): 
                domain = [('remote_sh_traing_batch_id', '=', batch.get('id'))]
                find_batch = self.env['sh.training.batch'].search(domain)
                if find_batch:
                    batch_list.append(find_batch.id) 
            if batch_list:
                task_vals['batch_id']=[(6,0,batch_list)]
    

        if data.get('sale_product_id') and data.get('sale_product_id'):
            domain = [('remote_product_product_id', '=', data.get('sale_product_id'))]
            find_product = self.env['product.product'].search(domain)
            if find_product:
                task_vals['sale_product_id'] = find_product[0].id     
        
        # =============== CREATE SALE ORDER IF NOT EXIST ====================================
        
        if data.get('sale_order_id') and data.get('sale_order_id')!=0:
            domain = [('remote_sale_order_id', '=', data.get('sale_order_id'))]
            find_order = self.env['sale.order'].search(domain)
            if find_order:
                task_vals['sale_order_id'] = find_order.id
        
        # ======== PREPARE SALE_LINE_ID IF EXIST THEN CONNECTED OTHER WISE CREATE ==============
        
        if data.get('sale_line_id') and data.get('sale_line_id')!=0:
            domain = [('remote_sale_order_line_id', '=', data.get('sale_line_id'))]
            find_order_line = self.env['sale.order.line'].search(domain)
            if find_order_line:
                task_vals['sale_line_id'] = find_order_line.id
        
        # ======== Get partner if already created or create =====
            
        if data.get('partner_id'):
            domain = [('remote_res_partner_id', '=', data['partner_id'])]
            find_customer = self.env['res.partner'].search(domain)
            if find_customer:
                task_vals['partner_id'] = find_customer.id
        
        
        # ======== Get Message Partner if already created or create =========
        
        if data.get('message_partner_ids'):
            partner_list=[]
            for m_partner in data.get('message_partner_ids'):
                domain = [('remote_res_partner_id', '=',m_partner)]
                find_customer = self.env['res.partner'].search(domain)
                
                # ======== CHECK IF PARTNER IS CREATED OR NOT IF CREATE THEN RETURN ELSE CREATE =======
                if find_customer:
                    partner_list.append((4,find_customer.id))
                        
            task_vals['message_partner_ids']=partner_list
        
        # ========== select Project ==========
        if data.get('project_id') :
            domain = [('remote_project_project_id','=',data['project_id'])]
            find_project=self.env['project.project'].search(domain)
            if find_project:
                task_vals['project_id']=find_project.id

            # print("\n\n==========find_project",find_project)
        if data.get('display_project_id'):
            domain = [('remote_project_project_id','=',data['display_project_id'])]
            find_project=self.env['project.project'].search(domain)
            if find_project:
                task_vals['display_project_id']=find_project.id
                    
                    
        # ======== Get User if already created or create =========
        user_list=[]
        if data.get('user_id') and data.get('user_id') !=0:
            domain_by_id = [('remote_res_user_id','=',data['user_id'])]
            find_user_id=self.env['res.users'].search(domain_by_id)
            if find_user_id:
                user_list.append((4,find_user_id.id))
        if data.get('responsible_ids'):
            for user in data.get('responsible_ids'):
                domain_by_id = [('remote_res_user_id','=',user)]
                find_user_id=self.env['res.users'].search(domain_by_id)

                # ========== SEARCH USER BY ID OR BY NAME IF EXIST THEN RETURN ELSE CREATE USE AND RETURN IT =====
                if find_user_id:
                    user_list.append((4,find_user_id.id))

        if user_list:
            task_vals['user_ids']=user_list


            # if find_user_id:
            #     task_vals['user_ids']=[(4,find_user_id.id )]
                    
        # ======== Get User if already created or create =========
        if data.get('manager_id') and data.get('manager_id')!=0:
            domain_by_id = [('remote_res_user_id','=',data['manager_id'])]
            find_user_id=self.env['res.users'].search(domain_by_id)
            if find_user_id:
                task_vals['manager_id']=find_user_id.id
        
        # ======== Get tags if already created or create =========            
                    
        if data.get('tag_ids'):
            tag_ids=[]
            for tag in data.get('tag_ids'):
                domain = [('remote_project_tag_id','=',tag['id'])]
                find_tag = self.env['project.tags'].search(domain)
                if find_tag:
                    tag_ids.append((4,find_tag.id))
                else:
                    tag_vals = {
                        'remote_project_tag_id' : tag['id'],
                        'color' : tag['color'],
                        'display_name':tag['display_name'],
                        'name':tag['name'],
                        }
                    tag_id=self.env['project.tags'].create(tag_vals)
                    if tag_id:
                        tag_ids.append((4,tag_id.id))
            if tag_ids:
                task_vals['tag_ids']=tag_ids
        # ============== prepare Timesheet Data =================
        
        # if data.get('timesheet_ids'):
        #     timesheet_list=self.process_timesheet_data(data.get('timesheet_ids'))
        #     if timesheet_list:
        #         task_vals['timesheet_ids']=timesheet_list 
        
        # ============== Prepare Mail_Message Data =================
        
        # if data.get('message_ids'):
        #     message_list = []
        #     message_list_create=[]
        #     remain_mail=[]           
        #     for message in data.get('message_ids'):   
        #         if message['id']:             
        #             domain = [('remote_mail_message_id','=',message['id'])]
        #             find_message = self.env['mail.message'].search(domain,limit=1)                    
        #             if find_message:
        #                 message_list.append((4,find_message.id))
        #             else:
        #                 remain_mail.append(message)
        #     if remain_mail:
        #         message_list_create = self.process_message_data(remain_mail)                                                
                            
        #     task_vals['message_ids']=message_list+message_list_create
                
        # ========== PREPARE CHILD TASK VALUE ==============        
                
        # if data.get('child_ids'):
        #     child_list = []
        #     for child in data['child_ids']:
        #         domain = [('remote_project_task_id', '=', child)]
        #         find_child = self.env['project.task'].search(domain)
        #         if not find_child:
        #             child_vals = self.import_one_task(child)
        #             if child_vals:
        #                 child_list.append((0,0,child_vals))
        #     task_vals['child_ids'] = child_list        
                
        # ======== CONNECT WTIH PARENT TASK ===========
        if data.get('parent_id'):
            domain = [('remote_project_task_id', '=', data.get('parent_id'))]
            related_task = self.env['project.task'].search(domain)
            if related_task:
                task_vals['parent_id']=related_task.id                  
        
         # ========== CONNECT ACCOUNT_MOVE WITH PROJECT TASK ==============
        if data.get('account_invoice_id'):
            if data.get('account_invoice_id')!=0:
                domain=[('remote_account_move_id','=',data.get('account_invoice_id'))]
                find_account_move_line = self.env['account.move'].search(domain)
                if find_account_move_line:
                    task_vals['account_move_id']=find_account_move_line.id
        
        # =========== CHECK RELATED TASK EXIST OR NOT IF EXIST IMPORT ============
        
        if data.get('existing_related_task'):
            domain = [('remote_project_task_id', '=', data.get('existing_related_task'))]
            related_task = self.env['project.task'].search(domain)
            if related_task:
                task_vals['existing_related_task']=related_task.id  
            # else:
            #     related_task_vals = self.import_one_task(data.get('existing_related_task'))
            #     if related_task_vals:
            #         related_task = self.env['project.task'].create(related_task_vals)
            #         if related_task:
            #             task_vals['existing_related_task']=related_task.id
                    
       # =========== CHECK RELATED TASK EXIST OR NOT IF EXIST IMPORT ===========             
                    
        if data.get('related_task'):
            domain = [('remote_project_task_id', '=', data.get('related_task'))]
            related_task = self.env['project.task'].search(domain)
            if related_task:
                task_vals['related_task']=related_task.id  
            # else:
            #     related_task_vals = self.import_one_task(data.get('related_task'))
            #     if related_task_vals:
            #         related_task = self.env['project.task'].create(related_task_vals)
            #         if related_task:
            #             task_vals['related_task']=related_task.id              
                    
       
        # ========== PREPARE SUB TASK LINE VALUE ==============        
                
        # if data['sh_sub_task_lines']:
        #     child_list = []
        #     for child in data['sh_sub_task_lines']:
        #         domain = [('remote_project_task_id', '=', child)]
        #         find_child = self.env['project.task'].search(domain)
        #         if not find_child:
        #             child_vals = self.import_one_task(child)
        #             if child_vals:
        #                 child_list.append((0,0,child_vals))
        #     task_vals['sh_sub_task_lines'] = child_list 
       
        # ============= PREPARE TAGS LIST WHICH ARE CONNECTED IN TASK =======
        if data.get('sh_tag_ids'):
            tag_list = []
            for tag in data.get('sh_tag_ids'):
                domain = [('remote_product_tags_id','=',data.get('sh_tag_ids'))]
                find_tag=self.env['product.tags'].search(domain)
                if find_tag:
                    tag_list.append(4,find_tag.id)
                else:
                    tag_vals={
                        'remote_product_tags_id':tag.get('id'),
                        'display_name':tag.get('display_name'),
                        'name':tag.get('name'),
                        'company_id':1,
                    }
                    find_tag=self.env['product.tags'].create(tag_vals)
                    if find_tag:
                        tag_list.append(4,find_tag.id)
            if tag_list:
                task_vals['sh_tag_ids']=tag_list
                    
        # ========== MAPPED RELATED TASK STATE ===========
        
        if data.get('related_task_state') and data.get('related_task_state').get('id') and data.get('related_task_state').get('id')!=0:
            domain = [('remote_project_task_type_id', '=', data.get('related_task_state')['id'])]
            find_task_type = self.env['project.task.type'].search(domain,limit=1)
            if find_task_type:
                task_vals['related_task_state']=find_task_type.id
            else:
                project_task_type_vals=self.process_project_task_type(data.get('related_task_state'))   
                create_task_type=self.env['project.task.type'].create(project_task_type_vals)    
                if create_task_type:
                    task_vals['related_task_state']=create_task_type.id   
           
        # ============= CHECK SALE_ORDER IS EXIST OR NOT IF NOT THEN CREATE =========
        if data.get('sh_sale_id') and data.get('sh_sale_id')!=0:
            domain = [('remote_sale_order_id', '=', data.get('sh_sale_id'))]
            find_sale_order = self.env['sale.order'].search(domain)
            if find_sale_order:
                task_vals['sh_sale_id']=find_sale_order.id

        # =========== CONNECT PRODUCT TEMPLATE WITH PROJECT TASK ===============
        # print("\n\n\=========data.get('product_template_id')",data.get('product_template_id'))
        if data.get('product_template_id'):
            domain = [('remote_product_template_id', '=', data['product_template_id'])]
            find_product = self.env['product.template'].search(domain,limit=1)
            # ============== IF PRODUCT TEMPLATE IS EXIST THEN RETURN ==================
            if find_product:
                task_vals['product_template_id']=find_product.id  
            
               
        # ========== PREPARE TICKET LIST WHICH ARE CONNECTED WITH TASK ================
        
        if data.get('sh_ticket_ids'):
            sh_ticket_list=[]
            for ticket in data.get('sh_ticket_ids'):
                domain=[('remote_sh_helpdesk_ticket_id','=',ticket)]
                find_ticket = self.env['sh.helpdesk.ticket'].search(domain)
                if find_ticket:
                    sh_ticket_list.append((4,find_ticket.id))
            if sh_ticket_list:
                task_vals['sh_ticket_ids']=sh_ticket_list
          
        # ============ PREPARE VALUE FOR CLAIMS WHICH ARE CONNECTED IN TASK  ===============  
        
        if data.get('claim_ids'):
            sh_claim_list=[]
            for claim in data.get('claim_ids'):
                domain=[('remote_sh_copyright_claim_id','=',claim['id'])]
                find_claim = self.env['sh.copyright.claim'].search(domain)
                if not find_claim:
                    claim_vals=self.process_claim_data(claim)
                    if claim_vals:
                        sh_claim_list.append((0,0,claim_vals))
            if sh_claim_list:
                task_vals['claim_ids']=sh_claim_list            
          
        # ========== PREPARE DEPENDS VALUES OF PROJECT TASK ===================
        
        if data.get('depends'):
            depends_list=[]
            for depend in data.get('depends'):
                domain=[('remote_sh_depends_id','=',depend['id'])]
                find_depend = self.env['sh.depends'].search(domain)
                if find_depend:
                    depends_list.append((4,find_depend.id))
                else:
                    depend_vals={
                        'remote_sh_depends_id':depend['id'],
                        'display_name':depend['display_name'],
                        'name':depend['name'],
                        'technical_name':depend['technical_name'],
                        'company_id':1,
                    }           
                    create_depend=self.env['sh.depends'].create(depend_vals)
                    if create_depend:
                        depends_list.append((4,create_depend.id))              
            if depends_list:
                task_vals['depends']=depends_list              
        
        # =========== CONNECT GIT_REPO WITH PROJECT TASK =================
        if data.get('git_repo') and data.get('git_repo')['id'] and data.get('git_repo')['id']!=0:
            domain=[('remote_sh_git_repo_id','=',data.get('git_repo')['id'])]
            find_git_repo = self.env['sh.git.repo'].search(domain)
            if find_git_repo:
                task_vals['git_repo']=find_git_repo.id  
            else:
                git_repo_vals={
                    'remote_sh_git_repo_id':data.get('git_repo')['id'],
                    'display_name':data.get('git_repo')['display_name'],
                    'name':data.get('git_repo')['name'],
                    'repo_link':data.get('git_repo')['repo_link'],
                    'company_id':1,
                }      
                if data.get('git_repo').get('responsible_user'):
                    domain_by_id = [('remote_res_user_id','=',data['git_repo']['responsible_user'])]
                    find_user_id=self.env['res.users'].search(domain_by_id)
                    
                    # ========== SEARCH USER BY ID OR BY NAME IF EXIST THEN RETURN ELSE CREATE USE AND RETURN IT =====
                    if find_user_id:
                        git_repo_vals['responsible_user']=find_user_id.id 
                                            
                create_git_repo=self.env['sh.git.repo'].create(git_repo_vals)
                if create_git_repo:
                    task_vals['git_repo']=create_git_repo.id
                        
        # ========== LICENSE WHICH IS USED IN TASK =====================
        if data.get('license') and data.get('license')['id'] and data.get('license')['id']!=0:
            domain=[('remote_sh_license_id','=',data.get('license')['id'])]
            find_license = self.env['sh.license'].search(domain)
            if find_license:
                task_vals['license']=find_license.id  
            else:                     
                license_vals={
                    'remote_sh_license_id':data.get('license').get('id'),
                    'display_name' :data.get('license').get('display_name'),
                    'name':data.get('license').get('name'),
                    'company_id':1,
                }                    
                create_license = self.env['sh.license'].create(license_vals)
                if create_license:
                    task_vals['license']=create_license.id     
        
        # ============= PREPARE PROJECT TASK CHANGE LOG DATA ==============
        if data.get('project_task_change_log_ids'):
            change_log_list=self.process_product_change_log_data(data.get('project_task_change_log_ids'))
            if change_log_list:
                task_vals['project_task_change_log_ids']=change_log_list      

        
        # ============ Connect supported_browsers with project task ================
        if data.get('supported_browsers'):
            supported_browser_list=[]
            for browser in data.get('supported_browsers'):
                domain=[('remote_product_browsers_id','=',browser.get('id'))]
                find_browser=self.env['product.browsers'].search(domain)
                if find_browser:
                    supported_browser_list.append((4,find_browser.id))
                else:
                    browser_vals={
                        'remote_product_browsers_id':browser.get('id'),
                        'display_name':browser.get('display_name'),
                        'name':browser.get('name'),  
                        'company_id':1,                      
                    }
                    created_browser=self.env['product.browsers'].create(browser_vals)
                    if created_browser:
                        supported_browser_list.append((4,created_browser.id))
            if supported_browser_list:
                task_vals['supported_browsers']=supported_browser_list    
                    
        # ============= Connect Version with Project task ==============
        if data.get('version_ids'):
            version_list=[]
            for version in data.get('version_ids'):
                domain=[('remote_sh_version_id','=',version.get('id'))]
                find_version=self.env['sh.version'].search(domain)
                if find_version:
                    version_list.append((4,find_version.id))
                else:
                    version_vals={
                        'remote_sh_version_id':version.get('id'),
                        'display_name':version.get('display_name'),
                        'name':version.get('name'), 
                        'company_id':1,                       
                    }
                    created_version=self.env['sh.version'].create(version_vals)
                    if created_version:
                        version_list.append((4,created_version.id))
            if version_list:
                task_vals['version_ids']=version_list                     
                              
        # ============== Connect Course_id with project task ====================
        if data.get('course_id'):
            domain=[('remote_sh_traing_course_id','=',data.get('course_id').get('id'))] 
            find_course=self.env['sh.training.course'].search(domain)
            if find_course:
                task_vals['course_id']=find_course.id
            else:
                course_vals={
                    'remote_sh_traing_course_id':data.get('course_id').get('id'),
                    'display_name':data.get('course_id').get('display_name'),
                    'name':data.get('course_id').get('name'),   
                    'company_id':1                 
                }    
                if data.get('course_id').get('responsible_user_ids'):
                    responsible_user_list=[]
                    for user in data.get('course_id').get('responsible_user_ids'):
                        domain_by_id = [('remote_res_user_id','=',user)]
                        find_user_id=self.env['res.users'].search(domain_by_id)
                        if find_user_id:
                            responsible_user_list.append((4,find_user_id.id ))
                    if responsible_user_list:
                        course_vals['responsible_user_ids']= responsible_user_list
                if course_vals:
                    created_course=self.env['sh.training.course'].create(course_vals)
                    if created_course:
                        task_vals['course_id']=created_course.id    
                        
        # ================= CONNECT HR APPLICANT WITH PROJECT TASK ================
        if data.get('hr_applicant_id') and  data.get('hr_applicant_id').get('id') and  data.get('hr_applicant_id').get('id')!=0:
            domain = [('remote_hr_applicant_id', '=', data.get('hr_applicant_id')['id'])]
            find_applicant = self.env['hr.applicant'].search(domain)
            if find_applicant:
                task_vals['hr_applicant_id']=find_applicant.id    
            else: 
                applicant_vals = self.process_hr_applicant_vals(data.get('hr_applicant_id'))
                created_applicant=self.env['hr.applicant'].create(applicant_vals)
                if created_applicant:
                    task_vals['hr_applicant_id']=created_applicant.id    
        
        # ==========  SCALE CONNECT WITH PROJECT TASK ================
        if data.get('sh_scale_ids'):
            domain =[('remote_sh_scale_id','=',data.get('sh_scale_ids'))]
            find_scale_id=self.env['sh.scale'].search(domain)
            if find_scale_id:
                task_vals['sh_scale_ids']=find_scale_id.id  
            else:
                scale_vals={
                    'remote_sh_scale_id':data.get('sh_scale_ids').get('id'),
                    'days':data.get('sh_scale_ids').get('days'),
                    'display_name':data.get('sh_scale_ids').get('display_name'),
                    'name':data.get('sh_scale_ids').get('name'), 
                    'company_id':1,                   
                }      
                create_scale_id=self.env['sh.scale'].create(scale_vals)
                if create_scale_id:
                    task_vals['sh_scale_ids']=create_scale_id.id     
        
        # ============== CONNECT  upcoming_feature_ids WITH PROJECT TASK ========
        if data.get('upcoming_feature_ids'):
            feature_list=[]
            for feature in data.get('upcoming_feature_ids'):
                feature_vals={
                    'remote_sh_task_upcoming_feature_id':feature.get('id'),
                    'display_name':feature.get('display_name'),
                    'description':feature.get('description'), 
                    'company_id':1,                    
                } 
                if feature.get('user_id'):
                    domain_by_id = [('remote_res_user_id','=',feature.get('user_id'))]
                    find_user_id=self.env['res.users'].search(domain_by_id)
                    
                    # ========== SEARCH USER BY ID OR BY NAME IF EXIST THEN RETURN ELSE CREATE USE AND RETURN IT =====
                    if find_user_id:
                        feature_vals['user_id']=find_user_id.id               
                find_upcoming_feature=self.env['sh.task.upcoming.feature'].search([('remote_sh_task_upcoming_feature_id','=',feature.get('id'))])
                if feature_vals and not find_upcoming_feature:
                    feature_list.append((0,0,feature_vals))
            if feature_list:
                task_vals['upcoming_feature_ids']=feature_list    
                
        # ============== CONNECT existing_related_task_state WITH CURRENT TASK ==========
        if data.get('existing_related_task_state') and data.get('existing_related_task_state').get('id') and data.get('existing_related_task_state').get('id')!=0:        
            domain = [('remote_project_task_type_id', '=', data.get('existing_related_task_state')['id'])]
            find_task_type = self.env['project.task.type'].search(domain,limit=1)
            if find_task_type:
                task_vals['existing_related_task_state']=find_task_type.id
            else:
                project_task_type_vals=self.process_project_task_type(data.get('existing_related_task_state'))   
                create_task_type=self.env['project.task.type'].create(project_task_type_vals)    
                if create_task_type:
                    task_vals['existing_related_task_state']=create_task_type.id       
        return task_vals
        
    