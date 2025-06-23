# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests

blog_post_max_id = False


class InheritImportBaseBlogPost(models.Model):
    _inherit = "sh.import.base"

    sh_blog_post_starting_from = fields.Integer(
        string='Starting From', default=0)
    records_per_page_blog_post = fields.Integer(
        string='Records Per Page (Blog Post)', default=0)
    sh_blog_post_upto = fields.Integer(string='Upto', default=0)
    sh_is_import_blog_post = fields.Boolean(
        string='Import Blog Post', default=False)

    @api.onchange('sh_is_import_blog_post')
    def _onchange_sh_is_import_blog(self):
        self.ensure_one()
        if not self.env.user.has_group('sh_product_base.group_product_tags_manager'):
            self.sh_is_import_blog_post = False
            raise UserError(
                _('You don\'t have a Shop Manager\'s Access right!'))

    def create_blog_post_fake_rec(self, current_id):
        # ==================================================
        # Create Fake Records To Maintain Ids
        # ==================================================
        if not self.env['blog.post'].search([('id', '=', current_id)]):
            self.env['blog.post'].create({
                'name': 'Fake Records',
                'blog_id': self.env['blog.blog'].search([], limit=1).id,
            })

    def import_blog_post(self):
        ''' ============= blog.post ============= '''
        global blog_post_max_id
        base_obj = self.env['sh.import.base'].search([], limit=1)

        if not base_obj.sh_is_import_blog_post:
            return False

        # ==================================================
        # Find blog_post_max_id
        # ==================================================
        if not blog_post_max_id:
            response = requests.get(
                '%s/api/public/blog.post?query={id}' % (base_obj.base_url))
            if response.status_code == 200:
                response_json = response.json()
                if response_json.get('error') != '0':
                    base_obj.create_log(
                        field_type='blog_post', error=response_json)
                    return False
                # Find Max Id
                if response_json.get('result'):
                    blog_post_max_id = 0
                    for id_dict in response_json['result']:
                        if id_dict['id'] > blog_post_max_id:
                            blog_post_max_id = id_dict['id']
                print(f"==>> \n\n ===blog_post_max_id: {blog_post_max_id}")

        # ==================================================
        # Set Default Id's Range (If Not Provided.)
        # ==================================================
        if base_obj.records_per_page_blog_post == 0:
            base_obj.records_per_page_blog_post = 50

        # ==================================================
        # Update Ids Range (From And To)
        # ==================================================
        base_obj.sh_blog_post_starting_from = base_obj.sh_blog_post_upto
        base_obj.sh_blog_post_upto = base_obj.sh_blog_post_starting_from + \
            base_obj.records_per_page_blog_post

        # ========================================
        # Reset Configurations For Blog Post
        # ========================================
        if base_obj.sh_blog_post_starting_from >= blog_post_max_id:
            base_obj.create_log(
                field_type='blog_post', error="Starting From is Out of range in v12's Id!")
            return False

        # ========================================
        # If Upto is Greater Than MAx ID
        # ========================================
        if base_obj.sh_blog_post_upto >= blog_post_max_id:
            base_obj.sh_blog_post_upto = blog_post_max_id

        response = requests.get('''%s/api/public/blog.post?query={
            id,name,display_name,subtitle,cover_properties,content,teaser,teaser_manual,author_avatar,visits,website_meta_title,website_meta_description,
            website_meta_keywords,website_url,buy_now,is_seo_optimized,website_meta_og_img,website_published,is_published,blog_image,published_date,
            post_date,author_id,sh_product_template_ids,blog_id,tag_ids,blog_image,
            sh_video{
                id,name,link,active
            }
        }&filter=[["id", ">", %s], ["id", "<=", %s]]''' % (base_obj.base_url, base_obj.sh_blog_post_starting_from, base_obj.sh_blog_post_upto))

        if response.status_code == 200:
            response_json = response.json()
            if response_json.get('error') != '0':
                base_obj.create_log(field_type='blog_post',
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
            last_rec = self.env['blog.post'].search(
                [], order='id desc', limit=1)
            if last_rec.id < base_obj.sh_blog_post_starting_from:
                for ind in range(last_rec.id+1, base_obj.sh_blog_post_starting_from+1):
                    base_obj.create_blog_post_fake_rec(ind)

            # ========================================
            # Create Or Write Blog Post
            # ========================================
            count = 0
            fail = 0
            for ind in range(base_obj.sh_blog_post_starting_from+1, base_obj.sh_blog_post_upto+1):
                if response_json['result']:
                    if ind == response_json['result'][0].get('id'):
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
                                base_obj.create_blog_post_fake_rec(ind)
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

                            response_json['result'].pop(0)

                        except Exception as e:
                            fail += 1
                            base_obj.create_fail_log(
                                name=blog_post.get('id'),
                                field_type='blog_post',
                                error=e,
                                import_json=blog_post,
                            )
                            base_obj.create_blog_post_fake_rec(ind)
                    else:
                        base_obj.create_blog_post_fake_rec(ind)
                # else:
                #     base_obj.create_blog_post_fake_rec(ind)

            if count > 0:
                base_obj.create_log(field_type='blog_post', error="%s Blog Post Imported Successfully" % (
                    count), state='success')
            if fail > 0:
                base_obj.create_log(field_type='blog_post',
                                    error="%s Blog Post Failed To Import." % (fail))
        else:
            base_obj.create_log(field_type='blog_post', error=response.text)

        # ========================================
        # Reset All Configurations For Blog Post
        # ========================================
        if base_obj.sh_blog_post_upto == blog_post_max_id:
            blog_post_max_id = False
            base_obj.sh_is_import_blog_post = False
            base_obj.sh_blog_post_starting_from = 0
            base_obj.sh_blog_post_upto = 0

    def process_blog_post_vals(self, data):
        # ========================================
        # Prepare Vals For Blog Post
        # ========================================
        vals = {
            "remote_blog_post_id": data.get('id'),
            "name": data.get('name'),
            "display_name": data.get('display_name'),
            "subtitle": data.get('subtitle'),
            "cover_properties": data.get('cover_properties'),
            "content": data.get('content'),
            "teaser": data.get('teaser'),
            "teaser_manual": data.get('teaser_manual'),
            "author_avatar": data.get('author_avatar'),
            "visits": data.get('visits'),
            "website_meta_title": data.get('website_meta_title'),
            "website_meta_description": data.get('website_meta_description'),
            "website_meta_keywords": data.get('website_meta_keywords'),
            "website_url": data.get('website_url'),
            "buy_now": data.get('buy_now'),
            "is_seo_optimized": data.get('is_seo_optimized'),
            "website_meta_og_img": data.get('website_meta_og_img'),
            "website_published": data.get('website_published'),
            "is_published": data.get('is_published'),
            "blog_image": data.get('blog_image'),
        }

        self.datetime_vals(data, vals, 'published_date')
        self.datetime_vals(data, vals, 'post_date')

        self.map_many2one_field(
            'res.partner', 'remote_res_partner_id', data, vals, 'author_id')
        self.map_product_template_ids(data, vals)
        self.map_many2one_field(
            'blog.blog', 'remote_blog_blog_id', data, vals, 'blog_id')
        self.map_blog_post_video_ids(data, vals)

        if data.get('tag_ids'):
            ids_list = []
            for id in data.get('tag_ids'):
                find_rec = self.env['blog.tag'].search(
                    [('remote_blog_tag_id', '=', id)])
                if find_rec:
                    ids_list.append((4, find_rec.id))
            if ids_list:
                data['tag_ids'] = ids_list

        return vals
