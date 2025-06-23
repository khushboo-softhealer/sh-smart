# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class InheritBlogTag(models.Model):
    _inherit = "blog.tag"

    remote_blog_tag_id = fields.Char(string='Remote Blog Tag Id',copy=False)


class InheritBlogPost(models.Model):
    _inherit = "blog.post"

    remote_blog_post_id = fields.Char(string='Remote Blog Post Id',copy=False)


class InheritBlogBlog(models.Model):
    _inherit = "blog.blog"

    remote_blog_blog_id = fields.Char(string='Remote Blog Blog Id',copy=False)


class InheritBlogTagCategory(models.Model):
    _inherit = "blog.tag.category"

    remote_blog_tag_category_id = fields.Char(string='Remote Blog Tag Category Id',copy=False)
