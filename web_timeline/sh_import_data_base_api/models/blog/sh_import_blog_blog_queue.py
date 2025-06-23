# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
import requests


class InheritImportBaseBlogBlogQueue(models.Model):
    _inherit = "sh.import.base"

    sh_is_import_blog_in_queue = fields.Boolean('Import Blog In Queue')
    sh_blog_from_date = fields.Date('From Date(Blog)')
    sh_blog_to_date = fields.Date('To Date(Blog)')
    sh_blog_ids_list = fields.Char('Blog Ids')

    def import_blog_in_queue(self):
        base_obj = self.env['sh.import.base'].search([], limit=1)
        if base_obj.sh_is_import_blog_in_queue:
            response = requests.get('''%s/api/public/blog.blog?query={id,write_date}&filter=[["write_date",">=","%s"],["write_date","<=","%s"]]''' % (
                base_obj.base_url, str(base_obj.sh_blog_from_date), str(base_obj.sh_blog_to_date)))
            if response.status_code == 200:
                response_json = response.json()
                # ========================================
                # Arrange Ids in Assending order.
                # ========================================
                if response_json.get('result'):
                    response_json['result'] = sorted(
                        response_json['result'], key=lambda d: d['id'])
                    base_obj.sh_blog_ids_list = [
                        r['id'] for r in response_json.get('result')]
                else:
                    base_obj.sh_blog_ids_list=False

    def import_blog_from_queue(self):
        base_obj = self.env['sh.import.base'].search([], limit=1)

        if not base_obj.sh_is_import_blog_in_queue:
            return False

        if base_obj.sh_blog_ids_list:
            blog_list = base_obj.sh_blog_ids_list.strip(
                '][').split(', ')
        else:
            return False

        if not blog_list[0]:
            base_obj.sh_is_import_blog_in_queue = False
            base_obj.sh_blog_ids_list = False
            return False

        ''' ============= blog.blog ============= '''
        count = 0
        fail = 0

        for blog_id in blog_list[0:10]:

            response = requests.get(
                '''%s/api/public/blog.blog/%s?query={
                id,display_name,name,is_seo_optimized,subtitle,website_meta_description,website_meta_keywords,
                website_meta_og_img,website_meta_title
            }''' % (base_obj.base_url, blog_id))

            if response.status_code == 200:

                response_json = response.json()
                if response_json.get('error') != '0':
                    base_obj.create_log(
                        field_type='blog', error=response_json)
                    return False

                # ========================================
                # For Maintain Ids
                # ========================================
                last_rec = self.env['blog.blog'].search(
                    [], order='id desc', limit=1)
                blog_id = int(blog_id)
                if last_rec.id < blog_id:
                    for ind in range(last_rec.id+1, blog_id+1):
                        base_obj.create_blog_blog_fake_rec(ind)

                # ========================================
                # Create Or Write Blog blog
                # ========================================
                if response_json.get('result'):
                    blog = response_json['result'][0]
                    try:
                        if not blog.get('id'):
                            fail += 1
                            base_obj.create_fail_log(
                                name=blog.get('id'),
                                field_type='blog',
                                error='Not get Id or blog_id!',
                                import_json=blog,
                            )
                            base_obj.create_blog_blog_fake_rec(blog_id)
                            continue

                        find_blog_blog = self.env['blog.blog'].search(
                            [('id', '=', blog['id'])])
                        blog_blog_vals = self.process_blog_blog_vals(
                            blog)
                        if find_blog_blog:
                            find_blog_blog.sudo().write(blog_blog_vals)
                        else:
                            self.env['blog.blog'].sudo().create(
                                blog_blog_vals)
                        count += 1

                    except Exception as e:
                        fail += 1
                        base_obj.create_fail_log(
                            name=blog.get('id'),
                            field_type='blog',
                            error=e,
                            import_json=blog,
                        )
                        base_obj.create_blog_blog_fake_rec(blog_id)
                else:
                    base_obj.create_blog_blog_fake_rec(blog_id)
            else:
                base_obj.create_log(field_type='blog',
                                    error=response.text)

        if count > 0:
            base_obj.create_log(field_type='blog', error="%s Blog Imported Successfully" % (
                count), state='success')
        if fail > 0:
            base_obj.create_log(field_type='blog',
                                error="%s Blog Failed To Import." % (fail))

        # ========================================
        # Update Ids List
        # ========================================
        base_obj.sh_blog_ids_list = '['+', '.join(
            [str(elem) for elem in blog_list[10:]])+']'
