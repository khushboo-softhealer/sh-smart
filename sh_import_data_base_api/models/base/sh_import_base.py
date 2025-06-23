# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
import requests
import json
from datetime import datetime

class ImportBase(models.Model):
    _name = "sh.import.base"
    _description = "Import Base"

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(string='Name',required=True,copy=False)
    base_url = fields.Char("Base Url")
    
    
    records_per_page = fields.Integer("No of records per page ")
    
    state = fields.Selection([('draft','Draft'),('success','Success')],default="draft",string="State")
    current_import_page = fields.Integer("Current Page ",default=0)
    
    log_historys = fields.One2many(
        'sh.import.base.log', 'base_config_id', string="Log History")
    failed_history = fields.One2many(
        'sh.import.failed', 'base_config_id', string="Failed History")

    def connect_database(self): 
        '''  
            MAKE CONNECTION TO OTHER DB AND TRY TO IMPORT PRODUCT BASIC THING LIKE PRODUCT CATGEORY
        '''
        response = requests.get('%s/api/public/res.country' %(self.base_url))
        if response.status_code == 200:
            
            # ========== IF CONNECTION ESTABLISH SUCCESSFULLY THEN CREATE LOG OF SUCCESS ============
            
            self.state = 'success'
            vals = {
                "name": self.name,
                "state": "success",
                "field_type": "auth",
                "error": "Connection Successful",
                "datetime": datetime.now(),
                "base_config_id": self.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals)
            
            # ===========   IMPORT PRODUCT CATEGORY AND UOM  ==============
            # self.import_product_category()
            # self.import_product_public_category()
            # self.import_unit_of_measure()
            # self.import_resource_resource()
            self.import_resource_calendar()
            # self.import_partner_category()
            # self.import_mail_message_subtype()
            # self.import_utm_medium()
            # ========= ELSE CREATE LOG OF GIVEN ERROR REGARDING ESTABLISH CONNECTION =============
        else:
            vals = {
                "name": self.name,
                "state": "error",
                "field_type": "auth",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": self.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals)

    

    def import_unit_of_measure(self):
        ''' ============  IMPORT UNIT OF MEASURE ================= '''
        
        response = requests.get('%s/api/public/uom.uom?query={id,name,uom_type,factor,rounding,category_id{*}}' %(self.base_url))
        if response.status_code == 200:
            response_json = response.json()
            total_count = response_json['count']
            count = 0
            for uom in response_json['result']:
                domain = []
                if  uom['name'] == 'Day(s)':
                    domain = [('name','=','Days')]
                elif  uom['name'] == 'Dozen(s)':
                    domain = [('name','=','Dozens')]
                elif  uom['name'] == 'Hour(s)':
                    domain = [('name','=','Hours')]
                elif  uom['name'] == 'Liter(s)':
                    domain = [('name','=','L')]
                elif  uom['name'] == 'Unit(s)':
                    domain = [('name','=','Units')]
                elif  uom['name'] == 'cm':
                    domain = [('name','=','cm')]
                elif  uom['name'] == 'fl oz':
                    domain = [('name','=','fl oz (US)')]
                elif  uom['name'] == 'foot(ft)':
                    domain = [('name','=','ft')]
                elif  uom['name'] == 'g':
                    domain = [('name','=','g')]
                elif  uom['name'] == 'gal(s)':
                    domain = [('name','=','gal (US)')]
                elif  uom['name'] == 'inch(es)':
                    domain = [('name','=','in')]
                elif  uom['name'] == 'kg':
                    domain = [('name','=','kg')]
                elif  uom['name'] == 'km':
                    domain = [('name','=','km')]
                elif  uom['name'] == 'lb(s)':
                    domain = [('name','=','lb')]
                elif  uom['name'] == 'm':
                    domain = [('name','=','m')]
                elif  uom['name'] == 'mile(s)':
                    domain = [('name','=','mi')]
                elif  uom['name'] == 'oz(s)':
                    domain = [('name','=','oz')]
                elif  uom['name'] == 'qt':
                    domain = [('name','=','qt (US)')]
                elif  uom['name'] == 't':
                    domain = [('name','=','t')]
                else:
                    domain = [('name', '=', uom['name'])]

                find_uom = False
                if domain:
                    find_uom = self.env['uom.uom'].search(domain)
                    
                # ===========  CHECK UOM IS NOT EXIST THEN CREATE IT ==================
                    
                if not find_uom:
                    uom_vals = {
                        'name' : uom['name'],
                        'rounding':uom['rounding'],
                        'uom_type':uom['uom_type']['sh_api_current_state'],                        
                        'remote_uom_uom_id':uom['id']
                    }
                    category = self.process_category(uom['category_id'])
                    if category:
                        uom_vals['category_id'] = category.id
                    uom_type = uom['uom_type']['sh_api_current_state']
                    if uom_type == 'reference':
                        uom_vals.update({'ratio':1})
                    elif uom_type == 'bigger':
                        uom_vals.update({'ratio':1/ uom['factor']})
                    elif uom_type == 'smaller':
                        uom_vals.update({'ratio':uom['factor']})
                    self.env['uom.uom'].sudo().create(uom_vals)
                
                 # ===========  CHECK UOM IS EXIST THEN UPDATE'S IT'S VALUE ==================
                
                else:
                    find_uom.sudo().write({'remote_uom_uom_id':uom['id']})
                count += 1
                
            # ========= CREATE LOG FOR SUCCESSFULLY IMPORT UOM =================
                
            if count == total_count:
                vals = {
                    "name": self.name,
                    "state": "success",
                    "field_type": "uom",
                    "error": "Unit of Measure Imported Successfully",
                    "datetime": datetime.now(),
                    "base_config_id": self.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)
                
        # ========= CREATE LOG FOR ERROR WHICH IS GENERATE DURING IMPORT UOM =================
        
        else:
            vals = {
                "name": self.name,
                "state": "error",
                "field_type": "uom",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": self.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals)                  
    
    def import_partner_category(self):
        ''' ============ IMPORT PARTNER CATEGORY ===========   '''
        
        confid = self.env['sh.import.base'].search([],limit=1)
        response = requests.get('''%s/api/public/partner.category''' %(confid.base_url))
        if response.status_code == 200:
            count=0
            response_json = response.json()     
            for data in response_json['result']:
                
                #  ============= PREAPRE RESOURCE CALENDAR VALS FOR IMPORT THAT ==============
                
                resource_partner_category_vals = {
                    'remote_partner_category_id':data.get('id'),
                    # 'active':data.get('active'),
                    'display_name':data.get('display_name'),
                    'name':data.get('name'),
                    # 'color':data.get('color'),
                }
                domain = ['|',('remote_partner_category_id', '=', data['id']),('name', '=', data['name'])]
                find_partner_category = self.env['partner.category'].search(domain)
                    
                    # ============ CHECK IF RESOURCE CALENDAR EXIST OR NOT ===============
                if find_partner_category:
                    find_partner_category.write(resource_partner_category_vals)                            
                else:
                    self.env['partner.category'].create(resource_partner_category_vals)  
                count += 1
            
            # for data in response_json['result']:
            #     domain = [('remote_partner_category_id', '=', data['id'])]
            #     find_partner_category = self.env['partner.category'].search(domain)  
            #     domain_parent=[('remote_partner_category_id', '=', data['parent_id'])]
            #     find_parent_category= self.env['partner.category'].search(domain_parent) 
            #     if find_parent_category and find_partner_category:
            #         find_partner_category.write({
            #             'parent_id':find_parent_category.id
            #         })   
                    
            # ========= CREATE LOG FOR SUCCESSFULLY IMPORT Partner Category =================
                
            if count:
                vals = {
                    "name": self.name,
                    "state": "success",
                    "field_type": "partner_category",
                    "error": "Partner Category Imported Successfully",
                    "datetime": datetime.now(),
                    "base_config_id": self.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)                       
                        
        # ========== CREATE LOG FOR ERROR WHICH IS  GENERATE DURING Partner Category IMPORT  ==============

        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "partner_category",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals)
    
    def process_tax(self,taxes):
        ''' ============ PREPARE VALUES FOR TAX =====================   '''
        print("================tax ")
        tax_list = []
        for value in taxes:
            if value.get('id') and value.get('id')!=0:
                domain = [('name', '=', value['name']),('amount_type', '=', value['amount_type']['sh_api_current_state']),('type_tax_use', '=', value['type_tax_use']['sh_api_current_state'])]
                find_tax = self.env['account.tax'].search(domain,limit=1)
                print("\n\n=====find_tax",find_tax,find_tax.name)
                # ============ CHECK IF TAX IS CREATED OR NOT IF CREATED THEN RETURN IT'S VALUE ELSE CREATE ===============
                
                if find_tax:
                    tax_list.append(find_tax.id)
                else:
                    tax_vals = {
                        'name' : value['name'],
                        'amount' : value['amount'],
                        'type_tax_use' : value['type_tax_use']['sh_api_current_state'],
                        'amount_type' : 'percent',
                    }
                    create_tax = self.env['account.tax'].create(tax_vals)
                    tax_list.append(create_tax.id)
                
                # ============= RETURN TAX LIST ==================
            
        return [(6,0,tax_list)]

    def process_seller_ids(self,seller_ids,product_tmpl_id):
        
        ''' ================= PREPARE SUPPLIER INFO LINES INSIDE PRODUCT  =================    '''
        
        for seller in seller_ids:
            vendor = self.get_proper_vendor(seller['name'])
            seller_vals = {
                'partner_id' : vendor.id,
                'price' :  seller['price'],
                'product_code' : seller['product_code'],
                'product_name' : seller['product_name'],
                'min_qty' : seller['min_qty'],
                'product_tmpl_id' : product_tmpl_id.id
            }
            if seller.get('date_start') != '':
                seller_vals['date_start'] = seller.get('date_start')
            if seller.get('date_end') != '':
                seller_vals['date_end'] = seller.get('date_end')
            domain = [('remote_uom_uom_id', '=', seller['product_uom'])]
            find_uom = self.env['uom.uom'].search(domain)
            if find_uom:
                seller_vals['product_uom'] = find_uom.id
            domain = [('remote_product_supplierinfo_id', '=', seller['id'])]
            find_supplierinfo = self.env['product.supplierinfo'].search(domain)
            
            # ============= CHECK IF SUPPLIERINFO INFO IS CREATED THEN RETURN ELSE CREATE AND RETURN IT  ==============
            
            if find_supplierinfo:
                find_supplierinfo.write(seller_vals)
            else:
                self.env['product.supplierinfo'].create(seller_vals)
        return []


    def import_resource_calendar(self):
        ''' ============ IMPORT RESOURCE CALEANDAR ===========   '''
        
        confid = self.env['sh.import.base'].search([],limit=1)
        response = requests.get('''%s/api/public/resource.calendar?query={*,attendance_ids{*},global_leave_ids{*,resource_id{*}}}''' %(confid.base_url))
        response_json = response.json()  
        
        print("\n\n======response_json",response_json)   
        if response.status_code == 200:
            count=0
            for data in response_json['result']:
                
                #  ============= PREAPRE RESOURCE CALENDAR VALS FOR IMPORT THAT ==============
                
                resource_calendar_vals = confid.process_resource_calendar_data(data)
                # print("\n\n======resource_calendar_vals",resource_calendar_vals)
                domain = [('remote_resource_calendar_id', '=', data['id'])]
                find_resource_calendar = self.env['resource.calendar'].search(domain)
                    
                    # ============ CHECK IF RESOURCE CALENDAR EXIST OR NOT ===============
                    
                if find_resource_calendar:
                    find_resource_calendar.write(resource_calendar_vals)                            
                else:
                    self.env['resource.calendar'].create(resource_calendar_vals)  
                count += 1
                
            # ========= CREATE LOG FOR SUCCESSFULLY IMPORT UOM =================
                
            if count:
                vals = {
                    "name": self.name,
                    "state": "success",
                    "field_type": "res_calendar",
                    "error": "Resource Calendar Imported Successfully",
                    "datetime": datetime.now(),
                    "base_config_id": self.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)                       
                        
        # ========== CREATE LOG FOR ERROR WHICH IS  GENERATE DURING RESOURCE CALENDAR IMPORT  ==============

        else:
            vals = {
                "name": confid.name,
                "state": "error",
                "field_type": "res_calendar",
                "error": response.text,
                "datetime": datetime.now(),
                "base_config_id": confid.id,
                "operation": "import"
            }
            self.env['sh.import.base.log'].create(vals)

    def process_resource_calendar_data(self,data):
        calendar_vals={
            'remote_resource_calendar_id':data.get('id'),
            'display_name':data.get('display_name'),
            'except_from_half_day':data.get('except_from_half_day'),
            'hours_per_day':data.get('process_resource_calendar_datahours_per_day'),
            'name':data.get('name'),
            'sh_late_early_restriction':data.get('sh_late_early_restriction'),
            'timesheet_hrs':data.get('timesheet_hrs'),
            'tz':data.get('tz').get('sh_api_current_state'),
            'company_id':1
        }
        if data.get('attendance_ids'):
            attendance_list=[]
            for attendance in data.get('attendance_ids'):
                find_attendance=self.env['resource.calendar.attendance'].search([('remote_resource_calendar_attendance_id','=',attendance.get('id'))])
                if not find_attendance:
                    attendance_vals={
                        'remote_resource_calendar_attendance_id':attendance.get('id'),
                        'date_from':attendance.get('date_from') if attendance.get('date_from') else False,
                        'date_to':attendance.get('date_to') if attendance.get('date_to') else False,
                        'day_period':attendance.get('day_period').get('sh_api_current_state'),
                        'dayofweek':attendance.get('dayofweek').get('sh_api_current_state'),
                        'display_name':attendance.get('display_name'),
                        # 'display_type':attendance.get('display_type').get('sh_api_current_state'),
                        'high_priority':attendance.get('high_priority'),
                        'hour_from':attendance.get('hour_from'),
                        'hour_to':attendance.get('hour_to'),
                        'name':attendance.get('name'),
                        'sequence':attendance.get('sequence'),
                        'sh_break':attendance.get('sh_break'),
                        'sh_wroked_hours':attendance.get('sh_wroked_hours'),
                        'two_weeks_calendar':attendance.get('two_weeks_calendar'),
                        # 'week_type':attendance.get('week_type').get('sh_api_current_state'),
                        'two_weeks_calendar':attendance.get('two_weeks_calendar'),
                    } 
                    # if attendance.get('resource_id'):
                    #     domain = [('remote_resource_resource_id',
                    #        '=', attendance.get('resource_id').get('id'))]
                    #     find_resource = self.env['resource.resource'].search(domain)
                    #     resource_vals = self.prepare_resource_vals(attendance.get('resource_id'))
                    #     if find_resource:
                    #         find_resource.write(resource_vals)
                    #         attendance_vals['resource_id']=find_resource.id
                    #     else:
                    #         created_resource=self.env['resource.resource'].create(resource_vals)
                    #         attendance_vals['resource_id']=created_resource.id
                            
                    # print("\n\n\n======attendance_vals",attendance_vals)
                    attendance_list.append((0,0,attendance_vals))
            if attendance_list:
                calendar_vals['attendance_ids']=attendance_list   
                
                
                
        if data.get('global_leave_ids'):
            global_leave_list=[]
            for leave in data.get('global_leave_ids'):
                find_leave=self.env['resource.calendar.leaves'].search([('remote_resource_calendar_leaves_id','=',leave.get('id'))])
                if not find_leave:
                    global_leave_vals={
                        'remote_resource_calendar_leaves_id':leave.get('id'),
                        # 'date_from':leave.get('date_from') if leave.get('date_from') else False,
                        # 'date_to':leave.get('date_to') if leave.get('date_to') else False,
                        'display_name':leave.get('display_name'),
                        
                        'is_saturday_leave':leave.get('is_saturday_leave'),
                        'name':leave.get('name'),
                        'time_type':leave.get('time_type').get('sh_api_current_state'),
                        
                    } 
                    
                    if leave.get('date_from'):
                        date_time=datetime.strptime(leave.get('date_from'),'%Y-%m-%d-%H-%M-%S')
                        date_time=date_time.strftime('%Y-%m-%d %H:%M:%S')
                        global_leave_vals['date_from']=date_time
                        
                    if leave.get('date_to'):
                        date_time=datetime.strptime(leave.get('date_to'),'%Y-%m-%d-%H-%M-%S')
                        date_time=date_time.strftime('%Y-%m-%d %H:%M:%S')
                        global_leave_vals['date_to']=date_time
                    
                    if leave.get('holiday_id'):
                        domain = [('remote_leave_id', '=', leave['id'])]
                        find_leave = self.env['hr.leave'].search(domain)
                        if find_leave:
                            global_leave_vals['holiday_id']=find_leave.id   
                    
                    
                    if leave.get('resource_id'):
                        domain = [('remote_resource_resource_id',
                           '=', leave.get('resource_id'))]
                        find_resource = self.env['resource.resource'].search(domain)
                        # resource_vals = self.prepare_resource_vals(leave.get('resource_id'))
                        if find_resource:
                            # find_resource.write(resource_vals)
                            global_leave_vals['resource_id']=find_resource.id
                        # else:
                        #     created_resource=self.env['resource.resource'].create(resource_vals)
                        #     global_leave_vals['resource_id']=created_resource.id
                            
                    # print("\n\n\n======global_leave_vals",global_leave_vals)
                    global_leave_list.append((0,0,global_leave_vals))
            if global_leave_list:
                print("\n\n====global_leave_list",global_leave_list)
                calendar_vals['global_leave_ids']=global_leave_list   
                       
                
                
                
                
                
                
                
        return calendar_vals