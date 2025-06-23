
# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
import requests
import json
from datetime import datetime

class InheritImportBase(models.Model):
    _inherit = "sh.import.base"

    current_partner_page = fields.Integer("Current Partner Page",default=0)
    import_contacts = fields.Boolean("Import Contacts")

    sh_import_filter_partner = fields.Boolean("Import Filtered Product")
    sh_from_date_partner = fields.Datetime("From Date of Product")
    sh_to_date_partner = fields.Datetime("To Date Of Product")
    sh_import_partner_ids = fields.Char("Partner ids")

    json_data=fields.Char('')


    def import_partner_filtered_to_queue(self):
        ''' ========== Import Filtered Partners 
        between from date and end date ==================  '''
        confid = self.env['sh.import.base'].search([], limit=1)
        if confid.sh_import_filter_partner:
            response = requests.get('''%s/api/public/res.partner?query={id,write_date}&filter=[["write_date",">=","%s"],["write_date","<=","%s"],["company_id","=",1]]'''
                                    % (confid.base_url, str(confid.sh_from_date_partner), str(confid.sh_to_date_partner)))
            response_json = response.json()
            if response_json.get('result'):
                confid.sh_import_partner_ids = [r['id']
                                                for r in response_json.get('result')]
            
            else:
                confid.sh_import_partner_ids=False

    def import_partner_from_queue(self):
        ''' ========== Import partner  ==================  '''
        confid = self.env['sh.import.base'].search([],limit=1)
        if confid.sh_import_filter_partner and confid.sh_import_partner_ids:   
            partners = confid.sh_import_partner_ids.strip('][').split(',')

            if not partners[0]:
                confid.sh_import_partner_ids = False
                return False

            count=0
            failed=0
            failed_dict = {}
            print("\n\n=========partners[0:10]",partners[0:10])
            for partner in partners[0:50]:
                partner = partner.replace(" ",'')
                response = requests.get('%s/api/public/res.partner/%s?query={name,user_id,function,property_product_pricelist,partner_category_id{*},vat,title,ref,type,website,supplier,street,street2,city,state_id{name,code},country_id{name},zip,email,is_company,phone,mobile,id,company_type,customer,child_ids{name,title,ref,type,website,supplier,street,street2,city,state_id{name,code},country_id{name},zip,email,is_company,phone,mobile,id,company_type,customer,child_ids}}' %(confid.base_url,partner))
                if response.status_code==200:
                    response_json = response.json()
                    for data in response_json['result']:
                        try:
                            partner_vals = confid.process_contact_data(data)
                            domain = [('remote_res_partner_id', '=', data['id'])]
                            find_partner = self.env['res.partner'].search(domain)
                            print("\n\n\n",find_partner)
                            if find_partner:
                                find_partner.write(partner_vals)                            
                            elif 'name' in partner_vals and partner_vals['name']:
                                print("\n\n\n",partner_vals['name'])
                                self.env['res.partner'].create(partner_vals)
                            count += 1
                        except Exception as e:
                            failed_dict[partner] = e
                            failed += 1
                    confid.sh_import_partner_ids='['+', '.join([str(elem) for elem in partners[10:]])+']'
                else:
                    failed_dict[partner] = response.text
                    failed += 1
            if count > 0:
                self.create_log(field_type='customer', error="%s Contact Imported Successfully" % (count), state='success')
            if failed > 0:
                failed_dict['Total Failed'] = failed
                self.create_log(field_type='customer', error=failed_dict)

            confid.sh_import_partner_ids = '['+','.join(
                [str(elem) for elem in partners[50:]])+']'


    def import_contacts_cron(self):   
        confid = self.env['sh.import.base'].search([],limit=1)
        # confid.import_partner_from_queue()
        if confid.import_contacts:
            confid.current_partner_page += 1
            response = requests.get('%s/api/public/res.partner?query={name,user_id,function,property_product_pricelist,partner_category_id{*},vat,title,ref,type,website,supplier,street,street2,city,state_id{name,code},country_id{name},zip,email,is_company,phone,mobile,id,company_type,customer,child_ids{name,title,ref,type,website,supplier,street,street2,city,state_id{name,code},country_id{name},zip,email,is_company,phone,mobile,id,company_type,customer,child_ids}}&page_size=%s&page=%s' %(confid.base_url,confid.records_per_page,confid.current_partner_page))
            if response.status_code == 200:
                response_json = response.json()
                # ======= CHECK RECORD PER PAGE IS NOT EQUAL TO COUNT THEN IMPORT CONTACT FALSE =============
                
                if confid.records_per_page != response_json['count']:
                    confid.import_contacts = False
                    confid.current_partner_page = 0
                    
                count = 0
                failed = 0
                print("\n\n\n",len(response_json['result']))
                for data in response_json['result']:
                    
                    #  ============= PREAPRE CONTACT VALS FOR IMPORT CONTACT ==============
                    contact_vals = confid.process_contact_data(data)
                    domain = [('remote_res_partner_id', '=', data['id'])]
                    find_contact = self.env['res.partner'].search(domain)
                    # try:
                    print("\n ======= data['id']", data['id'],"=find_contact==",find_contact,data['name'])
                        # ============ CHECK IF PARTNER EXIST OR NOT ===============
                    # print("\n\n\n",contact_vals)
                    if find_contact:
                        
                        # =========== EXIST THEN UPDATE VALUES ===========
                        count += 1
                        find_contact.write(contact_vals)                            
                    else:
                        
                        # domain = [('login','=',data['email']),('name','=',data['name'])]
                        # check_user = self.env['res.users'].search(domain)
                        # if check_user and check_user.partner_id:
                        #     count += 1
                        #     print("\n\n\n\n\ oooooooooooooooooooooo",contact_vals)
                        #     check_user.partner_id.write(contact_vals)
                        # else:
                            # =========== ELSE CREATE PARTNER  ===========
                        create_contact=self.env['res.partner'].create(contact_vals)
                        print("===========create_contact",create_contact)  
                        count += 1
                                                    
                    # except Exception as e:
                        
                    #     # ========== CREATE EXCEPTION LOG ==============
                        
                    #     failed += 1
                    #     vals = {
                    #         "name": data['id'],
                    #         "error": e,
                    #         "import_json" : data,
                    #         "field_type": "customer",                           
                    #         "datetime": datetime.now(),
                    #         "base_config_id": confid.id,
                    #     }
                    #     self.env['sh.import.failed'].create(vals)  
                        
                # ========== CREATE LOG FOR SUCCESSFULLY IMPORT CUSTOMER  ==============
                         
                if count > 0:              
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "customer",
                        "error": "%s Contacts Imported Successfully" %(count - failed),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)
                
                # ========== CREATE LOG FOR FAILED CUSTOMER  ==============
                
                if failed > 0:
                    vals = {
                        "name": confid.name,
                        "state": "error",
                        "field_type": "customer",
                        "error": "%s Failed To Import" %(failed),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)

            # ========== CREATE LOG FOR ERROR WHICH IS  GENERATE DURING CUSTOMER IMPORT  ==============

            else:
                vals = {
                    "name": confid.name,
                    "state": "error",
                    "field_type": "customer",
                    "error": response.text,
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)

    
    def process_contact_data(self,contact):
        ''' ========== PREPARE VALUES FOR PARTNER =========   '''
        
        contact_vals = {
            'name' : contact.get('name'),
            'email' : contact.get('email'),
            'type' : contact.get('type')['sh_api_current_state'],
            'website' : contact.get('website'),
            'street' : contact.get('street'),
            'phone' : contact.get('phone'),
            'mobile' : contact.get('mobile'),
            'company_type' : contact.get('company_type')['sh_api_current_state'],
            'ref' : contact.get('ref'),
            'is_company' : contact.get('is_company'),
            'remote_res_partner_id' : contact.get('id'),
            'street2' : contact.get('street2'),
            'city' : contact.get('city'),
            'zip' : contact.get('zip'),
            'comment':contact.get('comment'),
            'function':contact.get('function'),
            'lang':'en_US',
            # 'vat' : contact.get('vat'),
        }      
        if contact.get('website_id'):
            contact_vals['website_id']=1

        # print("\n\n===========contact.get('user_id')",contact.get('user_id'))
        if contact.get('user_id') and contact.get('user_id')!=0:
            find_user=self.env['res.users'].search([('remote_res_user_id','=',contact.get('user_id'))])
            if find_user:
                print("\n\n=============find_user",find_user)
                contact_vals['user_id'] = find_user.id 
               
        if 'show_in_website' in contact and contact['show_in_website']:
            contact_vals.update({
                'show_in_website':contact.get('show_in_website'),
            })        
        if contact['state_id']:
            domain = [('name','=',contact['state_id']['name']),('name','=',contact['state_id']['code'])]
            find_state = self.env['res.country.state'].search(domain)
            if find_state:
                contact_vals['state_id'] = find_state.id

    
                
        if contact.get('property_product_pricelist'):
            find_pricelist=self.env['product.pricelist'].search([('remote_product_pricelist_id','=',contact.get('property_product_pricelist'))])
            if find_pricelist:
                contact_vals['property_product_pricelist']=find_pricelist.id

        if contact['country_id']:
            country_domain = [('name', '=', contact['country_id']['name'])]
            find_country = self.env['res.country'].search(country_domain)
            if find_country:
                contact_vals['country_id'] = find_country.id
                
        if contact['supplier']:
            contact_vals['supplier_rank'] = 1
            
        if contact['customer']:
            contact_vals['customer_rank'] = 1
        if contact.get('partner_category_id') and contact.get('partner_category_id').get('id') and contact.get('partner_category_id').get('id')!=0:
            domain=['|',('remote_partner_category_id','=',contact.get('partner_category_id').get('id')),('name','=',contact.get('partner_category_id').get('name'))]    
            find_partner_category=self.env['partner.category'].search(domain)
            if find_partner_category:
                contact_vals['partner_category_id']=find_partner_category.id              
            else:
                category_vals={
                    'remote_partner_category_id':contact.get('partner_category_id').get('id'),
                    'display_name':contact.get('partner_category_id').get('display_name'),
                    'from_invoice_amount':contact.get('partner_category_id').get('from_invoice_amount'),
                    'name':contact.get('partner_category_id').get('name'),
                    'sequence':contact.get('partner_category_id').get('sequence'),
                    'to_invoice_amount':contact.get('partner_category_id').get('to_invoice_amount'),
                }    
                created_category=self.env['partner.category'].create(category_vals)
                if created_category:
                    contact_vals['partner_category_id']=created_category.id 
                      
        # ============ PREAPRE PARTNER'S CHILD PARTNER'S DATA ==============
        if contact['child_ids']:
            child_list = []
            for child in contact['child_ids']:
                child_vals = self.process_contact_data(child)
                domain = [('remote_res_partner_id', '=', child['id'])]
                find_child = self.env['res.partner'].search(domain)
                if not find_child:
                    child_list.append((0,0,child_vals))
            contact_vals['child_ids'] = child_list
            
        return contact_vals
    
    def get_proper_vendor(self,vendor):
        ''' ========= CHECK IF VENDOR CREATED OR NOT IF CREATED THEN RETURN IT ELSE PREPARE VALUS AND CREATE IT THEN RETURN ===    '''
        
        domain = [('remote_res_partner_id', '=', vendor['id'])]
        find_vendor = self.env['res.partner'].search(domain)
        if find_vendor:
            return find_vendor
        else:
            vendor_vals = {
                'name' : vendor.get('name'),
                'email' : vendor.get('email'),
                'type' : vendor.get('type')['sh_api_current_state'],
                'website' : vendor.get('website'),
                'street' : vendor.get('street'),
                'phone' : vendor.get('phone'),
                'mobile' : vendor.get('mobile'),
                'company_type' : vendor.get('company_type')['sh_api_current_state'],
                'ref' : vendor.get('ref'),
                'is_company' : vendor.get('is_company'),
                'remote_res_partner_id' : vendor.get('id'),
            }
            if vendor['supplier']:
                vendor_vals['supplier_rank'] = 1
            create_vendor = self.env['res.partner'].create(vendor_vals)
            return create_vendor