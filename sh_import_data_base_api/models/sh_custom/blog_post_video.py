# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class BlogPostVideo(models.Model):
    _inherit = 'blog.post.video'

    remote_blog_post_video_id = fields.Char("Remote Blog Post Video ID",copy=False)




