# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
import requests

blog_max_id = False
is_import_blog_tag_categ = True


class InheritImportBaseBlogBlog(models.Model):
    _inherit = "sh.import.base"

    sh_blog_blog_starting_from = fields.Integer(
        string='Starting From(Blog)', default=0)
    records_per_page_blog_blog = fields.Integer(
        string='Records Per Page (Blog)', default=20)
    sh_blog_blog_upto = fields.Integer(string='Upto(Blog)', default=0)
    sh_is_import_blog = fields.Boolean(
        string='Import Blog Basic', default=False)

    def create_blog_blog_fake_rec(self, current_id):
        # ==================================================
        # Create Fake Records To Maintain Ids
        # ==================================================
        if not self.env['blog.blog'].search([('id', '=', current_id)]):
            self.env['blog.blog'].create({'name': 'Fake Records'})

    def import_blog_basic(self):
        # global is_import_blog_tag_categ
        base_obj = self.env['sh.import.base'].search([], limit=1)
        if base_obj.sh_is_import_blog:
            base_obj.import_blog_tag_category()
            base_obj.sh_is_import_blog = False
        # base_obj.import_blog_blog()

    def import_blog_blog(self):
        ''' ============= blog.blog ============= '''

        global blog_max_id
        base_obj = self.env['sh.import.base'].search([], limit=1)
        if not base_obj.sh_is_import_blog:
            return False

        # ==================================================
        # Find blog_max_id
        # ==================================================
        if not blog_max_id:
            response = requests.get(
                '%s/api/public/blog.blog?query={id}' % (base_obj.base_url))
            if response.status_code == 200:
                response_json = response.json()
                if response_json.get('error') != '0':
                    base_obj.create_log(
                        field_type='blog', error=response_json)
                    return False
                # Find Max Id
                if response_json.get('result'):
                    blog_max_id = 0
                    for id_dict in response_json['result']:
                        if id_dict['id'] > blog_max_id:
                            blog_max_id = id_dict['id']

        # ==================================================
        # Set Default Id's Range (If Not Provided.)
        # ==================================================
        if base_obj.records_per_page_blog_blog == 0:
            base_obj.records_per_page_blog_blog = 50

        # ==================================================
        # Update Ids Range (From And To)
        # ==================================================
        base_obj.sh_blog_blog_starting_from = base_obj.sh_blog_blog_upto
        base_obj.sh_blog_blog_upto = base_obj.sh_blog_blog_starting_from + \
            base_obj.records_per_page_blog_blog

        # ========================================
        # Reset Configurations For Blog
        # ========================================
        if base_obj.sh_blog_blog_starting_from >= blog_max_id:
            self.create_log(field_type='blog',
                            error="Starting From is Out of range in v12's Id!")
            return False

        # ========================================
        # If Upto is Greater Than MAx ID
        # ========================================
        if base_obj.sh_blog_blog_upto >= blog_max_id:
            base_obj.sh_blog_blog_upto = blog_max_id

        response = requests.get(
            '''%s/api/public/blog.blog?query={
                id,display_name,name,is_seo_optimized,subtitle,website_meta_description,website_meta_keywords,
                website_meta_og_img,website_meta_title
            }&filter=[["id", ">", %s], ["id", "<=", %s]]''' % (base_obj.base_url, base_obj.sh_blog_blog_starting_from, base_obj.sh_blog_blog_upto))

        if response.status_code == 200:
            response_json = response.json()
            if response_json.get('error') != '0':
                base_obj.create_log(field_type='blog',
                                    error=response_json)
                return False

            # ========================================
            # Arrange Ids in Assending order.
            # ========================================
            if response_json.get('result'):
                response_json['result'] = sorted(
                    response_json['result'], key=lambda d: d['id'])

            count = 0
            failed = 0

            # ========================================
            # For Maintain Ids
            # ========================================
            last_rec = self.env['blog.blog'].search(
                [], order='id desc', limit=1)
            if last_rec.id < base_obj.sh_blog_blog_starting_from:
                for ind in range(last_rec.id+1, base_obj.sh_blog_blog_starting_from+1):
                    base_obj.create_blog_blog_fake_rec(ind)

            # ========================================
            # Create Or Write Blog
            # ========================================
            for ind in range(base_obj.sh_blog_blog_starting_from+1, base_obj.sh_blog_blog_upto+1):
                if response_json['result']:
                    if ind == response_json['result'][0].get('id'):
                        blog_blog = response_json['result'][0]
                        try:
                            if not blog_blog.get('id'):
                                failed += 1
                                self.create_fail_log(
                                    name=blog_blog.get('id'),
                                    field_type='blog_blog',
                                    error='Not get Id!',
                                    import_json=blog_blog,
                                )
                                base_obj.create_blog_blog_fake_rec(ind)
                                continue

                            find_blog_blog = self.env['blog.blog'].search(
                                [('id', '=', blog_blog['id'])])
                            blog_blog_vals = self.process_blog_blog_vals(
                                blog_blog)
                            if find_blog_blog:
                                find_blog_blog.sudo().write(blog_blog_vals)
                            else:
                                self.env['blog.blog'].sudo().create(
                                    blog_blog_vals)
                            count += 1

                            response_json['result'].pop(0)

                        except Exception as e:
                            failed += 1
                            self.create_fail_log(
                                name=blog_blog.get('id'),
                                field_type='blog',
                                error=e,
                                import_json=blog_blog,
                            )
                            base_obj.create_blog_blog_fake_rec(ind)
                    else:
                        base_obj.create_blog_blog_fake_rec(ind)
                else:
                    base_obj.create_blog_blog_fake_rec(ind)

            if count > 0:
                self.create_log(field_type='blog', error="%s Blog Blog Imported Successfully" % (
                    count), state='success')
            if failed > 0:
                self.create_log(field_type='blog',
                                error="%s Blog Blog Failed To Import." % (failed))

        else:
            self.create_log(field_type='blog', error=response.text)

        # ========================================
        # Reset All Configurations For Blog
        # ========================================
        if base_obj.sh_blog_blog_upto == blog_max_id:
            blog_max_id = False
            base_obj.sh_is_import_blog = False
            base_obj.sh_blog_blog_starting_from = 0
            base_obj.sh_blog_blog_upto = 0

    def process_blog_blog_vals(self, data):
        if not data.get('id'):
            return False
        # ========================================
        # Prepare Vals For Blog
        # ========================================
        vals = {
            "remote_blog_blog_id": data.get('id'),
            "display_name": data.get('name'),
            "name": data.get('name'),
            "is_seo_optimized": data.get('is_seo_optimized'),
            "subtitle": data.get('subtitle'),
            "website_meta_description": data.get('website_meta_description'),
            "website_meta_keywords": data.get('website_meta_keywords'),
            "website_meta_og_img": data.get('website_meta_og_img'),
            "website_meta_title": data.get('website_meta_title'),
        }
        return vals
