# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
import requests
import json
from datetime import datetime

class InheritImportHelpdeskBase(models.Model):
    _inherit = "sh.import.base"
    
    def import_basic_helpdesk_cron(self):   
        ''' ========== Connect db for import Helpdesk basic  ==================  '''
        confid = self.env['sh.import.base'].search([],limit=1)
        response = requests.get('''%s/api/public/helpdesk.stages''' %(confid.base_url))
        response_json = response.json()
        if response.status_code==200:
            pass
            self.import_helpdesk_category()
            self.import_helpdesk_subcategory()
            self.import_helpdesk_priority()
            self.import_helpdesk_stage()
            self.import_helpdesk_tags()
            self.import_helpdesk_team()
            self.import_helpdesk_ticket_type()
            self.import_helpdesk_sub_type()
            self.import_helpdesk_alarm()
            self.import_helpdesk_sla()
        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "helpdesk_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals) 
            
    def import_helpdesk_category(self):
        ''' ============== Import Helpdesk Category ==============  '''
        
        confid = self.env['sh.import.base'].search([],limit=1)
        response = requests.get('''%s/api/public/helpdesk.category''' %(confid.base_url))
        response_json = response.json()
        if response.status_code==200:
            count = 0
            for category in response_json['result']:
                domain = ['|',('remote_sh_helpdesk_category_id', '=', category['id']),('name', '=', category['name'])]
                find_category = self.env['sh.helpdesk.category'].search(domain)
                helpdesk_category_vals={
                    'remote_sh_helpdesk_category_id' : category['id'],
                    'display_name':category['display_name'],
                    'name':category['name'],
                    'sequence' : category['sequence'],
                }
                if find_category:
                    count += 1
                    find_category.write(helpdesk_category_vals)
                else:
                    self.env['sh.helpdesk.category'].create(helpdesk_category_vals)
                    count += 1
                    
            if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "helpdesk_basic",
                        "error": "%s Helpdesk Category Imported Successfully" %(count),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "helpdesk_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals) 
            
    def import_helpdesk_subcategory(self):
        ''' ============== Import Helpdesk Sub Category ==============  '''
        
        confid = self.env['sh.import.base'].search([],limit=1)
        response = requests.get('''%s/api/public/helpdesk.subcategory?query={*,parent_category_id{*}}''' %(confid.base_url))
        response_json = response.json()
        if response.status_code==200:
            count = 0
            for category in response_json['result']:
                domain = ['|',('remote_helpdesk_subcategory_id', '=', category['id']),('name', '=', category['name'])]
                find_subcategory = self.env['helpdesk.subcategory'].search(domain)
                helpdesk_subcategory_vals={
                    'remote_helpdesk_subcategory_id' : category['id'],
                    'display_name':category['display_name'],
                    'name':category['name'],
                    'sequence' : category['sequence'],
                }
                if category.get('parent_category_id'):
                    domain_category=[('remote_sh_helpdesk_category_id','=',category.get('parent_category_id').get('id'))] 
                    find_category=self.env['sh.helpdesk.category'].search(domain_category)
                    if find_category:
                       helpdesk_subcategory_vals['parent_category_id']=find_category.id
                    else:
                        helpdesk_category_vals={
                            'remote_sh_helpdesk_category_id' : category['parent_category_id']['id'],
                            'display_name':category['parent_category_id']['display_name'],
                            'name':category['parent_category_id']['name'],
                            'sequence' : category['parent_category_id']['sequence'],
                        }
                        helpdesk_category=self.env['sh.helpdesk.category'].create(helpdesk_category_vals)
                        helpdesk_subcategory_vals['parent_category_id']=helpdesk_category.id
                if find_subcategory:
                    count += 1
                    find_subcategory.write(helpdesk_subcategory_vals)
                else:
                    self.env['helpdesk.subcategory'].create(helpdesk_subcategory_vals)
                    count += 1
                    
            if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "helpdesk_basic",
                        "error": "%s Helpdesk  SubCategory Imported Successfully" %(count),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "helpdesk_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals)
            
    def import_helpdesk_priority(self):
        ''' ============== Import Helpdesk priority ==============  '''
        
        confid = self.env['sh.import.base'].search([],limit=1)
        response = requests.get('''%s/api/public/helpdesk.priority''' %(confid.base_url))
        response_json = response.json()
        if response.status_code==200:
            count = 0
            for priority in response_json['result']:
                domain = ['|',('remote_helpdesk_priority_id', '=', priority['id']),('name', '=', priority['name'])]
                find_priority = self.env['helpdesk.priority'].search(domain)
                helpdesk_priority_vals={
                    'remote_helpdesk_priority_id' : priority['id'],
                    'display_name':priority['display_name'],
                    'name':priority['name'],
                    'sequence' : priority['sequence'],
                    'color':priority['color'],
                }
                if find_priority:
                    count += 1
                    find_priority.write(helpdesk_priority_vals)
                else:
                    self.env['helpdesk.priority'].create(helpdesk_priority_vals)
                    count += 1
                    
            if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "helpdesk_basic",
                        "error": "%s Helpdesk Priority Imported Successfully" %(count),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "helpdesk_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals) 
            
    def import_helpdesk_stage(self):   
        ''' ============== Import Helpdesk Stage ==============  '''
        
        confid = self.env['sh.import.base'].search([],limit=1)
        response = requests.get('''%s/api/public/helpdesk.stages?query={*,sh_next_stage{*}}''' %(confid.base_url))
        response_json = response.json()
        if response.status_code==200:
            count = 0
            for stage in response_json['result']:
                domain = ['|',('remote_sh_helpdesk_stages_id', '=', stage['id']),('name', '=', stage['name'])]
                find_stage = self.env['sh.helpdesk.stages'].search(domain,limit=1)
                helpdesk_stages_vals={
                    'remote_sh_helpdesk_stages_id' : stage['id'],
                    'display_name':stage['display_name'],
                    'name':stage['name'],
                    'is_cancel_button_visible':stage['is_cancel_button_visible'],
                    'is_done_button_visible':stage['is_done_button_visible'],
                    'sequence':stage['sequence'],
                }
                if find_stage:
                    count += 1
                    find_stage.write(helpdesk_stages_vals)
                else:
                    self.env['sh.helpdesk.stages'].create(helpdesk_stages_vals)
                    count += 1
            for stage in response_json['result']:
                domain_next = [('remote_sh_helpdesk_stages_id', '=', stage['sh_next_stage']['id'])]
                find_next_stage = self.env['sh.helpdesk.stages'].search(domain_next)
                domain_current_stage=[('remote_sh_helpdesk_stages_id','=',stage['id'])]
                find_current_stage=self.env['sh.helpdesk.stages'].search(domain_current_stage)
                if find_current_stage and find_next_stage:
                    find_current_stage.write({
                        'sh_next_stage':find_next_stage.id
                    })
            if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "helpdesk_basic",
                        "error": "%s Helpdesk Stage Imported Successfully" %(count),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "helpdesk_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals) 
            
    def import_helpdesk_tags(self):   
        ''' ============== Import Helpdesk Tags ==============  '''
        
        confid = self.env['sh.import.base'].search([],limit=1)
        response = requests.get('''%s/api/public/helpdesk.tags''' %(confid.base_url))
        response_json = response.json()
        if response.status_code==200:
            count = 0
            for tag in response_json['result']:
                domain = ['|',('remote_sh_helpdesk_tags_id', '=', tag['id']),('name', '=', tag['name'])]
                find_tag = self.env['sh.helpdesk.tags'].search(domain)
                helpdesk_tag_vals={
                    'remote_sh_helpdesk_tags_id' : tag['id'],
                    'display_name':tag['display_name'],
                    'name':tag['name'],
                    'color':tag['color'],
                }
                if find_tag:
                    count += 1
                    find_tag.write(helpdesk_tag_vals)
                else:
                    self.env['sh.helpdesk.tags'].create(helpdesk_tag_vals)
                    count += 1
            if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "helpdesk_basic",
                        "error": "%s Helpdesk Tags Imported Successfully" %(count),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "helpdesk_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals) 
            
            
    def process_helpdesk_sla_data(self,data):
        ''' =============== Prepare Sla data for import helpdesk sla =============  '''
        
        helpdesk_sla_vals={
            'remote_sh_helpdesk_sla_id' : data['id'],
            'display_name':data['display_name'],
            'name':data['name'],
            'sh_days':data['sh_days'],
            'sh_hours' : data['sh_hours'],
            'sh_minutes':data['sh_minutes'],
            'sh_sla_target_type':data['sh_sla_target_type']['sh_api_current_state'],
            'sla_ticket_count':data['sla_ticket_count'],
            'company_id':1,
        }
        
        # ======= get stage if created or create =========
        if data.get('sh_stage_id'):
            domain = [('remote_sh_helpdesk_stages_id', '=', data.get('sh_stage_id')['id'])]
            find_stage = self.env['sh.helpdesk.stages'].search(domain)
            if find_stage:
                helpdesk_sla_vals['sh_stage_id']=find_stage.id
            else:
                helpdesk_stages_vals={
                    'remote_sh_helpdesk_stages_id' : data['sh_stage_id']['id'],
                    'display_name':data['sh_stage_id']['display_name'],
                    'name':data['sh_stage_id']['name'],
                    'is_cancel_button_visible':data['sh_stage_id']['is_cancel_button_visible'],
                    'is_done_button_visible':data['sh_stage_id']['is_done_button_visible'],
                    'sequence':data['sh_stage_id']['sequence'],
                }
                created_stage=self.env['sh.helpdesk.stages'].create(helpdesk_stages_vals)
                helpdesk_sla_vals['sh_stage_id']=created_stage.id
        
        # ============= get team if created or create =============== 
        if data.get('sh_team_id') and  data.get('sh_team_id').get('id') and  data.get('sh_team_id').get('id')!=0 :
            domain = [('remote_sh_helpdesk_team_id','=',data.get('sh_team_id').get('id'))]
            find_team = self.env['sh.helpdesk.team'].search(domain)
            if find_team:
                helpdesk_sla_vals['sh_team_id']=find_team.id
            else:
                helpdesk_team_vals = self.process_helpdesk_team_data(data.get('sh_team_id'))
                team_id=self.env['sh.helpdesk.team'].create(helpdesk_team_vals)
                helpdesk_sla_vals['sh_team_id']=team_id.id
            
        # ===== get ticket type if create or create  =============
        if data.get('sh_ticket_type_id'):
            domain = [('remote_sh_helpdesk_ticket_type_id', '=', data['sh_ticket_type_id']['id'])]
            find_ticket_type = self.env['sh.helpdesk.ticket.type'].search(domain)
            if find_ticket_type:
                helpdesk_sla_vals['sh_ticket_type_id']=find_ticket_type.id
            else:
                helpdesk_ticket_type_vals={
                    'remote_sh_helpdesk_ticket_type_id' : data['sh_ticket_type_id']['id'],
                    'display_name':data['sh_ticket_type_id']['display_name'],
                    'name':data['sh_ticket_type_id']['name'],
                    'sla_count':data['sh_ticket_type_id']['sla_count'],
                }
                ticket_type = self.env['sh.helpdesk.ticket.type'].create(helpdesk_ticket_type_vals)
                if ticket_type:
                    helpdesk_sla_vals['sh_ticket_type_id']=ticket_type.id
        return helpdesk_sla_vals    
            
            
            
    def import_helpdesk_sla(self):   
        ''' ============== Import Helpdesk Sla ==============  '''
        
        confid = self.env['sh.import.base'].search([],limit=1)
        response = requests.get('''%s/api/public/sh.helpdesk.sla?query={*,sh_stage_id{*,sh_next_stage{*}},sh_team_id{*,team_head{id,active,active_partner,alias_contact,barcode,city,color,comment,contact_address,country_id{name},lang,login,mobile,name,new_password,partner_id{name,vat,title,ref,type,website,supplier,street,street2,city,state_id{name,code},country_id{name},zip,email,is_company,phone,mobile,id,company_type,customer,child_ids{name,title,ref,type,website,supplier,street,street2,city,state_id{name,code},country_id{name},zip,email,is_company,phone,mobile,id,company_type,customer,child_ids}},credit_limit,customer,display_name,email,email_formatted,
                                    password,phone,state,state_id{name,code},street,street2,supplier,type,vat,tz,tz_offset},team_members{id,active,active_partner,alias_contact,barcode,city,color,comment,contact_address,country_id{name},lang,login,mobile,name,new_password,partner_id{name,vat,title,ref,type,website,supplier,street,street2,city,state_id{name,code},country_id{name},zip,email,is_company,phone,mobile,id,company_type,customer,child_ids{name,title,ref,type,website,supplier,street,street2,city,state_id{name,code},country_id{name},zip,email,is_company,phone,mobile,id,company_type,customer,child_ids}},credit_limit,customer,display_name,email,email_formatted,
                                    password,phone,state,state_id{name,code},street,street2,supplier,type,vat,tz,tz_offset}},sh_ticket_type_id{*}}''' %(confid.base_url))
        response_json = response.json()
        if response.status_code==200:
            count = 0
            for sla in response_json['result']:
                domain = ['|',('remote_sh_helpdesk_sla_id', '=', sla['id']),('name', '=', sla['name'])]
                find_sla = self.env['sh.helpdesk.sla'].search(domain)
                helpdesk_sla_vals=self.process_helpdesk_sla_data(sla)
                if find_sla:
                    count += 1
                    find_sla.write(helpdesk_sla_vals)
                else:
                    self.env['sh.helpdesk.sla'].create(helpdesk_sla_vals)
                    count += 1
            if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "helpdesk_basic",
                        "error": "%s Helpdesk Sla Imported Successfully" %(count),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "helpdesk_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals)          
            
    def import_helpdesk_ticket_type(self):
        ''' ============== Import Helpdesk Ticket Type ==============  '''
        
        confid = self.env['sh.import.base'].search([],limit=1)
        response = requests.get('''%s/api/public/helpdesk.ticket.type''' %(confid.base_url))
        response_json = response.json()
        if response.status_code==200:
            count = 0
            for ticket_type in response_json['result']:
                domain = ['|',('remote_sh_helpdesk_ticket_type_id', '=', ticket_type['id']),('name', '=', ticket_type['name'])]
                find_ticket_type = self.env['sh.helpdesk.ticket.type'].search(domain)
                helpdesk_ticket_type_vals={
                    'remote_sh_helpdesk_ticket_type_id' : ticket_type['id'],
                    'display_name':ticket_type['display_name'],
                    'name':ticket_type['name'],
                    'sla_count':ticket_type['sla_count'],
                }
                if find_ticket_type:
                    count += 1
                    find_ticket_type.write(helpdesk_ticket_type_vals)
                else:
                    self.env['sh.helpdesk.ticket.type'].create(helpdesk_ticket_type_vals)
                    count += 1
            if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "helpdesk_basic",
                        "error": "%s Helpdesk Ticket Type Imported Successfully" %(count),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "helpdesk_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals) 
    
    
    def import_helpdesk_sub_type(self):
        ''' ============== Import Helpdesk Sub Type ==============  '''
        
        confid = self.env['sh.import.base'].search([],limit=1)
        response = requests.get('''%s/api/public/helpdesk.sub.type''' %(confid.base_url))
        response_json = response.json()
        if response.status_code==200:
            count = 0
            for sub_type in response_json['result']:
                domain = ['|',('remote_helpdesk_sub_type_id', '=', sub_type['id']),('name', '=', sub_type['name'])]
                find_sub_type = self.env['sh.helpdesk.sub.type'].search(domain)
                helpdesk_sub_type_vals={
                    'remote_helpdesk_sub_type_id' : sub_type['id'],
                    'display_name':sub_type['display_name'],
                    'name':sub_type['name'],
                    # 'sla_count':sub_type['sla_count'],
                }
                if find_sub_type:
                    count += 1
                    find_sub_type.write(helpdesk_sub_type_vals)
                else:
                    self.env['sh.helpdesk.sub.type'].create(helpdesk_sub_type_vals)
                    count += 1
            if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "helpdesk_basic",
                        "error": "%s Helpdesk Sub Type Imported Successfully" %(count),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "helpdesk_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals) 
    
    def import_helpdesk_alarm(self):
        ''' ============== Import Helpdesk Alarm ==============  '''
        
        confid = self.env['sh.import.base'].search([],limit=1)
        response = requests.get('''%s/api/public/sh.ticket.alarm''' %(confid.base_url))
        response_json = response.json()
        if response.status_code==200:
            count = 0
            for ticket_alarm in response_json['result']:
                domain = ['|',('remote_sh_ticket_alarm_id', '=', ticket_alarm['id']),('name', '=', ticket_alarm['name'])]
                find_alarm = self.env['sh.ticket.alarm'].search(domain)
                helpdesk_ticket_alarm_vals={
                    'remote_sh_ticket_alarm_id' : ticket_alarm['id'],
                    'display_name':ticket_alarm['display_name'],
                    'name':ticket_alarm['name'],
                    'sh_remind_before':ticket_alarm['sh_remind_before'],
                    'sh_reminder_unit':ticket_alarm['sh_reminder_unit']['sh_api_current_state'],
                    'type':ticket_alarm['type']['sh_api_current_state'],
                    'company_id':1,
                }
                if find_alarm:
                    count += 1
                    find_alarm.write(helpdesk_ticket_alarm_vals)
                else:
                    self.env['sh.ticket.alarm'].create(helpdesk_ticket_alarm_vals)
                    count += 1
            if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "helpdesk_basic",
                        "error": "%s Helpdesk Ticket Alarm Imported Successfully" %(count),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "helpdesk_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals) 
    
    def process_helpdesk_team_data(self,data):
        helpdesk_team_vals={
            'remote_sh_helpdesk_team_id' : data['id'],
            'display_name':data['display_name'],
            'name':data['name'],
            'sla_count':data['sla_count'],
        }
        
        # ======== Get team Head if already created or create =========
        if data.get('team_head') and data.get('team_head').get('id') and data.get('team_head').get('id')!=0:
            domain_by_id = [('remote_res_user_id','=',data['team_head']['id'])]
            find_user_id=self.env['res.users'].search(domain_by_id)
            domain_by_login = [('login','=',data['team_head']['login'])]
            find_user_login=self.env['res.users'].search(domain_by_login)
            if find_user_id:
                helpdesk_team_vals['team_head']=find_user_id.id 
            elif find_user_login:
                helpdesk_team_vals['team_head']=find_user_login.id 
            else:
                # user_vals=self.process_user_data(data['helpdesk_team_vals']) 
                user_vals=self.process_user_data(data['team_head'])       
                user_id=self.env['res.users'].create(user_vals)
                if user_id:
                    helpdesk_team_vals['team_head']=user_id.id
        
        # ========= Get Team member if already created or create ===========
        
        if data.get('team_members') :
            team_members=[]
            for member in data.get('team_members'):
                if member.get('id') and member.get('id')!=0:
                    domain_by_id = [('remote_res_user_id','=',member['id'])]
                    find_user_id=self.env['res.users'].search(domain_by_id)
                    domain_by_login = [('login','=',member['login'])]
                    find_user_login=self.env['res.users'].search(domain_by_login)
                    if find_user_id:
                        team_members.append((4,find_user_id.id ))
                    elif find_user_login:
                        team_members.append((4,find_user_login.id ))
                    else:
                        user_vals=self.process_user_data(member)       
                        user_id=self.env['res.users'].create(user_vals)
                        if user_id:
                            team_members.append((4,user_id.id ))
            if team_members:
                helpdesk_team_vals['team_members']=team_members            
        
        return helpdesk_team_vals
    
    
    def import_helpdesk_team(self):
        ''' ============== Import Helpdesk Team ==============  '''
        
        confid = self.env['sh.import.base'].search([],limit=1)
        response = requests.get('''%s/api/public/helpdesk.team?query={*,team_head{id,active,active_partner,alias_contact,notification_type,barcode,city,color,comment,contact_address,country_id{name},lang,login,mobile,name,new_password,partner_id{name,vat,title,ref,type,website,supplier,street,street2,city,state_id{name,code},country_id{name},zip,email,is_company,phone,mobile,id,company_type,customer,child_ids{name,title,ref,type,website,supplier,street,street2,city,state_id{name,code},country_id{name},zip,email,is_company,phone,mobile,id,company_type,customer,child_ids}},credit_limit,customer,display_name,email,email_formatted,
                                    password,phone,state,state_id{name,code},street,street2,supplier,type,vat,tz,tz_offset},team_members{id,active,active_partner,alias_contact,barcode,city,color,comment,contact_address,country_id{name},lang,login,mobile,name,new_password,partner_id{name,vat,title,ref,type,website,supplier,street,street2,city,state_id{name,code},country_id{name},zip,email,is_company,phone,mobile,id,company_type,customer,child_ids{name,title,ref,type,website,supplier,street,street2,city,state_id{name,code},country_id{name},zip,email,is_company,phone,mobile,id,company_type,customer,child_ids}},credit_limit,customer,display_name,email,email_formatted,
                                    password,phone,state,state_id{name,code},street,street2,supplier,type,vat,tz,tz_offset}}''' %(confid.base_url))
        response_json = response.json()
        if response.status_code==200:
            count = 0
            for helpdesk_team in response_json['result']:
                domain = ['|',('remote_sh_helpdesk_team_id', '=', helpdesk_team['id']),('name', '=', helpdesk_team['name'])]
                find_team = self.env['sh.helpdesk.team'].search(domain)
                # helpdesk_team_vals={
                #     'remote_sh_helpdesk_team_id' : helpdesk_team['id'],
                #     'display_name':helpdesk_team['display_name'],
                #     'name':helpdesk_team['name'],
                #     'sla_count':helpdesk_team['sla_count'],
                #     'team_head':helpdesk_team['team_head'],
                #     'team_members':helpdesk_team['team_members'],
                # }
                helpdesk_team_vals = self.process_helpdesk_team_data(helpdesk_team)
                if find_team:
                    count += 1
                    find_team.write(helpdesk_team_vals)
                else:
                    self.env['sh.helpdesk.team'].create(helpdesk_team_vals)
                    count += 1
            if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "helpdesk_basic",
                        "error": "%s Helpdesk Team Imported Successfully" %(count),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "helpdesk_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals) 
    
    