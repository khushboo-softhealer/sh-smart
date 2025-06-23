# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models


class InheritImportBaseBlogMethods(models.Model):
    _inherit = "sh.import.base"


    def map_blog_tag_ids(self, data, vals, data_key='tag_ids', vals_key=None):
        '''many2many(blog.tag) data_key(default) = tag_ids'''
        if data.get(data_key):
            ids_list = []
            for blog_tag_dict in data.get(data_key):
                if not blog_tag_dict.get('id'):
                    continue
                find_rec = self.env['blog.tag'].search([('remote_blog_tag_id', '=', blog_tag_dict.get('id'))])
                if find_rec:
                    ids_list.append((4, find_rec.id))
                else:
                    blog_tag_vals = {
                        "remote_blog_tag_id": blog_tag_dict.get('id'),
                        "name": blog_tag_dict.get('name'),
                        "display_name": blog_tag_dict.get('display_name'),
                        "is_seo_optimized": blog_tag_dict.get('is_seo_optimized'),
                        "website_meta_title": blog_tag_dict.get('website_meta_title'),
                        "website_meta_description": blog_tag_dict.get('website_meta_description'),
                        "website_meta_keywords": blog_tag_dict.get('website_meta_keywords'),
                        "website_meta_og_img": blog_tag_dict.get('website_meta_og_img'),
                    }
                    # self.map_blog_post_ids(blog_tag_dict, blog_tag_vals)
                    ids_list.append((0, 0, blog_tag_vals))
            if ids_list:
                if not vals_key and data_key:
                    vals_key = data_key
                vals[vals_key] = ids_list


    def map_blog_post_ids(self, data, vals, data_key='post_ids', vals_key=None):
        '''many2many(blog.post) data_key(default) = post_ids'''
        if data.get(data_key):
            ids_list = []
            for blog_post_dict in data.get(data_key):
                if not blog_post_dict.get('id'):
                    continue
                find_rec = self.env['blog.post'].search([('remote_blog_post_id', '=', blog_post_dict.get('id'))])
                if find_rec:
                    ids_list.append((4, find_rec.id))
                else:
                    blog_post_vals = {
                        "remote_blog_post_id": blog_post_dict.get('id'),
                        "name": blog_post_dict.get('name'),
                    }
                    # self.map_blog_id(blog_post_dict, blog_post_vals)
                    self.map_many2one_field('blog.blog', 'remote_blog_blog_id', blog_post_dict, blog_post_vals, 'blog_id')
                    created_rec = self.env['blog.post'].create(blog_post_vals)
                    if created_rec:
                        ids_list.append((4, created_rec.id))
            if ids_list:
                if not vals_key and data_key:
                    vals_key = data_key
                vals[vals_key] = ids_list


    def map_blog_id(self, data, vals, data_key='blog_id', vals_key=None):
        '''many2one(blog.blog) data_key(default) = blog_id'''
        if data.get(data_key) and data.get(data_key) != 0:
            if data.get(data_key).get('id') and data.get(data_key).get('id') != 0:
                if not vals_key:
                    vals_key = data_key
                find_rec = self.env['blog.blog'].search([('remote_blog_blog_id', '=', data[data_key].get('id'))])
                if find_rec:
                    vals[vals_key] = find_rec.id
                else:
                    rec_vals = {
                        'remote_blog_blog_id': data.get(data_key).get('id'),
                        'name': data.get(data_key).get('name'),
                    }
                    create_rec = self.env['blog.blog'].create(rec_vals)
                    if create_rec:
                        vals[vals_key] = create_rec.id


    def map_product_template_ids(self, data, vals, data_key='sh_product_template_ids', vals_key=None):
        '''many2many(product.template) data_key(default) = sh_product_template_ids'''
        if data.get(data_key):
            ids_list = []
            for id in data.get(data_key):
                if not id:
                    continue
                find_rec = self.env['product.template'].search([('remote_product_template_id', '=', id)])
                if find_rec:
                    ids_list.append((4, find_rec.id))
            if ids_list:
                if not vals_key and data_key:
                    vals_key = data_key
                vals[vals_key] = ids_list


    def map_blog_post_video_ids(self, data, vals, data_key='sh_video', vals_key=None):
        '''many2many(blog.post.video) data_key(default) = sh_video'''
        if data.get(data_key):
            ids_list = []
            for video in data.get(data_key):
                if not video.get('id'):
                    continue
                find_rec = self.env['blog.post.video'].search([('remote_blog_post_video_id', '=', video.get('id'))])
                if find_rec:
                    ids_list.append((4, find_rec.id))
                else:
                    related_video_vals={
                        'name':video['name'],
                        'link':video['link'],
                        'active':video['active'],
                        'remote_blog_post_video_id':video['id'],
                        'company_id':1
                    }
                    created_rec = self.env['blog.post.video'].create(related_video_vals)
                    if created_rec:
                        ids_list.append((4, created_rec.id))
            if ids_list:
                if not vals_key and data_key:
                    vals_key = data_key
                vals[vals_key] = ids_list
            

