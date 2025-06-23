# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
from datetime import datetime
import requests
import json

class InheritImportBase(models.Model):
    _inherit = "sh.import.base"
    
    def import_basic_crm_cron(self):   
        ''' ========== Connect db for import Crm basic  ==================  '''
        confid = self.env['sh.import.base'].search([],limit=1)
        response = requests.get('''%s/api/public/crm.lead''' %(confid.base_url))
        response_json = response.json()
        if response.status_code==200:
            
            # ======  CONNECT THEN IMPORT BASIC THING REGARDING CRM =============
            self.import_crm_tag()
            self.import_crm_stage()
            self.import_crm_team()
            self.import_crm_lost_reason()
        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "crm_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals) 
            

    
    def import_crm_tag(self):
        ''' ============== Import Crm Tags ====================== '''
        response = requests.get('%s/api/public/crm.lead.tag' %(self.base_url))
        if response.status_code == 200:
            response_json = response.json()
            count=0
            for tag in response_json.get('result'):
                
                # ========= CHECK CRM TAG IS EXIST CHECK BY ID AND THEN CHECK BY NAME ==============
                
                domain_by_id=[('remote_crm_tag_id','=',tag.get('id'))]
                already_crm_tag_id = self.env['crm.tag'].search(domain_by_id,limit=1)
                domain_by_name=[('name','=',tag.get('name'))]
                already_crm_tag_name = self.env['crm.tag'].search(domain_by_name,limit=1)
                crm_tag_data={
                    'remote_crm_tag_id':tag.get('id'),
                    'color' : tag.get('color'),  
                    'display_name':tag.get('display_name'),
                    'name':tag.get('name'),
                    }
                try:
                    if already_crm_tag_id:
                        already_crm_tag_id.write(crm_tag_data)
                    elif already_crm_tag_name:
                        already_crm_tag_name.write(crm_tag_data)
                    else:
                        
                        # ======= CRATE IF NOT EXIST CRM TAG =========
                        
                        crm_tag_id=self.env['crm.tag'].create(crm_tag_data)
                    count += 1
                    
                # ======= CREATE LOG FOR EXCEPTION WHICH IS GENERATE DURING IMPORT TAG ======= 
                    
                except Exception as e:
                    vals = {
                        "name": tag['id'],
                        "error": e,
                        "import_json" : tag,
                        "field_type": "crm_basic",                           
                        "datetime": datetime.now(),
                        "base_config_id": self.id,
                    }
                    self.env['sh.import.failed'].create(vals)
                
            # ======= CREATE LOG FOR SUCCESSFULLY IMPORT TAG ======= 
                 
            if count:
                vals = {
                    "name": self.name,
                    "state": "success",
                    "field_type": "crm_basic",
                    "error": "Crm Tags Imported Successfully",
                    "datetime": datetime.now(),
                    "base_config_id": self.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)
                
        # ======= CREATE LOG FOR ERROR WHICH IS GENERATE DURING IMPORT TAG ======= 
        else:
            vals = {
                "name": self.name,
                "state": "error",
                "field_type": "crm_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": self.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals)
            
    def process_lead_stage_data(self,data):
        ''' ========= PREPARE VALUES FOR CRM STAGE DATA =============   '''
                
        crm_stage_data={
            'remote_crm_stage_id':data.get('id'),
            'display_name':data.get('display_name'),
            'name':data.get('name'),
            'fold':data.get('fold'),
            'requirements':data.get('requirements'),
            'sequence':data.get('sequence'),
            'team_count':data.get('team_count'),
        }
        
        # =========== GET TEAM WHICH IS CONNECTED TO STAGE ==========
        
        if data.get('team_id'):
            domain=[('remote_crm_team_id','=',data.get('team_id').get('id'))]    
            find_crm_team_id=self.env['crm.team'].search(domain)
            
            # =========== CHECK IF CREATED TEAM OR NOT IF CREATE THEN RETURN ELSE CREATE AND RETURN =============
            if find_crm_team_id:
                crm_stage_data['team_id']=find_crm_team_id.id 
            else:
                team_vals=self.process_crm_team_data(data['team_id'])       
                team_id=self.env['crm.team'].create(team_vals)
                if team_id:
                    crm_stage_data['team_id']=team_id.id
                    
        return crm_stage_data  
            
    def import_crm_stage(self):
        ''' ============== Import Crm Stage ====================== '''
        response = requests.get('''%s/api/public/crm.stage?query={*,team_id{*}}''' %(self.base_url))
        if response.status_code == 200:
            response_json = response.json()
            count=0
            for stage in response_json.get('result'):
                
                # ========== CHECK IF EXIST CRM STAGE OR NOT SEARCH BY THEN SEARCH BY NAME ==============
                
                domain_by_id=[('remote_crm_stage_id','=',stage.get('id'))]
                already_crm_stage_id = self.env['crm.stage'].search(domain_by_id,limit=1)
                domain_by_name=[('name','=',stage.get('name'))]
                already_crm_stage_name = self.env['crm.stage'].search(domain_by_name,limit=1)
                crm_stage_data = self.process_lead_stage_data(stage)
                try:
                    # ============= IF EXIST THEN UPDATE IT'S DATA ==================
                    if already_crm_stage_id:
                        already_crm_stage_id.write(crm_stage_data)
                    elif already_crm_stage_name:
                        already_crm_stage_name.write(crm_stage_data)
                    else:
                        # ============= ELSE CRATE CRM STAGE  ==================
                        crm_stage_id=self.env['crm.stage'].create(crm_stage_data)
                    count += 1
                    
                # ============= CREATE LOG FOR EXCEPTION WHICH IS GENERATE DURING IMPORT STAGE  ==================    
                except Exception as e:
                    vals = {
                        "name": stage['id'],
                        "error": e,
                        "import_json" : stage,
                        "field_type": "crm_basic",                           
                        "datetime": datetime.now(),
                        "base_config_id": self.id,
                    }
                    self.env['sh.import.failed'].create(vals)
              
            # ============= CREATE LOG FOR SUCCESSFULLY IMPORT STAGE  ==================     
            if count:
                vals = {
                    "name": self.name,
                    "state": "success",
                    "field_type": "crm_basic",
                    "error": "Crm Stage Imported Successfully",
                    "datetime": datetime.now(),
                    "base_config_id": self.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)
                
        # ============= CREATE LOG FOR ERROR WHICH IS GENERATE DURING IMPORT STAGE  ==================
        else:
            vals = {
                "name": self.name,
                "state": "error",
                "field_type": "crm_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": self.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals)
            
    def process_crm_team_data(self,data):
        ''' ============= PREPARE CRM TEAM DATA ===============  '''
        
        crm_team_data={
            'remote_crm_team_id':data.get('id'),
            'active':data.get('active'),
            'color':data.get('color'),
            'dashboard_button_name':data.get('dashboard_button_name'),
            'dashboard_graph_data':data.get('dashboard_graph_data'),
            'display_name':data.get('display_name'),
            'is_favorite':data.get('is_favorite'),
            'name':data.get('name'),
            'opportunities_amount':data.get('opportunities_amount'),
            'opportunities_count':data.get('opportunities_count'),
            'use_leads':data.get('use_leads'),
            'use_opportunities':data.get('use_opportunities'),
            'company_id':1,
        }
        # ======== Get User if already created or create =========
            
        if data.get('user_id') and data.get('user_id')!=0:
            domain_by_id = [('remote_res_user_id','=',data['user_id'])]
            find_user_id=self.env['res.users'].search(domain_by_id)
            
            # ========== SEARCH USER BY ID OR BY NAME IF EXIST THEN RETURN ELSE CREATE USE AND RETURN IT =====
            if find_user_id:
                crm_team_data['user_id']=find_user_id.id 
                    
        # ======== Get User if already created or create =========
            
        if data.get('favorite_user_ids') :
            favorite_users=[]
            for f_user in data.get('favorite_user_ids'):
                domain_by_id = [('remote_res_user_id','=',f_user)]
                find_user_id=self.env['res.users'].search(domain_by_id)
                
                # ========== SEARCH USER BY ID OR BY NAME IF EXIST THEN RETURN ELSE CREATE USE AND RETURN IT =====
                
                if find_user_id:
                    favorite_users.append((4,find_user_id.id ))

            if favorite_users:
                crm_team_data['favorite_user_ids']=favorite_users
                
        # ======== Get Member if already created or create =========        
                
        if data.get('member_ids'):
            member_user_ids=[]
            for member in data.get('member_ids'):
                domain_by_id = [('remote_res_user_id','=',member)]
                find_user_id=self.env['res.users'].search(domain_by_id)
                
                # ========== SEARCH USER BY ID OR BY NAME IF EXIST THEN RETURN ELSE CREATE USE AND RETURN IT =====
                
                if find_user_id:
                    member_user_ids.append((4,find_user_id.id ))
            if favorite_users:
                crm_team_data['member_ids']=member_user_ids
            
        return crm_team_data
            
  
            
    def import_crm_team(self):
        ''' ============== Import Crm Team ====================== '''
        response = requests.get('''%s/api/public/crm.team?query={*}''' %(self.base_url))
        if response.status_code == 200:
            response_json = response.json()
            count=0
            for team in response_json.get('result'):
                domain=['|',('remote_crm_team_id','=',team.get('id')),('name','=',team.get('name'))]
                already_crm_team = self.env['crm.team'].search(domain,limit=1)
                
                # ============ PREPARE CRM TEAM DATA FOR CREATE OR UPDATE  =============
                crm_team_data = self.process_crm_team_data(team)
                try:
                    
                    # ======= CHECK IF NOT EXIST THEN CRETE ===========
                    if not already_crm_team:
                        crm_team_id=self.env['crm.team'].create(crm_team_data)
                        
                    # ======= ELSE UPDATE CRM TEAM WITH PREPARE VALUES ===========
                    else:
                        already_crm_team.write(crm_team_data)
                    count += 1
                    
                # ============= CREATE LOG FOR EXCEPTION WHICH IS GENERATE DURING IMPORT CRM TEAM  ==================   
                except Exception as e:
                    vals = {
                        "name": team['id'],
                        "error": e,
                        "import_json" : team,
                        "field_type": "crm_basic",                           
                        "datetime": datetime.now(),
                        "base_config_id": self.id,
                    }
                    self.env['sh.import.failed'].create(vals)
                
            # ============= CREATE LOG FOR SUCCESSFULLY IMPORT CRM TEAM  ==================
            if count:
                vals = {
                    "name": self.name,
                    "state": "success",
                    "field_type": "crm_basic",
                    "error": "Crm Team Imported Successfully",
                    "datetime": datetime.now(),
                    "base_config_id": self.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)
                
        # ============= CREATE LOG FOR ERROR WHICH IS GENERATE DURING IMPORT CRM TEAM  ==================
        else:
            vals = {
                "name": self.name,
                "state": "error",
                "field_type": "crm_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": self.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals)
            
            
    def import_crm_lost_reason(self):
        ''' ============== Import Crm Lost Reason ====================== '''
        response = requests.get('%s/api/public/crm.lost.reason' %(self.base_url))
        if response.status_code == 200:
            response_json = response.json()
            count=0
            for reason in response_json.get('result'):
                
                # ========== CHECK IF EXIST CRM LOST REASON =============
                
                domain_by_id=[('remote_crm_lost_reason_id','=',reason.get('id'))]
                already_crm_lost_reason_id = self.env['crm.lost.reason'].search(domain_by_id,limit=1)
                domain_by_name=[('name','=',reason.get('name'))]
                already_crm_lost_reason_name = self.env['crm.lost.reason'].search(domain_by_name,limit=1)
                
                # ========== PREAPRE VALUE FOR UPDATE OR CREATE CRM LOST REASON ==========
                crm_lost_reason_data={
                    'remote_crm_lost_reason_id':reason.get('id'),
                    'active' : reason.get('active'),  
                    'display_name':reason.get('display_name'),
                    'name':reason.get('name'),
                    'leads_count':reason.get('leads_count'),
                    }
                
                try:
                    # ========== SEARCH BY ID OR SEARCH BY NAME IF EXIST THEN UPDATE ===========
                    if already_crm_lost_reason_id:
                        already_crm_lost_reason_id.write(crm_lost_reason_data)
                    elif already_crm_lost_reason_name:
                        already_crm_lost_reason_name.write(crm_lost_reason_data)
                    
                    # ========== IF NOT EXIST THEN CREATED ===========
                    
                    else:
                        crm_tag_id=self.env['crm.lost.reason'].create(crm_lost_reason_data)
                    count += 1
                    
                # ============= CREATE LOG FOR EXCEPTION WHICH IS GENERATE DURING IMPORT CRM LOST REASON  ==================      
                except Exception as e:
                    vals = {
                        "name": reason['id'],
                        "error": e,
                        "import_json" : reason,
                        "field_type": "crm_basic",                           
                        "datetime": datetime.now(),
                        "base_config_id": self.id,
                    }
                    self.env['sh.import.failed'].create(vals)
                
            # ============= CREATE LOG FOR SUCCESSFULLY IMPORT CRM LOST REASON  ==================     
            if count:
                vals = {
                    "name": self.name,
                    "state": "success",
                    "field_type": "crm_basic",
                    "error": "Crm Lost Reason Imported Successfully",
                    "datetime": datetime.now(),
                    "base_config_id": self.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)
                
        # ============= CREATE LOG FOR ERROR WHICH IS GENERATE DURING IMPORT CRM LOST REASON ==================          
        else:
            vals = {
                "name": self.name,
                "state": "error",
                "field_type": "crm_basic",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": self.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals)     