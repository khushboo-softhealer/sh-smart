# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models
import ast
import base64
from datetime import datetime


# MONTHS_LIST = ['jan', 'feb', 'mar', 'apr', 'may',
#                'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
# POSTFIX_LIST = ['st', 'nd', 'rd', 'th']
# IGNORE_LIST = ['Date:', 'date:']


class ShModuleIndex(models.Model):
    _inherit = "sh.module"

    # ====================================================
    #  (Temp) Update Product Category
    # ====================================================
    # def update_product_categ(self, connector_obj):
    #     if not "." in self.sh_branch_id.name:
    #         return "error", f"Somthing Went Wrong in Branch '{self.sh_branch_id.name}'!"
    #     # manifest_file_name = '__manifest__.py'
    #     # try:
    #     #     if float(self.sh_branch_id.name) < 10:
    #     #         manifest_file_name = '__openerp__.py'
    #     # except:
    #     #     pass
    #     # url = self.sh_module_url.replace(
    #     #     self.name, f"{self.name}/{manifest_file_name}")
    #     # response = connector_obj.get_req(url)
    #     # if response.status_code != 200:
    #     #     return "error", f"Failed To Get '{manifest_file_name}' For '{self.name}'."
    #     url = self.sh_module_url.replace(
    #         self.name, f"{self.name}/__manifest__.py")
    #     response = connector_obj.get_req(url)
    #     if response.status_code != 200:
    #         url = url.replace('__manifest__.py', '__openerp__.py')
    #         response = connector_obj.get_req(url)
    #         if response.status_code != 200:
    #             return "error", f"Failed To Get '__manifest__' or '__openerp__.py' For '{self.name}'."
    #     # ===== Read Manifest ======
    #     manifest = ast.literal_eval(response.text)
    #     categ = False
    #     # ===== Create/Update Product ======
    #     if manifest.get('category'):
    #         map_categs = self.env['sh.map.categ'].sudo().search([])
    #         if not map_categs:
    #             return "error", f"Please First Check The Map Categ Configuration."
    #         m_categ = manifest['category'].strip()
    #         for map_categ in map_categs:
    #             if m_categ in map_categ.categ_like:
    #                 categ = map_categ.categ_id
    #                 break
    #     else:
    #         return "error", f"Failed To Get Category From Manifest For '{self.name}'."
    #     if not categ:
    #         return "error", f"Failed To Find Category Like '{manifest['category']}'."
    #     find_product_tmpl = self.env["product.template"].sudo().search(
    #         [("sh_technical_name", "=", self.name)], limit=1)
    #     if find_product_tmpl:
    #         find_product_tmpl.sudo().write({
    #             'public_categ_ids': [(6, 0, [categ.id])]
    #         })
    #         find_product = self.env["product.product"].sudo().search([
    #             ("sh_technical_name", "=", self.name)
    #         ])
    #         if find_product:
    #             for product in find_product:
    #                 product.sudo().write({
    #                     'public_categ_ids': [(6, 0, [categ.id])]
    #                 })
    #             return "success", "Category Write Successfully."
    #         else:
    #             return "error", f"Failed To Find Product Variant 'v{m_version} {find_product.sh_technical_name}'"
    #     else:
    #         return "error", f"Failed To Find Product Tmpl For '{self.name}'."

    def _get_list_price(self, m_price):
        ''' Convert the Euro price into Inr price '''
        try:
            price_dict = {'price': 0.0}

            if not m_price:
                return price_dict

            eur_currency_obj = self.env['res.currency'].sudo().search([
                ('name', '=', 'EUR')
            ], limit=1, order='id desc')
            if not eur_currency_obj:
                return price_dict

            inr_currency_obj = self.env['res.currency'].sudo().search([
                ('name', '=', 'INR')
            ], limit=1, order='id desc')
            if not inr_currency_obj:
                return price_dict

            inr_price = eur_currency_obj._convert(
                from_amount=m_price,
                to_currency=inr_currency_obj,
                company=self.env.company,
                date=datetime.today().date(),
            )
            if inr_price:
                price_dict.update({'price': inr_price})
                return price_dict
            return price_dict
        except:
            return {}

    # ====================================================
    #  Update Product Template
    # ====================================================

    # def update_product_tmpl(self, connector_obj, product_tmpl, product_vals, price, date):
    def update_product_tmpl(self, connector_obj, product_tmpl, product_vals, price):
        product_tmpl_vals = {}
        # ===== Responsible Users =====
        if product_vals.get('other_responsible_users'):
            product_tmpl_vals['other_responsible_users'] = product_vals['other_responsible_users']
        # ===== Price & Image =====
        is_latest_version = False
        try:
            is_latest_version = int(self.sh_branch_id.name.split('.')[0]) >= product_tmpl.latest_version
        except:
            pass
        # ===== Product Tmpl Image =====
        if is_latest_version or not product_tmpl.image_1920:
            tmpl_img_url = self.sh_module_url.replace(
                self.name, f'{self.name}/static/description/sh_icon.png')
            tmpl_img_response = connector_obj.get_req(tmpl_img_url)
            if tmpl_img_response.status_code == 200:
                product_tmpl_vals['image_1920'] = base64.b64encode(
                    tmpl_img_response.content)
        # ===== Price =====
        product_vals['euro_price'] = product_tmpl.euro_price_duplicate
        if is_latest_version or not product_tmpl.euro_price_duplicate:
            product_vals['euro_price'] = price
            product_tmpl_vals['euro_price_duplicate'] = price
        # ===== Sales Price =====
        list_price_dict = self._get_list_price(product_vals.get('euro_price'))
        if 'price' in list_price_dict:
            list_price = list_price_dict.get('price')
            product_tmpl_vals['list_price'] = list_price
            product_vals['lst_price'] = list_price

        # ===== Date =====
        if is_latest_version:
            product_tmpl_vals['module_last_updated_date'] = datetime.now()
        # if date:
        #     if is_latest_version or not product_tmpl.module_last_updated_date:
        #         product_tmpl_vals['module_last_updated_date'] = date
        # ===== website_meta_og_img =====
        product_tmpl_vals['website_meta_og_img'] = f'/web/image/product.template/{product_tmpl.id}/image_1024'
        # ===== Update Tmpl =====
        product_tmpl.sudo().write(product_tmpl_vals)

    # ====================================================
    #  Update Product Vals
    # ====================================================

    def find_category(self, categ_complete_name):
        ''' Return Child Category Id'''
        categs_ids_list = []
        previous_categ = False
        for x in categ_complete_name.split('/'):
            x = x.strip()
            if x != '':
                search_categ = self.env['product.public.category'].sudo().search(
                    [('name', '=', x)], limit=1)
                if search_categ:
                    categs_ids_list.append(search_categ.id)
                    if previous_categ:
                        search_categ.update({'parent_id': previous_categ})
                    previous_categ = search_categ.id
                else:
                    # create new one
                    categ_id = False
                    if previous_categ:
                        categ_id = self.env['product.public.category'].sudo().create({
                            'name': x,
                            'parent_id': previous_categ
                        })
                    else:
                        categ_id = self.env['product.public.category'].sudo().create({
                            'name': x})
                    if categ_id:
                        categs_ids_list.append(categ_id.id)
                        previous_categ = categ_id.id
        if categs_ids_list:
            return categs_ids_list[-1]
        return False

    def update_product_vals(self, data, vals, connector_obj):
        '''Those are the comman vals in Product And Template.'''
        vals["git_repo"] = self.sh_branch_id.repo_id.id
        vals["detailed_type"] = "service"
        # ===== Category ======
        if data.get("category"):
            # categ_id = self.find_category(data['category'])
            # if categ_id:
            #     vals["public_categ_ids"] = [(6, 0, [categ_id])]
            map_categs = self.env['sh.map.categ'].sudo().search([])
            if map_categs:
                m_categ = data['category'].strip()
                for map_categ in map_categs:
                    if m_categ in map_categ.categ_like:
                        category_list = map_categ.categ_like.split('|')
                        for ilike_categ in category_list:
                            if m_categ == ilike_categ.strip():
                                vals["public_categ_ids"] = [
                                    (6, 0, [map_categ.categ_id.id])]
                                break
        # ===== Product Category ======
        if connector_obj.categ_id:
            vals["categ_id"] = connector_obj.categ_id.id
        # ===== Assign To ======
        if self.sh_branch_id.repo_id.responsible_user:
            vals["resposible_user_id"] = self.sh_branch_id.repo_id.responsible_user.id
        # ===== Responsible User ======
        if self.sh_branch_id.repo_id.other_responsible_user_ids:
            user_list = []
            if self.sh_branch_id.repo_id.other_responsible_user_ids:
                for user in self.sh_branch_id.repo_id.other_responsible_user_ids:
                    user_list.append((4, user.id))
                if user_list:
                    vals["other_responsible_users"] = user_list

    def raise_for_status(self, version, is_success, index_message, operation='Created'):
        ''' Return status and message '''
        message = f"Product 'v{version} {self.name}' {operation} Successfully."
        if index_message:
            message += f" \n{index_message}"
        if is_success:
            return "success", message
        else:
            return "error", message

    # ------------------------------------------
    #  Product Created Notification
    # ------------------------------------------

    def _product_create_notification(self, connector_obj, product, title):
        if connector_obj.activity_user_ids:
            for user in connector_obj.activity_user_ids:
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                self.env['user.push.notification'].push_notification(
                    list_of_user_ids=[user],
                    title=title,
                    message=f'v{product.product_version} {product.sh_technical_name}.',
                    link=f'{base_url}/mail/view?model=product.product&res_id={str(product.id)}',
                    res_model='product.product',
                    res_id=product.id,
                    type='project'
                )

    # ====================================================
    #  Create/Update Product
    # ====================================================
    def create_update_product(self, connector_obj):
        if not "." in self.sh_branch_id.name:
            return "error", f"Somthing Went Wrong in Branch '{self.sh_branch_id.name}'!"
        url = self.sh_module_url.replace(
            self.name, f"{self.name}/__manifest__.py")
        response = connector_obj.get_req(url)
        if response.status_code != 200:
            url = url.replace('__manifest__.py', '__openerp__.py')
            response = connector_obj.get_req(url)
            if response.status_code != 200:
                return "error", f"Failed To Get '__manifest__' or '__openerp__.py' For '{self.name}', URL: {url}, Response text: {response.text}"
        # ====== Read Manifest ======
        # To filter text data into Dictionary
        manifest = ast.literal_eval(response.text)
        m_version = manifest.get("version")
        # ===== Product Vals ======
        product_vals = {
            "product_version": m_version,
            "sh_branch_id": self.sh_branch_id.id,
            "sh_seo_summary": manifest.get("summary"),
            "sh_seo_description": manifest.get("description"),
            'last_updated_date': datetime.now()
        }
        self.update_product_vals(manifest, product_vals, connector_obj)
        # ===== Last Update Date ======
        # date = self.get_last_update_date(connector_obj)
        # if date:
        #     product_vals['last_updated_date'] = date
        # ===== Price ======
        price = 0
        if manifest.get("price"):
            try:
                price = float(manifest.get("price"))
            except ValueError:
                pass
        # ===== License ======
        if manifest.get("license"):
            find_license = self.env["sh.license"].sudo().search(
                [("name", "=ilike", manifest.get("license"))], limit=1)
            if find_license:
                product_vals["license"] = find_license.id
            else:
                product_vals["license"] = self.env["sh.license"].sudo().create(
                    {"name": manifest.get("license")}).id
        # ===== Depends ======
        if manifest.get("depends"):
            depends_vals = []
            required_app_list = []
            for depends_module in manifest.get("depends"):
                if "sh_" in depends_module:
                    find_depends = self.env["sh.depends"].sudo().search([
                        ("technical_name", "=", depends_module)
                    ], limit=1)
                    if find_depends:
                        depends_vals.append(find_depends.id)
                    else:
                        depends_vals.append(
                            self.env['sh.depends'].sudo().create({
                                "name": depends_module,
                                "technical_name": depends_module
                            }).id)
                else:
                    find_depends = self.env["sh.required.apps"].sudo().search(
                        [("technical_name", "=", depends_module)], limit=1)
                    if find_depends:
                        required_app_list.append(find_depends.id)
                    else:
                        required_app_list.append(
                            self.env['sh.required.apps'].sudo().create({
                                "name": depends_module,
                                "technical_name": depends_module
                            }).id)
            if depends_vals:
                # product_vals["depends"] = depends_vals
                product_vals["depends"] = [(6, 0, depends_vals)]
            if required_app_list:
                product_vals["required_apps"] = [(6, 0, required_app_list)]

        # ===== Create/Update Product ======
        find_product = False
        find_product_tmpl = False
        if self.sh_product_id:
            find_product = self.sh_product_id
            find_product_tmpl = self.sh_product_id.product_tmpl_id
        if not find_product_tmpl:
            find_product_tmpl = self.env["product.template"].sudo().search(
                [("sh_technical_name", "=", self.name)], limit=1)
        if find_product_tmpl:
            # self.update_product_tmpl(
            #     connector_obj, find_product_tmpl, product_vals, price, date)
            self.update_product_tmpl(
                connector_obj, find_product_tmpl, product_vals, price)
            # ==============================
            #  Add/Update Template Variant
            # ==============================
            if not find_product:
                find_product = self.env["product.product"].sudo().search([
                    ("sh_technical_name", "=", self.name),
                    ("sh_branch_id", "=", self.sh_branch_id.id),
                ], limit=1)
                # ===== If not get product by branch id ======
                if not find_product:
                    find_product = self.find_variant_from_variants(connector_obj)

            if find_product:
                # ==============================
                #  Update Product Variant
                # ==============================
                # if not find_product.related_sub_task:
                #     self.process_module_task(connector_obj)
                is_status_done, index_message = self.update_product_and_index(
                    find_product, product_vals, connector_obj)
                return self.raise_for_status(m_version, is_status_done, index_message, 'Write')
            else:
                # ==============================
                #  Create Product Variant
                # ==============================
                if not find_product_tmpl.attribute_line_ids:
                    return 'error', f"Failed To Create Variant For 'v{m_version} {find_product_tmpl.sh_technical_name}'"
                for line in find_product_tmpl.attribute_line_ids:
                    if line.attribute_id == connector_obj.product_attribute_id:
                        variant_obj, attr_error = self.process_attribute_id(connector_obj)
                        if not variant_obj:
                            return 'error', attr_error
                        line.sudo().write({"value_ids": [(4, variant_obj.id)]})
                # ===== Find That Created Product Variant ======
                find_product = self.find_variant_from_variants(connector_obj)
                if find_product:
                    # if not find_product.related_sub_task:
                    #     self.process_module_task(connector_obj)
                    is_status_done, index_message = self.update_product_and_index(
                        find_product, product_vals, connector_obj)
                    # ==== Notification ===
                    self._product_create_notification(connector_obj, find_product, 'Product Variant Created')
                    self._link_product_task(connector_obj, find_product)
                    return self.raise_for_status(m_version, is_status_done, index_message)
                else:
                    return 'error', f"Failed To Create Variant For 'v{m_version} {find_product_tmpl.sh_technical_name}'"
        else:
            # ======================================
            #  Create Product Template And Variant
            # ======================================
            product_tmpl_vals = {
                "name": manifest.get("name"),
                "sh_technical_name": self.name,
                "module_last_updated_date": datetime.now(),
                'is_published': False
            }
            self.update_product_vals(
                manifest, product_tmpl_vals, connector_obj)
            # # ===== Date ======
            # if date:
            #     product_tmpl_vals['module_last_updated_date'] = date
            # ===== Image ======
            tmpl_img_url = self.sh_module_url.replace(
                self.name, f'{self.name}/static/description/sh_icon.png')
            tmpl_img_response = connector_obj.get_req(tmpl_img_url)
            if tmpl_img_response.status_code == 200:
                product_tmpl_vals['image_1920'] = base64.b64encode(
                    tmpl_img_response.content)
            # ===== Price ======
            # if price:
            product_tmpl_vals["euro_price_duplicate"] = price
            product_vals['euro_price'] = price
            # ===== Sales Price =====
            list_price_dict = self._get_list_price(price)
            if 'price' in list_price_dict:
                list_price = list_price_dict.get('price')
                product_vals['lst_price'] = list_price
                product_tmpl_vals['list_price'] = list_price
            # ===================================================
            #  For Creating Variant Along With Product Template
            # ===================================================
            if connector_obj.product_attribute_id:
                variant_obj, attr_error = self.process_attribute_id(connector_obj)
                if not variant_obj:
                    return "error", attr_error
                product_tmpl_vals["attribute_line_ids"] = [(0, 0, {
                    "attribute_id": connector_obj.product_attribute_id.id,
                    "value_ids": [(4, variant_obj.id)],
                })]
            product_tmpl = self.env["product.template"].sudo().create(product_tmpl_vals)
            # ===== website_meta_og_img =====
            product_tmpl.sudo().write({
                'website_meta_og_img': f'/web/image/product.template/{product_tmpl.id}/image_1024'
            })
            # ===== Find That Created Product Variant ======
            find_product = self.find_variant_from_variants(connector_obj)
            if find_product:
                # # if not find_product.related_sub_task:
                # #     self.process_module_task(connector_obj)
                product_vals['is_published'] = False
                is_status_done, index_message = self.update_product_and_index(
                    find_product, product_vals, connector_obj)
                # ==== Notification ===
                self._product_create_notification(connector_obj, find_product, 'Product Created')
                self._link_product_task(connector_obj, find_product, True)
                return self.raise_for_status(m_version, is_status_done, index_message)
            else:
                return "error", f"Failed to Find Product 'v{m_version} {manifest.get('name')}'!"

    # ====================================================
    #  Find Specific Product From All of Its Variants
    # ====================================================
    def find_variant_from_variants(self, connector_obj):
        find_products = self.env["product.product"].sudo().search([
            ("sh_technical_name", "=", self.name),
        ])
        if not find_products:
            return False
        if len(find_products) == 1:
            if not find_products.product_tmpl_id.attribute_line_ids:
                return False
            for line in find_products.product_tmpl_id.attribute_line_ids:
                if line.attribute_id == connector_obj.product_attribute_id:
                    if not line.value_ids.name:
                        continue
                    if self.sh_branch_id.name.split(".")[0] in line.value_ids.name:
                        return find_products
            return False
        for product in find_products:
            if not product.product_template_variant_value_ids.name:
                continue
            if self.sh_branch_id.name.split(".")[0] in product.product_template_variant_value_ids.name:
                product.sudo().write({"sh_branch_id": self.sh_branch_id.id})
                return product
        return False

    # ====================================================
    #  Update Product
    # ====================================================
    def update_product_and_index(self, find_product, product_vals, connector_obj=False):
        find_product.sudo().write(product_vals)
        # ===== Link Module To Product Variant =====
        if not self.sh_product_id:
            self.sudo().write({"sh_product_id": find_product.id})
        # ===== Link Module To Blog Post =====
        if self.sh_blog_post_id and find_product.sh_blog_post_id:
            if self.sh_blog_post_id.active == False:
                self.create_blog_post(connector_obj)
            return self.process_full_blog(connector_obj)
        elif self.sh_blog_post_id and not find_product.sh_blog_post_id:
            if self.sh_blog_post_id.active == False:
                self.create_blog_post(connector_obj)
            else:
                find_product.sudo().write(
                    {'sh_blog_post_id': self.sh_blog_post_id.id})
        elif not self.sh_blog_post_id and find_product.sh_blog_post_id:
            self.sudo().write(
                {'sh_blog_post_id': find_product.sh_blog_post_id.id})
        else:
            self.create_blog_post(connector_obj)
        return self.process_full_blog(connector_obj)
        # ==========================================
        # if self.sh_blog_post_id:
        #     return self.sh_blog_post_id
        # if self.sh_product_id.sh_blog_post_id:
        #     self.create_update_index_queue(connector_obj)
        #     return self.sh_product_id.sh_blog_post_id
        # if not connector_obj:
        #     return False
        # # Create Blog
        # return self.create_blog_post(connector_obj)

    # ====================================================
    #  Find Attribute/Version (Like Odoo 16)
    # ====================================================
    def process_attribute_id(self, connector_obj):
        variant = f"Odoo {self.sh_branch_id.name.split('.')[0]}"
        attr_val_obj = self.env["product.attribute.value"].sudo().search([
            ("name", "=", variant),
            ("attribute_id", "=", connector_obj.product_attribute_id.id),
        ], limit=1)
        # f"Failed to Find Product Attribute Value 'Odoo {self.sh_branch_id.name.split('.')[0]}'"
        odoo_version = f"Odoo {self.sh_branch_id.name.split('.')[0]}"
        return attr_val_obj, f"Failed To find the Product Attribute Value '{odoo_version}' For Attribute '{connector_obj.product_attribute_id.name}' in order to create the product variant !"

    # ====================================================
    #  Get The Date From Chagelog Data
    # ====================================================

    # def get_month_num(self, month_char):
    #     global MONTHS_LIST
    #     for i in range(len(MONTHS_LIST)):
    #         if MONTHS_LIST[i] in month_char:
    #             return i+1
    #     return 1

    # def get_day(self, raw_day):
    #     global POSTFIX_LIST
    #     if len(raw_day) < 3:
    #         return int(raw_day)
    #     else:
    #         if not raw_day:
    #             return False
    #         if ':' in raw_day:
    #             raw_day = raw_day.split(':')[1]
    #         if not raw_day:
    #             return False
    #         # for ignore in IGNORE_LIST:
    #         #     if ignore in raw_day:
    #         #         raw_day = raw_day.replace(ignore, '')
    #         #         break
    #         for postfix in POSTFIX_LIST:
    #             if postfix in raw_day:
    #                 if raw_day:
    #                     raw_day = int(raw_day.replace(postfix, ''))
    #                 break
    #         return raw_day

    # def scrap_date(self, response):
    #     '''Filter date from changelog.rst file's Data'''
    #     my_list = response.text.split('(')
    #     if not my_list:
    #         return False
    #     my_list = my_list[-1].split(")")
    #     if not my_list:
    #         return False
    #     raw_date_list = my_list[0].split()
    #     if not raw_date_list:
    #         return False
    #     raw_date_list_len = len(raw_date_list)
    #     day = False
    #     month_digit = False
    #     year = False
    #     if raw_date_list_len >= 3:
    #         # When Formate: Date:31st March 2023
    #         year = int(raw_date_list[-1])
    #         month_digit = self.get_month_num(
    #             raw_date_list[raw_date_list_len-2].lower())
    #         day = self.get_day(raw_date_list[raw_date_list_len-3])
    #     elif raw_date_list_len == 2:
    #         # When Formate: 1-june 2022
    #         year = int(raw_date_list[1])
    #         if '-' in raw_date_list[0]:
    #             raw_date_list = raw_date_list[0].split('-')
    #             if len(raw_date_list) == 2:
    #                 day = self.get_day(raw_date_list[0])
    #                 month_digit = self.get_month_num(raw_date_list[1].lower())
    #     elif raw_date_list_len == 1:
    #         # When Formate: july-15,2022
    #         if ',' in my_list[0]:
    #             raw_date_list = my_list[0].split(',')
    #             if len(raw_date_list) == 2:
    #                 year = int(raw_date_list[1])
    #                 if '-' in raw_date_list[0]:
    #                     raw_date_list = raw_date_list[0].split('-')
    #                     if len(raw_date_list) == 2:
    #                         day = self.get_day(raw_date_list[1])
    #                         month_digit = self.get_month_num(
    #                             raw_date_list[0].lower())
    #     if day and month_digit and year:
    #         return datetime(year, month_digit, day)
    #     return False

    # def get_last_update_date(self, connector_obj):
    #     date_url = self.sh_module_url.replace(
    #         self.name, f"{self.name}/doc/changelog.rst")
    #     date_response = connector_obj.get_req(date_url)
    #     if date_response.status_code == 200:
    #         try:
    #             return self.scrap_date(date_response)
    #         except:
    #             return False
    #     return False
