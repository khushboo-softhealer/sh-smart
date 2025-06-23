# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models
import requests


class InheritImportBase(models.Model):
    _inherit = "sh.import.base"

    def process_product_varient_data(self, data):
        #-------------------prepare product variant vals-----------------------#
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
            'active': data['active'],
            'remote_product_product_id': data['id'],
            'pricelist_exception': data.get('pricelist_exception', False),
            'excluded_from_disocunt': data.get('excluded_from_disocunt', False),
            'website_meta_description': data.get('website_meta_description', False),
            'website_meta_keywords': data.get('website_meta_keywords', False),
            'website_meta_og_img': data.get('website_meta_og_img', False),
            'website_meta_title': data.get('website_meta_title', False),
            'is_published':data.get('is_published'),
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
        if data.get('change_log_count'):
            product_vals.update({
                'change_log_count': data.get('change_log_count')
            })
        if data.get('check_down_version'):
            product_vals.update({
                'check_down_version': data.get('check_down_version')
            })
        if data.get('banner_duplicate'):
            product_vals.update({
                'banner_duplicate': data.get('banner_duplicate')
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
        if data.get('sh_sub_task_created'):
            product_vals.update({
                'sh_sub_task_created': data.get('sh_sub_task_created')
            })
        if data.get('product_version_duplicate'):
            product_vals.update({
                'product_version_duplicate': data.get('product_version_duplicate')
            })
        if data.get('soft_url'):
            product_vals.update({
                'soft_url': data.get('soft_url')
            })
        if data.get('user_guide'):
            product_vals.update({
                'user_guide': data.get('user_guide')
            })
        if data.get('user_guide_duplicate'):
            product_vals.update({
                'user_guide_duplicate': data.get('user_guide_duplicate')
            })
        if data.get('usd_price'):
            product_vals.update({
                'usd_price': data.get('usd_price')
            })
        if data.get('module_last_updated_date'):
            product_vals.update({
                'module_last_updated_date': data.get('module_last_updated_date')
            })
        if data.get('last_updated_date'):
            product_vals.update({
                'last_updated_date': data.get('last_updated_date')
            })
        if data.get('last_updated_2'):
            product_vals.update({
                'last_updated_2': data.get('last_updated_2')
            })
        if data.get('last_updated_date_duplicate'):
            product_vals.update({
                'last_updated_date_duplicate': data.get('last_updated_date_duplicate')
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
        if data.get('copyright_claim_user'):
            copyright_claim_user = []
            if data.get('copyright_claim_user') != 0:
                domain_by_id = [('remote_res_user_id', '=',
                                 data.get('copyright_claim_user'))]
                find_user_id = self.env['res.users'].search(domain_by_id)
            if find_user_id:
                product_vals.update({'copyright_claim_user': find_user_id.id})

        if data.get('migrated_by'):
            if data.get('migrated_by') != 0:
                domain_by_id = [
                    ('remote_res_user_id', '=', data.get('migrated_by'))]
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

        if data.get('responsible_user'):
            if data.get('responsible_user'):
                if data.get('responsible_user') != 0:
                    domain_by_id = [
                        ('remote_res_user_id', '=', data.get('responsible_user'))]
                    find_user_id = self.env['res.users'].search(domain_by_id)
            if find_user_id:
                product_vals.update({'responsible_user': find_user_id.id})

        if data.get('responsible_user_id'):
            if data.get('responsible_user_id'):
                if data.get('responsible_user_id') != 0:
                    domain_by_id = [
                        ('remote_res_user_id', '=', data.get('responsible_user'))]
                    find_user_id = self.env['res.users'].search(domain_by_id)
            if find_user_id:
                product_vals.update({'responsible_user_id': find_user_id.id})

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
        if data.get('related_video'):
            related_video = []
            for video in data.get('related_video'):
                if video['id'] != 0:
                    domain = [('remote_blog_post_video_id', '=', video['id'])]
                    find_video = self.env['blog.post.video'].search(domain)
                    if find_video:
                        related_video.append(find_video.id)
                    else:
                        related_video_vals = {
                            'name': video['name'],
                            'link': video['link'],
                            'active': video['active'],
                            'remote_blog_post_video_id': video['id'],
                        }
                        find_video = self.env['blog.post.video'].create(
                            related_video_vals)
                        if find_video:
                            related_video.append(find_video.id)
            if related_video:
                product_vals.update({'related_video': related_video})

        if data.get('related_video_duplicate'):
            related_video = []
            for video in data.get('related_video_duplicate'):
                if video['id'] != 0:
                    domain = [('remote_blog_post_video_id', '=', video['id'])]
                    find_video = self.env['blog.post.video'].search(domain)
                    if find_video:
                        related_video.append(find_video.id)
                    else:
                        related_video_vals = {
                            'name': video['name'],
                            'link': video['link'],
                            'active': video['active'],
                            'remote_blog_post_video_id': video['id'],
                        }
                        find_video = self.env['blog.post.video'].create(
                            related_video_vals)
                        if find_video:
                            related_video.append(find_video.id)
            if related_video:
                product_vals.update({'related_video_duplicate': related_video})
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
                        required_app_obj = self.env['sh.required.apps'].create(
                            required_app_vals)
                        if required_app_obj:
                            required_apps.append(required_app_obj.id)
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
        if data.get('sh_scale_ids') and data.get('sh_scale_ids')['id'] != 0:
            scale_ids = []
            if data.get('sh_scale_ids')['id'] != 0:
                domain = [('remote_sh_scale_id', '=',
                           data.get('sh_scale_ids')['id'])]
                scale_obj = self.env['sh.scale'].search(domain, limit=1)
                if scale_obj:
                    scale_ids.append(scale_obj.id)
                elif data.get('sh_scale_ids')['name'] != '':
                    domain = [('name', '=', data.get('sh_scale_ids')['name'])]
                    scale_obj = self.env['sh.scale'].search(domain, limit=1)
                    if scale_obj:
                        scale_obj.write({
                            'remote_sh_scale_id': data.get('sh_scale_ids')['id']
                        })
                        scale_ids.append(scale_obj.id)
                else:
                    scale_vals = {
                        'name': data.get('sh_scale_ids')['name'],
                        'days': data.get('sh_scale_ids')['days'],
                        'remote_sh_scale_id': data.get('sh_scale_ids')['id'],
                    }
                    scale_obj = self.env['sh.scale'].create(scale_vals)
                    if scale_obj:
                        scale_ids.append(scale_obj.id)
            if scale_ids:
                product_vals.update({'sh_scale_ids': scale_obj.id})
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
            license_obj = self.env['sh.license']
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
                        ('remote_res_user_id', '=', data['git_repo']['responsible_user']['id'])]
                    find_user_id = self.env['res.users'].search(domain_by_id)
                    domain_by_login = [
                        ('login', '=', data['git_repo']['responsible_user']['login'])]
                    find_user_login = self.env['res.users'].search(
                        domain_by_login)

                    # ========== SEARCH USER BY ID OR BY NAME IF EXIST THEN RETURN ELSE CREATE USE AND RETURN IT =====
                    if find_user_id:
                        git_repo_vals['responsible_user'] = find_user_id.id
                    elif find_user_login:
                        git_repo_vals['responsible_user'] = find_user_login.id
                    else:
                        user_vals = self.process_user_data(
                            data['git_repo']['responsible_user'])
                        user_id = self.env['res.users'].create(user_vals)
                        if user_id:
                            git_repo_vals['responsible_user'] = user_id.id

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

    def process_varient_product(self, varient_ids, attribute_ids, product_tmpl_id, base_url):
        #----------------------Import Product Varient---------------------#
        vals = {}
        if product_tmpl_id.attribute_line_ids:
            product_tmpl_id.attribute_line_ids.unlink()
        attribute_line_obj = self.env['product.template.attribute.line']
        vals.update({
            'product_tmpl_id': product_tmpl_id.id
        })
        attribute_line_list = []
        attribute_value_dic = {}
        if attribute_ids:
            for attribute_line in attribute_ids:
                attr_values = []
                attribute = self.env['product.attribute'].sudo().search(
                    [('name', '=', attribute_line['attribute_id']['name'])])
                if attribute:
                    vals.update({
                        'attribute_id': attribute.id,
                    })
                else:
                    attribute = self.env['product.attribute'].sudo().create({
                        'name': attribute_line['attribute_id']['name']
                    })
                    if attribute:
                        vals.update({
                            'attribute_id': attribute.id,
                        })
                for values in attribute_line['value_ids']:
                    attribute_value = self.env['product.attribute.value'].sudo().search(
                        [('attribute_id', '=', attribute.id), ('name', '=', values['name'])])
                    if attribute_value:
                        attr_values.append(attribute_value.id)
                        attribute_value_dic.update({
                            attribute_value.remote_product_attribute_value_id: attribute_value.id
                        })
                    else:
                        attribute_value = self.env['product.attribute.value'].sudo().create({
                            'attribute_id': attribute.id,
                            'name': values['name'],
                            'is_custom': values['is_custom'],
                            'remote_product_attribute_value_id': values['id']
                        })
                        if attribute_value:
                            attr_values.append(attribute_value.id)
                            attribute_value_dic.update({
                                attribute_value.remote_product_attribute_value_id: attribute_value.id
                            })
                if attr_values:
                    vals.update({
                        'value_ids': attr_values,
                        'active': True,
                    })
                att_line_obj = attribute_line_obj.sudo().search(
                    [('product_tmpl_id', '=', product_tmpl_id.id), ('attribute_id', '=', attribute.id), ('value_ids', 'in', attr_values)])
                if att_line_obj:
                    attribute_line_list.append(att_line_obj.id)
                else:
                    att_line_obj = attribute_line_obj.sudo().create(vals)
                    if att_line_obj:
                        attribute_line_list.append(att_line_obj.id)
                # ---------------Update remote product Varient Id --------------#
                response = requests.get('''%s/api/public/product.template/%s''' %
                                        (base_url, product_tmpl_id.remote_product_template_id))
                if response.status_code == 200:
                    response_json = response.json()
                    for data in response_json['result']:
                        if data['product_variant_ids'] and data.get('product_variant_ids'):
                            if varient_ids == data['product_variant_ids']:
                                pass
                            else:
                                varient_ids = data['product_variant_ids']
                if varient_ids:
                    for varient in varient_ids:
                        all_keys = []
                        response = requests.get(
                            '%s/api/public/product.product/%s' % (base_url, varient))
                        if response.status_code == 200:
                            response_json = response.json()
                        for data in response_json['result']:
                            if 'attribute_line_ids' in data:
                                if data.get('attribute_line_ids'):
                                    for name in data.get('attribute_value_ids'):
                                        for key, value in attribute_value_dic.items():
                                            if int(key) == int(name):
                                                all_keys.append(value)
                        attribute_value = self.env['product.attribute.value'].sudo().search([
                            ('id', 'in', all_keys)])
                        product_var_obj = self.env['product.product']
                        domain = []
                        domain.append(
                            ('product_tmpl_id', '=',
                                product_tmpl_id.id))
                        if attribute_value:
                            for attr_value_id in attribute_value:
                                domain.append((
                                    'product_template_attribute_value_ids.product_attribute_value_id.id',
                                    '=', attr_value_id.id))
                        product_varient = product_var_obj.search(
                            domain, limit=1)
                        if product_varient:
                            product_varient.sudo().write({
                                'remote_product_product_id': varient
                            })
                            self.update_product_variant_Id(
                                varient, product_varient, base_url)

    def update_product_variant_Id(self, product_variant_id_v12, product_varient_v16, base_url):
        config = self.env['sh.import.base'].search([], limit=1)
        response = requests.get('%s/api/public/product.product/%s?query={*,license{*},license_duplicate{*},tag_ids{*},tag_ids_duplicate{*},git_repo{*},sh_scale_ids{*},supported_browsers{*},supported_browsers_duplicate{*},required_apps_duplicate{*},sh_blog_post_ids{*},sh_blog_post_ids_duplicate{*},sh_edition_ids{*},sh_edition_ids_duplicate{*},individual_modules{*},related_video{*},related_video_duplicate{*},required_apps{*},product_change_log_id{*},depends{*},depends_duplicate{*},attribute_line_ids{attribute_id{id,name},value_ids{id,name,is_custom}},taxes_id{name,amount,type_tax_use},supplier_taxes_id{name,amount,type_tax_use}, seller_ids{*,name{name,title,ref,type,website,supplier,street,email,is_company,phone,mobile,id,company_type}},website_meta_description,website_meta_keywords,website_meta_og_img,website_meta_title}'
                                % (base_url, product_variant_id_v12))
        if response.status_code == 200:
            response_json = response.json()
            for data in response_json['result']:
                product_vals = config.process_product_varient_data(data)
                domain = [('remote_product_product_id',
                           '=', product_variant_id_v12)]
                product_product_obj = self.env['product.product'].search(
                    domain, limit=1)
                if product_product_obj == product_varient_v16:
                    product_product_obj.write(product_vals)
