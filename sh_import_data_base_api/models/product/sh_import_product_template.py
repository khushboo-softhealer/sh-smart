# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
import requests
from datetime import datetime
product_temp_max_ud = False


class InheritImportBase(models.Model):
    _inherit = "sh.import.base"

    import_product = fields.Boolean("Import Products")
    sh_import_filter_product = fields.Boolean("Import Filtered Product")
    sh_from_date_product = fields.Datetime("From Date of Product")
    sh_to_date_product = fields.Datetime("To Date Of Product")
    sh_import_product_ids = fields.Char("Product ids")

    sh_product_starting_from = fields.Integer(
        string='Starting From ', default=0)
    records_per_page_product = fields.Integer(
        string='Records Per Page', default=0)
    sh_product_upto = fields.Integer(string='Upto ', default=0)
    json = fields.Text()

    def import_product_filtered_to_queue(self):
        ''' ========== Import Filtered Product 
        between from date and end date ==================  '''
        confid = self.env['sh.import.base'].search([], limit=1)
        if confid.sh_import_filter_product:
            response = requests.get('''%s/api/public/product.template?query={id,write_date}&filter=[["write_date",">=","%s"],["write_date","<=","%s"]]'''
                                    % (confid.base_url, str(confid.sh_from_date_product), str(confid.sh_to_date_product)))
            response_json = response.json()
            if response_json.get('result'):
                confid.sh_import_product_ids = [r['id'] for r in response_json.get('result')]


    def import_product_from_queue(self):

        confid = self.env['sh.import.base'].search([], limit=1)

        if confid.sh_import_filter_product:
            products = confid.sh_import_product_ids.strip('][').split(', ')
            count = 0
            fail = 0
            for product in products[0:1]:

                response = requests.get('''%s/api/public/product.template?query={*,license{*},license_duplicate{*},tag_ids{*},tag_ids_duplicate{*},git_repo{*},sh_scale_ids{*},supported_browsers{*},supported_browsers_duplicate{*},required_apps_duplicate{*},sh_blog_post_ids{*},sh_blog_post_ids_duplicate{*},sh_edition_ids{*},sh_edition_ids_duplicate{*},individual_modules{*},related_video{*},related_video_duplicate{*},required_apps{*},product_change_log_id{*},depends{*},depends_duplicate{*},attribute_line_ids{attribute_id{id,name},value_ids{id,name,is_custom}},taxes_id{name,amount,type_tax_use},supplier_taxes_id{name,amount,type_tax_use}, seller_ids{*,name{name,title,ref,type,website,supplier,street,email,is_company,phone,mobile,id,company_type}},website_meta_description,website_meta_keywords,website_meta_og_img,website_meta_title}
                &filter=[["id", "=", %s],"|",["active","=",true],["active","=",false],["company_id","=",1]]''' % (
                    confid.base_url, int(product)))
                if response.status_code == 200:
                    response_json = response.json()
                    if response_json.get('error') != '0':
                        confid.create_log(field_type='product',
                                        error=response_json)
                        return False

                    # ========================================
                    # Arrange Ids in Assending order.
                    # ========================================
                    if response_json.get('result'):
                        response_json['result'] = sorted(
                            response_json['result'], key=lambda d: d['id'])

                    # ========================================
                    # For Maintain Ids
                    # ========================================
                    last_rec = self.env['product.template'].search(
                        [], order='id desc', limit=1)
                    if last_rec.id < confid.sh_product_starting_from:
                        for ind in range(last_rec.id+1, confid.sh_product_starting_from+1):
                            confid.create_product_fake_rec(ind)

                    
                    # for ind in range(60, 80):
                    if response_json['result']:
                        # break
                        if int(product) == response_json['result'][0].get('id'):
                            product_dic = response_json['result'][0]

                            try:
                                if not product_dic.get('id'):
                                    confid.create_product_fake_rec(product)
                                    continue
                                product_tempalte_vals = confid.process_product_data(
                                    product_dic)
                                domain = [('id', '=', product_dic['id'])]
                                product_tmpl_obj = self.env['product.template'].search(
                                    domain, limit=1)
                                if product_tempalte_vals.get('detailed_type') != 'product':
                                    if product_tmpl_obj:
                                        count += 1
                                        product_tmpl_obj.write(
                                            product_tempalte_vals)
                                        if product_dic.get('seller_ids'):
                                            self.process_seller_ids(
                                                product_dic['seller_ids'], product_tmpl_obj)
                                    else:
                                        count += 1
                                        product_tmpl_obj = self.env['product.template'].create(
                                            product_tempalte_vals)
                                        if product_dic.get('seller_ids'):
                                            self.process_seller_ids(
                                                product_dic['seller_ids'], product_tmpl_obj)
                                    if product_tmpl_obj:
                                        if product_dic.get('attribute_line_ids'):
                                            self.process_varient_product(
                                                product_dic['product_variant_ids'], product_dic['attribute_line_ids'], product_tmpl_obj, confid.base_url)
                                        else:
                                            product_product_obj = self.env['product.product'].sudo().search(
                                                [('product_tmpl_id', '=', product_tmpl_obj.id)])
                                            if len(product_product_obj) == 1:
                                                product_product_obj.write({
                                                    'remote_product_product_id': product_dic['product_variant_ids'][0]
                                                })
                                else:
                                    confid.create_product_fake_rec(product)
                                response_json['result'].pop(0)

                            except Exception as e:
                                fail += 1
                                self.create_fail_log(
                                    name=product_dic.get('id'),
                                    field_type='product',
                                    error=e,
                                    import_json=product_dic,
                                )
                                confid.create_product_fake_rec(product)
                                response_json['result'].pop(0)
                        else:
                            confid.create_product_fake_rec(product)
                            # response_json['result'].pop(0)
                    else:
                        confid.create_product_fake_rec(product)
                        # response_json['result'].pop(0)
            confid.sh_import_product_ids='['+', '.join([str(elem) for elem in products[1:]])+']'
            if count > 0:
                vals = {
                    "name": confid.name,
                    "state": "success",
                    "field_type": "product",
                    "error": "%s Product Update Successfully" % (count),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)

            if fail > 0:
                vals = {
                    "name": confid.name,
                    "state": "error",
                    "field_type": "product",
                    "error": "%s Failed To Import" % (fail),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)

            else:
                vals = {
                    "name": confid.name,
                    "state": "error",
                    "field_type": "product",
                    "error": response.text,
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)



    def create_product_fake_rec(self, current_id):
        '''create fake record'''
        domain = [('id', '=', current_id)]
        find_product = self.env['product.template'].search(domain)
        if not find_product:
            vals = {
                'name': 'Fake Records',
            }
            find_product = self.env['product.template'].create(vals)

    def import_product_cron(self):

        confid = self.env['sh.import.base'].search([], limit=1)

        if confid.import_product:

            global product_temp_max_ud
            # ==================================================
            # Find product_temp_max_ud
            # ==================================================
            if not product_temp_max_ud:
                response = requests.get(
                    '%s/api/public/product.template?query={id}&filter=[["company_id","=",1]]' % (confid.base_url))
                if response.status_code == 200:
                    response_json = response.json()
                    if response_json.get('error') != '0':
                        confid.create_log(
                            field_type='product', error=response_json)
                        return False
                    # Find Max Id
                    if response_json.get('result'):
                        product_temp_max_ud = 0
                        for id_dict in response_json['result']:
                            if id_dict['id'] > product_temp_max_ud:
                                product_temp_max_ud = id_dict['id']

            # ==================================================
            # Set Default Id's Range (If Not Provided.)
            # ==================================================
            if confid.records_per_page_product == 0:
                confid.records_per_page_product = 20

            # ==================================================
            # Update Ids Range (From And To)
            # ==================================================
            confid.sh_product_starting_from = confid.sh_product_upto
            confid.sh_product_upto = confid.sh_product_starting_from + \
                confid.records_per_page_product

            # ========================================
            # Reset Configurations For Blog
            # ========================================
            if confid.sh_product_starting_from >= product_temp_max_ud:
                self.create_log(field_type='product',
                                error="Starting From is Out of range in v12's Id!")
                return False

            # ========================================
            # If Upto is Greater Than MAx ID
            # ========================================
            if confid.sh_product_upto >= product_temp_max_ud:
                confid.sh_product_upto = product_temp_max_ud

            confid.current_import_page += 1
            response = requests.get('''%s/api/public/product.template?query={*,license{*},license_duplicate{*},tag_ids{*},tag_ids_duplicate{*},git_repo{*},sh_scale_ids{*},supported_browsers{*},supported_browsers_duplicate{*},required_apps_duplicate{*},sh_blog_post_ids{*},sh_blog_post_ids_duplicate{*},sh_edition_ids{*},sh_edition_ids_duplicate{*},individual_modules{*},related_video{*},related_video_duplicate{*},required_apps{*},product_change_log_id{*},depends{*},depends_duplicate{*},attribute_line_ids{attribute_id{id,name},value_ids{id,name,is_custom}},taxes_id{name,amount,type_tax_use},supplier_taxes_id{name,amount,type_tax_use}, seller_ids{*,name{name,title,ref,type,website,supplier,street,email,is_company,phone,mobile,id,company_type}},website_meta_description,website_meta_keywords,website_meta_og_img,website_meta_title}
            &filter=[["id", ">", %s], ["id", "<=", %s],"|",["active","=",true],["active","=",false],["company_id","=",1]]''' % (
                confid.base_url, confid.sh_product_starting_from, confid.sh_product_upto))
            # response = requests.get('%s/api/public/product.template?query={*,license{*},license_duplicate{*},tag_ids{*},tag_ids_duplicate{*},git_repo{*},sh_scale_ids{*},supported_browsers{*},supported_browsers_duplicate{*},required_apps_duplicate{*},sh_blog_post_ids{*},sh_blog_post_ids_duplicate{*},sh_edition_ids{*},sh_edition_ids_duplicate{*},individual_modules{*},related_video{*},related_video_duplicate{*},required_apps{*},product_change_log_id{*},depends{*},depends_duplicate{*},attribute_line_ids{attribute_id{id,name},value_ids{id,name,is_custom}},taxes_id{name,amount,type_tax_use},supplier_taxes_id{name,amount,type_tax_use}, seller_ids{*,name{name,title,ref,type,website,supplier,street,email,is_company,phone,mobile,id,company_type}},website_meta_description,website_meta_keywords,website_meta_og_img,website_meta_title}&filter=[["id", ">", "60"], ["id", "<=", "80"]]' % (
            #     confid.base_url))
            if response.status_code == 200:
                # self.json = response.json()
                # return
                response_json = response.json()
                if response_json.get('error') != '0':
                    confid.create_log(field_type='product',
                                      error=response_json)
                    return False

                # ========================================
                # Arrange Ids in Assending order.
                # ========================================
                if response_json.get('result'):
                    response_json['result'] = sorted(
                        response_json['result'], key=lambda d: d['id'])

                # ========================================
                # For Maintain Ids
                # ========================================
                last_rec = self.env['product.template'].search(
                    [], order='id desc', limit=1)
                if last_rec.id < confid.sh_product_starting_from:
                    for ind in range(last_rec.id+1, confid.sh_product_starting_from+1):
                        confid.create_product_fake_rec(ind)

                count = 0
                fail = 0
                confid.json=response_json['result']
                for ind in range(confid.sh_product_starting_from+1, confid.sh_product_upto+1):
                # for ind in range(60, 80):
                    if response_json['result']:
                        # break
                        if ind == response_json['result'][0].get('id'):
                            product_dic = response_json['result'][0]

                            try:
                                if not product_dic.get('id'):
                                    confid.create_product_fake_rec(ind)
                                    continue
                                product_tempalte_vals = confid.process_product_data(
                                    product_dic)
                                domain = [('id', '=', product_dic['id'])]
                                product_tmpl_obj = self.env['product.template'].search(
                                    domain, limit=1)
                                if product_tempalte_vals.get('detailed_type') != 'product':
                                    if product_tmpl_obj:
                                        count += 1
                                        product_tmpl_obj.write(
                                            product_tempalte_vals)
                                        if product_dic.get('seller_ids'):
                                            self.process_seller_ids(
                                                product_dic['seller_ids'], product_tmpl_obj)
                                    else:
                                        count += 1
                                        product_tmpl_obj = self.env['product.template'].create(
                                            product_tempalte_vals)
                                        if product_dic.get('seller_ids'):
                                            self.process_seller_ids(
                                                product_dic['seller_ids'], product_tmpl_obj)
                                    if product_tmpl_obj:
                                        if product_dic.get('attribute_line_ids'):
                                            self.process_varient_product(
                                                product_dic['product_variant_ids'], product_dic['attribute_line_ids'], product_tmpl_obj, confid.base_url)
                                        else:
                                            product_product_obj = self.env['product.product'].sudo().search(
                                                [('product_tmpl_id', '=', product_tmpl_obj.id)])
                                            if len(product_product_obj) == 1:
                                                product_product_obj.write({
                                                    'remote_product_product_id': product_dic['product_variant_ids'][0]
                                                })
                                else:
                                    confid.create_product_fake_rec(ind)
                                response_json['result'].pop(0)

                            except Exception as e:
                                fail += 1
                                self.create_fail_log(
                                    name=product_dic.get('id'),
                                    field_type='product',
                                    error=e,
                                    import_json=product_dic,
                                )
                                confid.create_product_fake_rec(ind)
                                response_json['result'].pop(0)
                        else:
                            confid.create_product_fake_rec(ind)
                            # response_json['result'].pop(0)
                    else:
                        confid.create_product_fake_rec(ind)
                        # response_json['result'].pop(0)
                if count > 0:
                    vals = {
                        "name": confid.name,
                        "state": "success",
                        "field_type": "product",
                        "error": "%s Product Imported Successfully" % (count),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)

                if fail > 0:
                    vals = {
                        "name": confid.name,
                        "state": "error",
                        "field_type": "product",
                        "error": "%s Failed To Import" % (fail),
                        "datetime": datetime.now(),
                        "base_config_id": confid.id,
                        "operation": "import"
                    }
                    self.env['sh.import.base.log'].create(vals)

            else:
                vals = {
                    "name": confid.name,
                    "state": "error",
                    "field_type": "product",
                    "error": response.text,
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)

            # ========================================
            # Reset All Configurations For Blog
            # ========================================
            if confid.sh_product_upto == product_temp_max_ud:
                product_temp_max_ud = False
                confid.import_product = False
                confid.sh_product_starting_from = 0
                confid.sh_product_upto = 0

    def process_product_data(self, data):
        product_vals = {
            'name': data.get('name', ''),
            'description': data.get('description', ''),
            'description_purchase': data.get('description_purchase', ''),
            'description_sale': data.get('description_sale', ''),
            'list_price': data.get('list_price', ''),
            'standard_price': data.get('standard_price', ''),
            'volume': data.get('volume', 0.0),
            'weight': data.get('weight', 0.0),
            'sale_ok': data.get('sale_ok'),
            'purchase_ok': data.get('purchase_ok'),
            'color': data.get('color'),
            'barcode': data.get('barcode', ''),
            'default_code': data.get('default_code'),
            'detailed_type': data['type']['sh_api_current_state'] if data.get('type') and data.get('type').get('sh_api_current_state') else 'consu',
            'invoice_policy': data['invoice_policy']['sh_api_current_state'],
            'expense_policy': data['expense_policy']['sh_api_current_state'],
            'active': True,
            'sh_active' : data['active'],
            'remote_product_template_id': data['id'],
            'pricelist_exception': data.get('pricelist_exception', False),
            'excluded_from_disocunt': data.get('excluded_from_disocunt', False),
            'website_meta_description': data.get('website_meta_description', False),
            'website_meta_keywords': data.get('website_meta_keywords', False),
            'website_meta_og_img': data.get('website_meta_og_img', False),
            'website_meta_title': data.get('website_meta_title', False),
        }
        if data.get('sh_task_created'):
            product_vals.update({
                'sh_task_created': data.get('sh_task_created')
            })
        if data.get('warning_removed'):
            product_vals.update({
                'warning_removed': data.get('warning_removed')
            })
        if data.get('request_for_quotation_duplicate'):
            product_vals.update({
                'request_for_quotation_duplicate': data.get('request_for_quotation_duplicate')
            })
        if data.get('request_for_quotation'):
            product_vals.update({
                'request_for_quotation': data.get('request_for_quotation')
            })
        if data.get('ready_for_release'):
            product_vals.update({
                'ready_for_release': data.get('ready_for_release')
            })
        if data.get('qty_show_duplicate'):
            product_vals.update({
                'qty_show_duplicate': data.get('qty_show_duplicate')
            })
        if data.get('qty_show'):
            product_vals.update({
                'qty_show': data.get('qty_show')
            })
        if data.get('not_unique_product'):
            product_vals.update({
                'not_unique_product': data.get('not_unique_product')
            })
        if data.get('multi_website'):
            product_vals.update({
                'multi_website': data.get('multi_website')
            })
        if data.get('multi_language'):
            product_vals.update({
                'multi_language': data.get('multi_language')
            })
        if data.get('multi_company'):
            product_vals.update({
                'multi_company': data.get('multi_company')
            })
        if data.get('is_support_product'):
            product_vals.update({
                'is_support_product': data.get('is_support_product')
            })
        if data.get('comment'):
            product_vals.update({
                'comment': data.get('comment')
            })
        if data.get('claim_created'):
            product_vals.update({
                'claim_created': data.get('claim_created')
            })
        if data.get('check_down_version'):
            product_vals.update({
                'check_down_version': data.get('check_down_version')
            })
        if data.get('banner'):
            product_vals.update({
                'banner': data.get('banner')
            })
        if data.get('warning_removed'):
            product_vals.update({
                'warning_removed': data.get('warning_removed')
            })
        if data.get('git_hub_url'):
            product_vals.update({
                'git_hub_url': data.get('git_hub_url')
            })
        if data.get('live_demo'):
            product_vals.update({
                'live_demo': data.get('live_demo')
            })
        if data.get('live_demo_duplicate'):
            product_vals.update({
                'live_demo_duplicate': data.get('live_demo_duplicate')
            })
        if data.get('odoo_url'):
            product_vals.update({
                'odoo_url': data.get('odoo_url')
            })
        if data.get('product_version'):
            product_vals.update({
                'product_version': data.get('product_version')
            })
        if data.get('product_version_duplicate'):
            product_vals.update({
                'product_version_duplicate': data.get('product_version_duplicate')
            })
        if data.get('sh_technical_name'):
            product_vals.update({
                'sh_technical_name': data.get('sh_technical_name')
            })
        if data.get('soft_url'):
            product_vals.update({
                'soft_url': data.get('soft_url')
            })
        if data.get('user_guide'):
            product_vals.update({
                'user_guide': data.get('user_guide')
            })
        if data.get('module_last_updated_date'):
            product_vals.update({
                'module_last_updated_date': data.get('module_last_updated_date')
            })
        if data.get('released_date'):
            product_vals.update({
                'released_date': data.get('released_date')
            })
        if data.get('released_date_duplicate'):
            product_vals.update({
                'released_date_duplicate': data.get('released_date_duplicate')
            })
        if data.get('euro_price'):
            product_vals.update({
                'euro_price': data.get('euro_price')
            })
        if data.get('euro_price_duplicate'):
            product_vals.update({
                'euro_price_duplicate': data.get('euro_price_duplicate')
            })
        if data.get('pylint_score'):
            product_vals.update({
                'pylint_score': data.get('pylint_score')
            })
        if data.get('sh_features'):
            product_vals.update({
                'sh_features': data.get('sh_features')
            })
        if data.get('sh_features_duplicate'):
            product_vals.update({
                'sh_features_duplicate': data.get('sh_features_duplicate')
            })
        if data.get('website_description'):
            product_vals.update({
                'website_description': data.get('website_description')
            })
        if data.get('website_description_duplicate'):
            product_vals.update({
                'website_description_duplicate': data.get('website_description_duplicate')
            })
        if data.get('sh_product_counter'):
            product_vals.update({
                'sh_product_counter': data.get('sh_product_counter')
            })
        if data.get('index_state').get('sh_api_current_state'):
            product_vals.update({
                'index_state': data.get('index_state').get('sh_api_current_state')
            })
        if data.get('status').get('sh_api_current_state'):
            product_vals.update({
                'status': data.get('status').get('sh_api_current_state')
            })

        if data.get('product_change_log_id'):
            product_change_log_id = self.process_product_change_log_data(
                data.get('product_change_log_id'))
            if product_change_log_id:
                product_vals.update({
                    'product_change_log_id': product_change_log_id,
                })

        if data.get('last_update_by'):
            if data.get('last_update_by') != 0:
                domain_by_id = [('remote_res_user_id', '=',
                                 data.get('last_update_by'))]
                find_user_id = self.env['res.users'].search(domain_by_id)
                if find_user_id:
                    product_vals.update({'last_update_by': find_user_id.id})

        if data.get('resposible_user_id'):
            if data.get('resposible_user_id') != 0:
                domain_by_id = [('remote_res_user_id', '=',
data.get('resposible_user_id'))]
                find_user_id = self.env['res.users'].search(domain_by_id)
                if find_user_id:
                    product_vals.update({'resposible_user_id': find_user_id.id})



        if data.get('copyright_claim_user'):
            if data.get('copyright_claim_user') != 0:
                domain_by_id = [('remote_res_user_id', '=',data.get('copyright_claim_user'))]
                find_user_id = self.env['res.users'].search(domain_by_id)
                if find_user_id:
                    product_vals.update({'copyright_claim_user': find_user_id.id})

        if data.get('migrated_by'):
            if data.get('migrated_by') != 0:
                domain_by_id = [('remote_res_user_id', '=', data.get('migrated_by'))]
                find_user_id = self.env['res.users'].search(domain_by_id)
                if find_user_id:
                    product_vals.update({'migrated_by': find_user_id.id})

        if data.get('other_responsible_users'):
            other_responsible_users = []
            for f_user in data.get('other_responsible_users'):
                if f_user and f_user != 0:
                    domain_by_id = [('remote_res_user_id', '=', f_user)]
                    find_user_id = self.env['res.users'].search(domain_by_id)
                    # ========== SEARCH USER BY ID OR BY NAME IF EXIST THEN RETURN ELSE CREATE USE AND RETURN IT =====
                    if find_user_id:
                        other_responsible_users.append(find_user_id.id)

            if other_responsible_users:
                product_vals.update(
                    {'other_responsible_users': other_responsible_users})

        if data.get('responsible_user') and data.get('responsible_user') != 0:
            domain_by_id = [('remote_res_user_id', '=', data.get('responsible_user'))]
            find_user_id = self.env['res.users'].search(domain_by_id)
            if find_user_id:
                product_vals.update({'responsible_user': find_user_id.id})

        # if data.get('responsible_user_id') and data.get('responsible_user_id') != 0:
        #     domain_by_id = [
        #         ('remote_res_user_id', '=', data.get('responsible_user_id'))]
        #     find_user_id = self.env['res.users'].search(domain_by_id)
        #     if find_user_id:
        #         product_vals.update({'responsible_user_id': find_user_id.id})

        if data.get('tested_by'):
            if data.get('tested_by'):
                if data.get('tested_by') != 0:
                    domain_by_id = [
                        ('remote_res_user_id', '=', data.get('tested_by'))]
                    find_user_id = self.env['res.users'].search(domain_by_id)
            if find_user_id:
                product_vals.update({'tested_by': find_user_id.id})

        if data.get('depends'):
            depends_list = []
            for depend in data.get('depends'):
                if depend['id'] != 0:
                    domain = [('remote_sh_depends_id', '=', depend['id'])]
                    find_depend = self.env['sh.depends'].search(domain)
                    if find_depend:
                        depends_list.append(find_depend.id)
                    else:
                        depend_vals = {
                            'remote_sh_depends_id': depend['id'],
                            'display_name': depend['display_name'],
                            'name': depend['name'],
                            'technical_name': depend['technical_name'],
                        }
                        create_depend = self.env['sh.depends'].create(
                            depend_vals)
                        if create_depend:
                            depends_list.append(create_depend.id)
            if depends_list:
                product_vals.update({'depends': depends_list})
        if data.get('depends_duplicate'):
            depends_list = []
            for depend in data.get('depends_duplicate'):
                if depend['id'] != 0:
                    domain = [('remote_sh_depends_id', '=', depend['id'])]
                    find_depend = self.env['sh.depends'].search(domain)
                    if find_depend:
                        depends_list.append(find_depend.id)
                    else:
                        depend_vals = {
                            'remote_sh_depends_id': depend['id'],
                            'display_name': depend['display_name'],
                            'name': depend['name'],
                            'technical_name': depend['technical_name'],
                        }
                        create_depend = self.env['sh.depends'].create(
                            depend_vals)
                        if create_depend:
                            depends_list.append(create_depend.id)
            if depends_list:
                product_vals.update({'depends_duplicate': depends_list})
        if data.get('required_apps'):
            required_apps = []
            for required_app in data.get('required_apps'):
                if required_app['id'] != 0 and required_app['name'] != '' and required_app['technical_name'] != '':
                    domain = [('remote_sh_required_apps_id',
                               '=', required_app['id'])]
                    required_app_obj = self.env['sh.required.apps'].search(
                        domain)
                    if required_app_obj:
                        required_apps.append(required_app_obj.id)
                    else:
                        required_app_vals = {
                            'name': required_app['name'],
                            'technical_name': required_app['technical_name'],
                            'remote_sh_required_apps_id': required_app['id'],
                        }
            if required_apps:
                product_vals.update({'required_apps': required_apps})
        if data.get('required_apps_duplicate'):
            required_apps = []
            for required_app in data.get('required_apps_duplicate'):
                if required_app['id'] and required_app['id'] != 0 and required_app['name'] != '' and required_app['technical_name'] != '':
                    domain = [('remote_sh_required_apps_id',
                               '=', required_app['id'])]
                    required_app_obj = self.env['sh.required.apps'].search(
                        domain)
                    if required_app_obj:
                        required_apps.append(required_app_obj.id)
                    else:
                        required_app_vals = {
                            'name': required_app['name'],
                            'technical_name': required_app['name'],
                            'remote_sh_required_apps_id': required_app['id'],
                        }
                        required_app_obj = self.env['sh.required.apps'].create(
                            required_app_vals)
                        if required_app_obj:
                            required_apps.append(required_app_obj.id)
            if required_apps:
                product_vals.update({'required_apps_duplicate': required_apps})

        if data.get('sh_edition_ids'):
            edition_ids = []
            for edition in data.get('sh_edition_ids'):
                if edition['id'] != 0:
                    domain = [('remote_sh_edition_id', '=', edition['id'])]
                    edition_obj = self.env['sh.edition'].search(domain)
                    if edition_obj:
                        edition_ids.append((edition_obj.id))

                    else:
                        edition_vals = {
                            'name': edition['name'],
                            'active': edition['active'],
                            'sh_display_in_frontend': edition['sh_display_in_frontend'],
                            'remote_sh_edition_id': edition['id'],
                        }
                        edition_obj = self.env['sh.edition'].create(
                            edition_vals)
                        if edition_obj:
                            edition_ids.append(edition_obj.id)
            if edition_ids:
                product_vals.update({'sh_edition_ids': edition_ids})
        if data.get('sh_edition_ids_duplicate'):
            edition_ids = []
            for edition in data.get('sh_edition_ids_duplicate'):
                if edition['id'] != 0:
                    domain = [('remote_sh_edition_id', '=', edition['id'])]
                    edition_obj = self.env['sh.edition'].search(domain)
                    if edition_obj:
                        edition_ids.append(edition_obj.id)

                    else:
                        edition_vals = {
                            'name': edition['name'],
                            'active': edition['active'],
                            'sh_display_in_frontend': edition['sh_display_in_frontend'],
                            'remote_sh_edition_id': edition['id'],
                        }
                        edition_obj = self.env['sh.edition'].create(
                            edition_vals)
                        if edition_obj:
                            edition_ids.append(edition_obj.id)
            if edition_ids:
                product_vals.update({'sh_edition_ids_duplicate': edition_ids})



        if data.get('sh_scale_ids') and data.get('sh_scale_ids').get('id') and data.get('sh_scale_ids').get('id')!=0 :
            find_scale=self.env['sh.scale'].search([('remote_sh_scale_id','=',data.get('sh_scale_ids').get('id')),('name','=',data.get('sh_scale_ids').get('name'))],limit=1)
            if find_scale:
                product_vals.update({'sh_scale_ids': find_scale.id})    

            else:
                scale_vals = {
                    'name': data.get('sh_scale_ids')['name'],
                    'days': data.get('sh_scale_ids')['days'],
                    'remote_sh_scale_id': data.get('sh_scale_ids')['id'],
                }
                scale_id = self.env['sh.scale'].create(scale_vals)
                product_vals.update({'sh_scale_ids': scale_id.id}) 


        if data.get('public_categ_ids'):
            categ_list=[]
            for categ in data.get('public_categ_ids'):
                if categ and categ!=0:
                    find_categ=self.env['product.public.category'].search([('remote_product_public_categ_id','=',categ)])
                    if find_categ:
                        categ_list.append((4,find_categ.id))                    
            product_vals.update({'public_categ_ids': categ_list})

    
        if data.get('supported_browsers'):
            support_ids = []
            for support in data.get('supported_browsers'):
                if support['id'] != 0:
                    domain = [
                        ('remote_product_browsers_id', '=', support['id'])]
                    support_obj = self.env['product.browsers'].search(domain)
                    if support_obj:
                        support_ids.append(support_obj.id)

                    else:
                        support_vals = {
                            'name': support['name'],
                            'remote_product_browsers_id': support['id'],
                        }
                        support_obj = self.env['product.browsers'].create(
                            support_vals)
                        if support_obj:
                            support_ids.append(support_obj.id)
            if support_ids:
                product_vals.update({'supported_browsers': support_ids})

        if data.get('supported_browsers_duplicate'):
            support_ids = []
            for support in data.get('supported_browsers_duplicate'):
                domain = [('remote_product_browsers_id', '=', support['id'])]
                support_obj = self.env['product.browsers'].search(domain)
                if support_obj:
                    support_ids.append(support_obj.id)

                else:
                    support_vals = {
                        'name': support['name'],
                        'remote_product_browsers_id': support['id'],
                    }
                    support_obj = self.env['product.browsers'].create(
                        support_vals)
                    if support_obj:
                        support_ids.append(support_obj.id)
            if support_ids:
                product_vals.update(
                    {'supported_browsers_duplicate': support_ids})
        if data.get('tag_ids'):
            tag_ids = []
            for tag in data.get('tag_ids'):
                if tag['id'] != 0:
                    domain = [('remote_product_tags_id', '=', tag['id'])]
                    tag_obj = self.env['product.tags'].search(domain)
                    if tag_obj:
                        tag_ids.append(tag_obj.id)

                    else:
                        tag_vals = {
                            'name': tag['name'],
                            'remote_product_tags_id': tag['id'],
                        }
                        tag_obj = self.env['product.tags'].create(tag_vals)
                        if tag_obj:
                            tag_ids.append(tag_obj.id)
            if tag_ids:
                product_vals.update({'tag_ids': tag_ids})

        if data.get('tag_ids_duplicate'):
            tag_ids = []
            for tag in data.get('tag_ids_duplicate'):
                if tag['id'] != 0:
                    domain = [('remote_product_tags_id', '=', tag['id'])]
                    tag_obj = self.env['product.tags'].search(domain)
                    if tag_obj:
                        tag_ids.append(tag_obj.id)

                    else:
                        tag_vals = {
                            'name': tag['name'],
                            'remote_product_tags_id': tag['id'],
                        }
                        tag_obj = self.env['product.tags'].create(tag_vals)
                        if tag_obj:
                            tag_ids.append(tag_obj.id)
            if tag_ids:
                product_vals.update({'tag_ids_duplicate': tag_ids})

        if data.get('license'):
            license_obj = self.env['sh.license']
            if data.get('license'):
                if data.get('license')['id'] != 0:
                    domain = [('remote_sh_license_id', '=',
                               data.get('license')['id'])]
                    license_obj = self.env['sh.license'].search(
                        domain, limit=1)
                    if not license_obj:
                        license_vals = {
                            'name': data.get('license')['name'],
                            'remote_sh_license_id': data.get('license')['id'],
                        }
                        license_obj = self.env['sh.license'].create(
                            license_vals)
            if license_obj:
                product_vals.update({'license': license_obj.id})

        if data.get('license_duplicate'):
            # license_obj = self.env['sh.license']
            if data.get('license_duplicate') and data.get('license_duplicate')['id'] != 0:
                domain = [('remote_sh_license_id', '=',
                           data.get('license_duplicate')['id'])]
                license_obj = self.env['sh.license'].search(domain, limit=1)
                if not license_obj:
                    license_vals = {
                        'name': data.get('license_duplicate')['name'],
                        'remote_sh_license_id': data.get('license_duplicate')['id'],
                    }
                    license_obj = self.env['sh.license'].create(license_vals)
                if license_obj:
                    product_vals.update({'license_duplicate': license_obj.id})

        if data.get('git_repo') and data.get('git_repo')['id'] != 0:
            domain = [('remote_sh_git_repo_id', '=',
                       data.get('git_repo')['id'])]
            find_git_repo = self.env['sh.git.repo'].search(domain)
            if find_git_repo:
                product_vals.update({'git_repo': find_git_repo.id})
            else:
                git_repo_vals = {
                    'remote_sh_git_repo_id': data.get('git_repo')['id'],
                    'display_name': data.get('git_repo')['display_name'],
                    'name': data.get('git_repo')['name'],
                    'repo_link': data.get('git_repo')['repo_link'],
                }
                if data.get('git_repo').get('responsible_user'):
                    domain_by_id = [
                        ('remote_res_user_id', '=', data['git_repo']['responsible_user'])]
                    find_user_id = self.env['res.users'].search(domain_by_id)

                    # ========== SEARCH USER BY ID OR BY NAME IF EXIST THEN RETURN ELSE CREATE USE AND RETURN IT =====
                    if find_user_id:
                        git_repo_vals['responsible_user'] = find_user_id.id

                create_git_repo = self.env['sh.git.repo'].create(git_repo_vals)
                if create_git_repo:
                    product_vals.update({'git_repo': create_git_repo.id})

        domain = [('remote_product_category_id', '=', data['categ_id'])]
        find_category = self.env['product.category'].search(domain, limit=1)
        if find_category:
            product_vals['categ_id'] = find_category.id
        if data['taxes_id']:
            tax_list = self.process_tax(data['taxes_id'])
            if tax_list:
                product_vals['taxes_id'] = tax_list
        if data['supplier_taxes_id']:
            supplier_tax_list = self.process_tax(data['supplier_taxes_id'])
            if supplier_tax_list:
                product_vals['supplier_taxes_id'] = supplier_tax_list
        return product_vals
