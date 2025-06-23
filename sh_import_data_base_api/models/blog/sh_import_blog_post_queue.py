# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields
import requests


class InheritImportBaseBlogPostQueue(models.Model):
    _inherit = "sh.import.base"

    sh_is_import_blog_post_in_queue = fields.Boolean(
        'Import Blog Post In Queue')
    sh_blog_post_from_date = fields.Date('From Date(Post)')
    sh_blog_post_to_date = fields.Date('To Date(Post)')
    sh_blog_post_ids_list = fields.Char('Blog Post Ids')

    def import_blog_post_in_queue(self):
        base_obj = self.env['sh.import.base'].search([], limit=1)
        if base_obj.sh_is_import_blog_post_in_queue:
            response = requests.get('''%s/api/public/blog.post?query={id,write_date}&filter=[["write_date",">=","%s"],["write_date","<=","%s"]]''' % (
                base_obj.base_url, str(base_obj.sh_blog_post_from_date), str(base_obj.sh_blog_post_to_date)))
            if response.status_code == 200:
                response_json = response.json()
                # ========================================
                # Arrange Ids in Assending order.
                # ========================================
                if response_json.get('result'):
                    response_json['result'] = sorted(
                        response_json['result'], key=lambda d: d['id'])
                    base_obj.sh_blog_post_ids_list = [
                        r['id'] for r in response_json.get('result')]
                else:
                    base_obj.sh_blog_post_ids_list=False

    def import_blog_post_from_queue(self):
        base_obj = self.env['sh.import.base'].search([], limit=1)

        if not base_obj.sh_is_import_blog_post_in_queue:
            return False

        if base_obj.sh_blog_post_ids_list:
            blog_post_list = base_obj.sh_blog_post_ids_list.strip(
                '][').split(', ')
        else:
            return False

        if not blog_post_list[0]:
            base_obj.sh_is_import_blog_post_in_queue = False
            base_obj.sh_blog_post_ids_list = False
            return False

        ''' ============= blog.post ============= '''
        count = 0
        fail = 0

        for blog_post_id in blog_post_list[0:10]:

            response = requests.get('''%s/api/public/blog.post/%s?query={
                id,name,display_name,subtitle,cover_properties,content,teaser,teaser_manual,author_avatar,visits,website_meta_title,website_meta_description,
                website_meta_keywords,website_url,buy_now,is_seo_optimized,website_meta_og_img,website_published,is_published,blog_image,published_date,
                post_date,author_id,sh_product_template_ids,blog_id,tag_ids,blog_image,
                sh_video{
                    id,name,link,active
                }
            }''' % (base_obj.base_url, blog_post_id))

            if response.status_code == 200:

                response_json = response.json()
                if response_json.get('error') != '0':
                    base_obj.create_log(
                        field_type='blog_post', error=response_json)
                    return False

                # ========================================
                # For Maintain Ids
                # ========================================
                last_rec = self.env['blog.post'].search(
                    [], order='id desc', limit=1)
                blog_post_id = int(blog_post_id)
                if last_rec.id < blog_post_id:
                    for ind in range(last_rec.id+1, blog_post_id+1):
                        base_obj.create_blog_post_fake_rec(ind)

                # ========================================
                # Create Or Write Blog Post
                # ========================================
                if response_json.get('result'):
                    blog_post = response_json['result'][0]
                    try:
                        if not blog_post.get('id') or not blog_post.get('blog_id'):
                            fail += 1
                            base_obj.create_fail_log(
                                name=blog_post.get('id'),
                                field_type='blog_post',
                                error='Not get Id or blog_id!',
                                import_json=blog_post,
                            )
                            base_obj.create_blog_post_fake_rec(blog_post_id)
                            continue

                        find_blog_post = self.env['blog.post'].search(
                            [('id', '=', blog_post['id'])])
                        blog_post_vals = base_obj.process_blog_post_vals(
                            blog_post)
                        if find_blog_post:
                            find_blog_post.sudo().write(blog_post_vals)
                        else:
                            self.env['blog.post'].sudo().create(
                                blog_post_vals)
                        count += 1

                    except Exception as e:
                        fail += 1
                        base_obj.create_fail_log(
                            name=blog_post.get('id'),
                            field_type='blog_post',
                            error=e,
                            import_json=blog_post,
                        )
                        base_obj.create_blog_post_fake_rec(blog_post_id)
                else:
                    base_obj.create_blog_post_fake_rec(blog_post_id)
            else:
                base_obj.create_log(field_type='blog_post',
                                    error=response.text)

        if count > 0:
            base_obj.create_log(field_type='blog_post', error="%s Blog Post Imported Successfully" % (
                count), state='success')
        if fail > 0:
            base_obj.create_log(field_type='blog_post',
                                error="%s Blog Post Failed To Import." % (fail))

        # ========================================
        # Update Ids List
        # ========================================
        base_obj.sh_blog_post_ids_list = '['+', '.join(
            [str(elem) for elem in blog_post_list[10:]])+']'
